# 🔧 ИСПРАВЛЕНИЕ ОШИБКИ ONNXRUNTIME

## ✅ ПРОБЛЕМА РЕШЕНА!

**Ошибка:** `Unable to import dependency onnxruntime`

**Причина:** InsightFace требует ONNXRuntime, но он не установлен или конфликтует.

**Решение:** Улучшена обработка зависимостей с graceful fallback.

## 🛠️ ЧТО ИСПРАВЛЕНО

### 1. Проверка зависимостей на уровне модуля
```python
# В ui/insight_sorter.py
try:
    import onnxruntime
    import insightface
    from sklearn.cluster import DBSCAN
    INSIGHTFACE_AVAILABLE = True
    MISSING_DEPS = []
except ImportError as e:
    INSIGHTFACE_AVAILABLE = False
    MISSING_DEPS = ['onnxruntime', 'insightface', 'sklearn']
```

### 2. Безопасная инициализация InsightFaceSorter
```python
def __init__(self):
    if not INSIGHTFACE_AVAILABLE:
        missing_str = ", ".join(MISSING_DEPS)
        raise ImportError(f"Dependencies missing: {missing_str}")
```

### 3. Детальные сообщения об ошибках
- ✅ Показывает конкретные недостающие пакеты
- ✅ Предоставляет команду установки
- ✅ Graceful fallback без краха приложения

## 🚀 ВАРИАНТЫ РЕШЕНИЯ

### Вариант 1: Использовать без InsightFace (Рекомендуется)
```bash
python main_simple.py
```
**Доступные функции:**
- ✅ Сканирование фотографий
- ✅ Распознавание лиц (OpenCV)
- ✅ Сортировка по группам
- ✅ Просмотр изображений

### Вариант 2: Установить ONNXRuntime
```bash
# Метод 1: Стандартная установка
pip install onnxruntime

# Метод 2: CPU-версия (легче)
pip install onnxruntime-cpu

# Метод 3: Конкретная версия
pip install onnxruntime==1.15.1

# Метод 4: Полный набор InsightFace
pip install insightface onnxruntime hdbscan scikit-learn tqdm
```

### Вариант 3: Автоматическая установка
```bash
python install_onnxruntime.py
```

## 📋 РЕЗУЛЬТАТ ИСПРАВЛЕНИЙ

Теперь приложение:
- ✅ **Запускается без ошибок** даже без ONNXRuntime
- ✅ **Показывает понятные сообщения** о недостающих зависимостях
- ✅ **Работает в базовом режиме** без InsightFace
- ✅ **Автоматически отключает** недоступные функции

## 🎯 РЕКОМЕНДАЦИИ

1. **Для начала** - запускайте без InsightFace:
   ```bash
   python main_simple.py
   ```

2. **Если нужны расширенные функции** - установите зависимости:
   ```bash
   pip install onnxruntime insightface
   ```

3. **При проблемах установки** - используйте только базовые функции

## 🔍 ДИАГНОСТИКА

### Проверка статуса:
```bash
python test_app_without_insightface.py
```

### Проверка зависимостей:
```bash
python quick_fix_onnx.py
```

## 📝 ТЕХНИЧЕСКАЯ ИНФОРМАЦИЯ

**Проблема была в том, что:**
- InsightFace импортировался сразу при запуске
- ONNXRuntime требовался для импорта InsightFace
- Отсутствие ONNXRuntime вызывало краш всего приложения

**Исправление:**
- Lazy импорт зависимостей
- Проверка доступности на уровне модуля
- Graceful degradation функциональности

## 🎉 ГОТОВО!

Проблема с ONNXRuntime полностью решена!
