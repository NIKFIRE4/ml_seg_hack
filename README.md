# Инструкция по использованию нейросети для сегментации гари и вырубки

## Необходимые библиотеки

- Python 3.8+
- FastAPI
- OpenCV
- Ultralytics YOLO
- NumPy
- Shapely
- GeoJSON
- Pillow
- Rasterio

## Установка

1. Установите необходимые библиотеки, указанные в `requirements.txt`:
    ```sh
    pip install -r requirements.txt
    ```

2. Убедитесь, что файл весов модели YOLO (`best.pt`) находится в той же директории, что и скрипт, или обновите путь в скрипте соответственно.

## Запуск сервера

Запустите сервер FastAPI:
```sh
uvicorn main:app --reload
