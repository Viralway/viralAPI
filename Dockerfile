FROM mcr.microsoft.com/playwright:v1.62.0-jammy

WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip3 install --upgrade pip && pip3 install .
RUN python3 -m playwright install --with-deps
