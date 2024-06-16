# Инструкция по использованию нейросети для сегментации гари и вырубки

## Необходимые библиотеки:

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

1. Установите библиотеки из `requirements.txt`:
    ```sh
    pip install -r requirements.txt
    ```

2. Убедитесь, что файл весов модели YOLO (`best.pt`) находится в той же директории, что и скрипт, или обновите путь в скрипте соответственно.

## Запуск сервера

3. Запустите сервер FastAPI:
    ```sh
    uvicorn main:app --reload
    ```

## Использование API

4. Загрузите ваш архив спутникового снимка, используя эндпоинт `/uploadfiles/` через Postman или любой API-клиент и загрузите через form data в поле `file`.

### Пример запроса

**POST** `/uploadfiles/`

**Запрос:**
- `files`: Архивированная папка с фотографиями JP2

**Ответ:**
- `message`: geojson

