#!/bin/bash -e

users=`cat /etc/passwd | grep clish_start | grep -v admin | cut -d\: -f1`
for user in ${users}; do
    mkdir -p /home/${user}
    chown -R ${user}:${user} /home/${user}
done

