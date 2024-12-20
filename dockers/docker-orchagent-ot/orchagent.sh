#!/usr/bin/env bash

OTSS_VARS_FILE=/usr/share/sonic/templates/otss_vars.j2

# Retrieve OTSS vars from sonic-cfggen
OTSS_VARS=$(sonic-cfggen -d -y /etc/sonic/sonic_version.yml -t $OTSS_VARS_FILE) || exit 1
export platform=$(echo $OTSS_VARS | jq -r '.asic_type')

# Create a folder for OTSS record files
mkdir -p /var/log/otss
ORCHAGENT_ARGS=" "

# Set orchagent pop batch size to 8192
ORCHAGENT_ARGS+="-b 8192 "

# Check if there is an "asic_id field" in the DEVICE_METADATA in configDB.
#"DEVICE_METADATA": {
#    "localhost": {
#        ....
#        "asic_id": "0",
#    }
#}
asic_id=$(echo $OTSS_VARS | jq -r '.asic_id')
if [ -n "$asic_id" ]
then
    ORCHAGENT_ARGS+="-i $asic_id "
fi

hwsku=`sonic-cfggen -d -v "DEVICE_METADATA['localhost']['hwsku']"`
if [ -n "$hwsku" ]
then
    ORCHAGENT_ARGS+="-c /etc/sonic/linecards/$hwsku/flexcounter.json "
fi

exec /usr/bin/orchagent ${ORCHAGENT_ARGS}
