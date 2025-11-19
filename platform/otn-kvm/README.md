# SONIC otn-kvm Demo Instructions

This doc contains the procedure to compile, run and test the SONiC-OTN KVM image, the prototype the team currently has.  
For SONiC compilation environment setup, please refer to [sonic-buildimage](https://github.com/sonic-net/sonic-buildimage) and [README.md](https://github.com/sonic-net/sonic-buildimage/blob/master/README.md)

# HOWTO Build otn-kvm image

``` bash
make init
make configure PLATFORM=otn-kvm
make target/sonic-otn-kvm.img.gz
```

# HOWTO setup KVM environment
1. Install Ubuntu KVM tools

```bash
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils -y 
```

2. Check CPU virtualization support

```bash
kvm-ok
INFO: /dev/kvm exists
KVM acceleration can be used
```

3. Copy the SONiC image to host
    - sonic-otn-kvm.img.gz      --- compressed SONiC image 

4. Decompress the image
```bash
gunzip sonic-otn-kvm.img.gz
```

## Running SONiC OTN KVM
```bash
sudo qemu-system-x86_64 \
  -hda sonic-otn-kvm.img \
  -enable-kvm -m 4096 -smp 4 \
  -nographic \
  -netdev user,id=net0,hostfwd=tcp::2222-:22 \
  -device e1000,netdev=net0


                             GNU GRUB  version 2.02

 +----------------------------------------------------------------------------+
 |*SONiC-OS-otn.0-dirty-202528.102930                                       | 
 | ONIE                                                                       |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            | 
 +----------------------------------------------------------------------------+

      Use the ^ and v keys to select which entry is highlighted.
      Press enter to boot the selected OS, `e' to edit the commands       
      before booting or `c' for a command-line.

                             GNU GRUB  version 2.02
```
If want to quit qemu, please hold Ctrl and press A, then release both keys, and press X.

# HOWTO use otn-kvm image
## Login directly in CLI
Input user and password to login, which are configured in config file, admin/YourPaSsWoRd for default.
```
sonic login: admin
Password: 
Linux sonic 6.1.0-29-2-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.123-1 (2025-01-02) x86_64
You are on
  ____   ___  _   _ _  ____
 / ___| / _ \| \ | (_)/ ___|
 \___ \| | | |  \| | | |
  ___) | |_| | |\  | | |___
 |____/ \___/|_| \_|_|\____|

-- Software for Open Networking in the Cloud --

Unauthorized access and/or use are prohibited.
All access and/or use are subject to monitoring.

Help:    https://sonic-net.github.io/SONiC/

Last login: Wed Jul 23 02:54:51 UTC 2025 on ttyS0
admin@sonic:~$
```

## Login via SSH
Use ssh port 2222 to locally login to SONiC.
```
ssh -p 2222 admin@localhost

The authenticity of host '[localhost]:2222 ([127.0.0.1]:2222)' can't be established.
RSA key fingerprint is SHA256:+pZRW181kQeX5mhEoVaK9VTm1b/nFsyxdkfNYNaQwWY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[localhost]:2222' (RSA) to the list of known hosts.
Debian GNU/Linux 12 \n \l

admin@localhost's password:
Linux sonic 6.1.0-29-2-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.123-1 (2025-01-02) x86_64
You are on
  ____   ___  _   _ _  ____
 / ___| / _ \| \ | (_)/ ___|
 \___ \| | | |  \| | | |
  ___) | |_| | |\  | | |___
 |____/ \___/|_| \_|_|\____|

-- Software for Open Networking in the Cloud --

Unauthorized access and/or use are prohibited.
All access and/or use are subject to monitoring.

Help:    https://sonic-net.github.io/SONiC/

Last login: Mon Aug 25 23:35:30 2025
admin@sonic:~$
```

## Show PMON platform information
### Show summary information
```bash
admin@sonic:~$ show platform summary 
Platform: x86_64-otn-kvm_x86_64-r0
HwSKU: OLS-V
ASIC: otn-kvm
ASIC Count: 1
Serial Number: D9401XXX
Model Number: 1835260XXX
Hardware Revision: 1.01
Switch Type: otn
admin@sonic:~$
```

### Show PSU information
```bash
admin@sonic:~$ show platform psu
PSU    Model    Serial               HW Rev      Voltage (V)    Current (A)    Power (W)  Status    LED
-----  -------  -------------------  --------  -------------  -------------  -----------  --------  -----
PSU 1  VM-PSU   G1251551NJ220600XXX  R00               11.96           1.97        23.62  OK        green
PSU 2  VM-PSU   G1251551NJ220600XXX  R00               11.98           2.01        23.95  OK        green
admin@sonic:~$ 
```

### Show fan information
```bash
admin@sonic:~$ show platform fan
  Drawer    LED            FAN    Speed              Direction    Presence    Status          Timestamp
--------  -----  -------------  -------  ---------------------  ----------  --------  -----------------
FanTray0  green  FanTray0-Fan0      51%  FAN_DIRECTION_EXHAUST     Present        OK  20250723 03:31:23
FanTray0  green  FanTray0-Fan1      53%  FAN_DIRECTION_EXHAUST     Present        OK  20250723 03:31:23
FanTray0  green  FanTray0-Fan2      55%  FAN_DIRECTION_EXHAUST     Present        OK  20250723 03:31:23
FanTray0  green  FanTray0-Fan3      57%  FAN_DIRECTION_EXHAUST     Present        OK  20250723 03:31:23
     N/A  green       PSU0-Fan     100%   FAN_DIRECTION_INTAKE     Present        OK  20250723 03:31:23
     N/A  green       PSU1-Fan     100%   FAN_DIRECTION_INTAKE     Present        OK  20250723 03:31:23
admin@sonic:~$
```

### Show thermal information
```bash
admin@sonic:~$ show platform temperature 
        Sensor    Temperature    High TH    Low TH    Crit High TH    Crit Low TH    Warning          Timestamp
--------------  -------------  ---------  --------  --------------  -------------  ---------  -----------------
  System Board              0         75        -5              70              0      False  20250723 03:32:23
System Exhaust              0         75        -5              70              0      False  20250723 03:32:23
admin@sonic:~$
```

### Show firmware information
```bash
admin@sonic:~$ show platform firmware status
Chassis    Module       Component    Version    Description
---------  -----------  -----------  ---------  -------------------------------------------------------------
OLA        LINE-CARD0   OA0-0        1.00.0002  Optical amplifier (west)
                        OA0-1        1.00.0002  Optical amplifier (east)
                        OSC0-0       1.02.0003  Optical supervisory channel (west)
                        OSC0-1       N/A        Optical supervisory channel (east)
                        OCM0-0       1.00.0003  Optical channel monitor
                        OTDR0-0      1.00.0004  Optical time domain reflectometer
           SUPERVISOR0  BIOS         5.6.5      Performs initialization of hardware components during booting
                        FPGA         1.01.0004  Platform managment controller for on-board components
                        CPLD         1.01.0005  Used for managing IO modules
                        ONIE         2022.08    Open network install environment
admin@sonic:~$
```

## Redis
We have added the following tables to support data of OCS. 
- For CONFIG_DB (DB 4)
  - OTN_ATTENUATOR
  - OTN_OA
  - OTN_OCM
  - OTN_OCM_CHANNEL
  - OTN_OSC
- For STATE_DB (DB 6)
  - OTN_ATTENUATOR_TABLE
  - OTN_OA_TABLE
  - OTN_OCM_CHANNEL_TABLE
  - OTN_OSC_TABLE

## CLI Support for OTN
We use SONiC CLI Auto-generation tool to support SONiC OTN CLI by ocs yang model. For more detail please refer to [SONiC CLI Auto-generation tool](https://github.com/sonic-net/SONiC/blob/master/doc/cli_auto_generation/cli_auto_generation.md)

### Generate OTN CLI command
```bash
sudo -i

```

### Features
- show xxxxx
- config xxxxx

### Show OTN xxxxx configuration
```bash
root@sonic:~# show xxxxx

root@sonic:~#
```

### Show OTN xxxxx state
```bash
root@sonic:~# show xxxxx 

root@sonic:~# 
```

## REST API Support for OTN
REST API follows RESTCONF protocol

In ```sonic-mgmt-common```, REST APIs are generated from ```sonic-xxxxx.yang``` yang model.

### Show OTN xxxxx configuration
```bash
admin@sonic:~$
```

### Show OTN xxxxx state
```bash
admin@sonic:~$
```
