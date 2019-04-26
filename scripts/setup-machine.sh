#!/usr/bin/env bash

set -euo pipefail

if [[ -z "$1" ]] || [[ ! -f "$2" ]]; then
  echo "Usage: $0 <ssh-endpoint> <path-to-prod-config-file>" >&2
  exit 1
fi

endpoint="$1"
config="$2"

ssh -t "${endpoint}" '
sudo apt-get update && \
sudo apt-get install -y curl git authbind && \
curl -fsSL https://get.docker.com -o get-docker.sh && \
sudo sh get-docker.sh && \
rm get-docker.sh && \
sudo usermod -aG docker ${USER} && \
sudo curl -fsSL "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
sudo chmod a+x /usr/local/bin/docker-compose && \
sudo touch /etc/authbind/byport/80 && \
sudo chown "${USER}:${USER}" /etc/authbind/byport/80 && \
sudo chmod 755 /etc/authbind/byport/80 && \
git clone https://github.com/c-w/gutenberg-http.git ~/gutenberg-http && \
echo "Done with machine setup"
'

scp "${config}" "${endpoint}:~/gutenberg-http/.env"

ssh -t "${endpoint}" '
cd ~/gutenberg-http && \
docker-compose up --build -d && \
(crontab -l; echo "0 1 * * * ${PWD}/scripts/update-data.sh") | crontab - && \
echo "Done with app setup"
'
