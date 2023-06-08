from dvslib.dvs_common import *

def test_psu_attribute():
    for id in range (5, 7):
        component_common_test(0, "PSU", f"PSU-1-{id}")
        sobj= {
            'capacity': r'\d+(\.\d+)?',
        }
        component_special_test(0, "PSU", f"PSU-1-{id}", sobj)
        
        gauge_pm_float_precision1_test(0, "PSU", f"PSU-1-{id}", "Temperature")
        gauge_pm_float_precision2_test(0, "PSU", f"PSU-1-{id}", "InputCurrent")
        gauge_pm_float_precision2_test(0, "PSU", f"PSU-1-{id}", "InputVoltage")
        gauge_pm_float_precision2_test(0, "PSU", f"PSU-1-{id}", "OutputCurrent")
        gauge_pm_float_precision2_test(0, "PSU", f"PSU-1-{id}", "OutputPower")
        gauge_pm_float_precision2_test(0, "PSU", f"PSU-1-{id}", "OutputVoltage")