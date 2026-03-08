import requests, json, time, random, sys
from datetime import datetime

# --- CONFIGURATION ---
PAGE_ACCESS_TOKEN = "EAAVZC3DLbbioBQwDRvRtZC232OSP7MA6Xx9Qjpt8ZCF9CefZBifDVtcdfZA1LCSeYLfmQ3FHBRq43fprurtI7S7ijkI7bCV4jW167NA5hBMKdgJblW5DRE5i1NM3YVt2gQynZCZA6jkii1LyFJ2V0TAqYDDuH86QMIQz8zdQ3mAhZBO63EAd1bmPZBaXjZBhjZBg8FRgV3XpuYZD"
PAGE_ID = "105858594332788"
IG_USER_ID = "17841480076010977"

# Endpoints
FB_GRAPH = "https://graph.facebook.com/v21.0"

# --- PART 1: AUTO-REPLY TO COMMENTS ---
def auto_reply_comments():
    print("\n[🛡️ Vigil] Checking for new comments...")
    
    # Get latest posts
    posts_url = f"{FB_GRAPH}/{IG_USER_ID}/media?fields=id,caption,comments{{text,username,id,replies}}&access_token={PAGE_ACCESS_TOKEN}"
    r = requests.get(posts_url)
    if r.status_code != 200:
        print(f"Error fetching posts: {r.text}")
        return

    data = r.json()
    if 'data' not in data:
        print("No posts found.")
        return

    # Keywords to trigger replies
    reply_map = {
        "price": "Fasal Seva app is 100% FREE! The IoT device is ₹3,499. DM us for details! 🌾",
        "cost": "App is free to download! 🌱",
        "download": "Download here: https://play.google.com/store/apps/details?id=com.fasalseva.app 📲",
        "nice": "Thank you! 🙏 Jai Jawan Jai Kisan!",
        "good": "Thanks for the support! 🚜",
        "great": "Glad you liked it! Do try the app. 🌾",
        "help": "We are here to help! Please DM us your query. 🤝"
    }

    # Iterate through posts and comments
    for post in data['data']:
        if 'comments' in post:
            for comment in post['comments']['data']:
                c_id = comment['id']
                c_text = comment['text'].lower()
                
                # Check if already replied (simple check: if 'replies' exists)
                # Ideally, we'd check if WE replied, but for MVP this prevents loops on un-replied threads
                if 'replies' in comment:
                    continue 

                # Determine reply
                reply_text = None
                for keyword, response in reply_map.items():
                    if keyword in c_text:
                        reply_text = response
                        break
                
                # Generic fallback for questions
                if not reply_text and "?" in c_text:
                    reply_text = "Thanks for asking! Our team will DM you shortly. 🌾"

                # Post reply
                if reply_text:
                    print(f"   ↳ Replying to '{c_text}' with: '{reply_text}'")
                    reply_url = f"{FB_GRAPH}/{c_id}/replies"
                    payload = {"message": reply_text, "access_token": PAGE_ACCESS_TOKEN}
                    rr = requests.post(reply_url, data=payload)
                    if rr.status_code == 200:
                        print("     ✅ Reply Sent!")
                    else:
                        print(f"     ❌ Failed: {rr.text}")
                    time.sleep(5) # Anti-spam delay

# --- PART 2: OUTREACH (FINDING USERS) ---
def hashtag_outreach():
    print("\n[⚡ Bolt] Scouting hashtags for potential users...")
    
    hashtags = ["indianfarmer", "kisan", "agritechindia", "smartfarming"]
    
    for tag in hashtags:
        # Search for hashtag ID
        search_url = f"{FB_GRAPH}/ig_hashtag_search?user_id={IG_USER_ID}&q={tag}&access_token={PAGE_ACCESS_TOKEN}"
        r = requests.get(search_url)
        if r.status_code != 200: continue
        
        tag_data = r.json()
        if not tag_data.get('data'): continue
        
        tag_id = tag_data['data'][0]['id']
        
        # Get recent posts for this hashtag
        media_url = f"{FB_GRAPH}/{tag_id}/recent_media?user_id={IG_USER_ID}&fields=id,caption,permalink&access_token={PAGE_ACCESS_TOKEN}&limit=5"
        mr = requests.get(media_url)
        
        if mr.status_code == 200:
            media = mr.json().get('data', [])
            print(f"   #{tag}: Found {len(media)} recent posts.")
            for m in media:
                print(f"     - {m.get('caption', '')[:30]}... ({m.get('permalink')})")
                # In a real tool, we would 'like' or 'comment' here.
                # Auto-commenting on strangers' posts is high-risk for bans, so we just Log for now.
                print("     (Action: Logged for manual engagement)")

# --- PART 3: ANALYTICS (GROWTH) ---
def analyze_growth():
    print("\n[📊 Nexus] Analyzing account health...")
    
    url = f"{FB_GRAPH}/{IG_USER_ID}?fields=followers_count,media_count&access_token={PAGE_ACCESS_TOKEN}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        print(f"   📈 Followers: {data['followers_count']}")
        print(f"   📸 Total Posts: {data['media_count']}")
        
        # Simple insight
        if data['followers_count'] < 100:
            print("   💡 Strategy: You are in 'Early Stage'. Focus on Replies + Reel consistency.")
        else:
            print("   💡 Strategy: You have traction. Focus on Viral Hooks + Collabs.")
            
# --- MAIN LOOP ---
if __name__ == "__main__":
    print("🚀 Fasal Seva Social Growth Engine Starting...")
    auto_reply_comments()
    hashtag_outreach()
    analyze_growth()
    print("\n✅ Cycle Complete.")
