FROM python:3.10.9-slim-buster

WORKDIR /bot

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxrender1 \
    libxi6 \
    libxcursor1 \
    libxcomposite1 \
    libxdamage1 \
    libxtst6 \
    libfreetype6 \
    libdbus-1-3 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxss1 \
    libasound2 \
    fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir webdriver_manager

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "utility.py"]
