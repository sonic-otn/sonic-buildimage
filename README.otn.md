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
We provide a test script to provision virtual linecards in the sonic-otn VM systems.

1. copy the test script [config_sonic_otn_linecard.sh](./config_sonic_otn_linecard.sh) to the sonic-otn system

```
scp -P 10022 config_sonic_otn_linecard.sh admin@localhost:/home/admin
```

2. provision slot 1 with e110c, which is a line system with VOA, OSC, EDFA, MUX/DEMUX and OLP.
```
admin@sonic:~$ ./config_sonic_otn_linecard.sh 1 e110c
1 e110c E110C 0
linecard type is e110c
plugin the linecard 1 ...
5
0
```

3. provision slot 2 with p230c, which is a transponder with four 100G Ethernet client port and one 400G line port.
```
admin@sonic:~$ ./config_sonic_otn_linecard.sh 2 p230c
2 p230c P230C 1
linecard type is p230c
plugin the linecard 2 ...
5
0
```

4. check the data in the database0 and database1
```
admin@sonic:~$ docker exec -ti database0 bash
root@sonic:/# redis-cli -n 6
root@sonic:/# redis-cli -n 2

admin@sonic:~$ docker exec -ti database1 bash
root@sonic:/# redis-cli -n 6
root@sonic:/# redis-cli -n 2
```

5. deprovision the linecard with test script  
It will plug out the virtual linecard and flush all data in the database
```
./config_sonic_otn_linecard.sh 1 none
./config_sonic_otn_linecard.sh 2 none

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

