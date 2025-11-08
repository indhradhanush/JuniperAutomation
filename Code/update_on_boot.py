#!/usr/bin/env python3

import time
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from lxml import etree

# Define the new hostname
NEW_HOSTNAME = "NEW-NAME"

def get_uptime(dev):
    """Fetch system uptime using RPC and extract uptime in seconds."""
    try:
        uptime_info = dev.rpc.get_system_uptime_information()
        
        # Extract <up-time seconds="XXX">
        uptime_element = uptime_info.find(".//up-time")
        if uptime_element is not None and "seconds" in uptime_element.attrib:
            uptime_seconds = int(uptime_element.attrib["seconds"])
            return uptime_seconds
        else:
            print("Error: Could not find 'up-time' in XML response.")
            return 0

    except Exception as e:
        print(f"Error fetching uptime: {e}")
        return 0

def wait_for_uptime(dev, target_uptime=180):  # 3 minutes = 180 seconds
    """Wait until system uptime reaches 3 minutes before executing configuration changes."""
    print("Waiting for system uptime to reach 3 minutes...")

    while True:
        with dev.open():
            uptime = get_uptime(dev)
            print(f"Current uptime: {uptime} seconds")

            if uptime >= target_uptime:
                print("Uptime reached 3 minutes. Proceeding with configuration changes...")
                return

        time.sleep(30)  # Check every 30 seconds

try:
    # Connect to the Junos device
    dev = Device()

    # Wait for uptime to reach 3 minutes before proceeding
    wait_for_uptime(dev)

    dev.open()
    cfg = Config(dev)

    # Delete Protocols
    cfg.load("delete protocols", format="set")
    # Delete VLANs
    cfg.load("delete vlans", format="set")
    # Delete Interfaces
    cfg.load("delete interfaces", format="set")

    cfg.commit()

    # Rollback and commit again
    cfg.rollback(1)
    cfg.load(f"set system host-name {NEW_HOSTNAME}", format="set")
    cfg.commit()

    print(f"Hostname successfully changed to: {NEW_HOSTNAME}")

except Exception as e:
    print(f"Error: {e}")

finally:
    dev.close()
