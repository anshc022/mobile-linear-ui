#!/usr/bin/env python3
"""Booking monitor — polls Supabase every 30s, posts new bookings to Discord."""

import json
import os
import time
import requests
from datetime import datetime

# Config
SUPABASE_URL = "https://hvtgvihbewmpubnhjelf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh2dGd2aWhiZXdtcHVibmhqZWxmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTM1MzY1MCwiZXhwIjoyMDg2OTI5NjUwfQ.yPV1Tdw3ev5nkRpGmVjl_jNQMgN_6fRPhlHs24_zRSY"
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "")
POLL_INTERVAL = 30  # seconds
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seen_bookings.json")


def load_seen():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(STATE_FILE, "w") as f:
        json.dump(list(seen), f)


def fetch_bookings():
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }
    resp = requests.get(
        f"{SUPABASE_URL}/rest/v1/bookings?select=*&order=created_at.desc&limit=20",
        headers=headers,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def send_discord(booking):
    if not DISCORD_WEBHOOK:
        print(f"[SKIP] No webhook configured. Booking: {booking['name']} ({booking['email']})")
        return

    embed = {
        "title": "🔔 New Booking Received!",
        "color": 0xC2A4FF,
        "fields": [
            {"name": "👤 Name", "value": booking.get("name", "—"), "inline": True},
            {"name": "📧 Email", "value": booking.get("email", "—"), "inline": True},
            {"name": "📱 Phone", "value": booking.get("phone") or "—", "inline": True},
            {"name": "🏢 Business", "value": booking.get("business_name") or "—", "inline": True},
            {"name": "📅 Date", "value": booking.get("preferred_date") or "—", "inline": True},
            {"name": "🕐 Time", "value": booking.get("preferred_time") or "—", "inline": True},
            {"name": "💬 Message", "value": booking.get("message") or "No message", "inline": False},
        ],
        "footer": {"text": f"Status: {booking.get('status', 'pending')}"},
        "timestamp": booking.get("created_at"),
    }

    resp = requests.post(
        DISCORD_WEBHOOK,
        json={"embeds": [embed]},
        timeout=10,
    )
    resp.raise_for_status()
    print(f"[SENT] Booking alert for {booking['name']}")


def main():
    print("🚀 Booking monitor started")
    seen = load_seen()
    print(f"   Tracking {len(seen)} existing bookings")

    while True:
        try:
            bookings = fetch_bookings()
            new_bookings = [b for b in bookings if b["id"] not in seen]

            for booking in reversed(new_bookings):  # oldest first
                send_discord(booking)
                seen.add(booking["id"])

            if new_bookings:
                save_seen(seen)
                print(f"[OK] {len(new_bookings)} new booking(s) processed")

        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
