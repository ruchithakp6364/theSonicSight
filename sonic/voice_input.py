import speech_recognition as sr

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
    try:
        cmd = r.recognize_google(audio)
        print("Heard:", cmd)
        return cmd.lower()
    except:
        return None