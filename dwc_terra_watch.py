#!/usr/bin/env python3
"""DWC Terra drop watcher. Pushes a phone alert (via ntfy.sh) when a purchase window opens.

Usage:
  NTFY_TOPIC=your-secret-topic python dwc_terra_watch.py          # normal check
  NTFY_TOPIC=your-secret-topic python dwc_terra_watch.py --test   # send a test alert
"""
import json
import os
import sys
import urllib.request

BASE = "https://delhiwatchcompany.com"
PRODUCT_URL = f"{BASE}/products/dwc-terra"
CLOSED_TEXT = "pre-orders are now closed"
UA = "Mozilla/5.0 (compatible; personal-restock-checker)"
TOPIC = os.environ.get("NTFY_TOPIC", "")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace")


def notify(title, message, url=PRODUCT_URL):
    if not TOPIC:
        sys.exit("Set NTFY_TOPIC first.")
    req = urllib.request.Request(
        f"https://ntfy.sh/{TOPIC}",
        data=message.encode("utf-8"),
        headers={"Title": title, "Priority": "urgent", "Click": url, "Tags": "watch,rotating_light"},
    )
    urllib.request.urlopen(req, timeout=20)

