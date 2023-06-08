from dvslib.dvs_common import *

def test_CLIENT_TRANSCEIVER_attribute():
    for id in range (1, 2):
        for client in range (1, 2):  
            component_common_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}")
            sobj= {
                'vendor': r'\w+',
                # 'vendor-expect': r'\w+',
                'vendor-rev': r'\w+',
                'date-code': r'\w+',
                'vendor-part': r'\w+',
                'fec-mode': r'FEC_ENABLED|FEC_DISABLED|FEC_AUTO',
                'form-factor': r'CFP|CFP2|CFP2_ACO|CFP4|QSFP|QSFP_PLUS|QSFP28|QSFP56_DD_TYPE1|QSFP56_DD_TYPE2|CPAK|SFP|SFP_PLUS|XFP|X2|OSFP|NON_PLUGGABLE|OTHER',
                'ethernet-pmd': r'ETH_100G_AOC|ETH_100G_ACC|ETH_100GBASE_SR10|ETH_100GBASE_SR4|ETH_100GBASE_LR4|ETH_100GBASE_ER4|ETH_100GBASE_CWDM4|ETH_100GBASE_CLR4|ETH_100GBASE_PSM4|ETH_100GBASE_CR4|ETH_100GBASE_FR|ETH_400GBASE_ZR|ETH_400GBASE_LR4|ETH_400GBASE_FR4|ETH_400GBASE_LR8|ETH_400GBASE_DR4|ETH_UNDEFINED|ETH_AUTO|ETH_100GBASE_4WDM10',
                'present': r'PRESENT|NOT_PRESENT',
                'enabled': r'true|false',
                'fault-condition': r'true|false',
                'connector-type': r'SC_CONNECTOR|LC_CONNECTOR|MPO_CONNECTOR|AOC_CONNECTOR|DAC_CONNECTOR',
                'firmware-version': r"\w+",
                'oui': r"\w+",
                'rn': r"\w+",
                'identifier': r"\w+",
                'cmis-revision': r"\w+",
                'wavelength': PRECISION2_PATTERN,
                'wavelength-tolerance': PRECISION2_PATTERN,
                'extend-module-code': r'SDR|DDR|QDR|FDR|EDR',
                'data-status': r'NOT_READY|READY',
                'encode': r'UNSPECIFIED|8B_10B|4B_5B|NRZ|SONET_SCRAMBLED|64B_66B|MANCH-ESTER|256B_257B|PAM4',
                'bitrate': PRECISION2_PATTERN,
                'extend-bit-rate': PRECISION2_PATTERN,
            }
            component_special_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}", sobj)
            
            gauge_pm_float_precision1_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}", "Temperature")
            
            gauge_pm_float_precision18_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}", "PreFecBer")
            gauge_pm_float_precision18_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}", "PostFecBer")
            
            gauge_pm_float_precision2_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}", "InputPower")
            gauge_pm_float_precision2_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}", "OutputPower")
            gauge_pm_float_precision2_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}", "LaserBiasCurrent")
            
            cntobj = {
                    'starttime': r'\d+',
                    'fec-corrected-bits': r'\d+',
                    'fec-uncorrectable-blocks': r'\d+',
                    'fec-corrected-bytes': r'\d+',
                    'fec-uncorrectable-words': r'\d+',
                    'validity': r'complete|incomplete|unavailable|invalid',
            }
            counter_pm_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}", cntobj)
            
            for ch in range (1, 5):
                cobj = {
                    'output-frequency': r'\d+',
                    'tx-laser': r'true|false',
                }
                component_special_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}|CH-{ch}", cobj)

                gauge_pm_float_precision2_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}:CH-{ch}", "InputPower")
                gauge_pm_float_precision2_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}:CH-{ch}", "OutputPower")
                gauge_pm_float_precision2_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-C{client}:CH-{ch}", "LaserBiasCurrent")



def test_LINE_TRANSCEIVER_attribute():
    for id in range (1, 2):
        for line in range (1, 2):  
            component_common_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-L{line}")
            sobj= {
                'vendor': r'\w+',
                # 'vendor-expect': r'\w+',
                'vendor-rev': r'\w+',
                'date-code': r'\w+',
                'vendor-part': r'\w+',
                'fec-mode': r'FEC_ENABLED|FEC_DISABLED|FEC_AUTO',
                'form-factor': r'CFP|CFP2|CFP2_ACO|CFP4|QSFP|QSFP_PLUS|QSFP28|QSFP56_DD_TYPE1|QSFP56_DD_TYPE2|CPAK|SFP|SFP_PLUS|XFP|X2|OSFP|NON_PLUGGABLE|OTHER',
                'ethernet-pmd': r'ETH_100G_AOC|ETH_100G_ACC|ETH_100GBASE_SR10|ETH_100GBASE_SR4|ETH_100GBASE_LR4|ETH_100GBASE_ER4|ETH_100GBASE_CWDM4|ETH_100GBASE_CLR4|ETH_100GBASE_PSM4|ETH_100GBASE_CR4|ETH_100GBASE_FR|ETH_400GBASE_ZR|ETH_400GBASE_LR4|ETH_400GBASE_FR4|ETH_400GBASE_LR8|ETH_400GBASE_DR4|ETH_UNDEFINED|ETH_AUTO|ETH_100GBASE_4WDM10',
                'present': r'PRESENT|NOT_PRESENT',
                'enabled': r'true|false',
                'fault-condition': r'true|false',
                'connector-type': r'SC_CONNECTOR|LC_CONNECTOR|MPO_CONNECTOR|AOC_CONNECTOR|DAC_CONNECTOR',
                'firmware-version': r"\w+",
                
                'laser-age': r'\d+',
                'operate-time': r'\d+',
                'lot-code': r"\w+",
                'clei-code': r"\w+",
                'power-class': r'BELOW_9W|BELOW_12W|BELOW_15W|ABOVE_15W',
                'newwork-bit-rate': PRECISION2_PATTERN,
                'host-bit-rate': PRECISION2_PATTERN,
                'sm-fiber-len': PRECISION2_PATTERN,
                'mm-fiber-len': PRECISION2_PATTERN,
                'copper-cable-len': PRECISION2_PATTERN,
                'max-wavelength': PRECISION2_PATTERN,
                'min-wavelength': PRECISION2_PATTERN,
                'max-tx-power': PRECISION2_PATTERN,
                'max-rx-power': PRECISION2_PATTERN,
                'max-oper-temp': PRECISION2_PATTERN,
                'min-oper-temp': PRECISION2_PATTERN,
                'vcc-high-alarm-threshold': PRECISION2_PATTERN,
                'vcc-high-warn-threshold': PRECISION2_PATTERN,
                'vcc-low-alarm-threshold': PRECISION2_PATTERN,
                'vcc-low-warn-threshold': PRECISION2_PATTERN,
                'rx-total-power-high-alarm-threshold': PRECISION2_PATTERN,
                'rx-total-power-high-warn-threshold': PRECISION2_PATTERN,
                'rx-total-power-low-alarm-threshold': PRECISION2_PATTERN,
                'rx-total-power-high-alarm-threshold': PRECISION2_PATTERN,
                'oa-pump-current-high-alarm-threshold': PRECISION2_PATTERN,
                'oa-pump-current-high-warn-threshold': PRECISION2_PATTERN,
                'oa-pump-current-low-alarm-threshold': PRECISION2_PATTERN,
                'oa-pump-current-low-warn-threshold': PRECISION2_PATTERN,
                'tx-bais-high-alarm-threshold': PRECISION2_PATTERN,
                'tx-bais-high-warn-threshold': PRECISION2_PATTERN,
                'tx-bais-low-alarm-threshold': PRECISION2_PATTERN,
                'tx-bais-low-warn-threshold': PRECISION2_PATTERN,
            }
            component_special_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-L{line}", sobj)
            
            gauge_pm_float_precision1_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-L{line}", "Temperature")
            gauge_pm_float_precision2_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-L{line}", "InputPower")
            gauge_pm_float_precision2_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-L{line}", "OutputPower")
            gauge_pm_float_precision2_test(id, "TRANSCEIVER", f"TRANSCEIVER-1-{id}-L{line}", "LaserBiasCurrent")
