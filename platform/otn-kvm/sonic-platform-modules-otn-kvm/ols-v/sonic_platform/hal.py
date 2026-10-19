#!/usr/bin/env python

#############################################################################
# OTN-KVM
#
# Native, in-process platform HAL driver.
#
# This replaces the previous thrift-based client (HalPlatformApi.client) that
# RPC'd to a HalPlatformApiServer running in the syncd container. For the
# virtual OTN-KVM platform there is no real hardware, so the driver simply
# keeps per-device state in memory and returns simulated values. All calls run
# in-process inside whatever daemon (pmon) imported it -- no thrift, no syncd
# server, no sockets.
#
# The public function surface (Chassis*/Psu*/Fan*/FanDrawer*/Thermal*/Module*/
# Component*/Led*/WatchDog*/Initialize/Destroy) is API-compatible with the old
# HalPlatformApi.client module, so sonic_platform classes only need to change
# their import.
#############################################################################

import re

# sonic_platform_base LED color strings.
LED_OFF = "off"
LED_RED = "red"
LED_GREEN = "green"
LED_AMBER = "amber"

# Fan airflow directions (sonic_platform_base.fan_base.FanBase).
FAN_DIRECTION_INTAKE = "intake"
FAN_DIRECTION_EXHAUST = "exhaust"

# Module types / statuses (sonic_platform_base.module_base.ModuleBase).
MODULE_TYPE_LINE = "LINE-CARD"
MODULE_STATUS_ONLINE = "Online"


# ---------------------------------------------------------------------------
# In-memory device registries. Each entry is lazily created with simulated
# defaults on first access, and mutated in place by the Set* calls so writes
# persist for the lifetime of the process.
# ---------------------------------------------------------------------------
_chassis = None
_psus = {}
_fans = {}
_fan_drawers = {}
_thermals = {}
_modules = {}
_components = {}
_leds = {}
_watchdogs = {}


def _index_from_name(name):
    """Best-effort 0-based index parsed from the trailing number in a name."""
    if not name:
        return 0
    m = re.findall(r'(\d+)', str(name))
    return int(m[-1]) if m else 0


def Initialize():
    """Initialize the driver. No external resource to open; always succeeds."""
    return True


def Destroy():
    """Release all simulated device state."""
    global _chassis
    _chassis = None
    _psus.clear()
    _fans.clear()
    _fan_drawers.clear()
    _thermals.clear()
    _modules.clear()
    _components.clear()
    _leds.clear()
    _watchdogs.clear()


# ---------------------------------------------------------------------------
# Default factories (mirror the previous HalPlatformApiServer virtual_device.h)
# ---------------------------------------------------------------------------
def _get_chassis():
    global _chassis
    if _chassis is None:
        _chassis = {
            "name": "ot-kvm-chassis",
            "model": "KVM-1234",
            "serial": "123456789",
            "revision": "1.0",
            "base_mac": "00:1A:2B:3C:4D:5E",
            "slot": 0,
            "led": LED_GREEN,
            "modular": False,
            "list": "null",
        }
    return _chassis


def _get_psu(name):
    d = _psus.get(name)
    if d is None:
        d = {
            "model": "PSU Model",
            "serial": "123456789",
            "revision": "1.0",
            "presence": True,
            "status": True,
            "replaceable": True,
            "voltage": 12.0,
            "current": 1.5,
            "power": 18.0,
            "temperature": 40.0,
            "input_voltage": 12.0,
            "input_current": 1.6,
            "led": LED_GREEN,
        }
        _psus[name] = d
    return d


def _get_fan(name):
    d = _fans.get(name)
    if d is None:
        d = {
            "model": "Fan Model",
            "serial": "123456789",
            "revision": "1.0",
            "presence": True,
            "status": True,
            "replaceable": True,
            "direction": FAN_DIRECTION_INTAKE,
            "speed": 50,
            "target_speed": 50,
            "tolerance": 10,
            "led": LED_GREEN,
        }
        _fans[name] = d
    return d


def _get_fan_drawer(name):
    d = _fan_drawers.get(name)
    if d is None:
        d = {"presence": True, "status": True, "replaceable": True, "led": LED_GREEN}
        _fan_drawers[name] = d
    return d


def _get_thermal(name):
    d = _thermals.get(name)
    if d is None:
        d = {
            "temperature": 35.0,
            "high_threshold": 70.0,
            "low_threshold": 10.0,
            "high_critical": 90.0,
            "low_critical": 5.0,
            "min_recorded": 25.0,
            "max_recorded": 45.0,
        }
        _thermals[name] = d
    return d


def _get_module(name):
    d = _modules.get(name)
    if d is None:
        d = {
            "model": "OTN Module",
            "serial": "123456789",
            "revision": "1.0",
            "base_mac": "00:1A:2B:3C:4D:5E",
            "slot": _index_from_name(name),
            "type": MODULE_TYPE_LINE,
            "status": MODULE_STATUS_ONLINE,
            "temperature": 42.0,
            "led": LED_GREEN,
        }
        _modules[name] = d
    return d


def _get_led(name):
    d = _leds.get(name)
    if d is None:
        d = {"state": LED_OFF}
        _leds[name] = d
    return d


def _get_watchdog(index):
    d = _watchdogs.get(index)
    if d is None:
        d = {"armed": False, "timeout": 60}
        _watchdogs[index] = d
    return d


# ---------------------------------------------------------------------------
# PSU
# ---------------------------------------------------------------------------
def PsuGetModel(name):
    return _get_psu(name)["model"]


def PsuGetSerial(name):
    return _get_psu(name)["serial"]


def PsuGetRevision(name):
    return _get_psu(name)["revision"]


def PsuGetPresence(name):
    return _get_psu(name)["presence"]


def PsuGetStatus(name):
    return _get_psu(name)["status"]


def PsuIsReplaceable(name):
    return _get_psu(name)["replaceable"]


def PsuGetVoltage(name):
    return _get_psu(name)["voltage"]


def PsuGetCurrent(name):
    return _get_psu(name)["current"]


def PsuGetPower(name):
    return _get_psu(name)["power"]


def PsuGetTemp(name):
    return _get_psu(name)["temperature"]


def PsuGetInputVoltage(name):
    return _get_psu(name)["input_voltage"]


def PsuGetInputCurrent(name):
    return _get_psu(name)["input_current"]


def PsuGetLedState(name):
    return _get_psu(name)["led"]


def PsuSetLedState(name, color):
    _get_psu(name)["led"] = color
    return True


# ---------------------------------------------------------------------------
# FAN
# ---------------------------------------------------------------------------
def FanGetModel(name):
    return _get_fan(name)["model"]


def FanGetSerial(name):
    return _get_fan(name)["serial"]


def FanGetRevision(name):
    return _get_fan(name)["revision"]


def FanGetPresence(name):
    return _get_fan(name)["presence"]


def FanGetStatus(name):
    return _get_fan(name)["status"]


def FanIsReplaceable(name):
    return _get_fan(name)["replaceable"]


def FanGetDirection(name):
    return _get_fan(name)["direction"]


def FanGetSpeed(name):
    return _get_fan(name)["speed"]


def FanGetTargetSpeed(name):
    return _get_fan(name)["target_speed"]


def FanGetSpeedTolerance(name):
    return _get_fan(name)["tolerance"]


def FanSetSpeed(name, speed):
    d = _get_fan(name)
    d["speed"] = speed
    d["target_speed"] = speed
    return True


def FanGetLedState(name):
    return _get_fan(name)["led"]


def FanSetLedState(name, color):
    _get_fan(name)["led"] = color
    return True


def FanGetPositionInParent(name):
    return _index_from_name(name) + 1


# ---------------------------------------------------------------------------
# FAN Drawer
# ---------------------------------------------------------------------------
def FanDrawerGetPresence(name):
    return _get_fan_drawer(name)["presence"]


def FanDrawerGetStatus(name):
    return _get_fan_drawer(name)["status"]


def FanDrawerIsReplaceable(name):
    return _get_fan_drawer(name)["replaceable"]


def FanDrawerGetLedState(name):
    return _get_fan_drawer(name)["led"]


def FanDrawerSetLedState(name, color):
    _get_fan_drawer(name)["led"] = color
    return True


# ---------------------------------------------------------------------------
# LED
# ---------------------------------------------------------------------------
def LedGetState(name):
    return _get_led(name)["state"]


def LedSetState(name, state):
    _get_led(name)["state"] = state
    return True


# ---------------------------------------------------------------------------
# THERMAL
# ---------------------------------------------------------------------------
def ThermalGetTemp(name):
    return _get_thermal(name)["temperature"]


def ThermalGetHighThreshold(name):
    return _get_thermal(name)["high_threshold"]


def ThermalGetLowThreshold(name):
    return _get_thermal(name)["low_threshold"]


def ThermalSetHighThreshold(name, temperature):
    _get_thermal(name)["high_threshold"] = temperature
    return True


def ThermalSetLowThreshold(name, temperature):
    _get_thermal(name)["low_threshold"] = temperature
    return True


def ThermalGetHighCriticalThreshold(name):
    return _get_thermal(name)["high_critical"]


def ThermalGetLowCriticalThreshold(name):
    return _get_thermal(name)["low_critical"]


def ThermalSetHighCriticalThreshold(name, temperature):
    _get_thermal(name)["high_critical"] = temperature
    return True


def ThermalSetLowCriticalThreshold(name, temperature):
    _get_thermal(name)["low_critical"] = temperature
    return True


def ThermalGetMinimumRecorded(name):
    return _get_thermal(name)["min_recorded"]


def ThermalGetMaximumRecorded(name):
    return _get_thermal(name)["max_recorded"]


# ---------------------------------------------------------------------------
# Watchdog
# ---------------------------------------------------------------------------
def WatchDogArm(index, seconds):
    d = _get_watchdog(index)
    d["armed"] = True
    d["timeout"] = seconds
    return True


def WatchDogDisrm(index):
    _get_watchdog(index)["armed"] = False
    return True


def WatchDogIsArmed(index):
    return _get_watchdog(index)["armed"]


# ---------------------------------------------------------------------------
# Chassis
# ---------------------------------------------------------------------------
def ChassisGetName():
    return _get_chassis()["name"]


def ChassisGetModel():
    return _get_chassis()["model"]


def ChassisGetSerial():
    return _get_chassis()["serial"]


def ChassisGetRevision():
    return _get_chassis()["revision"]


def ChassisGetBaseMac():
    return _get_chassis()["base_mac"]


def ChassisGetSlot():
    return _get_chassis()["slot"]


def ChassisGetLedState():
    return _get_chassis()["led"]


def ChassisSetLedState(color):
    _get_chassis()["led"] = color
    return True


def ChassisGetList():
    return _get_chassis()["list"]


def ChassisIsModular():
    return _get_chassis()["modular"]


# ---------------------------------------------------------------------------
# Module
# ---------------------------------------------------------------------------
def ModuleGetModel(name):
    return _get_module(name)["model"]


def ModuleGetSerial(name):
    return _get_module(name)["serial"]


def ModuleGetRevision(name):
    return _get_module(name)["revision"]


def ModuleGetBaseMac(name):
    return _get_module(name)["base_mac"]


def ModuleGetSlot(name):
    return _get_module(name)["slot"]


def ModuleGetType(name):
    return _get_module(name)["type"]


def ModuleGetStatus(name):
    return _get_module(name)["status"]


def ModuleGetTemp(name):
    return _get_module(name)["temperature"]


def ModuleGetLedState(name):
    return _get_module(name)["led"]


def ModuleSetLedState(name, color):
    _get_module(name)["led"] = color
    return True


# ---------------------------------------------------------------------------
# Component
# ---------------------------------------------------------------------------
def ComponentGetFwVer(name):
    return _components.get(name, "1.0")
