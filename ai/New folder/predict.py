
from ultralytics import YOLO
MODEL_PATH = r"C:\\Users\\Dell Pc\\Desktop\\new_models\\runs\\detect\\yolov11m-custom\\weights\\best.pt"
IMAGE_PATH = r"C:\Users\Dell Pc\Downloads\WhatsApp Image 2025-12-08 at 4.51.46 PM (1).jpeg"

model = YOLO(MODEL_PATH)
model.predict(source=IMAGE_PATH, save=True, verbose=False)