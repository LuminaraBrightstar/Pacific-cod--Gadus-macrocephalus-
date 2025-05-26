def display_sorted_networks(networks):
    if not networks:
        print("No networks found.")
        return

    sorted_nets = sorted(networks, key=lambda x: x.get("Signal", 0), reverse=True)
    
    print("Nearby Wi-Fi Networks (Sorted by Signal Strength):\n")
    for net in sorted_nets:
        print(f"SSID         : {net.get('SSID', 'N/A')}")
        print(f"Signal       : {net.get('Signal', 'N/A')}%")
        print(f"Security     : {net.get('Authentication', 'N/A')}")
        print("-" * 40)
