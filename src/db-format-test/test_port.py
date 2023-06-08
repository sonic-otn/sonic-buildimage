from dvslib.dvs_common import *

def test_CLIENT_TRANSCEIVER_attribute():
    for id in range (1, 2):
        for client in range (1, 2):  
            sobj= {
                'oper-status': r'ACTIVE|INACTIVE|DISABLE',
                'subcomponents': r'\w+',
            }
            component_special_test(id, "PORT", f"PORT-1-{id}-C{client}", sobj)
            

def test_LINE_TRANSCEIVER_attribute():
    for id in range (1, 2):
        for line in range (1, 2):  
            sobj= {
                'oper-status': r'ACTIVE|INACTIVE|DISABLE',
                'subcomponents': r'\w+',
            }
            component_special_test(id, "PORT", f"PORT-1-{id}-L{line}", sobj)
