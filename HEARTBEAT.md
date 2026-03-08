# HEARTBEAT.md

# One-off scheduled tasks
# When the condition is met, execute the action and then DELETE the task from this file.

- [ ] **Target:** 2026-03-09 03:30 UTC (09:00 IST)
  **Action:** Send WhatsApp to +916387953827 (Mehak)
  **Message:** "Good morning! ☀️\n\nPranshu asked me to remind you it's time for college. 🎓\n\nPlease travel safely and have a wonderful day! Be safe! 🛡️❤️\n\n- Echo 📡"
  **Condition:** If current_time >= Target, SEND immediately and REMOVE this entry.

# Continuous Tasks
# These run on every heartbeat.

- [ ] **Task:** Check for Client Request Status Updates
  **Action:**
  1. Call `curl -s https://chatty-onions-yell.loca.lt/api/pending-notifications` (or localhost if internal).
  2. If `notifications` array is not empty:
     - For each item:
       - Send message to WhatsApp Group 120363425325147181@g.us: "🔔 **Status Update:** Task #{id} is now *{status}*.\n📝 {content}"
       - Call `curl -X POST -H "Content-Type: application/json" -d '{"id": <id>}' https://chatty-onions-yell.loca.lt/api/mark-notified`
