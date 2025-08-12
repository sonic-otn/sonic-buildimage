#!/usr/bin/env python

########################################################################
# OTN-KVM
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Fan-Drawers' information available in the platform.
#
########################################################################

try:
    import os
    from sonic_platform_base.device_base import DeviceBase
    from sonic_platform_base.fan_drawer_base import FanDrawerBase
    from sonic_platform.fan import Fan
    from HalPlatformApi.client import *
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class FanDrawer(FanDrawerBase):
    """OTN-KVM Platform-specific Fan Drawer class"""

    def __init__(self, desc):
        FanDrawerBase.__init__(self)

        self.desc = desc
        self.name = desc['name']

        for item in desc['fans']:
            fan = Fan(item)
            self._fan_list.append(fan)


    def set_status_led(self, color):
        """
        Set led to expected color
        Args:
            color: A string representing the color with which to set the
                   fan module status LED
        Returns:
            bool: True if set success, False if fail.
        """
        # Leds are controlled by Smart-fussion FPGA.
        # Return True to avoid thermalctld alarm.
        return FanDrawerSetLedState(self.name, color)

    def get_status_led(self):
        """
        Gets the state of the Fan status LED

        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings.
        """
        return FanDrawerGetLedState(self.name)

    def get_maximum_consumed_power(self):
        """
        Retrives the maximum power drawn by Fan Drawer

        Returns:
            A float, with value of the maximum consumable power of the
            component.
        """
        return None

    def get_name(self):
        """
        Retrieves the fan name
        Returns:
            string: The name of the device
        """
        return self.name
