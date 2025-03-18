FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libssl-dev

COPY ../../ /data/app/
WORKDIR /data/app/

RUN pip install --no-cache-dir -r requirements.txt
