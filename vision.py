# vision.py - YOLOv8n optimized for SonicSight
from ultralytics import YOLO
import cv2
import torch

# Load YOLOv8 nano model
model = YOLO('yolov8n.pt')
model.to('cpu')
model.fuse()  # merge Conv + BN layers for speed

def detect_objects(frame):
    """Run YOLOv8 object detection on a frame."""
    results = model.predict(source=frame, imgsz=480, conf=0.45, verbose=False)

    detections = []
    annotated_frame = results[0].plot()  # draw boxes on frame

    for box in results[0].boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = box
        label = model.names[int(cls)]
        detections.append({
            "label": label,
            "confidence": round(float(conf), 2),
            "bbox": [int(x1), int(y1), int(x2), int(y2)]
        })

    return annotated_frame, detections

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame, detections = detect_objects(frame)
        print(detections)
        cv2.imshow("SonicSight - YOLOv8n", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()