#!/bin/bash

function debug()
{
    /usr/bin/logger $1
    /bin/echo `date` "- $1" >> ${DEBUGLOG}
}

function lock_service_state_change()
{
    debug "Locking ${LOCKFILE} from ${SERVICE}$DEV service"

    exec {LOCKFD}>${LOCKFILE}
    /usr/bin/flock -x ${LOCKFD}
    trap "/usr/bin/flock -u ${LOCKFD}" 0 2 3 15

    debug "Locked ${LOCKFILE} (${LOCKFD}) from ${SERVICE}$DEV service"
}

function unlock_service_state_change()
{
    debug "Unlocking ${LOCKFILE} (${LOCKFD}) from ${SERVICE}$DEV service"
    /usr/bin/flock -u ${LOCKFD}
}

function wait_for_database_service()
{
    # Wait for redis server start before database clean
    until [[ $($SONIC_DB_CLI PING | grep -c PONG) -gt 0 ]]; do
      sleep 1;
    done

    # Wait for configDB initialization
    until [[ $($SONIC_DB_CLI CONFIG_DB GET "CONFIG_DB_INITIALIZED") ]];
        do sleep 1;
    done
}

# This function cleans up the tables with specific prefixes from the database
# $1 the index of the database
# $2 the string of a list of table prefixes
function clean_up_tables()
{
    $SONIC_DB_CLI $1 EVAL "
    local tables = {$2}
    for i = 1, table.getn(tables) do
        local matches = redis.call('KEYS', tables[i])
        for j,name in ipairs(matches) do
            redis.call('DEL', name)
        end
    end" 0
}

start() {
    debug "Starting ${SERVICE}$DEV service..."

    lock_service_state_change

    wait_for_database_service

    $SONIC_DB_CLI APPL_DB FLUSHDB

    # start service docker
    /usr/bin/${SERVICE}.sh start $DEV
    debug "Started ${SERVICE}$DEV service..."

    # Unlock has to happen before reaching out to peer service
    unlock_service_state_change
}

wait() {
    if [[ ! -z $DEV ]]; then
        /usr/bin/docker-wait-any -s ${SERVICE}$DEV 
    else
        /usr/bin/docker-wait-any -s ${SERVICE}
    fi
}

stop() {
    debug "Stopping ${SERVICE}$DEV service..."

    [[ -f ${LOCKFILE} ]] || /usr/bin/touch ${LOCKFILE}

    lock_service_state_change

    /usr/bin/${SERVICE}.sh stop $DEV
    debug "Stopped ${SERVICE}$DEV service..."

    # Unlock has to happen before reaching out to peer service
    unlock_service_state_change
}

DEV=$2

SERVICE="otss"
DEBUGLOG="/tmp/otss-syncd-debug$DEV.log"
LOCKFILE="/tmp/otss-syncd-lock$DEV"
NAMESPACE_PREFIX="asic"
if [ "$DEV" ]; then
    NET_NS="$NAMESPACE_PREFIX$DEV" #name of the network namespace
    SONIC_DB_CLI="sonic-db-cli -n $NET_NS"
else
    NET_NS=""
    SONIC_DB_CLI="sonic-db-cli"
fi

case "$1" in
    start|wait|stop)
        $1
        ;;
    *)
        echo "Usage: $0 {start|wait|stop}"
        exit 1
        ;;
esac
