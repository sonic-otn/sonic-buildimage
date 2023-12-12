curl -u admin:admin -k --location --request DELETE 'https://localhost/restconf/data/openconfig-telemetry:telemetry-system'


curl -u admin:admin -k --location --request PUT 'https://localhost/restconf/data/openconfig-telemetry:telemetry-system' \
--header 'Content-Type: application/yang-data+json' \
--data-raw '{
    "telemetry-system": {
        "subscriptions": {
            "persistent-subscriptions": {
                "persistent-subscription": [
                    {
                        "destination-groups": {
                            "destination-group": [
                                {
                                    "group-id": "collector_dest_group",
                                    "config": {
                                        "group-id": "collector_dest_group"
                                    }
                                }
                            ]
                        },
                        "name": "obx1100e_hybrid_sub_v110",
                        "config": {
                            "protocol": "openconfig-telemetry-types:STREAM_GRPC",
                            "name": "obx1100e_hybrid_sub_v110",
                            "encoding": "openconfig-telemetry-types:ENC_JSON_IETF"
                        },
                        "sensor-profiles": {
                            "sensor-profile": [
                                {
                                    "sensor-group": "ethernet_sensor_group",
                                    "config": {
                                        "sample-interval": "5000",
                                        "sensor-group": "ethernet_sensor_group"
                                    }
                                },
                                {
                                    "sensor-group": "otn_sensor_group",
                                    "config": {
                                        "sample-interval": "5000",
                                        "sensor-group": "otn_sensor_group"
                                    }
                                },
                                {
                                    "sensor-group": "och_sensor_group",
                                    "config": {
                                        "sample-interval": "5000",
                                        "sensor-group": "och_sensor_group"
                                    }
                                },
                                {
                                    "sensor-group": "ocm_sensor_group",
                                    "config": {
                                        "sample-interval": "5000",
                                        "sensor-group": "ocm_sensor_group"
                                    }
                                },
                                {
                                    "sensor-group": "xcvr_sensor_group",
                                    "config": {
                                        "sample-interval": "5000",
                                        "sensor-group": "xcvr_sensor_group"
                                    }
                                },
                                {
                                    "sensor-group": "platform_sensor_group",
                                    "config": {
                                        "sample-interval": "5000",
                                        "sensor-group": "platform_sensor_group"
                                    }
                                },
                                {
                                    "sensor-group": "module_sensor_group",
                                    "config": {
                                        "sample-interval": "5000",
                                        "sensor-group": "module_sensor_group"
                                    }
                                },
                                {
                                    "sensor-group": "alarm_sensor_group",
                                    "config": {
                                        "sample-interval": "0",
                                        "sensor-group": "alarm_sensor_group"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "destination-groups": {
            "destination-group": [
                {
                    "group-id": "collector_dest_group",
                    "destinations": {
                        "destination": [
                            {
                                "destination-port": 8082,
                                "destination-address": "127.0.0.1",
                                "config": {
                                    "destination-port": 8082,
                                    "destination-address": "127.0.0.1"
                                }
                            }
                        ]
                    },
                    "config": {
                        "group-id": "collector_dest_group"
                    }
                }
            ]
        },
        "sensor-groups": {
            "sensor-group": [
                {
                    "sensor-group-id": "ethernet_sensor_group",
                    "sensor-paths": {
                        "sensor-path": [
                            {
                                "path": "/openconfig-interfaces:interfaces/interface/state/counters",
                                "config": {
                                    "path": "/openconfig-interfaces:interfaces/interface/state/counters"
                                }
                            },
                            {
                                "path": "/openconfig-terminal-device:terminal-device/logical-channels/channel/ethernet/state",
                                "config": {
                                    "path": "/openconfig-terminal-device:terminal-device/logical-channels/channel/ethernet/state"
                                }
                            }
                        ]
                    },
                    "config": {
                        "sensor-group-id": "ethernet_sensor_group"
                    }
                },
                {
                    "sensor-group-id": "otn_sensor_group",
                    "sensor-paths": {
                        "sensor-path": [
                            {
                                "path": "/openconfig-terminal-device:terminal-device/logical-channels/channel/otn/state",
                                "config": {
                                    "path": "/openconfig-terminal-device:terminal-device/logical-channels/channel/otn/state"
                                }
                            }
                        ]
                    },
                    "config": {
                        "sensor-group-id": "otn_sensor_group"
                    }
                },
                {
                    "sensor-group-id": "och_sensor_group",
                    "sensor-paths": {
                        "sensor-path": [
                            {
                                "path": "/openconfig-platform:components/component/openconfig-terminal-device:optical-channel/state",
                                "config": {
                                    "path": "/openconfig-platform:components/component/openconfig-terminal-device:optical-channel/state"
                                }
                            }
                        ]
                    },
                    "config": {
                        "sensor-group-id": "och_sensor_group"
                    }
                },
                {
                    "sensor-group-id": "ocm_sensor_group",
                    "sensor-paths": {
                        "sensor-path": [
                            {
                                "path": "/openconfig-channel-monitor:channel-monitors/channel-monitor/channels",
                                "config": {
                                    "path": "/openconfig-channel-monitor:channel-monitors/channel-monitor/channels"
                                }
                            }
                        ]
                    },
                    "config": {
                        "sensor-group-id": "ocm_sensor_group"
                    }
                },
                {
                    "sensor-group-id": "xcvr_sensor_group",
                    "sensor-paths": {
                        "sensor-path": [
                            {
                                "path": "/openconfig-platform:components/component/openconfig-platform-transceiver:transceiver/state",
                                "config": {
                                    "path": "/openconfig-platform:components/component/openconfig-platform-transceiver:transceiver/state"
                                }
                            },
                            {
                                "path": "/openconfig-platform:components/component/openconfig-platform-transceiver:transceiver/physical-channels/channel/state",
                                "config": {
                                    "path": "/openconfig-platform:components/component/openconfig-platform-transceiver:transceiver/physical-channels/channel/state"
                                }
                            }
                        ]
                    },
                    "config": {
                        "sensor-group-id": "xcvr_sensor_group"
                    }
                },
                {
                    "sensor-group-id": "platform_sensor_group",
                    "sensor-paths": {
                        "sensor-path": [
                            {
                                "path": "/openconfig-platform:components/component/power-supply/state",
                                "config": {
                                    "path": "/openconfig-platform:components/component/power-supply/state"
                                }
                            },
                            {
                                "path": "/openconfig-platform:components/component/fan/state",
                                "config": {
                                    "path": "/openconfig-platform:components/component/fan/state"
                                }
                            },
                            {
                                "path": "/openconfig-platform:components/component/state",
                                "config": {
                                    "path": "/openconfig-platform:components/component/state"
                                }
                            },
                            {
                                "path": "/openconfig-system:system/cpus/cpu/state",
                                "config": {
                                    "path": "/openconfig-system:system/cpus/cpu/state"
                                }
                            }
                        ]
                    },
                    "config": {
                        "sensor-group-id": "platform_sensor_group"
                    }
                },
                {
                    "sensor-group-id": "alarm_sensor_group",
                    "sensor-paths": {
                        "sensor-path": [
                            {
                                "path": "/openconfig-system:system/alarms/alarm/state",
                                "config": {
                                    "path": "/openconfig-system:system/alarms/alarm/state"
                                }
                            }
                        ]
                    },
                    "config": {
                        "sensor-group-id": "alarm_sensor_group"
                    }
                },
                {
                    "sensor-group-id": "module_sensor_group",
                    "sensor-paths": {
                        "sensor-path": [
                            {
                                "path": "/openconfig-transport-line-protection:aps/aps-modules/aps-module/ports",
                                "config": {
                                    "path": "/openconfig-transport-line-protection:aps/aps-modules/aps-module/ports"
                                }
                            },
                            {
                                "path": "/openconfig-optical-amplifier:optical-amplifier/amplifiers/amplifier/state",
                                "config": {
                                    "path": "/openconfig-optical-amplifier:optical-amplifier/amplifiers/amplifier/state"
                                }
                            },
                            {
                                "path": "/openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator/state",
                                "config": {
                                    "path": "/openconfig-optical-attenuator:optical-attenuator/attenuators/attenuator/state"
                                }
                            },
                            {
                                "path": "/openconfig-optical-amplifier:optical-amplifier/supervisory-channels/supervisory-channel/state",
                                "config": {
                                    "path": "/openconfig-optical-amplifier:optical-amplifier/supervisory-channels/supervisory-channel/state"
                                }
                            },
                            {
                                "path": "/openconfig-platform:components/component/port/openconfig-transport-line-common:optical-port/state",
                                "config": {
                                    "path": "/openconfig-platform:components/component/port/openconfig-transport-line-common:optical-port/state"
                                }
                            }
                        ]
                    },
                    "config": {
                        "sensor-group-id": "module_sensor_group"
                    }
                }
            ]
        }
    }
}'