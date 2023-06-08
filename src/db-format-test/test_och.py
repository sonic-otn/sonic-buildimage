from dvslib.dvs_common import *

def test_OCH_attribute():
    for id in range (1, 2):
        for line in range (1, 2):  
            sobj= {
                'operational-mode': r'\w+',
                'target-output-power': PRECISION2_PATTERN,
                'frequency': r'\d+',
                'line-port': r"\w+",
                'oper-status': r'ACTIVE|INACTIVE|DISABLE',
                'parent': r'\w+',
            }
            component_special_test(id, "OCH", f"OCH-1-{id}-L{line}", sobj)
            
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "InputPower")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "ChromaticDispersion")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "OutputPower")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "LaserBiasCurrent")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "PolarizationModeDispersion")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "SecondOrderPolarizationModeDispersion")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "Osnr")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "SopVectorS1")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "SopVectorS2")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "SopVectorS3")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "SopChangeRate")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "PolarizationDependentLoss")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "QMargin")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "InputSigPower")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "FreqOffset")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "Foff")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "Dgd")
            gauge_pm_float_precision2_test(id, "OCH", f"OCH-1-{id}-L{line}", "EdfaBiasCurrent")
            gauge_pm_long_test(id, "OCH", f"OCH-1-{id}-L{line}", "ActualFrequencyOffset")

            cntobj = {
                    'starttime': r'\d+',
                    'tx-laser-age': r'\d+',
                    'validity': r'complete|incomplete|unavailable|invalid',
            }
            counter_pm_test(id, "OCH", f"OCH-1-{id}-L{line}", cntobj)