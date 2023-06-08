from dvslib.dvs_common import *

def test_APS_attribute():
    for slot in range (1, 4):
        for port in range (1, 4):
            sobj= {
                'revertive': r'true|false',
                'wait-to-restore-time': r'\d+',
                'hold-off-time': r'\d+',
                'primary-switch-threshold': PRECISION2_PATTERN,
                'primary-switch-hysteresis': PRECISION2_PATTERN,
                'secondary-switch-threshold': PRECISION2_PATTERN,
                'relative-switch-threshold': PRECISION2_PATTERN,
                'relative-switch-threshold-offset': PRECISION2_PATTERN,
                'force-to-port': r'NONE|PRIMARY|SECONDARY',
                'active-path': r'PRIMARY|SECONDARY',
                #'part-no': r'EDFA',
                'location': f'1-{slot}',
                'parent': f'LINECARD-1-{slot}-{port}',
                'subcomponents': f'PORT-1-{slot}-{port}-OLPSECOUT,PORT-1-{slot}-{port}-OLPSECIN,PORT-1-{slot}-{port}-OLPPRIOUT,PORT-1-{slot}-{port}-OLPCOMIN,PORT-1-{slot}-{port}-OLPCOMOUT,PORT-1-{slot}-{port}-OLPPRIIN',
                'empty': r'true|false',
                'removable': r'true|false',
            }
            table_name = "APS"
            key = f"APS-1-{slot}-{port}"

            if key_exist(slot, table_name, key):
                component_common_test(slot, table_name, key)
                component_special_test(slot, table_name, key, sobj)

def test_APS_PORT_attribute():
    for slot in range(1, 4):
        for port in range(1, 4):
            sobj= {
                'enabled': r'true|false',
                'target-attenuation': PRECISION2_PATTERN,
                'attenuation': PRECISION2_PATTERN,
            }
            table_name = "APS_PORT"
            key = f"APS-1-{slot}-{port}"
            if key_exist(slot, "APS", key):
                gauge_pm_float_precision2_test(slot, table_name, key, "LinePrimaryIn_OpticalPower")
                gauge_pm_float_precision2_test(slot, table_name, key, "LinePrimaryOut_OpticalPower")
                gauge_pm_float_precision2_test(slot, table_name, key, "LineSecondaryIn_OpticalPower")
                gauge_pm_float_precision2_test(slot, table_name, key, "LineSecondaryOut_OpticalPower")
                gauge_pm_float_precision2_test(slot, table_name, key, "CommonIn_OpticalPower")
                gauge_pm_float_precision2_test(slot, table_name, key, "CommonOutput_OpticalPower")