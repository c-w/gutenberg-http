#!/usr/bin/env bash

set -euo pipefail

basedir="$(dirname "$0")/.."
db="db$(date +%s)"

(
  cd "${basedir}"

  sed -i "s|^APP_DB=.*|APP_DB=${db}|g" .env

  docker-compose exec web sh -c "GUTENBERG_DATA=/data/${db} python -m gutenberg_http initdb runserver"
)
