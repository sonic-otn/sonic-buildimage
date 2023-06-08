#!/bin/bash

echo "clear all ntp state records..."
sonic-db-cli STATE_DB keys "NTP*" | awk '{
  if ($1 != "") {
    if ($1 == "NTP|global") {
      rd=sprintf("sonic-db-cli STATE_DB hdel \"%s\" ntp-source-address ntp-server-selected ntp-status", $1)
      print rd
      system(rd)
    } else {
      rd=sprintf("sonic-db-cli STATE_DB del \"%s\"", $1)
      print rd
      system(rd)
    }
  }
}'

enabled=$(sonic-db-cli CONFIG_DB hget "NTP|global" enabled | awk '{print $1}')
echo "ntp state is $enabled"

if [ "$enabled" = 'true' ]; then
  sonic-cfggen -d -t /usr/share/sonic/templates/chrony.conf.j2 > /etc/chrony/chrony.conf
  echo "systemctl restart chrony"
  sudo mkdir -p /var/log/chrony
  systemctl --no-block restart chrony
else
  echo "systemctl stop chrony"
  systemctl --no-block stop chrony
fi

sleep 5

echo "systemctl restart chrony-sync"
systemctl --no-block restart chrony-sync