import subprocess

def get_raw_network_data():
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
