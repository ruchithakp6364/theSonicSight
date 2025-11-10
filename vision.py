import cv2
import torch
import json
import os
from datetime import datetime
from config import CONF_THRESHOLD

# Load YOLOv5 model once
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = CONF_THRESHOLD

def detect_objects(frame):
    results = model(frame)
    detections = []

    for *box, conf, cls in results.xyxy[0].tolist():
        if conf < CONF_THRESHOLD:
            continue
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls)]
        detections.append({
            "label": label,
            "confidence": round(conf, 2),
            "bbox": [x1, y1, x2, y2]
        })
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    os.makedirs("reports", exist_ok=True)
    with open(os.path.join("reports", f"detections_{datetime.now().strftime('%H%M%S')}.json"), "w") as f:
        json.dump(detections, f, indent=4)

    return frame, detections
