#!/bin/bash

. /usr/local/bin/syncd_common.sh

function stopplatform1()
{
    debug "shutdown syncd-ot process ..."
    /usr/bin/docker exec -i syncd-ot$DEV /usr/bin/syncd_request_shutdown --cold

    # wait until syncd-ot quits gracefully or force syncd-ot to exit after 
    # waiting for 20 seconds
    start_in_secs=${SECONDS}
    end_in_secs=${SECONDS}
    timer_threshold=20
    while docker top syncd-ot$DEV | grep -q /usr/bin/syncd-ot \
            && [[ $((end_in_secs - start_in_secs)) -le $timer_threshold ]]; do
        sleep 0.1
        end_in_secs=${SECONDS}
    done

    if [[ $((end_in_secs - start_in_secs)) -gt $timer_threshold ]]; then
        debug "syncd-ot process in container syncd-ot$DEV did not exit gracefully" 
    fi

    /usr/bin/docker exec -i syncd-ot$DEV /bin/sync
    debug "Finished shutdown syncd-ot process ..."
}

OP=$1
DEV=$2

SERVICE="syncd-ot"
DEBUGLOG="/tmp/swss-syncd-ot-debug$DEV.log"
LOCKFILE="/tmp/swss-syncd-ot-lock$DEV"
NAMESPACE_PREFIX="asic"
if [ "$DEV" ]; then
    NET_NS="$NAMESPACE_PREFIX$DEV" 
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
