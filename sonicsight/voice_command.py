import speech_recognition as sr
import json

with open("sj.json", "r") as f:
    DESTINATIONS = json.load(f)

def listen_for_destination():
    r = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Speak your destination…")

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio).lower()
        print("🗣 You said:", text)

        for dest in DESTINATIONS.keys():
            if dest.lower() in text:
                return dest

        print("❌ No valid destination found.")
        return None

    except:
        return None

