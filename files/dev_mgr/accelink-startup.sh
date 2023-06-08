#!/bin/sh -x

sudo hwclock -s

sudo insmod /usr/sbin/lpc_fpga.ko

sudo systemctl start devmgr.service

#UdpProxy for board calibration,  which transfers packages of udp 9000 to proper slot.
sudo /usr/sbin/UdpProxy &

sudo ifconfig eth0 up
echo "create eth0.1 eth0.2 eth0.3 eth0.4 eth0.5 eth0.6"
sudo vconfig add eth0 1 > /var/log/add_eth01.txt
sudo vconfig add eth0 2 > /var/log/add_eth02.txt
sudo vconfig add eth0 3 > /var/log/add_eth03.txt
sudo vconfig add eth0 4 > /var/log/add_eth04.txt
sudo vconfig add eth0 5 > /var/log/add_eth05.txt
sudo vconfig add eth0 6 > /var/log/add_eth06.txt

sudo vconfig set_flag eth0.1 1 1
sudo vconfig set_flag eth0.2 1 1
sudo vconfig set_flag eth0.3 1 1
sudo vconfig set_flag eth0.4 1 1
sudo vconfig set_flag eth0.5 1 1
sudo vconfig set_flag eth0.6 1 1
sudo ip link set eth0.2 up
sudo ifconfig eth0.2 117.103.88.243 netmask 255.255.248.0

sudo iptables -I INPUT -p TCP --dport 5000 -j DROP
sudo iptables -I INPUT -s 127.0.0.1 -p TCP --dport 5000 -j ACCEPT

sudo iptables -I INPUT -p TCP --dport 5001 -j DROP
sudo iptables -I INPUT -s 127.0.0.1 -p TCP --dport 5001 -j ACCEPT

sudo iptables -I INPUT -p TCP --dport 5002 -j DROP
sudo iptables -I INPUT -s 127.0.0.1 -p TCP --dport 5002 -j ACCEPT

sudo iptables -I INPUT -p TCP --dport 5003 -j DROP
sudo iptables -I INPUT -s 127.0.0.1 -p TCP --dport 5003 -j ACCEPT

sudo iptables -I INPUT -p UDP --dport 5499 -j DROP
sudo iptables -I INPUT -i eth0.2 -p UDP --dport 5499 -j ACCEPT

sudo iptables -I INPUT -p UDP --dport 5500 -j DROP
sudo iptables -I INPUT -i eth0.2 -p UDP --dport 5500 -j ACCEPT

sudo iptables -I INPUT -p UDP --dport 5501 -j DROP
sudo iptables -I INPUT -i eth0.2 -p UDP --dport 5501 -j ACCEPT

sudo iptables -I INPUT -p UDP --dport 5502 -j DROP
sudo iptables -I INPUT -i eth0.2 -p UDP --dport 5502 -j ACCEPT

sudo iptables -I INPUT -p UDP --dport 5999 -j DROP
sudo iptables -I INPUT -i eth0.2 -p UDP --dport 5999 -j ACCEPT

sudo iptables -I INPUT -p UDP --dport 6000 -j DROP
sudo iptables -I INPUT -i eth0.2 -p UDP --dport 6000 -j ACCEPT

sudo iptables -I INPUT -p UDP --dport 6001 -j DROP
sudo iptables -I INPUT -i eth0.2 -p UDP --dport 6001 -j ACCEPT

sudo iptables -I INPUT -p UDP --dport 6002 -j DROP
sudo iptables -I INPUT -i eth0.2 -p UDP --dport 6002 -j ACCEPT

# update mac info
echo "set mac "
python3 /usr/sbin/set_mac_to_sys.py > /var/log/set_mac_log.txt

