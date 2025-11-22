from gtts import gTTS
import os
import tempfile
import threading
import platform
import time

last_spoken = {"text": "", "time": 0}

def _play_audio(filename):
    """Play audio file in background depending on OS."""
    if platform.system() == "Windows":
        os.system(f"start /min {filename}")
    elif platform.system() == "Darwin":
        os.system(f"afplay {filename} &")
    else:
        os.system(f"mpg123 -q {filename} &")

def _generate_and_play(text):
    """Generate and play TTS without blocking main thread."""
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        filename = fp.name
        tts.save(filename)
    _play_audio(filename)

def speak_alert(text, cooldown=3):
    """
    Speak only if last message was different or cooldown passed.
    Prevents overlap and repeated noise.
    """
    global last_spoken
    now = time.time()

    # Skip if same alert spoken recently
    if text == last_spoken["text"] and (now - last_spoken["time"] < cooldown):
        return

    last_spoken = {"text": text, "time": now}
    threading.Thread(target=_generate_and_play, args=(text,), daemon=True).start()