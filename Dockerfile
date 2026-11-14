FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/core

RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

RUN pip install -i https://mirror-pypi.runflare.com/simple --no-cache-dir --upgrade pip  \
    && pip install -i https://mirror-pypi.runflare.com/simple --no-cache-dir -r ./requirements.txt

COPY . .
