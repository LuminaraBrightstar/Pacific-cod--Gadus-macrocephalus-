import os
import time
from utils.scanner import get_raw_network_data
from utils.parser import parse_networks
from utils.display import display_sorted_networks

def main():
    try:
        while True:
            os.system('cls')  # Clear terminal (Windows)
            raw_output = get_raw_network_data()
            networks = parse_networks(raw_output)
            display_sorted_networks(networks)
            time.sleep(5)  # Refresh every 5 seconds
    except KeyboardInterrupt:
        print("\nExiting Wi-Fi scanner.")

if __name__ == "__main__":
    main()
