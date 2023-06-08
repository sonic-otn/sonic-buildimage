#!/usr/bin/python3
import sys
import os
import re
import uuid
import time
import otn_pmon.public as pmon_public

def mac_add_one(mac):
    #  使用format格式化字符串，int函数，按照16进制算法，将输入的mac地址转换成十进制，然后加上偏移量
    # {:012X}将十进制数字，按照16进制输出。其中12表示只取12位，0表示不足的位数在左侧补0
    # print("int_mac",int(mac,16))
    mac_address = "{:012X}".format(int(mac, 16) + 1)
    new_mac_add = ":".join(re.findall(r".{2}",mac_address.upper()))
    return new_mac_add

def mac_add_index(mac,index):
    mac_address = "{:012X}".format(int(mac, 16) + index)
    new_mac_add = ":".join(re.findall(r".{2}",mac_address.upper()))
    return new_mac_add

def set_osc_mac(start_mac):
    ret = 0
    temp_mac = start_mac.replace(":","")
    for index in range (1,5):
        osc_mac1 = mac_add_index(temp_mac,index)
        #private mac
        osc_mac = "06:08:08"+osc_mac1[8:] 
        ret = os.system(f"ip link set eth0.{index+2} down")
        ret |=os.system(f"ip link set eth0.{index+2} address {osc_mac}")
        ret |=os.system(f"ip link set eth0.{index+2} up")
        if ret == 0:
            print(f"set eth0.{index+2} mac {osc_mac} successed")
        else:
            print(f"set eth0.{index+2} mac {osc_mac} Failed")
    return ret

def set_mac_to_sys():
    time.sleep(2)
    old_mac  = ":".join(re.findall(r".{2}",uuid.uuid1().hex[-12:].upper()))
    print("old_mac",old_mac)
    new_mac = pmon_public.get_chassis_mac()
    if not new_mac :
        return
    # new_mac="fe:ff:ff:ff:ff:ff"
    temp_mac = new_mac.replace(":","")
    eth0_1_mac = mac_add_one(temp_mac)
    print("eth0_1_mac",eth0_1_mac)

    if validate_mac(new_mac):
        ret = os.system("ip link set eth1 down")
        ret |=os.system(f"ip link set eth1 address {new_mac}")
        ret |=os.system("ip link set eth1 up")
        if ret == 0:
            print(f"set eth1 mac {new_mac} successed")
        else:
            print(f"set eth1 mac {new_mac} Failed")
        ret1 = os.system("ip link set eth0.1 down")
        ret1 |= os.system(f"ip link set eth0.1 address {eth0_1_mac}")
        ret1 |= os.system("ip link set eth0.1 up")
        if ret1 == 0:
            print(f"set eth0.1 mac {eth0_1_mac} successed")
        else:
            print(f"set eth0.1 mac {eth0_1_mac} Failed")

        ret2 = set_osc_mac(eth0_1_mac)
        if ret2 == 0:
            print(f"set osc mac all successed")
        else:
            print(f"set osc mac Failed")
    else:
        print("new_mac is not validat")

def validate_mac(value):
    if value.find('-') != -1:
        pattern = re.compile(r"^\s*([0-9a-fA-F]{2,2}-){5,5}[0-9a-fA-F]{2,2}\s*$")
        if pattern.match(value):
            return True
        else:
            return False
    if value.find(':') != -1:
        pattern = re.compile(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$")
        if pattern.match(value):
            return True
        else:
            return False


def Usage(prog):
    print(f"Usage: ./set_mac_to_sys.py ")
    sys.exit(-1)

# print("arg num",sys.argv)
# print(len(sys.argv))
if len(sys.argv) != 1:
    Usage(sys.argv[0])

set_mac_to_sys()




