from dvslib.dvs_common import *

def test_chassis_attribute():
    component_common_test(0, "CHASSIS", "CHASSIS-1")
    sobj= {
        'software-version': r'\w+',
        'subcomponents': r'\w+',
    }
    component_special_test(0, "CHASSIS", "CHASSIS-1", sobj)
    
    gauge_pm_float_precision1_test(0, "CHASSIS", "CHASSIS-1", "Temperature")
