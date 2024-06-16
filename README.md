Инструкция по использованию нейросети для сегментации гари и вырубки Необходимые библиотеки: 
• Python 3.8+ 
• FastAPI 
• OpenCV 
• Ultralytics YOLO 
• NumPy 
• Shapely 
• GeoJSON 
• Pillow 
• Rasterio

Установите requirements.txt
Убедитесь, что файл весов модели YOLO (“best.pt”) находится в той же директории или обновите путь в скрипте соответственно.
Запустите сервер FastAPI: 
uvicorn main:app –reload
Загрузите ваш архив c папкой GRANULE, используя эндпоинт “/uploadfiles/” через postman или любой API –клиент, например, Postman POST /uploadfiles/ 
Запрос: 
• “files”: Архивированная папка с фотографиями JP2 
Ответ: 
• “message” : geojson
