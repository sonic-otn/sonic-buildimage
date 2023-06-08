#!/bin/bash -e

if [ ! -f /etc/sonic/config_db0.json ] && [ -f /etc/sonic/factory/vs/config_db0.json ]; then
    cp -ar /etc/sonic/factory/vs/config_db0.json /etc/sonic/config_db0.json
fi

if [ ! -f /etc/sonic/config_db1.json ] && [ -f /etc/sonic/factory/vs/config_db1.json ]; then
    cp -ar /etc/sonic/factory/vs/config_db1.json /etc/sonic/config_db1.json
fi

if [ ! -f /etc/sonic/config_db2.json ] && [ -f /etc/sonic/factory/vs/config_db2.json ]; then
    cp -ar /etc/sonic/factory/vs/config_db2.json /etc/sonic/config_db2.json
fi

if [ ! -f /etc/sonic/config_db3.json ] && [ -f /etc/sonic/factory/vs/config_db3.json ]; then
    cp -ar /etc/sonic/factory/vs/config_db3.json /etc/sonic/config_db3.json
fi


