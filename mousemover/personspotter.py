from ultralytics import YOLO
import time

# Initialize theperson detector
model = YOLO("yolov8l.pt")
detectiondict = dict()
start = time.time()
for elem in list(model.model.names.values()):
    detectiondict[elem] = []
end = time.time()
print(detectiondict)
print(end-start)

