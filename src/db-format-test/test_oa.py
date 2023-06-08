from dvslib.dvs_common import *

def test_AMPLIFIER_attribute():
    for slot in range (1, 4):
        for port in range (1, 4):
            sobj= {
                'type': r'EDFA|FORWARD_RAMAN|BACKWARD_RAMAN|HYBRID',
                'target-gain': PRECISION2_PATTERN,
                'min-gain': PRECISION2_PATTERN,
                'max-gain': PRECISION2_PATTERN,
                'target-gain-tilt': PRECISION2_PATTERN,
                #'target-output-power': PRECISION2_PATTERN,
                'max-output-power': PRECISION2_PATTERN,
                #'ingress-voa-atten': PRECISION2_PATTERN,
                'gain-range': r'LOW_GAIN_RANGE|MID_GAIN_RANGE|HIGH_GAIN_RANGE|FIXED_GAIN_RANGE',
                'amp-mode': r'CONSTANT_GAIN|CONSTANT_POWER|DYNAMIC_GAIN',
                'fiber-type-profile': r'DSF|LEAF|SSMF|TWC|TWRS',
                'enabled': r'true|false',
                'component': f'AMPLIFIER-1-{slot}-{port}',
                'ingress-port': f'PORT-1-{slot}-{port}-EDFAIN',
                'egress-port': f'PORT-1-{slot}-{port}-EDFAOUT',
                'part-no': r'EDFA-',
                'location': f'1-{slot}',
                'parent': f'LINECARD-1-{slot}',
                'subcomponents': f'PORT-1-{slot}-{port}-EDFAIN,PORT-1-{slot}-{port}-EDFAOUT',
                'empty': r'true|false',
                'removable': r'true|false',
                'input-los-threshold': PRECISION2_PATTERN,
                'input-los-hysteresis': PRECISION2_PATTERN,
                'output-los-threshold': PRECISION2_PATTERN,
                'output-los-hysteresis': PRECISION2_PATTERN,
                'gain-low-threshold': PRECISION2_PATTERN,
                'gain-low-hysteresis': PRECISION2_PATTERN,
                'los-ase-delay': r'\w+',
            }

            table_name = "AMPLIFIER"
            key = f"AMPLIFIER-1-{slot}-{port}"

            if key_exist(slot, table_name, key):
                component_common_test(slot, table_name, key)
                component_special_test(slot, table_name, key, sobj)
                gauge_pm_float_precision2_test(slot, table_name, key, "ActualGain")
                gauge_pm_float_precision2_test(slot, table_name, key, "ActualGainTilt")
                gauge_pm_float_precision2_test(slot, table_name, key, "InputPowerTotal")
                #gauge_pm_float_precision2_test(slot, table_name, key, "InputPowerCBand")
                #gauge_pm_float_precision2_test(slot, table_name, key, "InputPowerLBand")
                #gauge_pm_float_precision2_test(slot, table_name, key, "OutputPowerCBand")
                #gauge_pm_float_precision2_test(slot, table_name, key, "OutputPowerLBand")
                gauge_pm_float_precision2_test(slot, table_name, key, "LaserBiasCurrent")
                #gauge_pm_float_precision2_test(slot, table_name, key, "OpticalReturnLoss")
                gauge_pm_float_precision1_test(slot, table_name, key, "Temperature")


def test_OSC_attribute():
    for slot in range(1, 4):
        for port in range(1, 4):
            sobj= {
                'interface': f'INTERFACE-1-{slot}-{port}-OSC',
                'output-frequency': r'\d+',
            }

            table_name = "OSC"
            key = f"OSC-1-{slot}-{port}"

            if key_exist(slot, table_name, key):
                component_common_test(slot, table_name, key)
                component_special_test(slot, table_name, key, sobj)
                gauge_pm_float_precision2_test(slot, table_name, key, "InputPower")
                gauge_pm_float_precision2_test(slot, table_name, key, "OutputPower")
                gauge_pm_float_precision2_test(slot, table_name, key, "LaserBiasCurrent")
                gauge_pm_float_precision1_test(slot, table_name, key, "Temperature")
