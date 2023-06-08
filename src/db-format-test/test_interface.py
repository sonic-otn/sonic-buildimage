from dvslib.dvs_common import *

def test_client_interface_attribute():
    sobj= {
        'transceiver': r'\w+',
        'type': r'\w+',
        'hardware-port': r'\w+',
        'name': r'\w+',
    }
    
    cntobj = {
        'in-octets': r"\d+",
        'in-pkts': r"\d+",
        'in-unicast-pkts': r"\d+",
        'in-broadcast-pkts': r"\d+",
        'in-multicast-pkts': r"\d+",
        'in-discards': r"\d+",
        'in-errors': r"\d+",
        'in-unknown-protos': r"\d+",
        'in-fcs-errors': r"\d+",
        'out-octets': r"\d+",
        'out-pkts': r"\d+",
        'out-unicast-pkts': r"\d+",
        'out-broadcast-pkts': r"\d+",
        'out-multicast-pkts': r"\d+",
        'out-discards': r"\d+",
        'out-errors': r"\d+",
        'carrier-transitions': r"\d+",
        'last-clear': r"\d+",
        'in-mac-control-frames ': r"\d+",
        'in-mac-pause-frames ': r"\d+",
        'in-oversize-frames ': r"\d+",
        'in-undersize-frames ': r"\d+",
        'in-jabber-frames ': r"\d+",
        'in-fragment-frames ': r"\d+",
        'in-8021q-frames ': r"\d+",
        'in-crc-errors ': r"\d+",
        'in-block-errors ': r"\d+",
        'in-carrier-errors': r"\d+",
        'in-interrupted-tx': r"\d+",
        'in-late-collision': r"\d+",
        'in-mac-errors-rx': r"\d+",
        'in-single-collision': r"\d+",
        'in-symbol-error': r"\d+",
        'in-maxsize-exceeded': r"\d+",
        'out-mac-control-frames ': r"\d+",
        'out-mac-pause-frames ': r"\d+",
        'out-8021q-frames ': r"\d+",
        'out-mac-errors-tx ': r"\d+",
        'in-frames-64-octets': r"\d+",
        'in-frames-65-127-octets': r"\d+",
        'in-frames-128-255-octets': r"\d+",
        'in-frames-256-511-octets': r"\d+",
        'in-frames-512-1023-octets': r"\d+",
        'in-frames-1024-1518-octets': r"\d+",
        'starttime': r'\d+',
        'validity': r'complete|incomplete|unavailable|invalid',
    }
    
    for id in range (1, 2):
        for client in range (1, 2):      
            component_special_test(id, "INTERFACE", f"INTERFACE-1-{id}-C{client}", sobj)  
            counter_pm_test(id, "INTERFACE", f"INTERFACE-1-{id}-C{client}", cntobj)  

        for mgmt in range (1, 3):
            component_special_test(id, "INTERFACE", f"INTERFACE-1-{id}-MGMT{mgmt}", sobj)  
            counter_pm_test(id, "INTERFACE", f"INTERFACE-1-{id}-MGMT{mgmt}", cntobj)  
