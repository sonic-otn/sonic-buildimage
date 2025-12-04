# SONiC otn-kvm CLI and NBI Examples

## CLI Support for OTN
SONiC CLI Auto-generation tool is used to support SONiC OTN CLIs at device level, i.e., only the CLIs applicable for the device will be available on the device.
- all OTN commands is generated at build time and included in the image.
- only commands applicable to the specific device is loaded during startup.

### Feature Examples (TBD)
- show xxxxx
- config xxxxx

## REST API Support for OTN
The OTN REST API follows the RESTCONF protocol and uses JSON-encoded YANG data.

In ```sonic-mgmt-common```, REST APIs are generated from both OpenConfig and SONiC YANG models. 

For OTN specifically, OpenConfig APIs are generated from:
- `openconfig-optical-amplifier.yang`
- `openconfig-optical-attenuator.yang`
- `openconfig-channel-monitor.yang`

SONiC APIs are generated from:
- `sonic-optical-amplifier.yang`
- `sonic-optical-attenuator.yang`
- `sonic-channel-monitor.yang`

Some example usage is shown below.
### Optical-amplifier (OA)
#### OpenConfig GET request
Below request retrieves configuration and operational state for all optical amplifiers on the device via the OpenConfig optical-amplifier RESTCONF resource.
```bash
admin@sonic:~$   curl -k -X GET\
   "https://127.0.0.1/restconf/data/openconfig-optical-amplifier:optical-amplifier/amplifiers" \
   -H "accept: application/yang-data+json" | jq
```
```json
{
  "openconfig-optical-amplifier:amplifiers": {
    "amplifier": [
      {
        "config": {
          "amp-mode": "openconfig-optical-amplifier:CONSTANT_GAIN",
          "enabled": true,
          "gain-range": "openconfig-optical-amplifier:FIXED_GAIN_RANGE",
          "name": "OA0-0",
          "target-gain": "4.2",
          "target-gain-tilt": "0.4",
          "type": "openconfig-optical-amplifier:EDFA"
        },
        "name": "OA0-0",
        "state": {
          "actual-gain": {
            "instant": "4.2"
          },
          "actual-gain-tilt": {
            "instant": "0.4"
          },
          "amp-mode": "openconfig-optical-amplifier:CONSTANT_GAIN",
          "egress-port": "",
          "enabled": true,
          "gain-range": "openconfig-optical-amplifier:FIXED_GAIN_RANGE",
          "ingress-port": "",
          "input-power-c-band": {
            "instant": "-60"
          },
          "input-power-l-band": {
            "instant": "25"
          },
          "input-power-total": {
            "instant": "25"
          },
          "laser-bias-current": {
            "instant": "25"
          },
          "name": "OA0-0",
          "optical-return-loss": {
            "instant": "25"
          },
          "output-power-c-band": {
            "instant": "25"
          },
          "output-power-l-band": {
            "instant": "25"
          },
          "output-power-total": {
            "instant": "25"
          },
          "target-gain": "4.2",
          "target-gain-tilt": "0.4",
          "type": "openconfig-optical-amplifier:EDFA"
        }
      },
      {
        "config": {
          "amp-mode": "openconfig-optical-amplifier:CONSTANT_GAIN",
          "enabled": true,
          "gain-range": "openconfig-optical-amplifier:FIXED_GAIN_RANGE",
          "name": "OA0-1",
          "target-gain": "5.2",
          "target-gain-tilt": "0.5",
          "type": "openconfig-optical-amplifier:EDFA"
        },
        "name": "OA0-1",
        "state": {
          "actual-gain": {
            "instant": "5.2"
          },
          "actual-gain-tilt": {
            "instant": "0.5"
          },
          "amp-mode": "openconfig-optical-amplifier:CONSTANT_GAIN",
          "egress-port": "",
          "enabled": true,
          "gain-range": "openconfig-optical-amplifier:FIXED_GAIN_RANGE",
          "ingress-port": "",
          "input-power-c-band": {
            "instant": "-60"
          },
          "input-power-l-band": {
            "instant": "25"
          },
          "input-power-total": {
            "instant": "25"
          },
          "laser-bias-current": {
            "instant": "25"
          },
          "name": "OA0-1",
          "optical-return-loss": {
            "instant": "25"
          },
          "output-power-c-band": {
            "instant": "25"
          },
          "output-power-l-band": {
            "instant": "25"
          },
          "output-power-total": {
            "instant": "25"
          },
          "target-gain": "5.2",
          "target-gain-tilt": "0.5",
          "type": "openconfig-optical-amplifier:EDFA"
        }
      }
    ]
  }
}
```

#### OpenConfig PUT request
Configure the OpenConfig optical amplifier target-gain parameter for amplifier OA0-0 via a RESTCONF PUT request.
```bash
curl -k  -X PUT \
    -H "Content-Type: application/yang-data+json" \
    -H "Accept: application/yang-data+json" \
    "https://127.0.0.1/restconf/data/openconfig-optical-amplifier:optical-amplifier/amplifiers/amplifier=OA0-0/config/target-gain" \
    -d '{"openconfig-optical-amplifier:target-gain": "5.0"}' | jq
```

#### SONiC GET request
Below request retrieves configuration and operational state for all optical amplifiers on the device via the SONiC optical-amplifier RESTCONF resource.
```bash
admin@sonic:~$    curl -k -X GET\
  "https://127.0.0.1/restconf/data/sonic-optical-amplifier:sonic-optical-amplifier/OTN_OA/OTN_OA_LIST" \
  -H "accept: application/yang-data+json" | jq
```
```json
{
  "sonic-optical-amplifier:OTN_OA_LIST": [
    {
      "amp-mode": "CONSTANT_GAIN",
      "enabled": true,
      "gain-range": "FIXED_GAIN_RANGE",
      "name": "OA0-0",
      "target-gain": "4.2",
      "target-gain-tilt": "0.4",
      "type": "EDFA"
    },
    {
      "amp-mode": "CONSTANT_GAIN",
      "enabled": true,
      "gain-range": "FIXED_GAIN_RANGE",
      "name": "OA0-1",
      "target-gain": "5.2",
      "target-gain-tilt": "0.5",
      "type": "EDFA"
    }
  ]
}
```
### Optical Attenuator (VOA)
#### OpenConfig GET request
Below request retrieves configuration and operational state for a specific variable optical attenuator (VOA0‑0) via the OpenConfig optical-attenuator RESTCONF resource.
```bash
admin@sonic:~$   curl -k -X GET \
   "https://127.0.0.1/restconf/data/openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator=VOA0-0" \
   -H "accept: application/yang-data+json" | jq
```
```json
{
  "openconfig-optical-attenuator:attenuator": [
    {
      "config": {
        "attenuation": "4.2",
        "attenuation-mode": "openconfig-optical-attenuator:CONSTANT_ATTENUATION",
        "enabled": true,
        "name": "VOA0-0"
      },
      "name": "VOA0-0",
      "state": {
        "actual-attenuation": {
          "instant": "4.2"
        },
        "attenuation": "4.2",
        "attenuation-mode": "openconfig-optical-attenuator:CONSTANT_ATTENUATION",
        "egress-port": "VOA0-0-OUT",
        "enabled": true,
        "ingress-port": "VOA0-0-IN",
        "name": "VOA0-0",
        "optical-return-loss": {
          "instant": "0"
        },
        "output-power-total": {
          "instant": "0"
        }
      }
    }
  ]
}
```
#### OpenConfig PUT request
Configure the OpenConfig optical attenuator attenuation parameter for attenuator VOA0-0 via a RESTCONF PUT request.
```bash
curl -k  -X PUT \
    -H "Content-Type: application/yang-data+json" \
    -H "Accept: application/yang-data+json" \
   "https://127.0.0.1/restconf/data/openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator=VOA0-0/config/attenuation" \
    -d '{"attenuation":"6.0"}' | jq
```

#### SONiC GET request
Below request retrieves configuration and operational state for all optical attenuators on the device via the SONiC optical-attenuator RESTCONF resource.
```bash
   curl -k -X GET\
  "https://127.0.0.1/restconf/data/sonic-optical-attenuator:sonic-optical-attenuator/OTN_ATTENUATOR/OTN_ATTENUATOR_LIST" \
  -H "accept: application/yang-data+json" | jq
```
```json
{
  "sonic-optical-attenuator:OTN_ATTENUATOR_LIST": [
    {
      "attenuation": "4.2",
      "attenuation-mode": "CONSTANT_ATTENUATION",
      "enabled": true,
      "name": "VOA0-0"
    },
    {
      "attenuation": "3.2",
      "attenuation-mode": "CONSTANT_ATTENUATION",
      "enabled": true,
      "name": "VOA0-1"
    }
  ]
}
```
### Optical Supervisory Channel (OSC)
#### OpenConfig GET request
Below request retrieves configuration and optical performance state for a specific optical supervisory channel (OSC0‑0) via the OpenConfig optical-amplifier RESTCONF resource.
```bash
admin@sonic:~$   curl -k -X GET\
   "https://127.0.0.1/restconf/data/openconfig-optical-amplifier:optical-amplifier/supervisory-channels/supervisory-channel=OSC0-0" \
    -H "accept: application/yang-data+json" | jq
```
```json
{
  "openconfig-optical-amplifier:supervisory-channel": [
    {
      "config": {
        "interface": "OSC0-0"
      },
      "interface": "OSC0-0",
      "state": {
        "input-power": {
          "instant": "1.42"
        },
        "interface": "OSC0-0",
        "laser-bias-current": {
          "instant": "0"
        },
        "output-frequency": "198538194",
        "output-power": {
          "instant": "1.34"
        }
      }
    }
  ]
}
```
#### SONiC GET request
```bash
     curl -k -X GET\
  "https://127.0.0.1/restconf/data/sonic-optical-amplifier:sonic-optical-amplifier/OTN_OSC/OTN_OSC_LIST" \
  -H "accept: application/yang-data+json" | jq
```
```json
{
  "sonic-optical-amplifier:OTN_OSC_LIST": [
    {
      "interface": "OSC0-0"
    },
    {
      "interface": "OSC0-1"
    }
  ]
}
```
### Optical Channel Monitor (OCM)
#### Get configuration and live monitoring data from a specific Optical Channel Monitor (OCM0-0) via OpenConfig YANG
```bash
admin@sonic:~$     curl -k -X GET\
  "https://127.0.0.1/restconf/data/openconfig-channel-monitor:channel-monitors/channel-monitor=OCM0-0" \
  -H "accept: application/yang-data+json" | jq
```
```json
{
  "openconfig-channel-monitor:channel-monitor": [
    {
      "channels": {
        "channel": [
          {
            "lower-frequency": "191262500",
            "state": {
              "lower-frequency": "191262500",
              "power": "0.12",
              "target-power": "0.22",
              "upper-frequency": "191337500"
            },
            "upper-frequency": "191337500"
          },
          {
            "lower-frequency": "191337500",
            "state": {
              "lower-frequency": "191337500",
              "power": "0.14",              
              "target-power": "0.24",
              "upper-frequency": "191412500"
            },
            "upper-frequency": "191412500"
          },
          
          // additional channels omitted for brevity
        ]
      },
      "config": {
        "monitor-port": "LineIn",
        "name": "OCM0-0"
      },
      "name": "OCM0-0",
      "state": {
        "monitor-port": "LineIn",
        "name": "OCM0-0"
      }
    }
  ]
}
```

#### Get configuration and monitoring data from a single channel (lower-frequency=196062500, upper-frequency=196137500) of the Optical Channel Monitor (OCM0-0)
```bash
admin@sonic:~$   curl -k -X GET\
   "https://127.0.0.1/restconf/data/openconfig-channel-monitor:channel-monitors/channel-monitor=OCM0-0/channels/channel=196062500,196137500" \
   -H "accept: application/yang-data+json" | jq
```
```json
{
  "openconfig-channel-monitor:channel": [
    {
      "lower-frequency": "196062500",
      "state": {
        "lower-frequency": "196062500",
        "power": "1.4",
        "target-power": "1.5",
        "upper-frequency": "196137500"
      },
      "upper-frequency": "196137500"
    }
  ]
}
```
#### Get channel power data from a single channel (lower-frequency=196062500, upper-frequency=196137500) of the Optical Channel Monitor (OCM0-0)
```bash
admin@sonic:~$   curl -k -X GET\
   "https://127.0.0.1/restconf/data/openconfig-channel-monitor:channel-monitors/channel-monitor=OCM0-0/channels/channel=196062500,196137500/state/power" \
   -H "accept: application/yang-data+json" | jq
```
```json
{
  "openconfig-channel-monitor:power": "1.4"
}
```

#### Get the list of configured OTN channel monitor instances and their associated monitor ports using the SONiC YANG model
```bash
  curl -k -X GET\
  "https://127.0.0.1/restconf/data/sonic-channel-monitor:sonic-channel-monitor/OTN_OCM/OTN_OCM_LIST" \
  -H "accept: application/yang-data+json" | jq
```
```json
{
  "sonic-channel-monitor:OTN_OCM_LIST": [
    {
      "monitor-port": "LineIn",
      "name": "OCM0-0"
    },
    {
      "monitor-port": "LineOut",
      "name": "OCM0-1"
    },
    {
      "monitor-port": "ClientIn",
      "name": "OCM0-2"
    },
    {
      "monitor-port": "ClientOut",
      "name": "OCM0-3"
    },
    {
      "monitor-port": "OcmIn",
      "name": "OCM0-4"
    }
  ]
}
```


## gNMI Support for OTN
The SONiC `otn-kvm` image supports gNMI for model-driven management using OpenConfig YANG models. 
With a gNMI client, you can perform `get`, `set`, `capabilities` and `subscribe` operations 
on OTN resources to retrieve configuration, apply changes, and stream telemetry from the device.

### gNMI client used for test
```bash
~/sonic$ gnmic version
version : 0.42.1
 commit : 6b35566f
   date : 2025-10-20T17:04:55Z
 gitURL : https://github.com/openconfig/gnmic
   docs : https://gnmic.openconfig.net
```

### gNMI GET
#### Example of a get on the full attenuator tree
```bash
    gnmic -a 127.0.0.1:8080 -u admin -p YourPaSsWoRd --insecure \
       get --path openconfig-optical-attenuator:optical-attenuator/attenuators
```
```json
[
  {
    "source": "127.0.0.1:8080",
    "timestamp": 1767914082242916571,
    "time": "2026-01-08T18:14:42.242916571-05:00",
    "updates": [
      {
        "Path": "openconfig-optical-attenuator:optical-attenuator/attenuators",
        "values": {
          "openconfig-optical-attenuator:optical-attenuator/attenuators": {
            "openconfig-optical-attenuator:attenuators": {
              "attenuator": [
                {
                  "config": {
                    "attenuation": "9",
                    "attenuation-mode": "openconfig-optical-attenuator:CONSTANT_ATTENUATION",
                    "enabled": true,
                    "name": "VOA0-0"
                  },
                  "name": "VOA0-0",
                  "state": {
                    "actual-attenuation": {
                      "instant": "9"
                    },
                    "attenuation": "9",
                    "attenuation-mode": "openconfig-optical-attenuator:CONSTANT_ATTENUATION",
                    "egress-port": "VOA0-0-OUT",
                    "enabled": true,
                    "ingress-port": "VOA0-0-IN",
                    "name": "VOA0-0",
                    "optical-return-loss": {
                      "instant": "0"
                    },
                    "output-power-total": {
                      "instant": "0"
                    }
                  }
                },
                {
                  "config": {
                    "attenuation": "3.2",
                    "attenuation-mode": "openconfig-optical-attenuator:CONSTANT_ATTENUATION",
                    "enabled": true,
                    "name": "VOA0-1"
                  },
                  "name": "VOA0-1",
                  "state": {
                    "actual-attenuation": {
                      "instant": "3.2"
                    },
                    "attenuation": "3.2",
                    "attenuation-mode": "openconfig-optical-attenuator:CONSTANT_ATTENUATION",
                    "egress-port": "VOA0-1-OUT",
                    "enabled": true,
                    "ingress-port": "VOA0-1-IN",
                    "name": "VOA0-1",
                    "optical-return-loss": {
                      "instant": "0"
                    },
                    "output-power-total": {
                      "instant": "0"
                    }
                  }
                }
              ]
            }
          }
        }
      }
    ]
  }
]
```

#### Example of get on a specific attenuator 
```bash
    gnmic -a 127.0.0.1:8080 -u admin -p YourPaSsWoRd --insecure \
       get --path openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator[name=VOA0-0]
```
```json
[
  {
    "source": "127.0.0.1:8080",
    "timestamp": 1767914294530024577,
    "time": "2026-01-08T18:18:14.530024577-05:00",
    "updates": [
      {
        "Path": "openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator[name=VOA0-0]",
        "values": {
          "openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator": {
            "openconfig-optical-attenuator:attenuator": [
              {
                "config": {
                  "attenuation": "9",
                  "attenuation-mode": "openconfig-optical-attenuator:CONSTANT_ATTENUATION",
                  "enabled": true,
                  "name": "VOA0-0"
                },
                "name": "VOA0-0",
                "state": {
                  "actual-attenuation": {
                    "instant": "9"
                  },
                  "attenuation": "9",
                  "attenuation-mode": "openconfig-optical-attenuator:CONSTANT_ATTENUATION",
                  "egress-port": "VOA0-0-OUT",
                  "enabled": true,
                  "ingress-port": "VOA0-0-IN",
                  "name": "VOA0-0",
                  "optical-return-loss": {
                    "instant": "0"
                  },
                  "output-power-total": {
                    "instant": "0"
                  }
                }
              }
            ]
          }
        }
      }
    ]
  }
]
```

### gNMI set on an OTN resource
Note: The set service is disabled by default in the otn-kvm image.
To turn on the set service, the image needs to be rebuilt with
`ENABLE_TRANSLIB_WRITE = y` in [`sonic-buildimage/rules/config`](https://github.com/sonic-otn/sonic-buildimage/blob/202411_otn/rules/config).
```bash
gnmic -a 127.0.0.1:8080 \
   -u admin -p YourPaSsWoRd --insecure \
   set \
   --update 'openconfig-optical-attenuator:/optical-attenuator/attenuators/attenuator[name=VOA0-0]/    config:::json_ietf:::{
     "openconfig-optical-attenuator:config": {
       "attenuation": "6.0"
     }
   }'
```
```json
{
  "source": "127.0.0.1:8080",
  "time": "1969-12-31T19:00:00-05:00",
  "results": [
    {
      "operation": "UPDATE",
      "path": "openconfig-optical-attenuator:openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator[name=VOA0-0]/config"
    }
  ]
}
```
### gNMI Telemetry
#### Sample mode
In this mode the the client will send a stream subscription request and the server will push an update to the client at the default rate set by the server.
NOTE: the default stream sample rate is set to 20 seconds by the server.
```bash
gnmic --address 127.0.0.1:8080 \
  --username admin \
  --password YourPaSsWoRd \
  --insecure \
  subscribe \
  --mode stream \
  --stream-mode sample \
  --target OC-YANG \
  --path 'openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator[name=VOA0-0]/state'
```
```json
{
  "source": "127.0.0.1:8080",
  "subscription-name": "default-1767981301",
  "timestamp": 1767981300621649573,
  "time": "2026-01-09T12:55:00.621649573-05:00",
  "prefix": "openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator[name=VOA0-0]/state",
  "target": "OC-YANG",
  "updates": [
    {
      "Path": "actual-attenuation/instant",
      "values": {
        "actual-attenuation/instant": 6
      }
    },
    {
      "Path": "attenuation",
      "values": {
        "attenuation": 6
      }
    },
    {
      "Path": "ingress-port",
      "values": {
        "ingress-port": "VOA0-0-IN"
      }
    },
    {
      "Path": "optical-return-loss/instant",
      "values": {
        "optical-return-loss/instant": 0
      }
    },
    {
      "Path": "output-power-total/instant",
      "values": {
        "output-power-total/instant": 0
      }
    },
    {
      "Path": "attenuation-mode",
      "values": {
        "attenuation-mode": "CONSTANT_ATTENUATION"
      }
    },
    {
      "Path": "egress-port",
      "values": {
        "egress-port": "VOA0-0-OUT"
      }
    },
    {
      "Path": "enabled",
      "values": {
        "enabled": true
      }
    },
    {
      "Path": "name",
      "values": {
        "name": "VOA0-0"
      }
    }
  ]
}
{
  "sync-response": true
}
{
  "source": "127.0.0.1:8080",
  "subscription-name": "default-1767981301",
  "timestamp": 1767981320626278955,
  "time": "2026-01-09T12:55:20.626278955-05:00",
  "prefix": "openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator[name=VOA0-0]/state",
  "target": "OC-YANG",
  "updates": [
    {
      "Path": "output-power-total/instant",
      "values": {
        "output-power-total/instant": 0
      }
    },
    {
      "Path": "optical-return-loss/instant",
      "values": {
        "optical-return-loss/instant": 0
      }
    },
    {
      "Path": "name",
      "values": {
        "name": "VOA0-0"
      }
    },
    {
      "Path": "ingress-port",
      "values": {
        "ingress-port": "VOA0-0-IN"
      }
    },
    {
      "Path": "enabled",
      "values": {
        "enabled": true
      }
    },
    {
      "Path": "egress-port",
      "values": {
        "egress-port": "VOA0-0-OUT"
      }
    },
    {
      "Path": "attenuation-mode",
      "values": {
        "attenuation-mode": "CONSTANT_ATTENUATION"
      }
    },
    {
      "Path": "attenuation",
      "values": {
        "attenuation": 6
      }
    },
    {
      "Path": "actual-attenuation/instant",
      "values": {
        "actual-attenuation/instant": 6
      }
    }
  ]
}
```

#### Polling mode
In this mode the client will send a POLL subscription and prints the initial response (if any).
After that, it waits; each time you press Enter in the terminal, gnmic client sends a new Poll request and prints one more snapshot.
```bash
gnmic \
  --address 127.0.0.1:8080 \
  --username admin \
  --password YourPaSsWoRd \
  --insecure \
  subscribe \
  --mode poll \
  --target OC-YANG \
  --path 'openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator[name=VOA0-0]/state'
```
```json
{
  "timestamp": 1767981636874327255,
  "time": "2026-01-09T13:00:36.874327255-05:00",
  "prefix": "openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator[name=VOA0-0]",
  "target": "OC-YANG",
  "updates": [
    {
      "Path": "state/name",
      "values": {
        "state/name": "VOA0-0"
      }
    },
    {
      "Path": "state/attenuation-mode",
      "values": {
        "state/attenuation-mode": "CONSTANT_ATTENUATION"
      }
    },
    {
      "Path": "state/attenuation",
      "values": {
        "state/attenuation": 6
      }
    },
    {
      "Path": "state/egress-port",
      "values": {
        "state/egress-port": "VOA0-0-OUT"
      }
    },
    {
      "Path": "state/enabled",
      "values": {
        "state/enabled": true
      }
    },
    {
      "Path": "state/ingress-port",
      "values": {
        "state/ingress-port": "VOA0-0-IN"
      }
    },
    {
      "Path": "state/optical-return-loss/instant",
      "values": {
        "state/optical-return-loss/instant": 0
      }
    },
    {
      "Path": "state/output-power-total/instant",
      "values": {
        "state/output-power-total/instant": 0
      }
    },
    {
      "Path": "state/actual-attenuation/instant",
      "values": {
        "state/actual-attenuation/instant": 6
      }
    }
  ]
}
{
  "sync-response": true
}
received sync response 'true' from '127.0.0.1:8080'
{
  "timestamp": 1767981648418468479,
  "time": "2026-01-09T13:00:48.418468479-05:00",
  "prefix": "openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator[name=VOA0-0]",
  "target": "OC-YANG",
  "updates": [
    {
      "Path": "state/name",
      "values": {
        "state/name": "VOA0-0"
      }
    },
    {
      "Path": "state/optical-return-loss/instant",
      "values": {
        "state/optical-return-loss/instant": 0
      }
    },
    {
      "Path": "state/attenuation-mode",
      "values": {
        "state/attenuation-mode": "CONSTANT_ATTENUATION"
      }
    },
    {
      "Path": "state/enabled",
      "values": {
        "state/enabled": true
      }
    },
    {
      "Path": "state/egress-port",
      "values": {
        "state/egress-port": "VOA0-0-OUT"
      }
    },
    {
      "Path": "state/ingress-port",
      "values": {
        "state/ingress-port": "VOA0-0-IN"
      }
    },
    {
      "Path": "state/output-power-total/instant",
      "values": {
        "state/output-power-total/instant": 0
      }
    },
    {
      "Path": "state/actual-attenuation/instant",
      "values": {
        "state/actual-attenuation/instant": 6
      }
    },
    {
      "Path": "state/attenuation",
      "values": {
        "state/attenuation": 6
      }
    }
  ]
}
```
#### gNMI Once mode
A once subscription takes a single snapshot of the requested data and then terminates the subscription. 
It is useful when a point‑in‑time read is needed without continuous updates.
```bash
gnmic --address 127.0.0.1:8080 \
  --username admin \
  --password YourPaSsWoRd \
  --insecure \
  subscribe \
  --mode once \
  --target OC-YANG \
  --path 'openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator[name=VOA0-0]/state'
```

#### On-change mode
Server will push udpates to client only if there is a change in the value.
```bash
gnmic \
  --address 127.0.0.1:8080 \
  --username admin \
  --password YourPaSsWoRd \
  --insecure \
  subscribe \
  --mode stream \
  --stream-mode on-change \
  --target OC-YANG \
  --path /openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator[name=VOA0-0]/state
```

### Dial-out mode
In dial-out mode, the device initiates the gNMI connection to a telemetry collector. Subscription parameters are configured on the device, and telemetry updates are streamed automatically once the connection is established.
NOTE: Dial-out requires the device to reach the collector IP address. In QEMU environments using user-mode networking, the host is typically reachable via 10.0.2.2.

Dial-out mode does not currently support YANG urls.

#### Configure the telemetry subscription
```bash
sonic-db-cli CONFIG_DB HSET "TELEMETRY_CLIENT|Subscription_TEST" \
  dst_group LOCAL \
  path_target STATE_DB \
  paths "OTN_ATTENUATOR_TABLE*" \
  report_interval 5000 \
  report_type periodic
```
report_type periodic - corresponds to stream sample

report_interval - is specified in milliseconds

#### Configure the telemetry destination
```bash
sonic-db-cli CONFIG_DB HSET "TELEMETRY_CLIENT|DestinationGroup_LOCAL" \
  dst_addr "10.0.2.2:9090"
```
#### Global telemetry client config
```bash
sonic-db-cli CONFIG_DB HSET "TELEMETRY_CLIENT|Global" \
  encoding JSON_IETF \
  retry_interval 30 \
  src_ip 10.0.2.15 \
  unidirectional true
```

#### Optional: persist to config_db.json
If you want this persisted explicitly (not just Redis):
```bash
config save -y
#restart gnmi
systemctl restart gnmi
```

#### Start the gNMI dial-out collector
Run the reference gNMI dial-out server [`dialout_server_cli`](https://github.com/sonic-otn/sonic-gnmi/tree/otn_pre_202411/dialout/dialout_server_cli) on the host.
```bash
./dialout_server_cli \
  -allow_no_client_auth \
  -logtostderr \
  -port 9090 \
  -insecure \
  -v 2
```
This starts a plaintext gNMI server that accepts unauthenticated dial-out connections.
```log
I0112 11:45:49.480235   29924 dialout_server.go:66] Created Server on localhost:9090
I0112 11:45:49.480270   29924 dialout_server_cli.go:90] Starting RPC server on address: localhost:9090
== subscribeResponse:
update: <
  timestamp: 1768236353426026081
  prefix: <
    target: "STATE_DB"
  >
  update: <
    path: <
      elem: <
        name: "OTN_ATTENUATOR_TABLE*"
      >
    >
    val: <
      json_ietf_val: "{\"VOA0-0\":{\"actual-attenuation\":\"4.2\",\"attenuation\":\"4.2\",\"attenuation-mode\":\"CONSTANT_ATTENUATION\",\"egress-port\":\"VOA0-0-OUT\",\"enabled\":\"true\",\"ingress-port\":\"VOA0-0-IN\",\"name\":\"VOA0-0\",\"optical-return-loss\":\"0\",\"output-power-total\":\"0\"},\"VOA0-1\":{\"actual-attenuation\":\"3.2\",\"attenuation\":\"3.2\",\"attenuation-mode\":\"CONSTANT_ATTENUATION\",\"egress-port\":\"VOA0-1-OUT\",\"enabled\":\"true\",\"ingress-port\":\"VOA0-1-IN\",\"name\":\"VOA0-1\",\"optical-return-loss\":\"0\",\"output-power-total\":\"0\"}}"
    >
  >
>
```