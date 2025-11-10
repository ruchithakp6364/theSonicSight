import cv2
from camera_worker import get_camera
from vision import detect_objects
from navigation import calculate_ttc
from path_analyzer import predict_safe_path
from feedback import speak_alert
from imu_handler import read_imu_data
from sensor_fusion import fuse_data

def main():
    cap = get_camera()
    if cap is None:
        frame = cv2.imread("sample.jpg")
        frame, detections = detect_objects(frame)
        print(detections)
        return

    print("🎥 SonicSight running... Press Q to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, detections = detect_objects(frame)
        imu_data = read_imu_data()

        for d in detections:
            ttc = calculate_ttc(d["label"], d["bbox"])
            if ttc and ttc < 2.0:
                fused = fuse_data(ttc, imu_data)
                speak_alert(f"Warning! {d['label']} ahead in {fused} seconds!")

        suggestion = predict_safe_path(detections)
        cv2.putText(frame, suggestion, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.imshow("SonicSight", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
