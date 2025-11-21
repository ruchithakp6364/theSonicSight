# vision.py - YOLOv8n optimized for SonicSight
from ultralytics import YOLO
import cv2
import torch

# Load YOLOv8 nano model
model = YOLO('sonicsight/models/yolov8n.pt')
model.to('cpu')
model.fuse()  # merge Conv + BN layers for speed


def estimate_distance(bbox):
    """
    Estimate distance in meters from bounding box size.
    Works well for person, obstacles.
    Larger box = closer.
    """
    x1, y1, x2, y2 = bbox
    area = (x2 - x1) * (y2 - y1)

    # Tuned empirically for indoor navigation distance
    distance = 70000 / (area + 1)

    distance = max(0.3, min(distance, 8.0))  # between 0.3m and 8m
    return round(distance, 2)


def find_direction(frame_width, bbox):
    """
    Returns whether object is LEFT, CENTER, or RIGHT in view.
    """
    x1, _, x2, _ = bbox
    center_x = (x1 + x2) / 2

    if center_x < frame_width * 0.33:
        return "left"
    elif center_x > frame_width * 0.66:
        return "right"
    else:
        return "center"


def detect_objects(frame):
    """Run YOLOv8 object detection on a frame."""
    h, w = frame.shape[:2]
    results = model.predict(source=frame, imgsz=480, conf=0.45, verbose=False)

    detections = []
    annotated_frame = results[0].plot()  # draw boxes on frame

    for box in results[0].boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = box
        label = model.names[int(cls)]

        bbox = [int(x1), int(y1), int(x2), int(y2)]

        detections.append({
            "label": label,
            "confidence": round(float(conf), 2),
            "bbox": bbox,
            "distance_m": estimate_distance(bbox),
            "direction": find_direction(w, bbox)
        })

    return annotated_frame, detections


# Debug tester
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
