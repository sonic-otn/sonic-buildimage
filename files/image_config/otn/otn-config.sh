#!/bin/bash

PLATFORM=${PLATFORM:-`sonic-cfggen -d -v DEVICE_METADATA.localhost.platform`}
sonic-cfggen -j /usr/share/sonic/device/$PLATFORM/otn_metadata.json --write-to-db
HWSKU=${HWSKU:-`sonic-cfggen -d -v DEVICE_METADATA.localhost.hwsku`}
sonic-cfggen -j /usr/share/sonic/device/$PLATFORM/$HWSKU/otn_config.json --write-to-db
