from dvslib.dvs_common import *

def test_client_OTN_attribute():
    for id in range (ODU4_1_C1, ODU4_1_C4+1):
        sobj= {
            'index': r'\w+',
            'delay-measurement-enabled': r'true|false',
            'delay-measurement-mode': r'LOOPBACK|MEASURE',
        }
        slot= int(id/100)
        component_special_test(slot, "OTN", f"CH{id}", sobj)    

def test_line_OTN_attribute():
    for id in range (OTU_1_L1, OTU_1_L2+1):
        sobj= {
            'index': r'\w+',
            'tti-msg-transmit': r'\w+',
            'tti-msg-expected': r'\w+',
            'tti-msg-auto': r'true|false',
            'tti-msg-recv': r'\w+',
            'rdi-msg': r'\w+',
        }
        slot= int(id/100)
        
        component_special_test(slot, "OTN", f"CH{id}", sobj)
        
            
        gauge_pm_float_precision18_test(slot, "OTN", f"CH{id}", "PreFecBer")
        gauge_pm_float_precision18_test(slot, "OTN", f"CH{id}", "PostFecBer")
        
        gauge_pm_float_precision2_test(slot, "OTN", f"CH{id}", "Esnr")
        gauge_pm_float_precision2_test(slot, "OTN", f"CH{id}", "QValue")
        
        gauge_pm_long_test(slot, "OTN", f"CH{id}", "Delay")

        cntobj = {
            'errored-seconds ': r'\d+',
            'severely-errored-seconds ': r'\d+',
            'unavailable-seconds ': r'\d+',
            'code-violations': r'\d+',
            'errored-blocks': r'\d+',
            'fec-uncorrectable-blocks ': r'\d+',
            'fec-uncorrectable-words ': r'\d+',
            'fec-corrected-bytes ': r'\d+',
            'fec-corrected-bits ': r'\d+',
            'background-block-errors ': r'\d+',
            'sm-bip8': r'\d+',
            'sm-bei': r'\d+',
            'starttime': r'\d+',
            'validity': r'complete|incomplete|unavailable|invalid',
        }
        
        counter_pm_test(slot, "OTN", f"CH{id}", cntobj)
        
        
       




