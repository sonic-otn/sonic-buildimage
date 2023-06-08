from dvslib.dvs_common import *

def test_ATTENUATOR_attribute():
    for slot in range (1, 4):
        for port in range (1, 4):
            sobj= {
                # 'target-output-power': PRECISION2_PATTERN,
                'attenuation': PRECISION2_PATTERN,
                'attenuation-mode': r'CONSTANT_POWER|CONSTANT_ATTENUATION',
                'enabled': r'true|false',
                'component': r'\w+',
                'ingress-port': r'PORT-1-[1-4]-[1-4]-VOAIN',
                'egress-port': r'PORT-1-[1-4]-[1-4]-VOAOUT',
            }

            table_name = "ATTENUATOR"
            key = f"ATTENUATOR-1-{slot}-{port}"
            if key_exist(slot, table_name, key):
                # component_common_test(slot, table_name, key)
                component_special_test(slot, table_name, key, sobj)
                gauge_pm_float_precision2_test(slot, table_name, key, "ActualAttenuation")
                gauge_pm_float_precision2_test(slot, table_name, key, "OutputPowerTotal")
                # gauge_pm_float_precision2_test(slot, table_name, key, "OpticalReturnLoss")
