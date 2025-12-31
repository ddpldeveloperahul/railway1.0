from ultralytics import YOLO

# Load a model
model = YOLO("D://yolo_model_trian//yolo11m.pt")  # load a pretrained YOLO

model.train(data="D://yolo_model_trian//data.yaml", epochs=100, imgsz=640, batch=8, name="yolov11m-custom", workers=0, device="cpu")