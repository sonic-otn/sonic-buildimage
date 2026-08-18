# SONIC otn-kvm Platform Build and Run Instructions

This doc contains the procedure to compile, run and test the SONiC-OTN KVM image, the prototype the team currently has.  
For SONiC compilation environment setup, please refer to [sonic-buildimage](https://github.com/sonic-net/sonic-buildimage) and [README.md](https://github.com/sonic-net/sonic-buildimage/blob/master/README.md)

# HOWTO Build otn-kvm image

``` bash
make init
make configure PLATFORM=otn-kvm
make NOBOOKWORM=1 target/sonic-otn-kvm.img.gz
```

> `NOBOOKWORM=1` skips the redundant Debian Bookworm build pass. otn-kvm is
> Trixie-only (all containers, including `syncd`, are Trixie-based), so the
> Bookworm pass produces nothing the image needs and only wastes build time.
> The top-level `Makefile` still defaults to `NOBOOKWORM ?= 0` (upstream
> Bookworm→Trixie transition scaffolding), so pass `NOBOOKWORM=1` explicitly
> on the otn-kvm build.

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
Linux sonic 6.12.41+deb13-sonic-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.41-1 (2026-07-13) x86_64
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
Debian GNU/Linux 13 \n \l

admin@localhost's password:
Linux sonic 6.12.41+deb13-sonic-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.41-1 (2026-07-13) x86_64
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
> otn-kvm is backed by a simulated HAL, so the inventory fields (model, serial,
> hardware revision) and the sensor readings below are synthetic placeholders,
> not values read from real hardware. Timestamps and the kernel version in the
> examples come from one particular build and will differ on yours.

### Show summary information
```bash
admin@sonic:~$ show platform summary 
Platform: x86_64-otn-kvm_x86_64-r0
HwSKU: OLS-V
ASIC: otn-kvm
ASIC Count: 1
Serial Number: 123456789
Model Number: KVM-1234
Hardware Revision: 1.0
Switch Type: otn
admin@sonic:~$
```

### Show PSU information
```bash
admin@sonic:~$ show platform psu
PSU    Model         Serial    HW Rev    Voltage (V)    Current (A)    Power (W)  Status    LED
-----  ---------  ---------  --------  -------------  -------------  -----------  --------  -----
PSU0   PSU Model  123456789      1.00          12.00           1.50        18.00  OK        green
PSU1   PSU Model  123456789      1.00          12.00           1.50        18.00  OK        green
admin@sonic:~$ 
```

### Show fan information
```bash
admin@sonic:~$ show platform fan
  Drawer    LED            FAN    Speed    Direction    Presence    Status          Timestamp
--------  -----  -------------  -------  -----------  ----------  --------  -----------------
FanTray0  green  FanTray0-Fan0      50%       intake     Present        OK  20260805 20:32:06
FanTray0  green  FanTray1-Fan1      50%       intake     Present        OK  20260805 20:32:06
FanTray0  green  FanTray2-Fan2      50%       intake     Present        OK  20260805 20:32:06
FanTray0  green  FanTray3-Fan3      50%       intake     Present        OK  20260805 20:32:06
     N/A  green       PSU0-Fan      50%       intake     Present        OK  20260805 20:32:06
     N/A  green       PSU1-Fan      50%       intake     Present        OK  20260805 20:32:06
admin@sonic:~$
```

All four chassis fans belong to the single `FanTray0` drawer, but their names come
straight from `platform.json` and are not renumbered per drawer, which is why
`FanTray1-Fan1` through `FanTray3-Fan3` appear under drawer `FanTray0`.

### Show thermal information
```bash
admin@sonic:~$ show platform temperature 
Failed to get port config
        Sensor    Temperature    High TH    Low TH    Crit High TH    Crit Low TH    Warning          Timestamp
--------------  -------------  ---------  --------  --------------  -------------  ---------  -----------------
  System Board             35         70        10              90              5      False  20260805 20:32:06
System Exhaust             35         70        10              90              5      False  20260805 20:32:06
admin@sonic:~$
```

The `Failed to get port config` line is expected: otn-kvm has no front-panel
Ethernet ports, so the command finds no port configuration to read transceiver
temperatures from. The chassis sensors above are unaffected.

### Show firmware information
```bash
admin@sonic:~$ show platform firmware status
Chassis    Module       Component      Version  Description
---------  -----------  -----------  ---------  -------------------------------------------------------------
OLA        LINE-CARD0   OA0-0                1  Optical amplifier (west)
                        OA0-1                1  Optical amplifier (east)
                        OSC0-0               1  Optical supervisory channel (west)
                        OSC0-1               1  Optical supervisory channel (east)
                        OCM0-0               1  Optical channel monitor
                        OTDR0-0              1  Optical time domain reflectometer
           SUPERVISOR0  BIOS                 1  Performs initialization of hardware components during booting
                        FPGA                 1  Platform managment controller for on-board components
                        CPLD                 1  Used for managing IO modules
                        ONIE                 1  Open network install environment
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

## OTN gNMI and REST Examples
Detailed CLI, REST and gNMI examples for the `otn-kvm` device are available in
[OTN-KVM-NBI-Examples](./OTN-KVM-NBI-Example.md).