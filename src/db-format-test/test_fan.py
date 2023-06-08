from dvslib.dvs_common import *

def test_fan_attribute():
    for fan_id in range (7, 12):
        component_common_test(0, "FAN", f"FAN-1-{fan_id}")
        
        gauge_pm_float_precision1_test(0, "FAN", f"FAN-1-{fan_id}", "Temperature")
        gauge_pm_long_test(0, "FAN", f"FAN-1-{fan_id}", "Speed")

