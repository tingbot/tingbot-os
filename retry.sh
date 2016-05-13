#!/bin/bash

set -o errexit

function usage () {
    echo "usage:" >&2
    echo "  retry.sh SECONDS COMMAND..." >&2
    exit 1
}

function now () {
    date +%s
}

if [[ $# -lt 2 ]]; then
    usage
fi

# make sure the first argument is an integer
if ! [ "$1" -eq "$1" ] ; then
    usage
fi

timeout_seconds=$1
shift

start_time=$(now)

while [[ $(($start_time + $timeout_seconds)) -gt $(now) ]]; do
    set +o errexit
    ( "$@" )
    exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        break
    fi
    sleep 0.1
done

exit $exit_code
