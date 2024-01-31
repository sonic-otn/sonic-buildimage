#!/usr/bin/env bash

OTSS_VARS_FILE=/usr/share/sonic/templates/otss_vars.j2

# Retrieve OTSS vars from sonic-cfggen
OTSS_VARS=$(sonic-cfggen -d -y /etc/sonic/sonic_version.yml -t $OTSS_VARS_FILE) || exit 1
export platform=$(echo $OTSS_VARS | jq -r '.asic_type')

# Create a folder for OTSS record files
mkdir -p /var/log/otss
ORCHAGENT_ARGS="-d /var/log/otss "

# Set orchagent pop batch size to 8192
ORCHAGENT_ARGS+="-b 8192 "

# Set synchronous mode if it is enabled in CONFIG_DB
SYNC_MODE=$(echo $OTSS_VARS | jq -r '.synchronous_mode')
if [ "$SYNC_MODE" == "enable" ]; then
    ORCHAGENT_ARGS+="-s "
fi

# Check if there is an "asic_id field" in the DEVICE_METADATA in configDB.
#"DEVICE_METADATA": {
#    "localhost": {
#        ....
#        "asic_id": "0",
#    }
#},
# ID field could be integers just to denote the asic instance like 0,1,2...
# OR could be PCI device ID's which will be strings like "03:00.0"
# depending on what the SAI/SDK expects.
asic_id=$(echo $OTSS_VARS | jq -r '.asic_id')
if [ -n "$asic_id" ]
then
    ORCHAGENT_ARGS+="-i $asic_id "
fi

# for multi asic platforms add the asic name to the record file names
if [[ "$NAMESPACE_ID" ]]; then
    ORCHAGENT_ARGS+="-f otss.asic$NAMESPACE_ID.rec -j otairedis.asic$NAMESPACE_ID.rec "
fi

hwsku=`sonic-cfggen -d -v "DEVICE_METADATA['localhost']['hwsku']"`
if [ -n "$hwsku" ]
then
    ORCHAGENT_ARGS+="-c /etc/sonic/linecards/$hwsku/flexcounter.json "
fi

exec /usr/bin/orchagent ${ORCHAGENT_ARGS}
