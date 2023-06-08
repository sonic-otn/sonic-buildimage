from dvslib.dvs_common import *

def test_cu_attribute():
    component_common_test(0, "CU", "CU-1")
    sobj= {
        'memory-available': r'\d+',
        'memory-utilized': r'\d+',
        'software-version': r'\w+',
    }
    component_special_test(0, "CU", "CU-1", sobj)
    
    gauge_pm_float_precision1_test(0, "CU", "CU-1", "Temperature")
    gauge_pm_long_test(0, "CU", "CU-1", "Utilization")
