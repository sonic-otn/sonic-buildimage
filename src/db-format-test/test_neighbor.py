from dvslib.dvs_common import *

def test_client_OTN_attribute():
    for id in range (GE_1_C1, GE_1_C4+1):
        sobj= {
            'id': r'\d+',
            'system-name': r"\w+",
            'system-description': r"\w+",
            'chassis-id': r"\w+",
            'chassis-id-type': r"\w+",
            'age': r'\d+',
            'last-update': r'\d+',
            'ttl': r'\d+',
            'port-id': r"\w+",
            'port-id-type': r"INTERFACE_ALIAS|INTERFACE_ALIAS|PORT_COMPONENT|MAC_ADDRESS|NETWORK_ADDRESS|INTERFACE_NAME|LOCAL",
            'port-description': r"\w+",
            'management-address': r"\w+",
            'management-address-type': r"\w+",
        }
        slot= int(id/100)
        component_special_test(slot, "NEIGHBOR", f"CH{id}|1", sobj)  
        
        

