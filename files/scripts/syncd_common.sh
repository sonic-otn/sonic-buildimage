#!/bin/bash

#
# common functions used by "syncd" scipts (syncd.sh, gbsyncd.sh, etc..)
# scripts using this must provide implementations of the following functions:
# 
# waitplatform
# stopplatform1 and stopplatform2
# 
# For examples of these, see gbsyncd.sh and syncd.sh.
#

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

start() {
    debug "Starting ${SERVICE}$DEV service..."

    lock_service_state_change

    wait_for_database_service

    # start service docker
    /usr/bin/${SERVICE}.sh start $DEV
    debug "Started ${SERVICE} service..."

    unlock_service_state_change
}

wait() {
    /usr/bin/${SERVICE}.sh wait $DEV
}

stop() {
    debug "Stopping ${SERVICE}$DEV service..."

    lock_service_state_change

    stopplatform1

    /usr/bin/${SERVICE}.sh stop $DEV
    debug "Stopped ${SERVICE}$DEV service..."

    unlock_service_state_change
}
