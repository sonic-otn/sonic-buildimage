from dvslib.dvs_common import *

def test_client_OTN_attribute():
    for id in range (GE_1_C1, GE_1_C4+1):
        sobj= {
            'index': r'\d+',
            'enabled': r'true|false',
            'snooping': r'true|false',
        }
        slot= int(id/100)
        component_special_test(slot, "LLDP", f"CH{id}", sobj)  
        
        cntobj = {
            'frame-in': r'\d+',
            'frame-out': r'\d+',
            'frame-error-in': r'\d+',
            'frame-discard': r'\d+',
            'tlv-discard': r'\d+',
            'tlv-unknown': r'\d+',
            'last-clear': r'\d+',
            'frame-error-out': r'\d+',
            'starttime': r'\d+',
            'validity': r'complete|incomplete|unavailable|invalid',
        }
        
        counter_pm_test(slot, "LLDP", f"CH{id}", cntobj)  

