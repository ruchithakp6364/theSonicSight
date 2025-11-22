import cv2

def get_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("⚠️ Camera not found. Using sample image instead.")
        return None
    cap.set(3, 640)
    cap.set(4, 480)
    return cap