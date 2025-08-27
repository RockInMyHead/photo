# 🚀 Установка InsightFace для Photo Sorter

## 📋 Проблема:
Вы пытаетесь установить зависимости из неправильной папки.

## ✅ Решение:

### Шаг 1: Перейдите в папку проекта
```cmd
cd D:\photo
```

### Шаг 2: Установите зависимости
```cmd
pip install insightface onnxruntime hdbscan scikit-learn tqdm
```

ИЛИ используйте файл зависимостей:
```cmd
pip install -r requirements_insight.txt
```

### Шаг 3: Проверьте установку
```cmd
python -c "import insightface; print('InsightFace OK')"
```

### Шаг 4: Запустите приложение
```cmd
python main_simple_fixed.py
```

## 🎯 В приложении:
1. Выберите папку с фотографиями
2. Нажмите "Сканировать"
3. Нажмите "Сортировать (InsightFace, перенос)"
4. Выберите папку для результатов

## ⚠️ Если установка не работает:

### Вариант 1: Установка по частям
```cmd
pip install insightface
pip install onnxruntime
pip install hdbscan
pip install scikit-learn
pip install tqdm
```

### Вариант 2: Обновите pip
```cmd
python -m pip install --upgrade pip
pip install insightface onnxruntime hdbscan scikit-learn tqdm
```

### Вариант 3: Используйте conda
```cmd
conda install insightface
pip install hdbscan scikit-learn tqdm
```

## 📞 После установки:

Запустите приложение:
```cmd
python main_simple_fixed.py
```

И нажмите кнопку "Сортировать (InsightFace, перенос)" для использования продвинутого алгоритма!


