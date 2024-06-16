import os
import cv2
from ultralytics import YOLO
import numpy as np
from shapely.geometry import Polygon
import geojson
from PIL import Image
import rasterio
from fastapi import FastAPI, UploadFile, File
import shutil
from typing import List
import uvicorn
import zipfile
import io
from os import path
import root
app = FastAPI()
# Загрузка модели
model_best = YOLO("best.pt")
# Функция для масштабирования изображения
def upscale_image(image, scale_factor):
    image = Image.open(image)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    return image.resize((new_width, new_height), Image.LANCZOS)


# Путь к папке для временного хранения загруженных файлов
upload_folder = 'uploaded_files'
os.makedirs(upload_folder, exist_ok=True)

# Путь к папке для сохранения GeoJSON файлов
output_folder = 'geojson_output'
os.makedirs(output_folder, exist_ok=True)

# Словарь для масштабирования
rescale_dict = {
    "10m" : 1,
    "20m" : 2,
    "60m" : 6,
}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    image_zip = zipfile.ZipFile(io.BytesIO(file.file.read()), "r")
    #print(image_zip.open("GRANULE", "r", force_zip64=True))
    print(image_zip.infolist())
    for item in image_zip.infolist():
        if item.filename.endswith('.jp2'):
            key = item.filename.rstrip(".jp2")[-3:]
            if key in rescale_dict:
                scale_factor = rescale_dict[key]
                image_zip.extract(item.filename)


                filepath = "./" + item.filename
                bytes = open("./" + item.filename, "r")

                img_upscaled = upscale_image(filepath, scale_factor)
                img_array = np.array(img_upscaled)

                # Predict
                results = model_best.predict(source=img_array)

                # Получение геоинформации
                with rasterio.open(filepath) as src:
                    transform = src.transform
                    crs = src.crs

                bytes.close()
                os.remove(filepath)
                # Обработка результатов сегментации
                for idx, result in enumerate(results):
                    if result.masks is None:

                        print(f"No masks found for result {idx}")
                        continue  # Пропускаем, если маски отсутствуют

                    masks = result.masks.data.cpu().numpy()
                    orig_shape = result.orig_shape

                    features = []

                    for mask in masks:
                        # Преобразование в полигон
                        contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL,
                                                       cv2.CHAIN_APPROX_SIMPLE)

                        if len(contours) > 0:
                            polygon_pts = contours[0].reshape(-1, 2)
                            polygon_pts[:, 0] = np.clip(polygon_pts[:, 0], 0, orig_shape[1] - 1)
                            polygon_pts[:, 1] = np.clip(polygon_pts[:, 1], 0, orig_shape[0] - 1)
                            geo_polygon_pts = [rasterio.transform.xy(transform, y, x) for x, y in polygon_pts]
                            polygon = Polygon(geo_polygon_pts)
                            feature = geojson.Feature(geometry=polygon.__geo_interface__, properties={"class": "fire"})
                            features.append(feature)
                    feature_collection = geojson.FeatureCollection(features)
                    # GeoJSON

                    return geojson.dumps(feature_collection)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)







