#!/bin/sh

# chrony start or not
active=$(systemctl is-active chrony | awk '{
  if ($1 == "active") {
    print "true"
  } else {
    print "false"
  }
}')

local_addr=$(sonic-db-cli CONFIG_DB keys "MGMT_INTERFACE|*" | cut -d "|" -f3 | cut -d "/" -f1)
loopback_addr=$(sonic-db-cli CONFIG_DB keys "LOOPBACK_INTERFACE|Loopback0*" | cut -d "|" -f3 | cut -d "/" -f1)
if [ -n "$loopback_addr" ]; then
  local_addr=$loopback_addr
fi

if [ "$active" = 'true' ]; then
  sonic-db-cli STATE_DB hset "NTP|global" enabled true > /dev/null
  #echo "write latest chronyc info into redis"
  chronyc sources | awk '{
    if (NR > 3) {
      if ($1 == "^*") {
        global=sprintf("sonic-db-cli STATE_DB hset \"NTP|global\" ntp-source-address %s ntp-server-selected %s ntp-status SYNCHRONIZED > /dev/null", "'$local_addr'", $2)
        #print global
        system(global)
      } else if ($1 == "^?") {
        state=sprintf("sonic-db-cli STATE_DB hset \"NTP_SERVER|%s\"", $2)
        state=sprintf("%s stratum 0 poll-interval 0 root-delay 0 root-dispersion 0 offset 0 > /dev/null", state)
        #print state
        system(state)
      }
    }
  }'

  chronyc sources | awk '{if (NR>3) print $0}' | awk '{
    if ($1 != "^?") {
      cn=sprintf("chronyc ntpdata %s", $2)
      system(cn)
    }
  }' | awk '{
    if (NR%26 == 1)  {hs=sprintf("sonic-db-cli STATE_DB hset \"NTP_SERVER|%s\" address %s", $4, $4)}
    if (NR%26 == 2)  {hs=sprintf("%s port %s", hs, $4)}
    if (NR%26 == 5)  {hs=sprintf("%s version %s", hs, $3)}
    if (NR%26 == 6)  {hs=sprintf("%s association-type %s", hs, toupper($3))}
    if (NR%26 == 7)  {hs=sprintf("%s stratum %s", hs, $3)}
    if (NR%26 == 8)  {hs=sprintf("%s poll-interval %s", hs, 2^$4)}
    if (NR%26 == 10) {hs=sprintf("%s root-delay %d", hs, int($4 * 1000))}
    if (NR%26 == 11) {hs=sprintf("%s root-dispersion %d", hs, int($4 * 1000))}
    if (NR%26 == 14) {hs=sprintf("%s offset %s", hs, int(substr($3, 2, length($3)-1) * 1000))}
    if (NR%26 == 0) {
      hs=sprintf("%s > /dev/null", hs)
      #print hs
      system(hs)
    }
  }'
else
  # update ntp enabled false
  sonic-db-cli STATE_DB hset "NTP|global" enabled false > /dev/null
fi