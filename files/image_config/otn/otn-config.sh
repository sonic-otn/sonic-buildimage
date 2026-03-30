#!/bin/bash

PLATFORM=${PLATFORM:-$(sonic-cfggen -d -v DEVICE_METADATA.localhost.platform)}
HWSKU=${HWSKU:-$(sonic-cfggen -d -v DEVICE_METADATA.localhost.hwsku)}
OTN_CONFIG="/usr/share/sonic/device/$PLATFORM/$HWSKU/otn_config.json"
OTN_INIT_MARKER="/host/otn/otn-config.initialized"

log() { echo "$1"; logger -t otn-config "$1"; }

log "starting (platform=$PLATFORM hwsku=$HWSKU)"

sonic-cfggen -j /usr/share/sonic/device/$PLATFORM/otn_metadata.json --write-to-db

# Check whether every non-empty table from otn_config.json has at least one key in CONFIG_DB.
otn_config_present_in_db() {
    if [ ! -r "$OTN_CONFIG" ]; then
        log "OTN config not readable: $OTN_CONFIG"
        return 1
    fi

    local tables
    tables=$(python3 -c '
import json, sys
cfg = json.load(open(sys.argv[1]))
for k, v in cfg.items():
    if isinstance(v, dict) and v:
        print(k)
' "$OTN_CONFIG") || { log "failed to parse $OTN_CONFIG"; return 1; }

    if [ -z "$tables" ]; then
        log "no non-empty tables in $OTN_CONFIG"
        return 1
    fi

    local table count
    while IFS= read -r table; do
        [ -z "$table" ] && continue
        count=$(sonic-db-cli CONFIG_DB KEYS "${table}|*" | grep -c .)
        if [ "$count" -eq 0 ]; then
            log "table missing in CONFIG_DB: $table"
            return 1
        fi
    done <<< "$tables"

    return 0
}

# Primary guard: marker means this host was initialized at least once.
# Safety net: even with marker, re-apply defaults if OTN tables are missing
# (e.g. user never ran 'config save' and reboot lost the in-memory state).
if [ -f "$OTN_INIT_MARKER" ] && otn_config_present_in_db; then
    log "OTN config present in CONFIG_DB — skipping defaults load"
else
    log "applying OTN defaults from $OTN_CONFIG"
    if sonic-cfggen -j "$OTN_CONFIG" --write-to-db; then
        mkdir -p "$(dirname "$OTN_INIT_MARKER")"
        touch "$OTN_INIT_MARKER"
        log "OTN defaults applied; marker set"
    else
        log "ERROR: sonic-cfggen failed for $OTN_CONFIG"
        exit 1
    fi
fi
