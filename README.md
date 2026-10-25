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
