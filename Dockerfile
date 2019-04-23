FROM python:alpine3.6

RUN apk add --no-cache db-dev

ARG BUILD_DEPENDENCIES="build-base"
ADD requirements.txt /app/requirements.txt
RUN apk add --no-cache ${BUILD_DEPENDENCIES} \
 && python3 -m venv /venv \
 && /venv/bin/pip install -r /app/requirements.txt \
 && apk del ${BUILD_DEPENDENCIES}

ADD gutenberg_http/ /app/gutenberg_http/

ENV BERKELEYDB_DIR="/usr"
ENV GUTENBERG_DATA="/data"
ENV GUTENBERG_HTTP_RUNSERVER_HOST="0.0.0.0"
ENV GUTENBERG_HTTP_RUNSERVER_PORT="80"
ENV GUTENBERG_HTTP_RUNSERVER_WORKERS="2"

WORKDIR /app

EXPOSE ${PORT}

CMD ["/venv/bin/python", "-m", "gutenberg_http", "initdb", "runserver"]
