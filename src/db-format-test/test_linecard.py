from dvslib.dvs_common import *

def test_LINECARD_attribute():
    for id in range (1, 2):
        component_common_test(id, "LINECARD", f"LINECARD-1-{id}")
        sobj= {
            'software-version': r"\w+",
            'board-mode': r"LA_400G_CA_200GE|L1_400G_CA_100GE|L2_400G_CA_100GE|LA_400G_RE_200GE|LA_400G_SNCP_CA_100GE|LA_400G_SNCP_C12_200GE|LA_400G_SNCP_C34_200GE|LA_400G_RE_100GE",
            'linecard-type': r'\w+',
            'power-admin-state': r'POWER_ENABLED|POWER_DISABLED',
            'subcomponents': r'\w+',
        }
        component_special_test(id, "LINECARD", f"LINECARD-1-{id}", sobj)
        
        gauge_pm_long_test(id, "LINECARD", f"LINECARD-1-{id}", "CpuUtilization")
        gauge_pm_long_test(id, "LINECARD", f"LINECARD-1-{id}", "MemoryUtilization")
        gauge_pm_long_test(id, "LINECARD", f"LINECARD-1-{id}", "MemoryAvailable")
        gauge_pm_float_precision1_test(id, "LINECARD", f"LINECARD-1-{id}", "Temperature")
