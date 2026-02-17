FROM python:3.10-slim-bookworm

# System update aur FFmpeg install
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
#akown
COPY . /app/
WORKDIR /app/

# Python requirements install
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

# Bot start command
CMD ["bash", "start.sh"]
