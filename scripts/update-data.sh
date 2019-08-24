#!/usr/bin/env bash

set -euo pipefail

basedir="$(dirname "$0")/.."
db="db$(date +%s)"

(
  cd "${basedir}"

  sed -i "s|^APP_DB=.*|APP_DB=${db}|g" .env

  echo "[$(date)] Starting upgrade to ${db}"
  /usr/local/bin/docker-compose exec -T web sh -c "GUTENBERG_DATA=/data/${db} python -m gutenberg_http initdb runserver"
  echo "[$(date)] Done with upgrade to ${db}"
)
