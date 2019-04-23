FROM python:alpine3.6

RUN apk add --no-cache db-dev

WORKDIR /app

COPY requirements.txt .
RUN apk add --virtual .build-deps --no-cache build-base \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del .build-deps

COPY . .

ENV BERKELEYDB_DIR="/usr"
ENV GUTENBERG_DATA="/data/db1"
ENV HOST="0.0.0.0"
ENV PORT="80"
ENV WORKERS="2"

EXPOSE ${PORT}

CMD ["python", "-m", "gutenberg_http", "initdb", "runserver"]
