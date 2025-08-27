"""
InsightFace-based face detection, clustering, and move-only export worker.

Implements a robust pipeline using InsightFace (buffalo_l: SCRFD + ArcFace),
EXIF-aware loading, optional image preprocessing, Haar+ArcFace fallback,
per-image deduplication (IoU + cosine), clustering via HDBSCAN (if available)
or DBSCAN with cannot-link inside one image, and move-only export:

- Single-person images are MOVED to that person's folder
- Group images are MOVED once to canonical owner (lowest person id),
  and hardlinks/symlinks are created in other persons' folders (no copies)

Dependencies (install separately):
  pip install insightface onnxruntime opencv-python hdbscan numpy pillow tqdm scikit-learn
"""

from __future__ import annotations

import os
import csv
import shutil
from dataclasses import dataclass
from collections import defaultdict
from pathlib import Path
from typing import Optional, Tuple, List, Dict

import numpy as np
import cv2
from PIL import Image, ImageOps

from PyQt6.QtCore import QThread, pyqtSignal

# Check for required dependencies at module level
try:
    import onnxruntime
    import insightface
    from sklearn.cluster import DBSCAN
    INSIGHTFACE_AVAILABLE = True
    MISSING_DEPS = []
except ImportError as e:
    INSIGHTFACE_AVAILABLE = False
    MISSING_DEPS = []
    
    # Check which specific dependencies are missing
    for dep in ['onnxruntime', 'insightface', 'sklearn']:
        try:
            __import__(dep)
        except ImportError:
            MISSING_DEPS.append(dep)


@dataclass
class FaceRec:
    image: str                   # source path (before move)
    face_idx: int                # index of face within image after dedupe
    bbox: Tuple[float, float, float, float]  # (x1,y1,x2,y2)
    emb: np.ndarray              # (512,) float64 L2-normalized
    det_score: Optional[float] = None


def l2_normalize(v: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    v = np.asarray(v, dtype=np.float64)
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / (n + eps)


def cosine(u: np.ndarray, v: np.ndarray) -> float:
    return float(np.dot(u, v))


def cosine_dist(u: np.ndarray, v: np.ndarray) -> float:
    return 1.0 - cosine(u, v)


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def read_image_exif_bgr(path: str) -> np.ndarray:
    """
    Read image with proper Unicode support and EXIF handling
    """
    try:
        with Image.open(path) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            arr = np.array(im)
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Ошибка чтения изображения {path}: {e}")
        # Fallback to Unicode-safe reading
        from .unicode_utils import imread_unicode
        return imread_unicode(path)


def preprocess(img_bgr: np.ndarray, mode: str) -> np.ndarray:
    if mode == "none":
        return img_bgr
    if mode == "clahe":
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
        return cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)
    if mode.startswith("gamma"):
        try:
            g = float(mode.replace("gamma", ""))
        except Exception:
            g = 1.5
        inv = 1.0 / max(g, 1e-6)
        table = (np.linspace(0, 1, 256) ** inv * 255).astype(np.uint8)
        return cv2.LUT(img_bgr, table)
    return img_bgr


def rotate_image(img: np.ndarray, angle: int) -> np.ndarray:
    angle %= 360
    if angle == 0:
        return img
    if angle == 90:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    if angle == 180:
        return cv2.rotate(img, cv2.ROTATE_180)
    if angle == 270:
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    raise ValueError("Angle must be 0/90/180/270")


def map_bbox_back(b: np.ndarray, angle: int, W: int, H: int) -> np.ndarray:
    x1, y1, x2, y2 = b.tolist()
    angle %= 360
    if angle == 0:
        return np.array([x1, y1, x2, y2], dtype=np.float32)
    if angle == 90:
        return np.array([W - 1 - y2, x1, W - 1 - y1, x2], dtype=np.float32)
    if angle == 180:
        return np.array([W - 1 - x2, H - 1 - y2, W - 1 - x1, H - 1 - y1], dtype=np.float32)
    if angle == 270:
        return np.array([y1, H - 1 - x2, y2, H - 1 - x1], dtype=np.float32)


def clip_box(b: np.ndarray, W: int, H: int) -> np.ndarray:
    b[0] = np.clip(b[0], 0, W - 1)
    b[2] = np.clip(b[2], 0, W - 1)
    b[1] = np.clip(b[1], 0, H - 1)
    b[3] = np.clip(b[3], 0, H - 1)
    return b


def pil_crop(img_bgr: np.ndarray, bbox, size=256) -> Image.Image:
    x1, y1, x2, y2 = map(int, bbox)
    h, w = img_bgr.shape[:2]
    x1 = max(0, min(x1, w - 1)); x2 = max(0, min(x2, w - 1))
    y1 = max(0, min(y1, h - 1)); y2 = max(0, min(y2, h - 1))
    crop = img_bgr[y1:y2, x1:x2]
    if crop.size == 0:
        crop = img_bgr[max(0, h//4):min(h, 3*h//4), max(0, w//4):min(w, 3*w//4)]
    pil = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    return pil.resize((size, size), Image.Resampling.LANCZOS)


def _safe_hardlink(src: Path, dst: Path) -> bool:
    try:
        if dst.exists():
            dst.unlink()
        os.link(src, dst)
        return True
    except Exception:
        return False


def _safe_symlink(src: Path, dst: Path) -> bool:
    try:
        if dst.exists():
            dst.unlink()
        rel = os.path.relpath(src, start=dst.parent)
        os.symlink(rel, dst)
        return True
    except Exception:
        return False


def _unique_dest(base_dir: Path, filename: str) -> Path:
    dst = base_dir / filename
    if not dst.exists():
        return dst
    stem, suf = Path(filename).stem, Path(filename).suffix
    k = 1
    while True:
        cand = base_dir / f"{stem}__{k}{suf}"
        if not cand.exists():
            return cand
        k += 1


def _atomic_move(src: Path, dst: Path) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst = _unique_dest(dst.parent, dst.name)
    try:
        os.replace(src, dst)
    except OSError:
        shutil.move(str(src), str(dst))
    return dst


def _bbox_iou(a, b) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    iw = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    ih = max(0.0, min(ay2, by2) - max(ay1, by1))
    inter = iw * ih
    ua = (ax2 - ax1) * (ay1 - ay1) + (bx2 - bx1) * (by2 - by1) - inter
    return 0.0 if ua <= 0 else inter / ua


def _dedupe_iou_cos(boxes, scores, embs, iou_thr=0.55, cos_thr=0.12):
    if not boxes:
        return []
    order = np.argsort(np.asarray(scores))[::-1]
    boxes = [boxes[i] for i in order]; scores = [scores[i] for i in order]; embs = [embs[i] for i in order]
    used = [False] * len(boxes); groups = []
    for i in range(len(boxes)):
        if used[i]:
            continue
        grp = [i]; used[i] = True
        for j in range(i + 1, len(boxes)):
            if used[j]:
                continue
            iou = _bbox_iou(boxes[i], boxes[j])
            cosd = float(1.0 - np.dot(embs[i], embs[j]))
            if iou >= iou_thr or cosd <= cos_thr:
                grp.append(j); used[j] = True
        groups.append(grp)

    out = []
    for g in groups:
        w = np.array([scores[k] for k in g], dtype=np.float64)
        w = w / (w.sum() + 1e-9)
        b = (np.stack([boxes[k] for k in g]) * w[:, None]).sum(0).astype(np.float32)
        e = np.stack([embs[k] for k in g], 0).mean(0)
        e = e / (np.linalg.norm(e) + 1e-12)
        out.append((b, float(max([scores[k] for k in g])), e.astype(np.float64)))
    return out


def _extract_normed_embedding(face):
    emb = getattr(face, "normed_embedding", None)
    if emb is None:
        emb = getattr(face, "embedding", None)
    if emb is None:
        return None
    emb = np.asarray(emb, dtype=np.float64)
    if emb.ndim != 1 or emb.size == 0:
        return None
    n = np.linalg.norm(emb)
    if not np.isfinite(n) or n < 1e-12:
        return None
    return emb / n


class InsightFaceSorter(QThread):
    progress_updated = pyqtSignal(int, str)  # value, text
    sorting_finished = pyqtSignal(dict)      # stats dict
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        # Check dependencies before initialization
        if not INSIGHTFACE_AVAILABLE:
            missing_str = ", ".join(MISSING_DEPS) if MISSING_DEPS else "unknown dependencies"
            raise ImportError(f"InsightFace dependencies missing: {missing_str}. Install: pip install insightface onnxruntime hdbscan scikit-learn tqdm")
        
        self.input_dir: Optional[str] = None
        self.output_dir: Optional[str] = None
        self.device: str = "cpu"
        self.det_size: int = 1280
        self.det_rotations = (0, 90)
        self.det_score_thr = 0.20
        self.min_face = 18
        self.preproc_chain = ("none", "clahe", "gamma1.6")
        self.use_hdbscan = True
        self.merge_threshold: Optional[float] = None

    def sort_with_insight(self, input_dir: str, output_dir: str, device: str = "cpu"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.device = device
        if not self.isRunning():
            self.start()

    def run(self):
        # Dependencies should already be checked in __init__, but double-check
        if not INSIGHTFACE_AVAILABLE:
            missing_str = ", ".join(MISSING_DEPS) if MISSING_DEPS else "unknown dependencies"
            self.error_signal.emit(
                f"InsightFace dependencies missing: {missing_str}. Install: pip install insightface onnxruntime hdbscan scikit-learn tqdm"
            )
            self.sorting_finished.emit({"ok": False, "error": f"Missing dependencies: {missing_str}"})
            return

        try:
            # Import at runtime to avoid import errors
            from sklearn.cluster import DBSCAN  # noqa: F401
            try:
                import hdbscan  # noqa: F401
                has_hdbscan = True
            except Exception:
                has_hdbscan = False
            from insightface.app import FaceAnalysis
        except Exception as e:
            self.error_signal.emit(
                f"Ошибка импорта зависимостей: {str(e)}. Установите: pip install insightface onnxruntime hdbscan scikit-learn tqdm"
            )
            self.sorting_finished.emit({"ok": False, "error": str(e)})
            return

        if not self.input_dir or not self.output_dir:
            self.sorting_finished.emit({"ok": False, "error": "Не указаны папки"})
            return

        in_dir = Path(self.input_dir)
        out_dir = Path(self.output_dir)
        exts = (".jpg", ".jpeg", ".png")
        img_paths = sorted([p for p in in_dir.rglob("*") if p.suffix.lower() in exts])
        if not img_paths:
            self.sorting_finished.emit({"ok": False, "error": "Изображений не найдено"})
            return

        # Prepare InsightFace
        ctx_id = -1 if self.device == "cpu" else 0
        app = FaceAnalysis(name="buffalo_l")
        app.prepare(ctx_id=ctx_id, det_size=(self.det_size, self.det_size))

        recs: List[FaceRec] = []
        total = len(img_paths)
        processed = 0

        def run_once(img_bgr, W, H, all_boxes, all_scores, all_embs):
            for ang in self.det_rotations:
                rot = rotate_image(img_bgr, ang)
                faces = app.get(rot)
                for f in faces:
                    s = float(getattr(f, "det_score", 1.0))
                    if s < self.det_score_thr:
                        continue
                    b = np.array(list(map(float, f.bbox)), np.float32)
                    b = map_bbox_back(b, ang, rot.shape[1], rot.shape[0])
                    b = clip_box(b, W, H)
                    if (b[2] - b[0]) < self.min_face or (b[3] - b[1]) < self.min_face:
                        continue
                    emb = _extract_normed_embedding(f)
                    if emb is None:
                        continue
                    all_boxes.append(b); all_scores.append(s); all_embs.append(emb)

        # Detect and embed
        for path in img_paths:
            if self.isInterruptionRequested():
                return
            try:
                img0 = read_image_exif_bgr(str(path))
            except Exception:
                processed += 1
                self.progress_updated.emit(int(processed / max(total, 1) * 50), f"Пропуск: {path.name}")
                continue
            H, W = img0.shape[:2]

            all_boxes: List[np.ndarray] = []
            all_scores: List[float] = []
            all_embs: List[np.ndarray] = []

            # 1) base
            run_once(img0, W, H, all_boxes, all_scores, all_embs)

            # 2) if empty — preprocess
            if not all_boxes:
                for pre in self.preproc_chain:
                    if pre == "none":
                        continue
                    img_pre = preprocess(img0, pre)
                    run_once(img_pre, W, H, all_boxes, all_scores, all_embs)
                    if all_boxes:
                        break

            # 3) Haar proposals fallback
            if not all_boxes:
                gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
                cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(self.min_face, self.min_face))
                proposals = []
                for (x, y, w, h) in faces:
                    proposals.append(np.array([x, y, x + w, y + h], np.float32))
                for pbox in proposals:
                    x1, y1, x2, y2 = [int(v) for v in pbox]
                    pad = int(0.12 * max(x2 - x1, y2 - y1))
                    x1 = max(0, x1 - pad); y1 = max(0, y1 - pad)
                    x2 = min(W, x2 + pad); y2 = min(H, y2 + pad)
                    roi = img0[y1:y2, x1:x2]
                    faces_roi = app.get(roi)
                    if not faces_roi:
                        continue
                    f = max(faces_roi, key=lambda z: (z.bbox[2] - z.bbox[0]) * (z.bbox[3] - z.bbox[1]))
                    b = np.array(list(map(float, f.bbox)), np.float32)
                    b[:2] += (x1, y1); b[2:] += (x1, y1)
                    if (b[2] - b[0]) < self.min_face or (b[3] - b[1]) < self.min_face:
                        continue
                    emb = _extract_normed_embedding(f)
                    if emb is None:
                        continue
                    all_boxes.append(b); all_scores.append(float(getattr(f, "det_score", 0.9))); all_embs.append(emb)

            # 4) dedupe per-image
            dedup = _dedupe_iou_cos(all_boxes, all_scores, all_embs, iou_thr=0.55, cos_thr=0.12)
            for j, (bbox, score, emb) in enumerate(dedup):
                recs.append(FaceRec(image=str(path), face_idx=j, bbox=tuple(map(float, bbox.tolist())), emb=emb, det_score=score))

            processed += 1
            self.progress_updated.emit(int(processed / max(total, 1) * 70) + 10, f"Детекция: {processed}/{total}")

        if not recs:
            self.sorting_finished.emit({"ok": False, "error": "Лица не обнаружены"})
            return

        # Clustering
        from sklearn.cluster import DBSCAN
        try:
            import hdbscan  # type: ignore
            has_hdbscan = True
        except Exception:
            has_hdbscan = False

        X = l2_normalize(np.stack([r.emb for r in recs], axis=0))
        if self.use_hdbscan and has_hdbscan:
            try:
                labels = hdbscan.HDBSCAN(min_cluster_size=2, min_samples=1, metric="euclidean", approx_min_span_tree=False).fit_predict(X.astype(np.float64, copy=False))
            except Exception:
                labels = DBSCAN(eps=0.48, min_samples=1, metric="cosine").fit_predict(X)
        else:
            labels = DBSCAN(eps=0.48, min_samples=1, metric="cosine").fit_predict(X)

        # cannot-link within one image
        img_to_idxs: Dict[str, List[int]] = defaultdict(list)
        for idx, r in enumerate(recs):
            img_to_idxs[r.image].append(idx)
        for _, idxs in img_to_idxs.items():
            seen = {}
            for i in idxs:
                l = int(labels[i])
                if l == -1:
                    continue
                if l in seen:
                    labels[i] = -1
                else:
                    seen[l] = i

        # Optionally merge clusters by centroid distance
        if self.merge_threshold is not None:
            labels = self._merge_close_clusters_by_centroid(X, labels, self.merge_threshold)

        # Export (move-only)
        stats = self._export_move_only(recs, labels, out_dir)
        self.sorting_finished.emit(stats)

    @staticmethod
    def _merge_close_clusters_by_centroid(X: np.ndarray, labels: np.ndarray, thr: float) -> np.ndarray:
        X = l2_normalize(X)
        uniq = sorted([l for l in set(labels.tolist()) if l != -1])
        if len(uniq) <= 1:
            return labels
        centers = {l: l2_normalize(X[labels == l].mean(axis=0)) for l in uniq}
        parent = {l: l for l in uniq}

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        for i, a in enumerate(uniq):
            for b in uniq[i + 1:]:
                if cosine_dist(centers[a], centers[b]) < thr:
                    union(a, b)

        root_to_new, nxt = {}, 0
        for l in uniq:
            r = find(l)
            if r not in root_to_new:
                root_to_new[r] = nxt; nxt += 1

        new_labels = labels.copy()
        for i, l in enumerate(labels):
            if l == -1:
                continue
            new_labels[i] = root_to_new[find(int(l))]
        return new_labels

    def _export_move_only(self, recs: List[FaceRec], labels: np.ndarray, out_dir: Path) -> dict:
        ensure_dir(out_dir)
        thumbs_dir = out_dir / "thumbs"
        ensure_dir(thumbs_dir)

        valid_indices = [i for i, l in enumerate(labels) if l != -1]
        if not valid_indices:
            return {"ok": False, "error": "Нет валидных лиц", "groups": 0, "moved": 0}

        clusters: Dict[int, List[int]] = defaultdict(list)
        for idx in valid_indices:
            clusters[int(labels[idx])].append(idx)

        img_to_face_idxs: Dict[str, List[int]] = defaultdict(list)
        for i in valid_indices:
            img_to_face_idxs[recs[i].image].append(i)

        img_to_persons = {img: sorted({int(labels[i]) for i in idxs}) for img, idxs in img_to_face_idxs.items()}

        single_images = [img for img, persons in img_to_persons.items() if len(persons) == 1]
        group_images  = [img for img, persons in img_to_persons.items() if len(persons) >= 2]

        established_labels = set()
        for img in single_images:
            established_labels.update(img_to_persons[img])

        if not established_labels:
            established_labels = {l for l, idxs in clusters.items() if len(idxs) >= 2}
            if not established_labels:
                return {"ok": False, "error": "Нет устойчивых кластеров", "groups": 0, "moved": 0}

        centers = {}
        for l in established_labels:
            emb_stack = np.stack([recs[i].emb for i in clusters[l]], axis=0)
            centers[l] = l2_normalize(emb_stack.mean(axis=0))

        sorted_labels = sorted(established_labels)
        label_to_pid = {l: f"person_{i + 1:03d}" for i, l in enumerate(sorted_labels)}

        moved_path_of_image: Dict[str, Path] = {}
        mapping_rows = []
        moved_count = 0

        # 1) Singles — MOVE
        for img in single_images:
            persons = img_to_persons[img]
            if not persons:
                continue
            l = persons[0]
            if l not in established_labels:
                continue
            pid = label_to_pid[l]
            person_dir = out_dir / pid
            ensure_dir(person_dir)

            idx = next(i for i in img_to_face_idxs[img] if int(labels[i]) == l)
            r = recs[idx]

            src_path = Path(r.image)
            dest_path = _atomic_move(src_path, person_dir / src_path.name)
            moved_path_of_image[img] = dest_path
            moved_count += 1

            img_np = cv2.imread(str(dest_path))
            if img_np is not None:
                crop = pil_crop(img_np, r.bbox, size=256)
                crop.save(thumbs_dir / f"{pid}__{dest_path.stem}__f{r.face_idx}.jpg", quality=95)

            conf = cosine(r.emb, centers[l])
            mapping_rows.append([pid, r.image, str(dest_path), r.face_idx, r.bbox, f"{r.det_score or 1.0:.4f}", f"{conf:.4f}", pid])

        # 2) Group images — MOVE to owner + link others
        for img in group_images:
            persons = [l for l in img_to_persons[img] if l in established_labels]
            if not persons:
                continue
            persons_sorted = sorted(persons, key=lambda x: label_to_pid[x])
            owner_label = persons_sorted[0]
            owner_pid = label_to_pid[owner_label]
            owner_dir = out_dir / owner_pid
            ensure_dir(owner_dir)

            if img not in moved_path_of_image:
                src_path = Path(img)
                dest_path = _atomic_move(src_path, owner_dir / src_path.name)
                moved_path_of_image[img] = dest_path
                moved_count += 1
            else:
                dest_path = moved_path_of_image[img]

            for l in persons_sorted:
                pid = label_to_pid[l]
                person_dir = out_dir / pid
                ensure_dir(person_dir)

                idx = next(i for i in img_to_face_idxs[img] if int(labels[i]) == l)
                r = recs[idx]

                if pid != owner_pid:
                    link_path = person_dir / dest_path.name
                    linked = _safe_hardlink(dest_path, link_path) or _safe_symlink(dest_path, link_path)
                    if not linked:
                        # As a fallback, do nothing (no copies per spec)
                        pass

                img_np = cv2.imread(str(dest_path))
                if img_np is not None:
                    crop = pil_crop(img_np, r.bbox, size=256)
                    crop.save(thumbs_dir / f"{pid}__{dest_path.stem}__f{r.face_idx}.jpg", quality=95)

                conf = cosine(r.emb, centers[l])
                mapping_rows.append([pid, r.image, str(dest_path), r.face_idx, r.bbox, f"{r.det_score or 1.0:.4f}", f"{conf:.4f}", owner_pid])

        with open(out_dir / "mapping.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["person_id", "image_src", "dest_path", "face_idx", "bbox", "det_score", "cosine_to_centroid", "canonical_owner"])
            w.writerows(mapping_rows)

        return {"ok": True, "groups": len(sorted_labels), "moved": moved_count, "out": str(out_dir)}




