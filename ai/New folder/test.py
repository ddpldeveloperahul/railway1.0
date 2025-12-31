from ultralytics import YOLO

# Load a model
model = YOLO("C://Users//Dell Pc//Desktop//new_models//yolo11m.pt")  # load a pretrained YOLO

model.train(data="C://Users//Dell Pc//Desktop//new_models//data.yaml", epochs=100, imgsz=640, batch=8, name="yolov11m-custom", workers=0, device="cpu")