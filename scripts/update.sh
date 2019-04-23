#!/usr/bin/env bash

set -euo pipefail

basedir="$(dirname "$0")/.."
db="db$(date +%s)"

(
  cd "${basedir}"

  docker-compose exec web sh -c "GUTENBERG_DATA=/data/${db} python -m gutenberg_http initdb runserver"

  find . -type d -name 'db*' -and -not -name "${db}" -and -not -path '*/.git/*' -exec rm -rf {} \;
)
