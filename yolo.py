from ultralytics import YOLO


model = YOLO('yolov8n')

model.predict('PATH')