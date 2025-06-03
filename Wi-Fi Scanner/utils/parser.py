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
            # Netsh may output varying spaces around the colon. Split once on
            # the first colon to reliably extract the SSID name regardless of
            # formatting.
            ssid = line.split(":", 1)[1].strip()
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
