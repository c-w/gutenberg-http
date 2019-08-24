#!/usr/bin/env bash

set -euo pipefail

if [[ -z "$1" ]] || [[ ! -f "$2" ]]; then
  echo "Usage: $0 <ssh-endpoint> <version>" >&2
  exit 1
fi

endpoint="$1"
version="$2"

ssh -t "${endpoint}" "
cd ~/gutenberg-http && \
sed -i 's/^BUILD_TAG=.*/BUILD_TAG=${version}/g' .env && \
docker-compose pull && \
docker-compose down --remove-orphans --timeout=0 && \
docker-compose up -d && \
echo 'Updated app to ${version}'
"
