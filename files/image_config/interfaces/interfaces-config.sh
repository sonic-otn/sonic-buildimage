#!/bin/bash

ifdown --force eth1
ifdown --force eth0.1

# Create /e/n/i file for existing and active interfaces
CFGGEN_PARAMS=" \
    -d -t /usr/share/sonic/templates/interfaces.j2,/etc/network/interfaces \
"
sonic-cfggen $CFGGEN_PARAMS

systemctl restart networking

