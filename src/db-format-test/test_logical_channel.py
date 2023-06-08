from dvslib.dvs_common import *

def test_LOGICAL_CHANNEL_attribute():
    for id in range (GE_1_C1, GE_1_C4):
        sobj= {  
            'description': r'\w+',
            'admin-state': r'ENABLED|DISABLED|MAINT',
            'rate-class': r'TRIB_RATE_100G|TRIB_RATE_150G|TRIB_RATE_200G|TRIB_RATE_250G|TRIB_RATE_300G|TRIB_RATE_350G|TRIB_RATE_400G|TRIB_RATE_450G|TRIB_RATE_500G|TRIB_RATE_550G|TRIB_RATE_600G',
            'trib-protocol': r'PROT_100GE|PROT_100G_MLG|PROT_OTU4|PROT_OTUCN|PROT_ODUCN|PROT_ODU4|PROT_400GE|PROT_OTSIG|PROT_ODUFLEX_CBR|PROT_ODUFLEX_GFP',
            'logical-channel-type': r'PROT_ETHERNET|PROT_OTN',
            'loopback-mode': r'FACILITY|TERMINAL|NONE',
            'test-signal': r'true|false',
            'link-state': r'UP|DOWN|TESTING',
            'transceiver': r'\w+',
        }
        slot= int(id/100)
        component_special_test(slot, "LOGICAL_CHANNEL", f"CH{id}", sobj)