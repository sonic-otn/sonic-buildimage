## SONiC-OTN Buildimage Guide

### How to build the sonic-otn VM
```
  git clone https://github.com/sonic-otn/sonic-buildimage.git
  cd sonic-buildimage
  git checkout otn_pre_202411
  make init
  make configure PLATFORM=ot-vs
  make SONIC_BUILD_JOBS=8 target/sonic-ot-vs.img.gz
```

## Run SONiC-OTN OT-VS image on Virtual machine

### Prerequisites
* Install qemu
```
sudo apt-get install qemu-kvm
```
or
```
brew install qemu
```

* download sonic-otn virtual images

1. download ONIE image `onie-recovery-x86_64-ot_kvm_x86_64_4_asic-r0.iso` from https://github.com/sonic-otn/ot_kvm_onie/releases

2. download installer images `sonic-installer.img` and `sonic-4asic-ot-vs.img.gz`  
download these images from the github [actions](https://github.com/sonic-otn/sonic-buildimage/actions/workflows/sonic-otn-ot-vs-build.yml) artifacts, for example this workflow [build#13](https://github.com/sonic-otn/sonic-buildimage/actions/runs/9016531036)

  
* (optional) build sonic-otn virtual images
Build the whole project, then you can find the `sonic-installer.img` and `sonic-4asic-ot-vs.img.gz` in the root and `target` folder


# How to Start a Virtual Machine

1. Start VM via qemu
```
gunzip -k sonic-4asic-ot-vs.img.gz

sudo qemu-system-x86_64 -m 3072 -name onie -accel hvf -boot order=cd,once=d -cdrom ./onie-recovery-x86_64-ot_kvm_x86_64_4_asic-r0.iso  -device e1000,netdev=onienet -netdev user,id=onienet,hostfwd=:0.0.0.0:10022-:22 -vga std -drive file=./sonic-4asic-ot-vs.img,media=disk,if=virtio,index=0 -drive file=./sonic-installer.img,if=virtio,index=1 -serial telnet:127.0.0.1:7000,server
```
Note: you may need to change the `-accel hvf` to others hardware accelerator options, for example  `-accel KVM`

3. Open a new terminal, use console to login ONIE.
```
telnet 127.0.0.1 7000
```

4. Choose entry: `ONIE: Embed ONIE`

5. Choose entry: `ONIE: Install OS`

6. Wait until SONiC-OTN image installed.

7. The system will reboot automatically once sonic-otn is installed.

8. The system is ready to login with default username/password (admin/YourPaSsWoRd)

9. (Recommended) You can run the SONiC-OTN VM with bellow command directly.

```
sudo qemu-system-x86_64 -name sonic-vs -m 3072 -smp cpus=2 -accel hvf -machine smm=off -drive file=sonic-4asic-ot-vs.img,if=virtio,index=0,media=disk,id=drive0 -cpu qemu64 -nic user,hostfwd=tcp::10022-:22,hostfwd=tcp::18080-:8080,restrict=off,model=virtio-net-pci
```    
Note: you may need to change the `-accel hvf` to others hardware accelerator options, for example  `-accel KVM`

# How to Login Virtual Machine

1. Connect SONiC-OTN VM via console

```
telnet 127.0.0.1 7000
```

2. Connect SONiC-OTN VM via SSH

    a. Connect via console

    b. Request a new DHCP address

    ```
    sudo dhclient -v
    ```

    c. Connect via SSH
    ```
    ssh admin@localhost -p 10022
    ```

3. check the running dockers
```
admin@sonic:~$ docker ps
CONTAINER ID   IMAGE                                COMMAND                  CREATED          STATUS              PORTS     NAMES
7e1c62bc23e2   docker-platform-monitor:latest       "/usr/bin/docker_ini…"   2 minutes ago    Up About a minute             pmon
3fa53fd0fa0d   docker-sonic-mgmt-framework:latest   "/usr/local/bin/supe…"   2 minutes ago    Up 2 minutes                  mgmt-framework
035c2e080506   docker-lldp:latest                   "/usr/bin/docker-lld…"   2 minutes ago    Up 2 minutes                  lldp
621329efaac1   docker-sonic-gnmi:latest             "/usr/local/bin/supe…"   2 minutes ago    Up 2 minutes                  gnmi
83d06659a2ed   docker-syncd-ot-vs:latest            "/usr/local/bin/supe…"   5 minutes ago    Up 4 minutes                  syncd-ot3
281482c1a03b   docker-syncd-ot-vs:latest            "/usr/local/bin/supe…"   5 minutes ago    Up 4 minutes                  syncd-ot0
a0be913d53f3   docker-syncd-ot-vs:latest            "/usr/local/bin/supe…"   5 minutes ago    Up 4 minutes                  syncd-ot1
3ce2c63b401d   docker-syncd-ot-vs:latest            "/usr/local/bin/supe…"   5 minutes ago    Up 4 minutes                  syncd-ot2
efd864faac16   docker-orchagent-ot:latest           "/usr/bin/docker-ini…"   6 minutes ago    Up 5 minutes                  otss0
b9e7634a3e8b   docker-orchagent-ot:latest           "/usr/bin/docker-ini…"   6 minutes ago    Up 5 minutes                  otss1
db2d61583a66   docker-orchagent-ot:latest           "/usr/bin/docker-ini…"   6 minutes ago    Up 5 minutes                  otss3
22ce20e66188   docker-orchagent-ot:latest           "/usr/bin/docker-ini…"   6 minutes ago    Up 5 minutes                  otss2
2a4a3d1cdd04   docker-fpm-frr:latest                "/usr/bin/docker_ini…"   19 minutes ago   Up 5 minutes                  bgp
aa06aec6b3e2   docker-eventd:latest                 "/usr/local/bin/supe…"   21 minutes ago   Up 6 minutes                  eventd
9de7acae7b67   docker-database:latest               "/usr/local/bin/dock…"   22 minutes ago   Up 6 minutes                  database1
e453e15d1fe6   docker-database:latest               "/usr/local/bin/dock…"   22 minutes ago   Up 6 minutes                  database3
4ac2bc1b2a0d   docker-database:latest               "/usr/local/bin/dock…"   22 minutes ago   Up 6 minutes                  database2
b6b7e30bc8d8   docker-database:latest               "/usr/local/bin/dock…"   22 minutes ago   Up 6 minutes                  database0
68c79c6e02f5   docker-database:latest               "/usr/local/bin/dock…"   22 minutes ago   Up 6 minutes                  database
admin@sonic:~$
```

# Test provision a linecard
We provide CLI commands to provision virtual linecards in the sonic-otn VM systems.

1. provision slot 1 with linecard type P230C, which is a transponder with four 100G Ethernet client port and one 400G line port.

```
sudo config slot 1 type P230C
```

2. now you can check the slot configuration, state and alarm with these CLI commands.
```
admin@sonic:~$show slot 1 config
Card Type                                    : P230C
Board mode                                   : NA
Admin                                        : NA
Baudrate                                     : NA
Hostname                                     : NA
Temp Hi-Alarm(C)                             : NA
Temp Hi-Warning(C)                           : NA
Temp Low-Alarm(C)                            : NA
Temp Low-Warning(C)                          : NA

admin@sonic:~$ show slot 1 info
Card Type                                    : P230C
Board mode                                   : L1_400G_CA_100GE
Admin                                        : ENABLED
Oper Status                                  : ACTIVE
Part no                                      : NA
Serial no                                    : NA
Hardware ver                                 : NA
Software ver                                 : 1.0
Mfg name                                     : Alibaba
Mfg date                                     : NA
Alarm Led State                              : RED

Temperature(C)                               : 35.0
CPU utilized(%)                              : 742274744
Memory available(B)                          : 691489792
Memory utilized(B)                           : 382252064

admin@sonic:~$
admin@sonic:~$ show slot 1 alarm current
Slot 1 Current Alarm Total num: 1
  id  time-created             resource      severity    type-id                 text              sa    type
----  -----------------------  ------------  ----------  ----------------------  ----------------  ----  --------
   1  2025-03-10 12:16:25.174  LINECARD-1-1  MAJOR       HIGH_TEMPERATURE_ALARM  high temperature  sa    standing

admin@sonic:~$
```

3. You can show the configuration, state, PMs for each component on the linecard
```
admin@sonic:~$ show slot 1 line 1 state
Name                                         : TRANSCEIVER-1-1-L1
PortOperState                                : ACTIVE
PortAdministate                              : MAINT
DcoVendorPreconf                             : Alibaba
tx-laser                                     : true
LineLoop                                     : FACILITY
LinePrbsTx                                   : PRBS_PATTERN_TYPE_2E7
LinePrbsRx                                   : PRBS_PATTERN_TYPE_2E7
LineForceInsert                              : AIS
tti-msg-auto-mode                            : false
Tti_transmit                                 : SONIC-OTN:/1/1/L1
Tti_rx_expected                              : SONIC-OTN:/1/1/L1
TxPower(dBm)                                 : 0.5
Frequency(MHz)                               : 195875000
OperationlMode                               : test
Tti_rx                                       : SONiC-OTN:/1/2/L1
LineState                                    : true
LineExist                                    : PRESENT
LineFrequency(MHz)                           : 195875000
LinePrbsStateTx                              : PRBS_PATTERN_TYPE_2E7
LinePrbsStateRx                              : PRBS_PATTERN_TYPE_2E7
LedState                                     : RED

InputPower(dBm)                              : 20.0
OutputPower(dBm)                             : 20.0
LaserBias(mA)                                : 20.0
PowerConsumption(W)                          : 20.0
CaseTemp(C)                                  : 20.0
LaserTemp(C)                                 : 20.0
TX MOD BIAS X/I                              : 20.0
TX MOD BIAS X/Q                              : 20.0
TX MOD BIAS Y/I                              : 20.0
TX MOD BIAS Y/Q                              : 20.0
TX MOD BIAS X/PH                             : 20.0
TX MOD BIAS Y/PH                             : 20.0
Q-Factor                                     : 10.1
ESNR                                         : 0.0
PRE-FEC-BER                                  : 0.0000001
POST-FEC-BER                                 : 0.0000001
OSNR(dB)                                     : 0.01
CD(ps/nm)                                    : 10.1
PDL(dB)                                      : 0.01
FOFF(MHz)                                    : 742389350
DGD(ps)                                      : 10.1
SoPMD(ps^2)                                  : 10.1
SOP CHANGE RATE(rad/s)                       : 742389350
LASER BIAS(mA)                               : 10.1
EDFA BIAS(mA)                                : 10.1
Signal Input Power(dBm)                      : 10.1

admin@sonic:~$
```

4. provision slot 2 with e110c, which is a line system with VOA, OSC, EDFA, MUX/DEMUX and OLP.
```
admin@sonic:~$ sudo config slot 2 type E110C
Setting card 2 type E110C now, Wait for a minute..
plugin the virtual linecard 2 and power enabled...
3
virtual linecard otai library communication link status is up...
Successed
admin@sonic:~$
```

4. check the configuration, status and PMs for each optical components.
```
admin@sonic:~$ show slot 2 voa all info
Module Name                                  : ATTENUATOR-1-2-1
VOA Attenuation(dB)                          : 15.0
VOA fix Attenuation(dB)                      : 1.0

Module Name                                  : ATTENUATOR-1-2-2
VOA Attenuation(dB)                          : 15.0
VOA fix Attenuation(dB)                      : 1.0

Module Name                                  : ATTENUATOR-1-2-3
VOA Attenuation(dB)                          : 15.0
VOA fix Attenuation(dB)                      : 1.0

admin@sonic:~$
admin@sonic:~$ show slot 2 edfa all info
Module Name                                  : AMPLIFIER-1-2-1
Module PN                                    : 123
Module SN                                    : 123
Firmware version                             : 1.0
Work mode                                    : CONSTANT_GAIN
EDFA Switch Actual                           : true
Gain Range(dB)                               : LOW_GAIN_RANGE
Set gain(dB)                                 : 15.0
Set Gain tilt                                : 0.0
Work State                                   : LOS_A
Los Ase Delay(ms)                            : 10
Input LOS Th(dBm)                            : 10.0
Input LOS Hy(dB)                             : 1.0
Output LOP Th(dBm)                           : 10.0
Output LOP Hy(dB)                            : 1.0
Gain Low Alm Th(dBm)                         : 10.0
Gain Low Alm Hy(dB)                          : 1.0
Pin Low AlmTh(dBm)                           : 10.0
Pout Low AlmTh(dBm)                          : 10.0

Module temperature(C)                        : 10.0
Actual gain(dB)                              : 10.0
Actual Gain tilt                             : 1.0
Pump Iop(mA)                                 : 10.0
Pump temperature(C)                          : 10.0
Pump Itec(mA)                                : 10.0
Input power(Original)(dBm)                   : 10.0
Output power(Original)(dBm)                  : 10.0

Module Name                                  : AMPLIFIER-1-2-2
Module PN                                    : 123
Module SN                                    : 123
Firmware version                             : 1.0
Work mode                                    : CONSTANT_GAIN
EDFA Switch Actual                           : true
Gain Range(dB)                               : LOW_GAIN_RANGE
Set gain(dB)                                 : 15.0
Set Gain tilt                                : 0.0
Work State                                   : LOS_A
Los Ase Delay(ms)                            : 10
Input LOS Th(dBm)                            : 10.0
Input LOS Hy(dB)                             : 1.0
Output LOP Th(dBm)                           : 10.0
Output LOP Hy(dB)                            : 1.0
Gain Low Alm Th(dBm)                         : 10.0
Gain Low Alm Hy(dB)                          : 1.0
Pin Low AlmTh(dBm)                           : 10.0
Pout Low AlmTh(dBm)                          : 10.0

Module temperature(C)                        : 10.0
Actual gain(dB)                              : 10.0
Actual Gain tilt                             : 1.0
Pump Iop(mA)                                 : 10.0
Pump temperature(C)                          : 10.0
Pump Itec(mA)                                : 10.0
Input power(Original)(dBm)                   : 10.0
Output power(Original)(dBm)                  : 10.0

admin@sonic:~$
admin@sonic:~$ show slot 2 osc all info
Module Name                                  : OSC-1-2-1
Module PN                                    : 123
Module SN                                    : 123
Vendor                                       : alibaba
Frequency(MHz)                               : 1913000
Tx Laser State                               : true
link-status                                  : ACTIVE
Rx Low AlmTh(dBm)                            : 20.0
Rx High AlmTh(dBm)                           : 20.0
Tx Low AlmTh(dBm)                            : 20.0

temperatue(C)                                : 20.0
Tx Bias Current(ma)                          : 20.0
Tx Power(dBm)                                : 20.0
Rx Power(dBm)                                : 20.0

in-pkts                                      : 0
in-errors                                    : 0
out-pkts                                     : 0

admin@sonic:~$
```


5. deprovision the linecard with test script  
It will plug out the virtual linecard and flush all data in the database
```
admin@sonic:~$ sudo config slot 1 type NONE
Setting slot 1 type NONE now, Wait for a minute..
Successed
admin@sonic:~$
admin@sonic:~$ sudo config slot 2 type NONE
Setting slot 2 type NONE now, Wait for a minute..
Successed
admin@sonic:~$

```


# Customize the dummy data in ot-vs platform

1. Option 1, update the dummy json data
User can customize the dummy data for each OTAI objects by editing the json files `/usr/include/vslib/otai_sim_data` in the syncd-ot container, then restart the `syncd` process.

```
docker exec -ti syncd-ot0 bash
vi /usr/include/vslib/otai_sim_data/otai_oa_sim.json
supervisorctl restart syncd
```
Note: if the OTAI attribute is an enum type, the value should be an integer representation of the enum value. For example. `OTAI_ADMIN_STATE_ENABLED` is the first enumerator, and the value is 0.

You can verify the data is updated by retrieving the tables in state_db and counter_db.
```
admin@sonic:~$ docker exec -ti database0 bash
root@sonic:/# redis-cli -n 6
root@sonic:/# redis-cli -n 2
```

2. Option 2, configure the OTAI object in config_db
User can set an OTAI object attributes in config_db, then the state of this OTAI object will be updated in state_db.

For example, disable the transceiver of line port 1 on slot 2 optical linecard.
```
admin@sonic:~$ docker exec -ti database1 bash
root@sonic:/# redis-cli -n 4 hset "TRANSCEIVER|TRANSCEIVER-1-2-L1" "enabled" "false"
root@sonic:/# redis-cli -n 6 hget "TRANSCEIVER|TRANSCEIVER-1-2-L1" "enabled"
"false"
root@sonic:/#
```

