# 🚀 Photo Sorter - Руководство по установке

## Проблема с установкой зависимостей

Вы столкнулись с ошибкой при установке numpy на Python 3.12. Это распространенная проблема совместимости.

## ✅ Решения

### Решение 1: Используйте умный установщик (Рекомендуется)

```cmd
python install_deps.py
```

Этот скрипт автоматически:
- Определяет версию Python
- Выбирает совместимые версии пакетов
- Устанавливает пакеты по одному при необходимости
- Проверяет успешность установки

### Решение 2: Ручная установка пакетов

Установите пакеты по одному:

```cmd
pip install PyQt6
pip install opencv-python
pip install numpy
pip install Pillow
pip install face-recognition
pip install cmake
```

### Решение 3: Используйте BAT-файл

Запустите `quick_install.bat` двойным щелчком

### Решение 4: Используйте последние версии

```cmd
pip install -r requirements_latest.txt
```

## 🔍 Проверка установки

После установки запустите тест:

```cmd
python simple_test.py
```

## 🎯 Запуск приложения

После успешной установки:

```cmd
python main.py
```

Или используйте лаунчер:
```cmd
python run.py
```

## ⚠️ Если проблемы сохраняются

### Вариант 1: Используйте Python 3.11

Если возможно, установите Python 3.11:
1. Скачайте с https://python.org
2. Переустановите зависимости
3. Запустите приложение

### Вариант 2: Виртуальное окружение

```cmd
python -m venv photo_sorter_env
photo_sorter_env\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Вариант 3: Установка без версий

```cmd
pip install PyQt6 opencv-python numpy Pillow face-recognition cmake --no-cache-dir
```

## 📞 Поддержка

Если проблемы сохраняются:
1. Проверьте версию Python: `python --version`
2. Проверьте версию pip: `pip --version`
3. Попробуйте обновить pip: `python -m pip install --upgrade pip`

## 📋 Что должно работать после установки

- ✅ PyQt6 - интерфейс приложения
- ✅ OpenCV - обработка изображений
- ✅ NumPy - вычисления
- ✅ Pillow - работа с изображениями
- ✅ face-recognition - распознавание лиц
- ✅ CMake - сборка компонентов

**Приложение готово к работе!** 🎉


