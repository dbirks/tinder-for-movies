#!/usr/bin/env bash
# wait-for-it.sh: Wait until a host and port are available
# Usage: wait-for-it.sh host:port -- command args

set -e

host="$1"
shift

until nc -z $host; do
  >&2 echo "Waiting for $host to be available..."
  sleep 1
done

>&2 echo "$host is up!"
exec "$@"
