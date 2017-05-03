#!/usr/bin/env bash
set -o errexit -o nounset

make_url() { echo "https://gutenbergapi.org/texts/[$1-$2]"; }
num_connections=20
requests_per_connection=1000
first_id=2701
last_id=$((first_id + requests_per_connection))

start_time=$(date '+%s')
pidlist=""
for (( i=0; i<num_connections; i++ )); do
    curl -s "$(make_url ${first_id} ${last_id})" > /dev/null &
    pidlist="${pidlist} $!"
done
for job in ${pidlist}; do wait "${job}"; done
end_time=$(date '+%s')

run_time=$((end_time-start_time))
total_requests=$((num_connections*requests_per_connection))
echo "Served ${total_requests} requests in ${run_time} seconds"
