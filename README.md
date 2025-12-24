# 🦾 SonicSight  
### AI-Powered Real-Time Navigation for the Visually Impaired

---

## 📌 Problem Statement

Visually impaired individuals lack real-time awareness of nearby obstacles and safe paths.  
Most existing solutions are either expensive, hardware-heavy, or do not adapt dynamically to changing environments.

---

## 💡 Solution

**SonicSight** is an AI-powered navigation assistant that uses a camera and intelligent voice feedback to help users move safely.

It detects obstacles in real time, estimates distance and collision risk, and provides **clear spoken guidance** such as:

> “Person detected 1 meter ahead, slightly to your left.”

The system avoids repetition, adapts to congestion, and supports voice-driven destination navigation.

---

## 🧠 Technology Stack

- **Computer Vision**: YOLOv8n (Ultralytics)
- **AI / ML**: PyTorch
- **Navigation Logic**: Custom safe-path prediction
- **Audio Feedback**: Text-to-Speech (TTS)
- **Sensor Fusion**: Vision + IMU simulation
- **Automation**: GitLab CI/CD (headless validation)
- **Language**: Python

---

## 🌍 Open-Source Used

- Ultralytics YOLOv8
- OpenCV (GUI & headless)
- PyTorch ecosystem
- NumPy

All components are modular and open-source friendly.

---

## 🚀 Impact

- Improves independent mobility for visually impaired users
- Provides real-time environmental awareness
- Reduces collision risk through early warnings
- Demonstrates how AI + automation can power assistive technology

---

## 🤖 Why GitLab Automation Matters

GitLab CI/CD validates SonicSight in a **reproducible, hardware-independent environment**, proving engineering reliability beyond a demo.  
It ensures the project is **deployable, testable, and scalable**.

---

## 🏁 Status

SonicSight is an **MVP with real-time AI capabilities**, designed for further expansion into a production-ready assistive system.

---


## 🧪 How to Run Locally
```bash
pip install -r requirements.txt
python main.py

