#!/usr/bin/env bash

if [[ -z "$fake_platform"  ]]; then
    export platform=vs
else
    export platform=$fake_platform
fi

SWSS_VARS_FILE=/usr/share/sonic/templates/swss_vars.j2

# Retrieve SWSS vars from sonic-cfggen
SWSS_VARS=$(sonic-cfggen -d -y /etc/sonic/sonic_version.yml -t $SWSS_VARS_FILE) || exit 1

# Create a folder for SwSS record files
mkdir -p /var/log/swss
ORCHAGENT_ARGS="-d /var/log/swss "

# Set orchagent pop batch size to 8192
ORCHAGENT_ARGS+="-b 8192 "

# Set synchronous mode if it is enabled in CONFIG_DB
SYNC_MODE=$(echo $SWSS_VARS | jq -r '.synchronous_mode')
if [ "$SYNC_MODE" == "enable" ]; then
    ORCHAGENT_ARGS+="-s "
fi

exec /usr/bin/orchagent ${ORCHAGENT_ARGS}
