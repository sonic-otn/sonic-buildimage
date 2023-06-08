from dvslib.dvs_common import *

def test_client_OTN_attribute():
    for id in range (GE_1_C1, GE_1_C4+1):
        sobj= {
            'index': r'\d+',
            'client-als': r'LASER_SHUTDOWN|ETHERNET',
            'als-delay': r'\d+',
        }
        slot= int(id/100)
        component_special_test(slot, "ETHERNET", f"CH{id}", sobj)  
        
        cntobj = {
            'in-mac-control-frames': r'\d+',
            'in-mac-pause-frames': r'\d+',
            'in-oversize-frames': r'\d+',
            'in-undersize-frames': r'\d+',
            'in-jabber-frames': r'\d+',
            'in-fragment-frames': r'\d+',
            'in-8021q-frames': r'\d+',
            'in-crc-errors': r'\d+',
            'in-block-errors': r'\d+',
            'out-mac-control-frames': r'\d+',
            'out-mac-pause-frames': r'\d+',
            'out-8021q-frames': r'\d+',
            'in-pcs-bip-errors': r'\d+',
            'in-pcs-errored-seconds': r'\d+',
            'in-pcs-severely-errored-seconds': r'\d+',
            'in-pcs-unavailable-seconds': r'\d+',
            'out-pcs-bip-errors': r'\d+',
            'out-crc-errors': r'\d+',
            'out-block-errors': r'\d+',
            'starttime': r'\d+',
            'validity': r'complete|incomplete|unavailable|invalid',
        }
        
        counter_pm_test(slot, "ETHERNET", f"CH{id}", cntobj)  

