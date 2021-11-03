#! /usr/bin/env python
"""
Author: Hank Preston <hapresto@cisco.com>

example-logger.py
Illustrate the following concepts:
- using Python logging rather than print based logging
- leveraging different log handlers based on levels 
- setting message levels for filtering
"""

__author__ = "Hank Preston"
__author_email__ = "hapresto@cisco.com"
__copyright__ = "Copyright (c) 2021 Cisco Systems, Inc."
__license__ = "MIT"

import logging.config 
import logging 
from ncclient import manager
import xmltodict
import sys
from getpass import getpass

# Reading logging configuration and create logger
logging.config.fileConfig("logger.conf")
logger = logging.getLogger(__name__)


device = {
             "address": "ios-xe-mgmt-latest.cisco.com",
             "port": 830,
             "username": input("What username to connect with? "),
             "password": getpass("What password to connect with? ")
          } 

# NETCONF filter to use
netconf_filter = open("filter-ietf-interfaces.xml").read()

if __name__ == '__main__':
    logger.info(f"Attempt to connect to host {device['address']} on port {device['port']} as user {device['username']}")

    try: 
        with manager.connect(host=device["address"], port=device["port"],
                            username=device["username"],
                            password=device["password"],
                            hostkey_verify=False, 
                            timeout = 600) as m:
            
            logger.debug(f"Connection check: {m.connected}")

            # Get Configuration and State Info for Interface
            logger.debug(f"Sending NETCONF get with filter: {netconf_filter}")
            netconf_reply = m.get(netconf_filter)
            logger.info(f"Was get 'ok': {netconf_reply.ok}")
    except Exception as e: 
        logger.critical(f"❌🛑 ERROR: {e}")
        sys.exit(1)

    # Process the XML and store in useful dictionaries
    logger.debug(f"Raw netconf data returned: {netconf_reply.xml}")
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
