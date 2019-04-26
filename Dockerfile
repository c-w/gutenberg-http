ARG PYTHON_VERSION=3.6
FROM python:${PYTHON_VERSION}-alpine AS builder

WORKDIR /app

RUN apk add --no-cache db-dev \
 && apk add --no-cache build-base

COPY requirements.txt .
RUN pip install -r requirements.txt \
 && pip wheel -r requirements.txt -w /deps

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY . .

RUN flake8
RUN mypy --ignore-missing-imports --cache-dir=/dev/null gutenberg_http
RUN nose2 -v

RUN find . -name '__pycache__' -type d -print0 | xargs -0 rm -rf

FROM python:${PYTHON_VERSION}-alpine

RUN apk add --no-cache db-dev

COPY --from=builder /deps /deps
RUN pip install --no-cache-dir /deps/*.whl

COPY --from=builder /app /app
WORKDIR /app

ENV BERKELEYDB_DIR="/usr"
ENV GUTENBERG_DATA="/data/db1"
ENV LOG_LEVEL="info"
ENV HOST="0.0.0.0"
ENV PORT="80"
ENV WORKERS="2"

EXPOSE ${PORT}

CMD ["python", "-m", "gutenberg_http", "initdb", "runserver"]
