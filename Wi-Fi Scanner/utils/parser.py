import re

def parse_networks(output):
    networks = []
    current = {}
    for line in output.splitlines():
        line = line.strip()
        # Match SSID lines like "SSID 1: Name" or "SSID 1 : Name".
        # Netsh output varies spacing around the colon, so allow optional spaces.
        if re.match(r'^SSID\s+\d+\s*:\s*', line):
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
