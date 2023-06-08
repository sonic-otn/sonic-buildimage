#!/usr/bin/env python

import re
import os
import jinja2
import json
import argparse

def client_port_match(value, client_port):
    pattern = re.compile('PORT-1-[1-9]-C[1-9]+')
    for port in value:
        m = pattern.match(port)
        if m is not None:
            client_port.append(port)

def line_port_match(value, line_port):
    pattern = re.compile('PORT-1-[1-9]-L[1-9]+')
    for port in value:
        m = pattern.match(port)
        if m is not None:
            line_port.append(port)

def port_to_other_key(value, key):
    for i, port in enumerate(value):
        new_value = key + port[4:]
        value[i] = new_value

def logical_channel_to_other_key(value, key):
    for i, ch in enumerate(value):
        new_value = key + ch[2:]
        value[i] = new_value

def parse_ini_file(ini_file):
    entries = {}
    titles = ['name', 'index']
    with open(ini_file) as data:
        for line in data:
            if line.startswith('#'):
                if "name" in line:
                    titles = line.strip('#').split()
                    continue;
            tokens = line.split()
            if len(tokens) < 2:
                continue
            name_index = titles.index('name')
            name = tokens[name_index]
            data = {}
            for i, item in enumerate(tokens):
                if i == name_index:
                    continue
                data[titles[i]] = item
            entries[name] = data
    return entries

def deep_update(dst, src):
    """ Deep update of dst dict with contest of src dict"""
    pending_nodes = [(dst, src)]
    while len(pending_nodes) > 0:
        d, s = pending_nodes.pop(0)
        for key, value in s.items():
            if isinstance(value, dict):
                node = d.setdefault(key, type(value)())
                pending_nodes.append((node, value))
            else:
                d[key] = value
    return dst 

def _get_jinja2_env(paths):
    loader = jinja2.FileSystemLoader(paths)
    env = jinja2.Environment(loader=loader, trim_blocks=True)
    env.filters['client_port_match'] = client_port_match
    env.filters['line_port_match'] = line_port_match
    env.filters['port_to_other_key'] = port_to_other_key
    env.filters['logical_channel_to_other_key'] = logical_channel_to_other_key

    return env

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-l", "--logicalchannel-ini-file", help="logicalchannel ini file")
    parser.add_argument("-p", "--port-ini-file", help="port ini file")
    parser.add_argument("-T", "--template-file", help="template file")
    parser.add_argument("-d", "--template-dir", help="template directory")
    parser.add_argument("-t", "--linecard-type", help="linecard type")
    parser.add_argument("-i", "--linecard-id", help="linecard id")
    parser.add_argument("-m", "--board-mode", help="linecard mode")
    parser.add_argument("-n", "--asic-id", help="asic id")
    parser.add_argument("-k", "--hwsku", help="HwSKU")

    args = parser.parse_args()

    data = {}
    paths = [args.template_dir]

    if args.asic_id is not None:
        meta_data = {'DEVICE_METADATA': {'localhost': {
                     'asic_id': args.asic_id,
                     }}}
        deep_update(data, meta_data)
    
    if args.hwsku is not None:
        meta_data = {'DEVICE_METADATA': {'localhost': {
                     'hwsku': args.hwsku,
                     }}}
        deep_update(data, meta_data)
    
    ports = parse_ini_file(args.port_ini_file)
    deep_update(data, {'PORT': ports})
    
    logicalchannels = parse_ini_file(args.logicalchannel_ini_file)
    deep_update(data, {'LOGICAL_CHANNEL': logicalchannels})
    
    env = _get_jinja2_env(paths)
    env.globals['linecard_type'] = args.linecard_type
    env.globals['linecard_id'] = args.linecard_id
    env.globals['board_mode'] = args.board_mode

    template = env.get_template(os.path.basename(args.template_file))
    template_data = template.render(data)

    deep_update(data, json.loads(template_data))
    print(json.dumps(data, indent=4))

if __name__ == "__main__":
    main()

