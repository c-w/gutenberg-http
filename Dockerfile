FROM python:alpine3.6

RUN apk add --no-cache db-dev

ADD requirements.txt /app/requirements.txt
RUN apk add --virtual .build-deps --no-cache build-base \
 && pip install --no-cache-dir -r /app/requirements.txt \
 && apk del .build-deps

ADD gutenberg_http/ /app/gutenberg_http/

ENV BERKELEYDB_DIR="/usr"
ENV GUTENBERG_DATA="/data"
ENV HOST="0.0.0.0"
ENV PORT="80"
ENV WORKERS="2"

WORKDIR /app

EXPOSE ${PORT}

CMD ["python", "-m", "gutenberg_http", "initdb", "runserver"]
