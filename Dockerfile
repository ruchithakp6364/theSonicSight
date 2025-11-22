# ===============================
# SonicSight Fast Build Dockerfile
# ===============================

FROM python:3.10

# Use faster Debian mirror + retries to avoid timeout errors
RUN printf "deb http://deb.debian.org/debian trixie main\n\
deb http://security.debian.org/debian-security trixie-security main\n" \
> /etc/apt/sources.list

# Install system libs needed for OpenCV + audio (fast + stable)
RUN apt-get update -o Acquire::Retries=5 -o Acquire::http::No-Cache=True \
 && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    espeak \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy source code
WORKDIR /workspace
COPY . /workspace

# Test OpenCV + TTS works
CMD ["python", "-c", "import cv2, pyttsx3; print('OpenCV OK:', cv2.__version__); print('TTS OK')"]

