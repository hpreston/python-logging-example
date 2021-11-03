#! /usr/bin/env python
"""
Author: Hank Preston <hapresto@cisco.com>

example-print.py
Illustrate the following concepts:
- using "print" statements for logging/debugging
"""

__author__ = "Hank Preston"
__author_email__ = "hapresto@cisco.com"
__copyright__ = "Copyright (c) 2021 Cisco Systems, Inc."
__license__ = "MIT"

from ncclient import manager
import xmltodict
import sys
from getpass import getpass

device = {
             "address": "ios-xe-mgmt-latest.cisco.com",
             "port": 830,
             "username": input("What username to connect with? "),
             "password": getpass("What password to connect with? ")
          } 

# NETCONF filter to use
netconf_filter = open("filter-ietf-interfaces.xml").read()

if __name__ == '__main__':
    print(f"Attempt to connect to host {device['address']} on port {device['port']} as user {device['username']}")

    try: 
        with manager.connect(host=device["address"], port=device["port"],
                            username=device["username"],
                            password=device["password"],
                            hostkey_verify=False, 
                            timeout = 600) as m:
            
            print(f"Connection check: {m.connected}")

            # Get Configuration and State Info for Interface
            print(f"Sending NETCONF get with filter: {netconf_filter}")
            netconf_reply = m.get(netconf_filter)
            print(f"Was get 'ok': {netconf_reply.ok}")
    except Exception as e: 
        print(f"❌🛑 ERROR: {e}")
        sys.exit(1)

    # Process the XML and store in useful dictionaries
    print(f"Raw netconf data returned: {netconf_reply.xml}")
    intf_details = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
    intf_config = intf_details["interfaces"]["interface"]
    intf_info = intf_details["interfaces-state"]["interface"]

    print("")
    print("Interface Details:")
    print("  Name: {}".format(intf_config["name"]))
    print("  Description: {}".format(intf_config["description"]))
    print("  Type: {}".format(intf_config["type"]["#text"]))
    print("  MAC Address: {}".format(intf_info["phys-address"]))
    print("  Packets Input: {}".format(intf_info["statistics"]["in-unicast-pkts"]))
    print("  Packets Output: {}".format(intf_info["statistics"]["out-unicast-pkts"]))
