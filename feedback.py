from gtts import gTTS
import os
import tempfile
import platform

def speak_alert(message):
    print("🔊", message)
    tts = gTTS(text=message, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        filename = fp.name
        tts.save(filename)

    if platform.system() == "Windows":
        os.system(f"start {filename}")
    elif platform.system() == "Darwin":
        os.system(f"afplay {filename}")
    else:
        os.system(f"mpg123 {filename}")
