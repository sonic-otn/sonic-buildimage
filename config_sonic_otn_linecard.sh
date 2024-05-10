#!/bin/bash

#./config_sonic_otn_linecard.sh 1 e110c
#./config_sonic_otn_linecard.sh 1 none

SLOT_ID=$1
LINECARD_TYPE=$2
TERMINAL_MODE=$3
LINECARD_TYPE_UPPERCASE=${LINECARD_TYPE^^}
ASIC_ID=$((SLOT_ID-1))
echo $SLOT_ID $LINECARD_TYPE $LINECARD_TYPE_UPPERCASE $TERMINAL_MODE $ASIC_ID

PLATFORM=${PLATFORM:-`sonic-cfggen -H -v DEVICE_METADATA.localhost.platform`}

if [ $LINECARD_TYPE_UPPERCASE == NONE ]; then
    echo "linecard type is none"

    sudo systemctl stop otss@$ASIC_ID.service
    sudo systemctl stop syncd-ot@$ASIC_ID.service

    echo "flush all linedard $SLOT_ID in database"
    sonic-db-cli -n asic$ASIC_ID STATE_DB flushall
    sonic-db-cli -n asic$ASIC_ID CONFIG_DB SET "CONFIG_DB_INITIALIZED" "1"
    sudo rm /etc/sonic/config_db$ASIC_ID.json

    sudo systemctl start syncd-ot@$ASIC_ID.service
    sudo systemctl start otss@$ASIC_ID.service
else
    echo "linecard type is $LINECARD_TYPE"
    sudo cp -r /usr/share/sonic/device/$PLATFORM/linecards /etc/sonic
    sudo sh -c "SLOT_ID=$SLOT_ID ASIC_ID=$ASIC_ID j2 /etc/sonic/linecards/$LINECARD_TYPE/config_db.json.j2 > /etc/sonic/config_db$ASIC_ID.json"

    sudo systemctl stop otss@$ASIC_ID.service
    sudo systemctl stop syncd-ot@$ASIC_ID.service

    sudo /usr/local/bin/sonic-cfggen -j /etc/sonic/config_db$ASIC_ID.json  -n asic$ASIC_ID --write-to-db

    echo "plugin the linecard $SLOT_ID ..."
    sonic-db-cli -n asic$ASIC_ID STATE_DB hset "LINECARD|LINECARD-1-$SLOT_ID" "power-admin-state" "POWER_ENABLED" "oper-status" "INACTIVE" "empty" "false" "slot-status" "Ready" "linecard-type" "$LINECARD_TYPE_UPPERCASE"
    sonic-db-cli -n asic$ASIC_ID STATE_DB hset "LINECARD|LINECARD-1-$SLOT_ID" "oper-status" "ACTIVE" 
    sudo systemctl start syncd-ot@$ASIC_ID.service
    sudo systemctl start otss@$ASIC_ID.service
fi



