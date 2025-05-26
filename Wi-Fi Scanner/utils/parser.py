import re

def parse_networks(output):
    networks = []
    current = {}
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("SSID"):
            if current:
                networks.append(current)
                current = {}
            ssid = re.sub(r"^SSID \d+ : ", "", line)
            current["SSID"] = ssid
        elif "Signal" in line:
            signal = int(re.sub(r"[^\d]", "", line.split(":")[1]))
            current["Signal"] = signal
        elif "Authentication" in line:
            auth = line.split(":", 1)[1].strip()
            current["Authentication"] = auth
    if current:
        networks.append(current)
    return networks
