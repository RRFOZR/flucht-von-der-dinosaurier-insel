# Dockerfile for Flucht von der Dinosaurier-Insel
# WARNING: Docker is not ideal for desktop games with GUI!
# See PACKAGING.md for better alternatives (PyInstaller)

FROM python:3.11-slim

# Install system dependencies for pygame and audio
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    libjpeg-dev \
    python3-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy game files
COPY . .

# Set display for GUI (requires X11 forwarding)
ENV DISPLAY=:0

# Run the game
CMD ["python", "main.py"]
