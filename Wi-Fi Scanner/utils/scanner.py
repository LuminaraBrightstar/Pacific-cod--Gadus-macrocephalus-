"""Utilities for scanning Wi-Fi networks using Windows tools.

This module relies on the ``netsh`` command that ships with Windows to
retrieve information about nearby Wi-Fi networks. As a result, the
functionality here is Windows-only and will not work on other operating
systems.
"""

import subprocess

def get_raw_network_data():
    """Return raw Wi-Fi network data using the Windows ``netsh`` command."""
    try:
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
            encoding='utf-8',
            stderr=subprocess.STDOUT
        )
        return output
    except subprocess.CalledProcessError as e:
        print("Failed to scan Wi-Fi networks.")
        print(e.output)
        return ""
