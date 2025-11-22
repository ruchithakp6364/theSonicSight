import cv2
import pyttsx3
import numpy as np

print("✔ OpenCV version:", cv2.__version__)

engine = pyttsx3.init()
engine.say("Docker build successful")
engine.runAndWait()

print("✔ TTS OK")
