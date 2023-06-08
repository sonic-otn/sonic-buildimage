"""Common infrastructure for writing VS tests."""

import time
import redis
import re
import os
from datetime import datetime, timedelta
import pytest_check as check
from pytest_check import check_func

from dataclasses import dataclass
from typing import Any, Callable, Tuple
from swsscommon import swsscommon

PRECISION18_PATTERN = r'^(-)?[0-9]*(\.[0-9]{1,18})?$'
PRECISION2_PATTERN = r'^(-)?[0-9]*(\.[0-9]{1,2})?$'
PRECISION1_PATTERN = r'^(-)?[0-9]*(\.[0-9]{1})?$'

GE_1_C1=101
GE_1_C2=102
GE_1_C3=103
GE_1_C4=104
# ODU_1_L1=113
# ODU_1_L2=114
OTU_1_L1=115
OTU_1_L2=116
ODU4_1_C1=117
ODU4_1_C2=118
ODU4_1_C3=119
ODU4_1_C4=120

@dataclass
class PollingConfig:
    """Class containing parameters that are used to control polling behavior.

    Attributes:
        polling_interval: How often to poll, in seconds.
        timeout: The maximum amount of time to wait, in seconds.
        strict: If the strict flag is set, reaching the timeout will cause tests to fail.
    """

    polling_interval: float = 0.01
    timeout: float = 5.00
    strict: bool = True

    def iterations(self) -> int:
        """Return the number of iterations needed to poll with the given interval and timeout."""
        return 1 if self.polling_interval == 0 else int(self.timeout // self.polling_interval) + 1


def wait_for_result(
    polling_function: Callable[[], Tuple[bool, Any]],
    polling_config: PollingConfig = PollingConfig(),
    failure_message: str = None,
) -> Tuple[bool, Any]:
    """Run `polling_function` periodically using the specified `polling_config`.

    Args:
        polling_function: The function being polled. The function cannot take any arguments and
            must return a status which indicates if the function was succesful or not, as well as
            some return value.
        polling_config: The parameters to use to poll the polling function.
        failure_message: The message to print if the call times out. This will only take effect
            if the PollingConfig is set to strict.

    Returns:
        If the polling function succeeds, then this method will return True and the output of the
        polling function.

        If it does not succeed within the provided timeout, it will return False and whatever the
        output of the polling function was on the final attempt.
    """
    for _ in range(polling_config.iterations()):
        status, result = polling_function()

        if status:
            return (True, result)

        time.sleep(polling_config.polling_interval)

    if polling_config.strict:
        message = failure_message or f"Operation timed out after {polling_config.timeout} seconds"
        assert False, message

    return (False, result)

@check_func
def check_object(db, table, key, expected_attributes):
    found = 0
    tbl =  swsscommon.Table(db, table)
    keys = tbl.getKeys()
    check.is_in(key, keys, f"[Missing]: The desired {key} is not presented in talbe {table}")
    if key not in keys:
        return
    
    status, fvs = tbl.get(key)
    assert status, f"Got an error when get a {key}"
    data = dict(fvs)
    
    for name in expected_attributes:
        check.is_in(name, data.keys(), f"[Missing]: {name} in not in table {table} key {key} ")
        if name in data.keys():
            check.is_not_none(re.match(expected_attributes[name], data[name]), 
                f"[Wrong value]: {data[name]} for the attribute {name} in table {table} key {key}, expect format is {expected_attributes[name]}")
            

def get_port_type_id(table, port_type_attr, port_id_attr):
    asic_r = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=swsscommon.ASIC_DB,
                         encoding="utf-8", decode_responses=True)
    port_type = asic_r.hget(table, port_type_attr)
    port_id = asic_r.hget(table, port_id_attr)
    if (port_type == "LAI_PORT_TYPE_LINE"):
        port_type = "L" 
    else:
        port_type = "C" 
    return port_type, port_id

def get_port_lane_id(table, port_type_attr, port_id_attr, lane_id_attr):
    asic_r = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=swsscommon.ASIC_DB,
                         encoding="utf-8", decode_responses=True)
    port_type = asic_r.hget(table, port_type_attr)
    port_id = asic_r.hget(table, port_id_attr)
    lane_id = asic_r.hget(table, lane_id_attr)

    if (port_type == "LAI_PORT_TYPE_LINE"):
        port_type = "L" 
    else:
        port_type = "C" 

    return port_type, port_id, lane_id

def get_channel_id(table, channel_id_attr):
    asic_r = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=swsscommon.ASIC_DB,
                         encoding="utf-8", decode_responses=True)
    channel_id = asic_r.hget(table, channel_id_attr)
    return channel_id

def create_entry(tbl, key, pairs):
    fvs = swsscommon.FieldValuePairs(pairs)
    tbl.set(key, fvs)
    time.sleep(1)

def get_exist_entry(table):
    db = swsscommon.DBConnector(swsscommon.ASIC_DB, '/var/run/redis/redis.sock', 0)
    tbl =  swsscommon.Table(db, table)
    entries = list(tbl.getKeys())
    return entries[0]

def create_entry_tbl(db, table, key, pairs):
    tbl = swsscommon.Table(db, table)
    create_entry(tbl, key, pairs)

def create_entry_pst(db, table, separator, key, pairs):
    tbl = swsscommon.ProducerStateTable(db, table)
    create_entry(tbl, key, pairs)

def convert_string_to_s8_list(s):
    l = '%d' %len(s)
    l +=':'
    fist_char = True
    for c in s:
        if (fist_char == False):
            l += ','
        else:
            fist_char = False
        l += '%d' %ord(c)
    return l

def avg_min_max_instant_stats_precision1_check(counter_db, table, key):
    check_object(counter_db, table, key,
        {
            'starttime': r'\d+',
            'instant': PRECISION1_PATTERN,
            'avg': PRECISION1_PATTERN,
            'min': PRECISION1_PATTERN,
            'max': PRECISION1_PATTERN,
            'min-time': r'\d+',
            'max-time': r'\d+',
            'interval': r'\d+',
            'validity': r'complete|incomplete|unavailable|invalid',
        }
    ) 
    
def avg_min_max_instant_stats_precision2_check(counter_db, table, key):
    check_object(counter_db, table, key,
        {
            'starttime': r'\d+',
            'instant': PRECISION2_PATTERN,
            'avg': PRECISION2_PATTERN,
            'min': PRECISION2_PATTERN,
            'max': PRECISION2_PATTERN,
            'min-time': r'\d+',
            'max-time': r'\d+',
            'interval': r'\d+',
            'validity': r'complete|incomplete|unavailable|invalid',
        }
    )

def avg_min_max_instant_stats_precision18_check(counter_db, table, key):
    check_object(counter_db, table, key,
        {
            'starttime': r'\d+',
            'instant': PRECISION18_PATTERN,
            'avg': PRECISION18_PATTERN,
            'min': PRECISION18_PATTERN,
            'max': PRECISION18_PATTERN,
            'min-time': r'\d+',
            'max-time': r'\d+',
            'interval': r'\d+',
            'validity': r'complete|incomplete|unavailable|invalid',
        }
    )

def avg_min_max_instant_stats_long_check(counter_db, table, key):
    check_object(counter_db, table, key,
        {
            'starttime': r'\d+',
            'instant': r'^(-)?\d+$',
            'avg': r'^(-)?\d+$',
            'min': r'^(-)?\d+$',
            'max': r'^(-)?\d+$',
            'min-time': r'\d+',
            'max-time': r'\d+',
            'interval': r'\d+',
            'validity': r'complete|incomplete|unavailable|invalid',
        }
    )

def get_last_15min_timestamp():
    minuteDelta = (int(datetime.now().minute / 15) - 1)*15
    t15 = datetime.now().replace(second=0, microsecond=0, minute=0) + timedelta(minutes=minuteDelta)
    return int(t15.timestamp()*1000000000)

def get_last_24h_timestamp():
    t24 = datetime.now().replace(second=0, microsecond=0, minute=0, hour=0) - timedelta(days=1)
    return int(t24.timestamp()*1000000000)

def is_system_running_more_than_24h():
    uptime=os.popen('uptime -p').read()
    return "day" in uptime

def get_db_idx(slot):
    db_idx = slot - 1
    if db_idx < 0:
        db_idx = ''
    return db_idx

def gauge_pm_float_precision1_test(slot, table, key, field):
    time_15min = get_last_15min_timestamp()
    time_24h = get_last_24h_timestamp()
    db_idx = get_db_idx(slot)
    counter_db = swsscommon.DBConnector(swsscommon.COUNTERS_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    history_db = swsscommon.DBConnector(swsscommon.HISTORY_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    
    avg_min_max_instant_stats_precision1_check(counter_db, table, f"{key}_{field}:15_pm_current")
    avg_min_max_instant_stats_precision1_check(counter_db, table, f"{key}_{field}:24_pm_current")
    
    avg_min_max_instant_stats_precision1_check(history_db, table, f"{key}_{field}:15_pm_history_{time_15min}")
    if is_system_running_more_than_24h():
        avg_min_max_instant_stats_precision1_check(history_db, table, f"{key}_{field}:24_pm_history_{time_24h}")

def gauge_pm_float_precision2_test(slot, table, key, field):
    time_15min = get_last_15min_timestamp()
    time_24h = get_last_24h_timestamp()
    db_idx = get_db_idx(slot)
    counter_db = swsscommon.DBConnector(swsscommon.COUNTERS_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    history_db = swsscommon.DBConnector(swsscommon.HISTORY_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    avg_min_max_instant_stats_precision2_check(counter_db, table, f"{key}_{field}:15_pm_current")
    avg_min_max_instant_stats_precision2_check(counter_db, table, f"{key}_{field}:24_pm_current")
    
    avg_min_max_instant_stats_precision2_check(history_db, table, f"{key}_{field}:15_pm_history_{time_15min}")
    if is_system_running_more_than_24h():
        avg_min_max_instant_stats_precision2_check(history_db, table, f"{key}_{field}:24_pm_history_{time_24h}")

def gauge_pm_float_precision18_test(slot, table, key, field):
    time_15min = get_last_15min_timestamp()
    time_24h = get_last_24h_timestamp()
    db_idx = get_db_idx(slot)
    counter_db = swsscommon.DBConnector(swsscommon.COUNTERS_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    history_db = swsscommon.DBConnector(swsscommon.HISTORY_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    
    avg_min_max_instant_stats_precision18_check(counter_db, table, f"{key}_{field}:15_pm_current")
    avg_min_max_instant_stats_precision18_check(counter_db, table, f"{key}_{field}:24_pm_current")
    
    avg_min_max_instant_stats_precision18_check(history_db, table, f"{key}_{field}:15_pm_history_{time_15min}")
    if is_system_running_more_than_24h():
        avg_min_max_instant_stats_precision18_check(history_db, table, f"{key}_{field}:24_pm_history_{time_24h}")

def gauge_pm_long_test(slot, table, key, field):
    time_15min = get_last_15min_timestamp()
    time_24h = get_last_24h_timestamp()
    db_idx = get_db_idx(slot)
    counter_db = swsscommon.DBConnector(swsscommon.COUNTERS_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    history_db = swsscommon.DBConnector(swsscommon.HISTORY_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    
    avg_min_max_instant_stats_long_check(counter_db, table, f"{key}_{field}:15_pm_current")
    avg_min_max_instant_stats_long_check(counter_db, table, f"{key}_{field}:24_pm_current")
    
    avg_min_max_instant_stats_long_check(history_db, table, f"{key}_{field}:15_pm_history_{time_15min}")
    if is_system_running_more_than_24h():
        avg_min_max_instant_stats_long_check(history_db, table, f"{key}_{field}:24_pm_history_{time_24h}")


COMPONENT_COMMON_OBJ = {
            'empty': r"true|false",
            'part-no': '[0-9a-zA-Z]+',
            'serial-no': '[0-9a-zA-Z]+',
            'mfg-date': r'[0-9]{4}\-(0[1-9]|1[0-2])\-(0[1-9]|[1-2][0-9]|3[0-1])',
            'hardware-version': r"\w+",
            'oper-status': r'ACTIVE|INACTIVE|DISABLE',
            'removable': r"true|false",
            'parent': r'\w+',
            'mfg-name': r'\w+',
        }

def component_common_test(slot, table, key):
    db_idx = get_db_idx(slot)
    state_db = swsscommon.DBConnector(swsscommon.STATE_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    check_object(state_db, table, key, COMPONENT_COMMON_OBJ)

def component_special_test(slot, table, key, expectObj):
    db_idx = get_db_idx(slot)
    state_db = swsscommon.DBConnector(swsscommon.STATE_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    check_object(state_db, table, key, expectObj)
 
def counter_pm_test(slot, table, key, expectObj):
    time_15min = get_last_15min_timestamp()
    time_24h = get_last_24h_timestamp()
    db_idx = get_db_idx(slot)
    counter_db = swsscommon.DBConnector(swsscommon.COUNTERS_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    history_db = swsscommon.DBConnector(swsscommon.HISTORY_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    
    check_object(counter_db, table, f"{key}:current", expectObj)   
    check_object(counter_db, table, f"{key}:15_pm_current", expectObj)   
    check_object(counter_db, table, f"{key}:24_pm_current", expectObj)  
     
    check_object(history_db, table, f"{key}:24_pm_current_{time_15min}", expectObj) 
    if is_system_running_more_than_24h(): 
        check_object(history_db, table, f"{key}:24_pm_current_{time_24h}", expectObj)

def key_exist(slot, table, key):
    db_idx = get_db_idx(slot)
    state_db = swsscommon.DBConnector(swsscommon.STATE_DB, f"/var/run/redis{db_idx}/redis.sock", 0)
    tbl = swsscommon.Table(state_db, table)
    keys = tbl.getKeys()
    if key not in keys:
        return False
    return True
