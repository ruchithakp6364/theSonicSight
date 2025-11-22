import os
import time
import torch
import numpy as np

# Detect if running in GitLab CI or Docker (headless mode)
HEADLESS = os.getenv("CI") == "true" or os.getenv("GITLAB_CI") == "true"

try:
    import cv2
    if HEADLESS:
        print("🧠 Running in headless CI/CD mode (no GUI, no camera).")
    else:
        print("🖥️ Running in local GUI mode with camera access.")
except ImportError as e:
    print("⚠️ OpenCV import failed:", e)
    print("💡 Try installing 'opencv-python-headless' for CI environments.")
    cv2 = None

from vision import detect_objects
from feedback import speak_alert
from navigation import calculate_ttc, update_navigation_state
from sensor_fusion import fuse_data
from imu_handler import read_imu_data
from camera_worker import get_camera

# NEW import
from voice_command import listen_for_destination


def main():
    print("\n🎤 SonicSight ready. Please say your destination.")

    # 👉 NEW: voice-controlled destination
    destination_name = None
    while destination_name is None:
        destination_name = listen_for_destination()

    speak_alert(f"Navigating to {destination_name}")

    print("\n🚀 SonicSight System Initializing...")

    if not HEADLESS:
        cap = get_camera()
    else:
        cap = None

    # --- Handle missing camera in CI/CD ---
    if cap is None or not (hasattr(cap, "isOpened") and cap.isOpened()):
        print("⚠️ No camera detected or headless mode active! Running in test mode with sample frame.")
        if cv2 is not None:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)  # dummy black frame
            frame, detections = detect_objects(frame)
            print("🧠 Detected (simulated):", detections)
        else:
            print("❌ OpenCV not available, skipping detection.")
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

        # === 2️⃣ Navigation Logic (updated) ===
        nav_message, dist_to_goal = update_navigation_state(
            detections,
            destination_name=destination_name
        )

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

        # === 4️⃣ FPS Display ===
        if frame_count % 10 == 0:
            now = time.time()
            fps = 10 / (now - fps_time)
            fps_time = now
            cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # === 5️⃣ Display the frame ===
        if not HEADLESS:
            cv2.imshow("🦾 SonicSight - YOLOv8n Navigation", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("🛑 Exiting SonicSight...")
                break
        else:
            print(f"🧭 Headless Mode Output → {nav_message} | Distance: {dist_to_goal:.2f} m")
            break

    if not HEADLESS and cv2 is not None:
        cap.release()
        cv2.destroyAllWindows()

    print("✅ SonicSight stopped safely.")


if __name__ == "__main__":
    main()
