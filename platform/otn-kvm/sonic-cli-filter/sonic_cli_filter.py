"""
Platform-specific CLI command filter for SONiC platforms.

Removes unwanted switch-oriented CLI commands based on a per-device
blacklist configuration (cli_unwanted.json).

Uses lazy filtering by wrapping click.Group.list_commands / get_command
so commands registered after plugin load are also hidden.
"""

import json
import logging
import os
import types

logger = logging.getLogger(__name__)

DEVICE_BASE = "/usr/share/sonic/device"
CONFIG_FILENAME = "cli_unwanted.json"

_config_cache = None
_config_loaded = False


def _get_platform():
    try:
        from sonic_py_common import device_info
        return device_info.get_platform()
    except Exception:
        return None


def _get_config():
    global _config_cache, _config_loaded
    if _config_loaded:
        return _config_cache
    _config_loaded = True
    platform = _get_platform()
    if not platform:
        return None
    config_path = os.path.join(DEVICE_BASE, platform, CONFIG_FILENAME)
    if not os.path.isfile(config_path):
        return None
    try:
        with open(config_path, "r") as f:
            _config_cache = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Failed to load %s: %s", config_path, e)
    return _config_cache


def _parse_blacklist(cli_type):
    """
    Return (top_level_set, nested_dict) from the blacklist.
    top_level_set:  {'vlan', 'nat', ...}
    nested_dict:    {'ip': {'bgp'}, 'ipv6': {'bgp'}}
    """
    config = _get_config()
    if not config:
        return set(), {}
    unwanted = config.get(cli_type)
    if not unwanted:
        return set(), {}
    top = set()
    nested = {}
    for entry in unwanted:
        if "." in entry:
            parent, child = entry.split(".", 1)
            nested.setdefault(parent, set()).add(child)
        else:
            top.add(entry)
    return top, nested


def _wrap_group(group, hidden):
    """Wrap list_commands and get_command on a click.Group instance."""
    orig_list = group.list_commands
    orig_get = group.get_command

    def filtered_list_commands(ctx):
        return [n for n in orig_list(ctx) if n not in hidden]

    def filtered_get_command(ctx, cmd_name):
        if cmd_name in hidden:
            return None
        return orig_get(ctx, cmd_name)

    group.list_commands = filtered_list_commands
    group.get_command = filtered_get_command


def filter_commands(cli_type, root_command):
    """
    Patch *root_command* to hide blacklisted commands.
    Works for commands registered both before AND after this call.
    """
    top_hidden, nested = _parse_blacklist(cli_type)
    if not top_hidden and not nested:
        return

    if top_hidden:
        _wrap_group(root_command, top_hidden)

    for parent_name, child_set in nested.items():
        _wrap_nested(root_command, parent_name, child_set)


def _wrap_nested(root, parent_name, child_hidden):
    """
    For dotted paths like 'ip.bgp', intercept the parent sub-group
    and patch it to hide the child commands.
    """
    orig_get = root.get_command
    patched = [False]

    def intercepting_get(ctx, cmd_name):
        result = orig_get(ctx, cmd_name)
        if cmd_name == parent_name and result and not patched[0]:
            if hasattr(result, 'list_commands'):
                patched[0] = True
                _wrap_group(result, child_hidden)
        return result

    root.get_command = intercepting_get
