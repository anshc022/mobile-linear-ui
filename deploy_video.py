import requests
import json
import os
import sys

# Load tokens
try:
    with open('tokens.json', 'r') as f:
        tokens = json.load(f)
        PAGE_ACCESS_TOKEN = tokens['facebook']['pageToken']
        PAGE_ID = tokens['facebook']['pageId']
except Exception as e:
    print(f"❌ Error loading tokens: {e}")
    sys.exit(1)

VIDEO_PATH = "/home/ubuntu/.openclaw/media/fasal_demo_veo.mp4"
CAPTION = """📢 **Kisan Bhaiyon ke liye badi khushkhabri!** 📢

Ab kheti hogi aur bhi aasaan **Fasal Seva App** ke saath! 🌾📱

✅ **Satellite View:** Apne khet ki health space se dekhein. (Hara = Swasth, Laal = Khatra).
✅ **Voice AI:** Likhna nahi aata? Bas bol kar puchiye! (Sevak aapki madad karega).
✅ **Mausam:** 14 din ka sateek anuman.

📲 **Abhi Download Karein (Free):**
https://play.google.com/store/apps/details?id=com.fasalseva.app

#FasalSeva #SmartFarming #Kisan #Agriculture #TechForGood #JaiKisan"""

def deploy_video():
    print(f"🚀 Uploading Video to Page {PAGE_ID}...")
    
    if not os.path.exists(VIDEO_PATH):
        print(f"❌ Video file not found: {VIDEO_PATH}")
        return

    # 1. Initialize Upload
    url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/videos"
    
    # Simple upload for < 1GB (Video is ~2.4MB)
    files = {
        'source': open(VIDEO_PATH, 'rb')
    }
    data = {
        'access_token': PAGE_ACCESS_TOKEN,
        'description': CAPTION,
        'published': 'true'
    }
    
    try:
        r = requests.post(url, files=files, data=data, timeout=120)
        r.raise_for_status()
        res = r.json()
        print(f"✅ Video Posted Successfully!")
        print(f"📹 Post ID: {res.get('id')}")
    except Exception as e:
        print(f"❌ Upload Failed: {e}")
        if 'r' in locals():
            print(r.text)

if __name__ == "__main__":
    deploy_video()
