import cv2
import time
import torch
from vision import detect_objects
from feedback import speak_alert
from navigation import calculate_ttc, update_navigation_state
from sensor_fusion import fuse_data
from imu_handler import read_imu_data
from camera_worker import get_camera

def main():
    print("\n🚀 SonicSight System Initializing...")
    cap = get_camera()

    if cap is None or not cap.isOpened():
        print("⚠️ No camera detected! Running in test mode with sample image.")
        frame = cv2.imread("sample.jpg")
        frame, detections = detect_objects(frame)
        print("🧠 Detected:", detections)
        return

    print("🎥 SonicSight running... Press Q to quit.")
    
    last_nav_speech = 0
    last_detection_speech = 0
    fps_time = time.time()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Frame capture failed, stopping...")
            break

        frame_count += 1

        # === 1️⃣ Object Detection ===
        annotated_frame, detections = detect_objects(frame)
        imu_data = read_imu_data()

        # === 2️⃣ Navigation Logic ===
        nav_message, dist_to_goal = update_navigation_state(detections)

        # Speak navigation every 5s (not continuous)
        if time.time() - last_nav_speech > 5:
            speak_alert(f"{nav_message}. Distance to goal: {dist_to_goal:.1f} meters.")
            last_nav_speech = time.time()

        # === 3️⃣ Collision Warning (TTC Logic) ===
        for d in detections:
            ttc = calculate_ttc(d["label"], d["bbox"])
            if ttc and ttc < 2.0 and time.time() - last_detection_speech > 3:
                fused_ttc = fuse_data(ttc, imu_data)
                alert_text = f"Warning! {d['label']} ahead in {fused_ttc:.1f} seconds!"
                speak_alert(alert_text)
                last_detection_speech = time.time()

        # === 4️⃣ FPS Display for Performance ===
        if frame_count % 10 == 0:
            now = time.time()
            fps = 10 / (now - fps_time)
            fps_time = now
            cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # === 5️⃣ Display the frame ===
        cv2.imshow("🦾 SonicSight - YOLOv8n Navigation", annotated_frame)

        # Quit if 'q' pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 Exiting SonicSight...")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ SonicSight stopped safely.")

if __name__ == "__main__":
    main()