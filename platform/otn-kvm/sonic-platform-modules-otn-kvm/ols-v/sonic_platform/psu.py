#!/usr/bin/env python

########################################################################
# OTN-KVM
#
# Module contains an implementation of SONiC Platform Base API and
# provides the PSUs' information which are available in the platform
#
########################################################################


try:
    import os
    from sonic_platform_base.device_base import DeviceBase
    from sonic_platform_base.psu_base import PsuBase
    from sonic_platform.fan import Fan
    from HalPlatformApi.client import *
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class Psu(PsuBase):
    """OTN-KVM Platform-specific PSU class"""

    def __init__(self, desc):
        PsuBase.__init__(self)
        # PSU is 1-based in OTN-KVM platforms
        self.desc = desc
        self.name = desc['name']

        for item in desc['fans']:
            fan = Fan(item)
            self._fan_list.append(fan)

    def get_name(self):
        """
        Retrieves the name of the device

        Returns:
            string: The name of the device
        """

        return self.name

    def get_voltage(self):
        """
        Retrieves current PSU voltage output

        Returns:
            A float number, the output voltage in volts,
            e.g. 12.1
        """

        return PsuGetVoltage(self.name)

    def get_current(self):
        """
        Retrieves present electric current supplied by PSU

        Returns:
            A float number, electric current in amperes,
            e.g. 15.4
        """

        return PsuGetCurrent(self.name)

    def get_power(self):
        """
        Retrieves current energy supplied by PSU

        Returns:
            A float number, the power in watts,
            e.g. 302.6
        """

        return PsuGetPower(self.name)

    def get_powergood_status(self):
        """
        Retrieves the powergood status of PSU

        Returns:
            A boolean, True if PSU has stablized its output voltages and
            passed all its internal self-tests, False if not.
        """

        return PsuGetStatus(self.name)

    def set_status_led(self, color):
        """
        Sets the state of the PSU status LED
        Args:
            color: A string representing the color with which to set the
                   PSU status LED
        Returns:
            bool: True if status LED state is set successfully, False if
                  not
        """

        return PsuSetLedState(self.name, color)

    def get_status_led(self):
        """
        Gets the state of the PSU status LED

        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings.
        """

        return PsuGetLedState(self.name)

    def get_temperature(self):
        """
        Retrieves current temperature reading from PSU

        Returns:
            A float number of current temperature in Celsius up to
            nearest thousandth of one degree Celsius, e.g. 30.125
        """

        return PsuGetTemp(self.name)

    def get_temperature_high_threshold(self):
        """
        Retrieves the high threshold temperature of PSU

        Returns:
            A float number, the high threshold temperature of PSU in
            Celsius up to nearest thousandth of one degree Celsius,
            e.g. 30.125
        """
        return 90.0

    def get_voltage_high_threshold(self):
        """
        Retrieves the high threshold PSU voltage output

        Returns:
            A float number, the high threshold output voltage in volts,
            e.g. 12.1
        """
        voltage_high_threshold = 12.5

        return voltage_high_threshold

    def get_voltage_low_threshold(self):
        """
        Retrieves the low threshold PSU voltage output

        Returns:
            A float number, the low threshold output voltage in volts,
            e.g. 12.1
        """
        voltage_low_threshold = 11.5

        return voltage_low_threshold

    def get_maximum_supplied_power(self):
        """
        Retrieves the maximum supplied power by PSU

        Returns:
            A float number, the maximum power output in Watts.
            e.g. 1200.1
        """
        psu_maxpower = 120.0

        return psu_maxpower

    def get_psu_power_warning_suppress_threshold(self):
        """
        Retrieve the warning suppress threshold of the power on this PSU
        The value can be volatile, so the caller should call the API each time it is used.

        Returns:
            A float number, the warning suppress threshold of the PSU in watts.
        """
        return 120.0

    def get_psu_power_critical_threshold(self):
        """
        Retrieve the critical threshold of the power on this PSU
        The value can be volatile, so the caller should call the API each time it is used.

        Returns:
            A float number, the critical threshold of the PSU in watts.
        """
        return 120.0

    def get_input_voltage(self):
        """
        Retrieves current PSU voltage input

        Returns:
            A float number, the input voltage in volts,
            e.g. 12.1
        """

        return PsuGetInputVoltage(self.name)

    def get_input_current(self):
        """
        Retrieves the input current draw of the power supply

        Returns:
            A float number, the electric current in amperes, e.g 15.4
        """

        return PsuGetInputCurrent(self.name)

    def get_presence(self):
        """
        Retrieves the presence of the Power Supply Unit (PSU)

        Returns:
            bool: True if PSU is present, False if not
        """

        return PsuGetPresence(self.name)

    def get_model(self):
        """
        Retrieves the part number of the PSU

        Returns:
            string: Part number of PSU
        """

        return PsuGetModel(self.name)

    def get_serial(self):
        """
        Retrieves the serial number of the PSU

        Returns:
            string: Serial number of PSU
        """

        return PsuGetSerial(self.name)

    def get_revision(self):
        """
        Retrieves the hardware revision of the device

        Returns:
            string: Revision value of device
        """

        return PsuGetRevision(self.name)

    def is_replaceable(self):
        """
        Indicate whether this device is replaceable.
        Returns:
            bool: True if it is replaceable.
        """
        return PsuIsReplaceable(self.name)
