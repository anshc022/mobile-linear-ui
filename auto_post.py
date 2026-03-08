import requests
import json
import time
import random
import sys
import os
from datetime import datetime

# --- CONFIGURATION ---
# Load tokens securely
try:
    with open('tokens.json', 'r') as f:
        tokens = json.load(f)
        PAGE_ACCESS_TOKEN = tokens['facebook']['pageToken']
        PAGE_ID = tokens['facebook']['pageId']
except FileNotFoundError:
    print("❌ Error: tokens.json not found.")
    sys.exit(1)

API_VERSION = "v21.0"
FB_GRAPH_URL = f"https://graph.facebook.com/{API_VERSION}"

# Content Templates (Hinglish)
MANDI_TEMPLATES = [
    "📢 *Aaj Ka Mandi Bhav* 📢\n\nGehu (Wheat): ₹2275/qtl 🟢\nChana (Gram): ₹5400/qtl 🔴\n\nSahi daam janne ke liye Fasal Seva app download karein! 👇\n📲 https://play.google.com/store/apps/details?id=com.fasalseva.app",
    "🌾 *Kisan Bhaiyon Dhyan Dein* 🌾\n\nAaj mandi mein tezi hai! Apni fasal ka sahi daam check karein Fasal Seva par.\n\nDownload Link: 👇\nhttps://play.google.com/store/apps/details?id=com.fasalseva.app",
]

TIP_TEMPLATES = [
    "💡 *Kheti Ki Baat* 💡\n\nGarmi badh rahi hai? Apni fasal ko 'Heat Stress' se bachane ke liye shaam ko sinchai karein.\n\nAur mausam ki jankari ke liye Fasal Seva app dekhein! 🌦️\n👉 https://play.google.com/store/apps/details?id=com.fasalseva.app",
    "🚜 *Smart Farming Tip* 🚜\n\nMitti ki janch (Soil Test) har 2 saal mein zaruri hai. Isse khaad ka kharcha 20% kam ho sakta hai!\n\nExpert advice ke liye Fasal Seva download karein. 📲",
]

# Image Assets (Round Robin)
IMAGES = [
    "/home/ubuntu/.openclaw/media/fasal-seva-student-1.png",
    "/home/ubuntu/.openclaw/media/fasal_day1_weather.png", 
    "/home/ubuntu/.openclaw/media/fasal_day2_mandi.png"
]

def post_to_facebook(message, image_path=None):
    print(f"🚀 Preparing to post to Facebook Page {PAGE_ID}...")
    
    url = f"{FB_GRAPH_URL}/{PAGE_ID}/photos" if image_path else f"{FB_GRAPH_URL}/{PAGE_ID}/feed"
    
    payload = {
        'access_token': PAGE_ACCESS_TOKEN,
        'message': message,
        'published': 'true'
    }
    
    files = {}
    if image_path:
        if os.path.exists(image_path):
            files = {'source': open(image_path, 'rb')}
            print(f"📸 Attaching image: {image_path}")
        else:
            print(f"⚠️ Image not found at {image_path}, posting text only.")
            url = f"{FB_GRAPH_URL}/{PAGE_ID}/feed" # Fallback to text
    
    try:
        if files:
            response = requests.post(url, files=files, data=payload, timeout=30)
        else:
            response = requests.post(url, data=payload, timeout=30)
            
        response.raise_for_status()
        data = response.json()
        post_id = data.get('id') or data.get('post_id')
        print(f"✅ Successfully posted! Post ID: {post_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to post: {e}")
        if 'response' in locals():
            print(response.text)
        return False

def run_auto_post(post_type="tip"):
    if post_type == "mandi":
        content = random.choice(MANDI_TEMPLATES)
        # Prefer the mandi specific image if available
        img = "/home/ubuntu/.openclaw/media/fasal_day2_mandi.png"
    else:
        content = random.choice(TIP_TEMPLATES)
        img = random.choice(IMAGES)
    
    print(f"📝 Selected Content Type: {post_type.upper()}")
    post_to_facebook(content, img)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1] # "mandi" or "tip"
        run_auto_post(mode)
    else:
        # Default behavior (can be cron driven)
        # Randomly pick one
        run_auto_post(random.choice(["mandi", "tip"]))
