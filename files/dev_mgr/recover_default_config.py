#!/usr/bin/python3
import sys
import os

g_argumet_list = [
    "slot",
    "type"
]

def gen_running_config(slot_id,card_type,module_type="factory",check_flag=False):
    try:
        if check_flag == True and os.path.exists(f'/etc/sonic/config_db{slot_id-1}.json'):
            print(f' slot{slot_id} Config file is already existsed')
        else:
            cmd = f"cp /etc/sonic/{module_type}/{card_type}/config_db{slot_id-1}.json /etc/sonic/config_db{slot_id-1}.json"
            os.system(cmd)
            if os.path.exists(f'/etc/sonic/config_db{slot_id - 1}.json'):
                print(f' slot{slot_id} Config file generate Successfully')

                not_alarm = f"sudo touch /tmp/not_alarm_container_exit"
                if os.system(not_alarm) == 0:
                    print(f"touch not_alarm_container_exit successed")
                else:
                    print(f"touch not_alarm_container_exit failed")

                reload_systemd =f"sudo systemctl daemon-reload"
                if os.system(reload_systemd) == 0:
                    print(f"reload systemd successed")
                else:
                    print(f"reload systemd failed")

                stop_swss =f"sudo systemctl stop swss@{slot_id-1}.service"
                if os.system(stop_swss) == 0:
                    print(f"stop swss{slot_id-1} successed")
                else:
                    print(f"stop swss{slot_id-1} failed")

                stop_syncd =f"sudo systemctl stop syncd@{slot_id-1}.service"
                if os.system(stop_syncd) == 0:
                    print(f"stop syncd{slot_id-1} successed")
                else:
                    print(f"stop syncd{slot_id-1} failed")

                write_config_to_db = f"sudo /usr/local/bin/sonic-cfggen -j /etc/sonic/config_db{slot_id-1}.json  -n asic{slot_id-1} --write-to-db"
                if os.system(write_config_to_db) == 0:
                    print(f"write config_db{slot_id-1}.json to db successed")
                else:
                    print(f"write config_db{slot_id-1}.json to db failed")

                start_swss =f"sudo systemctl start swss@{slot_id-1}.service"
                if os.system(start_swss) == 0:
                    print(f"start swss{slot_id-1} successed")
                else:
                    print(f"start swss{slot_id-1} failed")

                start_syncd =f"sudo systemctl start syncd@{slot_id-1}.service"
                if os.system(start_syncd) == 0:
                    print(f"start syncd{slot_id-1} successed")
                else:
                    print(f"start syncd{slot_id-1} failed")

                alarm = f"sudo rm -f /tmp/not_alarm_container_exit"
                if os.system(alarm) == 0:
                    print(f"remove not_alarm_container_exit successed")
                else:
                    print(f"remove not_alarm_container_exit failed")

            else:
                print(f' slot{slot_id} Config file generate Failed')
    except Exception as e:
        print(e)

CARD_TYPE_LIST = ["p230c","e110c","e100c","e120c"]
def Usage(prog):
    print("Usage:%s [slot] [card_type] [module_type] \n" % prog)
    print(f"Usage: recover_default_config slot <1-4> type p230c|e110c|e100c  force")

    for config_type in g_argumet_list:
        print("\t\t\t %s\n" % config_type)
    sys.exit(-1)

# print(sys.argv)
if len(sys.argv) < 3:
    Usage(sys.argv[0])

if sys.argv[1] != "slot" and sys.argv[3] != "type":
    Usage(sys.argv[0])

if sys.argv[4] not in CARD_TYPE_LIST:
    Usage(sys.argv[0])

slot_id = int(sys.argv[2])
card_type = sys.argv[4]
# print("slot_id",int(slot_id))

# print("len(sys.argv)",len(sys.argv))
# print("sys.argv[5]",sys.argv[5])

if len(sys.argv)>=6 and sys.argv[5] == 'force':
    gen_running_config(slot_id,card_type)
else:
    gen_running_config(slot_id, card_type,check_flag=True)




