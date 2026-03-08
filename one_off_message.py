import time
import datetime
import os
import subprocess

# Target: 2026-03-09 09:00:00 IST
# IST = UTC + 5:30
# Target UTC: 2026-03-09 03:30:00

target_utc = datetime.datetime(2026, 3, 9, 3, 30, 0, tzinfo=datetime.timezone.utc)
now_utc = datetime.datetime.now(datetime.timezone.utc)

delay_seconds = (target_utc - now_utc).total_seconds()

if delay_seconds > 0:
    print(f"Waiting {delay_seconds} seconds...")
    time.sleep(delay_seconds)

# Message content
target_phone = "+916387953827"
message_body = "Good morning! ☀️\n\nPranshu asked me to remind you it's time for college. 🎓\n\nPlease travel safely and have a wonderful day! Be safe! 🛡️❤️\n\n- Echo 📡"

# Send via openclaw cli (simulating the tool call via CLI if available, or just printing for now?)
# Wait, I don't have the 'message' tool accessible from python script directly unless I use the CLI.
# I will use the 'openclaw' CLI to send the message.
# Command: openclaw message send --to "+916387953827" --message "..." --channel whatsapp

cmd = [
    "openclaw", "message", "send",
    "--to", target_phone,
    "--message", message_body,
    "--channel", "whatsapp"
]

print(f"Sending message to {target_phone}...")
subprocess.run(cmd, check=True)
print("Done.")
