import requests, json, time, random, sys
from datetime import datetime

# --- CONFIGURATION ---
# Token from previous context
PAGE_ACCESS_TOKEN = "EAAVZC3DLbbioBQwDRvRtZC232OSP7MA6Xx9Qjpt8ZCF9CefZBifDVtcdfZA1LCSeYLfmQ3FHBRq43fprurtI7S7ijkI7bCV4jW167NA5hBMKdgJblW5DRE5i1NM3YVt2gQynZCZA6jkii1LyFJ2V0TAqYDDuH86QMIQz8zdQ3mAhZBO63EAd1bmPZBaXjZBhjZBg8FRgV3XpuYZD"
PAGE_ID = "105858594332788"
IG_USER_ID = "17841480076010977"

# Growth Settings
TARGET_HASHTAGS = ["indianfarmer", "kisan", "agritechindia", "smartfarming", "organicfarmingindia"]
REPLY_DELAY = 10  # Seconds between replies to avoid spam flags

# --- API HELPERS ---
GRAPH_URL = "https://graph.facebook.com/v21.0"

def log(module, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{module}] {message}")

# --- MODULE 1: AUTO-REPLY (Community Manager) ---
def auto_reply():
    log("🛡️ Vigil", "Scanning for new comments on YOUR posts...")
    
    # Fetch recent media + comments
    url = f"{GRAPH_URL}/{IG_USER_ID}/media?fields=id,caption,comments{{id,text,username,replies}}&access_token={PAGE_ACCESS_TOKEN}&limit=10"
    r = requests.get(url)
    data = r.json()
    
    if "data" not in data:
        log("🛡️ Vigil", "No media found or token error.")
        return

    reply_map = {
        "price": "The Fasal Seva app is 100% FREE for farmers! 🌾📲",
        "cost": "It's completely free to download. Jai Kisan! 🇮🇳",
        "download": "Download here: https://play.google.com/store/apps/details?id=com.fasalseva.app 🚜",
        "link": "Link is in our bio! 📲",
        "nice": "Thank you for the support! 🙏",
        "good": "Glad you liked it! 🌾",
        "help": "Please DM us and we will help you immediately. 🤝"
    }

    replied_count = 0
    for post in data['data']:
        if 'comments' in post:
            for comment in post['comments']['data']:
                # Skip if already replied
                if 'replies' in comment: 
                    continue
                
                c_text = comment['text'].lower()
                c_id = comment['id']
                
                # Match keyword
                response = None
                for kw, ans in reply_map.items():
                    if kw in c_text:
                        response = ans
                        break
                
                if response:
                    log("🛡️ Vigil", f"Replying to '{comment['text']}' with: '{response}'")
                    # POST THE REPLY
                    reply_endpoint = f"{GRAPH_URL}/{c_id}/replies"
                    payload = {"message": response, "access_token": PAGE_ACCESS_TOKEN}
                    rr = requests.post(reply_endpoint, data=payload)
                    if rr.status_code == 200:
                        log("🛡️ Vigil", "✅ Reply Sent Successfully")
                        replied_count += 1
                        time.sleep(REPLY_DELAY)
                    else:
                        log("🛡️ Vigil", f"❌ Failed: {rr.text}")
    
    if replied_count == 0:
        log("🛡️ Vigil", "No new comments needing replies.")

# --- MODULE 2: LEAD SCOUT (Growth Hacker) ---
def scout_leads():
    log("⚡ Bolt", "Scouting viral posts for outreach...")
    
    for tag in TARGET_HASHTAGS:
        # 1. Search Hashtag ID
        s_url = f"{GRAPH_URL}/ig_hashtag_search?user_id={IG_USER_ID}&q={tag}&access_token={PAGE_ACCESS_TOKEN}"
        sr = requests.get(s_url)
        if sr.status_code != 200: continue
        
        s_data = sr.json()
        if not s_data.get('data'): continue
        tag_id = s_data['data'][0]['id']
        
        # 2. Get Top Media
        m_url = f"{GRAPH_URL}/{tag_id}/top_media?user_id={IG_USER_ID}&fields=id,caption,permalink,like_count,comments_count&access_token={PAGE_ACCESS_TOKEN}&limit=2"
        mr = requests.get(m_url)
        
        if mr.status_code == 200:
            media = mr.json().get('data', [])
            for m in media:
                caption = m.get('caption', '')[:30].replace('\n', ' ')
                link = m.get('permalink')
                likes = m.get('like_count', 0)
                log("⚡ Bolt", f"Found Lead [#{tag}]: {caption}... | ❤️ {likes} Likes")
                log("⚡ Bolt", f"👉 ENGAGE HERE: {link}")
                # Note: API does NOT allow auto-commenting on public media without special approval.
                # We log the link for the user to click & comment. This protects the account from bans.

# --- MODULE 3: ANALYTICS (Data) ---
def check_stats():
    log("📊 Nexus", "Pulling latest stats...")
    url = f"{GRAPH_URL}/{IG_USER_ID}?fields=followers_count,media_count&access_token={PAGE_ACCESS_TOKEN}"
    r = requests.get(url)
    if r.status_code == 200:
        d = r.json()
        log("📊 Nexus", f"Followers: {d['followers_count']} | Posts: {d['media_count']}")

# --- MAIN CONTROLLER ---
if __name__ == "__main__":
    print("\n🚜 FASAL SEVA MASTER ENGINE INITIALIZED 🚜")
    print("------------------------------------------")
    
    # Run once immediately
    check_stats()
    auto_reply()
    scout_leads()
    
    print("------------------------------------------")
    print("✅ Cycle Complete. Script can be scheduled (Cron) or looped.")
