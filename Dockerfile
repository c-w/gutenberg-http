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
WORKDIR /app
EXPOSE 80
CMD ["/venv/bin/python", "-m", "gutenberg_http", "--port=80", "--host=0.0.0.0"]
