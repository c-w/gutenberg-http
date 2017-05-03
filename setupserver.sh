#!/usr/bin/env sh
set -o errexit -o nounset

# configuration
package="gutenberg_http"
dependencies="libdb-dev"
port="8080"
user="$USER"
rootdir="/opt/${package}"
pyenv="${rootdir}/pyenv"
initfile="${rootdir}/daemon"
logfile="${rootdir}/log"
pidfile="${rootdir}/pid"
domain="gutenbergapi.org"
ssl_cert="/etc/letsencrypt/live/${domain}/fullchain.pem"
ssl_key="/etc/letsencrypt/live/${domain}/privkey.pem"
envs="GUTENBERG_DATA='${rootdir}/data'"
exe="${envs} '${pyenv}/bin/runserver' --port ${port}"

# install system dependencies
sudo apt-get update -q
sudo apt-get upgrade -q -y
sudo apt-get install -q -y python3-venv python3-dev build-essential nginx "${dependencies}"
sudo apt-get autoremove -q -y
sudo rm -f '/etc/nginx/sites-enabled/default'

# forward port 80 and 443 to application port
sudo tee "/etc/nginx/sites-available/${package}" << EOF
server {
    listen 80;
    server_name ${domain};
    rewrite ^(.*)$ https://\$http_host\$1 permanent;
}

server {
    listen 443;
    ssl on;
    ssl_certificate ${ssl_cert};
    ssl_certificate_key ${ssl_key};
    server_name ${domain};

    add_header 'Access-Control-Allow-Origin' "\$http_origin" always;
    add_header 'Access-Control-Allow-Credentials' 'true' always;
    add_header 'Access-Control-Allow-Methods' 'GET' always;
    add_header 'Access-Control-Allow-Headers' 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Requested-With' always;

    location / {
        proxy_pass_header Server;
        proxy_set_header Host \$http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Scheme \$scheme;
        proxy_pass http://127.0.0.1:${port};
    }
}
EOF
sudo ln -f -s "/etc/nginx/sites-available/${package}" '/etc/nginx/sites-enabled'

# install service
sudo mkdir -p "${rootdir}"
sudo chown "${user}:${user}" "${rootdir}"
'/usr/bin/python3' -m venv "${pyenv}"
"${pyenv}/bin/pip" install --upgrade pip
"${pyenv}/bin/pip" install "${package}"
tee "${initfile}" << EOF
#!/bin/sh
### BEGIN INIT INFO
# Provides:          ${package}
# Required-Start:    \$local_fs \$network \$named \$time \$syslog
# Required-Stop:     \$local_fs \$network \$named \$time \$syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       ${package} service
### END INIT INFO

# start of configuration
package="${package}"
SCRIPT="${exe}"
RUNAS="${user}"
PIDFILE="${pidfile}"
LOGFILE="${logfile}"
# end of configuration

log() { echo "\$@" >&2; }
is_running() { [ -s "\$PIDFILE" ] && pgrep --pidfile "\$PIDFILE" >/dev/null ; }
kill_process() { pkill --pidfile "\$PIDFILE"; }

start() {
  if is_running; then
    log 'Service already running'
    return 1
  fi
  log 'Starting service'
  local CMD="\$SCRIPT >> \\"\$LOGFILE\\" 2>&1 & echo \\\$!"
  su -c "\$CMD" \$RUNAS > "\$PIDFILE"
  log 'Service started'
}

stop() {
  if ! is_running; then
    log 'Service not running'
    return 1
  fi
  log 'Stopping service'
  if ! kill_process; then
    log 'Failed to stop service'
    return 2
  fi
  rm -f "\$PIDFILE"
  log 'Service stopped'
}

status() {
  if is_running; then
    log 'Service *is* running'
  else
    log 'Service _not_ running'
  fi
}

uninstall() {
  echo -n "Are you really sure you want to uninstall this service? That cannot be undone. [yes|No] "
  local SURE
  read SURE
  if [ "\$SURE" != "yes" ]; then
    return 1
  fi
  if ! stop; then
    log 'Aborting uninstall'
  fi
  log "Notice: log file will not be removed: '\$LOGFILE'"
  update-rc.d -f "\$package" remove
  rm -f "\$0"
}

case "\$1" in
  start)      start         ;;
  stop)       stop          ;;
  status)     status        ;;
  uninstall)  uninstall     ;;
  restart)    stop && start ;;
  *)          log "Usage: \$0 {start|stop|restart|uninstall}"
esac
EOF
chmod +x "${initfile}"
touch "${logfile}"
sudo ln -f -s "${initfile}" "/etc/init.d/${package}"
sudo update-rc.d "${package}" defaults

# start the service
date; eval "${exe}"
