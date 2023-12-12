

# Prerequisites
* Install qemu
```
sudo apt-get install qemu-kvm
```
or
```
brew install qemu
```


* download sonic-otn virtual images

1. download ONIE image `onie-recovery-x86_64-kvm_x86_64_4_asic-r0.iso`
```shell
curl https://sonicstorage.blob.core.windows.net/packages/onie/onie-recovery-x86_64-kvm_x86_64_4_asic-r0.iso\?sv\=2020-04-08\&st\=2021-08-27T22%3A41%3A07Z\&se\=2030-08-28T22%3A41%3A00Z\&sr\=b\&sp\=r\&sig\=zyaX7rHnE5jXldpgrnWq1nvsfmMTrVCSuESZqrIxDLc%3D --output onie-recovery-x86_64-kvm_x86_64_4_asic-r0.iso
```

2. download installer images `sonic-installer.img` and `sonic-4asic-vs.img`  
download these images from the github [actions](https://github.com/sonic-otn/sonic-buildimage/actions/workflows/otn-legacy-vs-image-build.yml) artifacts, for example this workflow [build#9](https://github.com/sonic-otn/sonic-buildimage/actions/runs/7179185281)

  
* (optional) build sonic-otn virtual images
Build these images with steps in [readme](./README.md). Then you can find the `sonic-installer.img` and `sonic-4asic-vs.img` in the root and `target` folder


# How to Start a Virtual Machine

1. Start VM via qemu
```
gunzip -k sonic-4asic-vs.img.gz

sudo qemu-system-x86_64 -m 3072 -name onie -accel hvf -boot order=cd,once=d -cdrom ./onie-recovery-x86_64-kvm_x86_64_4_asic-r0.iso  -device e1000,netdev=onienet -netdev user,id=onienet,hostfwd=:0.0.0.0:3040-:22 -vga std -drive file=./sonic-4asic-vs.img,media=disk,if=virtio,index=0 -drive file=./sonic-installer.img,if=virtio,index=1 -serial telnet:127.0.0.1:7000,server
```

3. Open a new terminal, use console to login ONIE.
```
telnet 127.0.0.1 7000
```

4. Choose entry: `ONIE: Embed ONIE`

5. Choose entry: `ONIE: Install OS`

6. Wait until AONOS image installed.
  
   Use 'blkid' to check if SONiC-OS partition is created.

```
ONIE:/ # blkid
/dev/vda3: LABEL="SONiC-OS" UUID="4e05cdd8-b229-4dbe-b0e9-c46f463f6222"
/dev/vdb: UUID="9DBD-175E"
/dev/vda2: LABEL="ONIE-BOOT" UUID="e0f5d6f2-64aa-4501-8123-62bed94e04ee"
```

7. reboot
```
ONIE:/ # reboot
```

# How to Login Virtual Machine

1. Connect AONOS VM via console

```
telnet 127.0.0.1 7000
```

2. Connect AONOS VM via SSH

    a. Connect via console

    b. Request a new DHCP address

    ```
    sudo dhclient -v
    ```

    c. Connect via SSH
    ```
    ssh root@localhost -p 3040
    ```

# AONOS CLI Demo

1. Show line-cards info
```
root@sonic:~# show chassis 1 slots
Succeeded
  Slot  Prov    Status    PN            SN            Hard-Ver    Soft-Ver    Temp(C)
------  ------  --------  ------------  ------------  ----------  ----------  ---------
     1  P230C   Ready     P230CAC000    AC049015C007  1.1         1.1.1       24.0
     2  P230C   Ready     P230CAC000    AC049015C008  1.1         1.1.1       27.0
     3  P230C   Ready     P230CAC000    AC049015C009  1.1         1.1.1       29.0
     4  E110C   Ready     E110CAC000    AC04B1167003  1.1         1.1.1       29.0
     5  PSU     Ready     GW-CRPS800N2  2K120052945   2.0         N/A         21.1
     6  PSU     Empty     N/A           N/A           N/A         N/A         NA
     7  FAN     Ready     FANAC000      AC042315901A  1.1         N/A         51.1
     8  FAN     Ready     FANAC000      AC042315901B  1.1         N/A         52.2
     9  FAN     Ready     FANAC000      AC042315901C  1.1         N/A         53.3
    10  FAN     Ready     FANAC000      AC042315901D  1.1         N/A         54.4
    11  FAN     Ready     FANAC000      AC042315901E  1.1         N/A         55.5
root@sonic:~# 
```

2. Show client-side transceiver info
```
root@sonic:~# show slot 1 client 1 state
Succeeded
Name                                         : TRANSCEIVER-1-1-C1
Exist                                        : PRESENT
PortAdmin                                    : ENABLED
TxLaser                                      : true
PowerMode                                    : NORMAL
PrecfgType                                   : ETH_10GBASE_LRM
FecMode                                      : FEC_AUTO
LoopBack                                     : NONE
prbs                                         : true
prbsPattern                                  : PRBS_PATTERN_TYPE_2E7
LinkDownDelayMode                            : true
LinkDownDelayHoldoff(ms)                     : 0
LinkUpDelayMode                              : true
LinkUpDelayHoldoff(s)                        : 0
LinkUpDelayActiveThreshold(ms)               : 0
DelayMeasAutoEnable                          : true
ClientAlsClientRxSwitch                      : NONE
ClientAlsClientRxHoldoff(ms)                 : 0
ClientAlsClientTxSwitch                      : NONE
ClientAlsClientTxHoldoff(ms)                 : 0
ClientAlsLineRxSwitch                        : NONE
ClientAlsLineRxHoldoff(ms)                   : 0
ForceInsert                                  : LF
LldpEnable                                   : true
ExtendModuleCode                             : SDR
Datastatus                                   : NOT_READY
Encode                                       : UNSPECIFIED
Bitrate(Gbit)                                : 0.0
Extendbitrate(Gbit)                          : 0.0
GeLinkState                                  : UP
ClientMode                                   : PROT_1GE
LedState                                     : RED

RxPowerTotal(dBm)                            : 75.0
TxPowerTotal(dBm)                            : 75.0
Temp(C)                                      : 75.0
Voltage(mV)                                  : 75.0
PreFecBer                                    : 75.0
DelayMeasureValue(us)                        : 75

<Lane-1>
InputPower(dBm)                              : 74.0
OutputPower(dBm)                             : 74.0
LaserBias(mA)                                : 74.0
<Lane-2>
InputPower(dBm)                              : 74.0
OutputPower(dBm)                             : 74.0
LaserBias(mA)                                : 74.0
<Lane-3>
InputPower(dBm)                              : 74.0
OutputPower(dBm)                             : 74.0
LaserBias(mA)                                : 74.0
<Lane-4>
InputPower(dBm)                              : 74.0
OutputPower(dBm)                             : 74.0
LaserBias(mA)                                : 74.0

root@sonic:~# 
```


3. Show line-side transceiver info
```
root@sonic:~# show slot 1 line 1 state
Succeeded
Name                                         : TRANSCEIVER-1-1-L1
PortOperState                                : ACTIVE
PortAdministate                              : ENABLED
DcoVendorPreconf                             : test data
tx-laser                                     : true
LineLoop                                     : NONE
LinePrbsTx                                   : PRBS_PATTERN_TYPE_2E7
LinePrbsRx                                   : PRBS_PATTERN_TYPE_2E7
LineForceInsert                              : AIS
tti-msg-auto-mode                            : true
Tti_transmit                                 : test data
Tti_rx_expected                              : test data
TxPower(dBm)                                 : 0.0
Frequency(MHz)                               : 0
OperationlMode                               : test data
Tti_rx                                       : test data
LineState                                    : true
LineExist                                    : PRESENT
LineFrequency(MHz)                           : 0
LinePrbsStateTx                              : PRBS_PATTERN_TYPE_2E7
LinePrbsStateRx                              : PRBS_PATTERN_TYPE_2E7
LedState                                     : RED

InputPower(dBm)                              : 2907.0
OutputPower(dBm)                             : 2907.0
LaserBias(mA)                                : 2907.0
PowerConsumption(W)                          : 2907.0
CaseTemp(C)                                  : 2907.0
LaserTemp(C)                                 : 2907.0
TX MOD BIAS X/I                              : 2907.0
TX MOD BIAS X/Q                              : 2907.0
TX MOD BIAS Y/I                              : 2907.0
TX MOD BIAS Y/Q                              : 2907.0
TX MOD BIAS X/PH                             : 2907.0
TX MOD BIAS Y/PH                             : 2907.0
Q-Factor                                     : 2907.0
ESNR                                         : 2907.0
PRE-FEC-BER                                  : 2907.0
POST-FEC-BER                                 : 2907.0
OSNR(dB)                                     : 2907.0
CD(ps/nm)                                    : 2907.0
PDL(dB)                                      : 2907.0
FOFF(MHz)                                    : 312758597
DGD(ps)                                      : 2907.0
SoPMD(ps^2)                                  : 2907.0
SOP CHANGE RATE(rad/s)                       : 312758597
LASER BIAS(mA)                               : 2907.0
EDFA BIAS(mA)                                : 2907.0
Signal Input Power(dBm)                      : 2907.0

root@sonic:~# 

```

4. Show edfa module info

```
root@sonic:~# show slot 4 edfa 1 info
Succeeded
Module Name                                  : AMPLIFIER-1-4-1
Module PN                                    : test data
Module SN                                    : test data
Firmware version                             : test data
Work mode                                    : CONSTANT_POWER
EDFA Switch Actual                           : true
Gain Range(dB)                               : LOW_GAIN_RANGE
Set gain(dB)                                 : 0.0
Set Gain tilt                                : 0.0
Work State                                   : LOS_A
Los Ase Delay(hold off time)(ms)             : 0
Input LOS Th(dBm)                            : 0.0
Input LOS Hy(dB)                             : 0.0
Output LOP Th(dBm)                           : 0.0
Output LOP Hy(dB)                            : 0.0
Gain Low Alm Th(dBm)                         : 0.0
Gain Low Alm Hy(dB)                          : 0.0
Pin Low AlmTh(dBm)                           : 0.0
Pout Low AlmTh(dBm)                          : 0.0

Module temperature(C)                        : 3035.0
Actual gain(dB)                              : 3035.0
Actual Gain tilt                             : 3035.0
Pump Iop(mA)                                 : 3035.0
Pump temperature(C)                          : 3035.0
Pump Itec(mA)                                : 3035.0
Input power(Original)(dBm)                   : 3035.0
Output power(Original)(dBm)                  : 3035.0
```

5. Show olp info

```
root@sonic:~# show slot 4 olp 1 info
Succeeded
Module Name                                  : APS-1-4-1
Work Mode (Revertive)                        : true
Work Line                                    : PRIMARY
Wait-to-restore-time(ms)                     : 0
Hold-off-time(ms)                            : 0
Switch Hysteresis(dB)                        : 0.0
Alarm Hysteresis(dB)                         : 0.0
Relative Diff Threshold(dB)                  : 0.0
Relative Diff Threshold Offset(dB)           : 0.0
Force-to-port                                : NONE
primary-in Switch Th.(dBm)                   : 0.0
secondary-in Switch Th.(dBm)                 : 0.0

LinePrimaryIn Los Th.(dBm)                   : 0.0
LinePrimaryIn Low Th.(dBm)                   : 0.0
LinePrimaryIn Optical Power(dBm)             : 3066.0
LinePrimaryOut Los Th.(dBm)                  : 0.0
LinePrimaryOut Low Th.(dBm)                  : 0.0
LinePrimaryOut Optical Power(dBm)            : 3066.0
LineSecondaryIn Los Th.(dBm)                 : 0.0
LineSecondaryIn Low Th.(dBm)                 : 0.0
LineSecondaryIn Optical Power(dBm)           : 3066.0
LineSecondaryOut Los Th.(dBm)                : 0.0
LineSecondaryOut Low Th.(dBm)                : 0.0
LineSecondaryOut Optical Power(dBm)          : 3066.0
CommonIn Los Th.(dBm)                        : 0.0
CommonIn Low Th.(dBm)                        : 0.0
CommonIn Optical Power(dBm)                  : 3066.0
CommonOutput Los Th.(dBm)                    : 0.0
CommonOutput Low Th.(dBm)                    : 0.0
CommonOutput Optical Power(dBm)              : 3066.0

root@sonic:~# 
```
# AONOS Restconf and Telemetry Demo

You can test Restconf with these commands in the OS:

```curl -u admin:admin -k https://localhost/restconf/data/openconfig-platform:components```

```curl -u admin:admin -k https://localhost/restconf/data/openconfig-interfaces:interfaces```

You can test telemetry with these commands in the telemetry container:
```docker exec -ti telemetry bash```

```gnmi_get -alsologtostderr -insecure -notls -xpath_target OC-YANG -xpath /openconfig-interfaces:interfaces/interface[name=INTERFACE-1-1-C1]/state -target_addr 127.0.0.1:8081```

```gnmi_get -alsologtostderr -insecure -notls -xpath_target OC-YANG -xpath /openconfig-platform:components/component[name=TRANSCEIVER-1-1-L1]/state -target_addr 127.0.0.1:8081```

You can test the telemetry dial-out with these commands:

1. Run the commands in [test-telemetry-subscription.sh](./test-telemetry-subscription.sh) to delete the telemetry subscription and add a new subscription  

2. Then you should be able to show the telemetry information via CLI, the telemetry server destination is `127.0.0.1:8082`
```
root@sonic:~# show telemetry info
destinations  : 127.0.0.1:8082
sensor-groups :
  group-id : alarm_sensor_group
    heartbeat-interval : 0
    sample-interval    : 0
    paths              : /openconfig-system:system/alarms/alarm/state
  group-id : module_sensor_group
    heartbeat-interval : 0
    sample-interval    : 5000
    paths              : /openconfig-transport-line-protection:aps/aps-modules/aps-module/ports,/openconfig-optical-amplifier:optical-amplifier/amplifiers/amplifier/state,/openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator/state,/openconfig-optical-amplifier:optical-amplifier/supervisory-channels/supervisory-channel/state,/openconfig-platform:components/component/port/openconfig-transport-line-common:optical-port/state
  group-id : platform_sensor_group
    heartbeat-interval : 0
    sample-interval    : 5000
    paths              : /openconfig-platform:components/component/power-supply/state,/openconfig-platform:components/component/fan/state,/openconfig-platform:components/component/state,/openconfig-system:system/cpus/cpu/state
  group-id : och_sensor_group
    heartbeat-interval : 0
    sample-interval    : 5000
    paths              : /openconfig-platform:components/component/openconfig-terminal-device:optical-channel/state
  group-id : ocm_sensor_group
    heartbeat-interval : 0
    sample-interval    : 5000
    paths              : /openconfig-channel-monitor:channel-monitors/channel-monitor/channels
  group-id : xcvr_sensor_group
    heartbeat-interval : 0
    sample-interval    : 5000
    paths              : /openconfig-platform:components/component/openconfig-platform-transceiver:transceiver/state,/openconfig-platform:components/component/openconfig-platform-transceiver:transceiver/physical-channels/channel/state
  group-id : otn_sensor_group
    heartbeat-interval : 0
    sample-interval    : 5000
    paths              : /openconfig-terminal-device:terminal-device/logical-channels/channel/otn/state
  group-id : ethernet_sensor_group
    heartbeat-interval : 0
    sample-interval    : 5000
    paths              : /openconfig-interfaces:interfaces/interface/state/counters,/openconfig-terminal-device:terminal-device/logical-channels/channel/ethernet/state
root@sonic:~#
```

3. Run the telemetry server to receive the data stream.
```
docker exec -ti telemetry bash
dialout_server_cli -allow_no_client_auth -logtostderr -port 8082 -insecure -v 2
I1212 20:26:34.035542      67 dialout_server.go:66] Created Server on localhost:8082
I1212 20:26:34.035609      67 dialout_server_cli.go:90] Starting RPC server on address: localhost:8082
== subscribeResponse:
update: <
  timestamp: 1702383999110043410
  prefix: <
    origin: "sonic"
    target: "OC-YANG"
  >
  update: <
    path: <
      elem: <
        name: "openconfig-terminal-device:terminal-device"
      >
      elem: <
        name: "logical-channels"
      >
      elem: <
        name: "channel"
        key: <
          key: "index"
          value: "319"
        >
      >
      elem: <
        name: "otn"
      >
      elem: <
        name: "state"
      >
    >
    val: <
      json_ietf_val: "{\"background-block-errors\":\"929\",\"code-violations\":\"929\",\"errored-blocks\":\"929\",\"errored-seconds\":\"929\",\"esnr\":{\"avg\":\"1\",\"instant\":\"1\",\"interval\":\"900000000000\",\"max\":\"1\",\"max-time\":\"1702383300950663263\",\"min\":\"1\",\"min-time\":\"1702383300950663263\"},\"fec-corrected-bits\":\"929\",\"fec-uncorrectable-blocks\":\"929\",\"post-fec-ber\":{\"avg\":\"1\",\"instant\":\"1\",\"interval\":\"900000000000\",\"max\":\"1\",\"max-time\":\"1702383300950663263\",\"min\":\"1\",\"min-time\":\"1702383300950663263\"},\"pre-fec-ber\":{\"avg\":\"1\",\"instant\":\"1\",\"interval\":\"900000000000\",\"max\":\"1\",\"max-time\":\"1702383300950663263\",\"min\":\"1\",\"min-time\":\"1702383300950663263\"},\"q-value\":{\"avg\":\"1\",\"instant\":\"1\",\"interval\":\"900000000000\",\"max\":\"1\",\"max-time\":\"1702383300950663263\",\"min\":\"1\",\"min-time\":\"1702383300950663263\"},\"severely-errored-seconds\":\"929\",\"unavailable-seconds\":\"929\"}"
    >
  >
```


