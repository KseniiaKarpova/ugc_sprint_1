FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN  apt-get update \
     && pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY ./src .

ENTRYPOINT ["python", "main.py"]