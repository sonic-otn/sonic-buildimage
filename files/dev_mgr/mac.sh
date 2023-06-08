#!/bin/bash
line=$(cat /var/log/set_mac_log.txt | grep "set $1")
mac=${line:15:17}
ifconfig $1 hw ether ${mac}
