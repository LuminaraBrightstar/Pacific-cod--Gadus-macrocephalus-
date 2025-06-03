import os
import sys

# Add the Wi-Fi Scanner directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Wi-Fi Scanner'))

from utils.parser import parse_networks

SAMPLE_OUTPUT = """
SSID 1 : TestNetwork
    Network type            : Infrastructure
    Authentication          : WPA2-Personal
    Encryption              : CCMP
    BSSID 1                 : aa:bb:cc:dd:ee:ff
         Signal             : 80%
         Radio type         : 802.11ac
         Channel            : 11

SSID 2 : AnotherOne
    Network type            : Infrastructure
    Authentication          : Open
    Encryption              : None
    BSSID 1                 : 00:11:22:33:44:55
         Signal             : 60%
"""

SAMPLE_OUTPUT_VARIATION = """
SSID 1:NoSpaces
Authentication:WPA3
Signal:70%
"""

def test_parse_standard_output():
    networks = parse_networks(SAMPLE_OUTPUT)
    assert networks == [
        {"SSID": "TestNetwork", "Signal": 80, "Authentication": "WPA2-Personal"},
        {"SSID": "AnotherOne", "Signal": 60, "Authentication": "Open"},
    ]

def test_parse_colon_variation():
    networks = parse_networks(SAMPLE_OUTPUT_VARIATION)
    assert networks == [
        {"SSID": "NoSpaces", "Signal": 70, "Authentication": "WPA3"}
    ]

