FROM python:3.10

ENV TZ=Europe/Moscow

WORKDIR /app

COPY requirements.txt .
RUN apt-get update

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir \
     && apt-get install -y netcat-traditional

COPY ./entrypoint.sh /
RUN chmod 777 /entrypoint.sh

COPY . /app

ENTRYPOINT ["/entrypoint.sh"]