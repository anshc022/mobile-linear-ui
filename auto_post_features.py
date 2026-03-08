import requests, json, sys, os
from datetime import datetime

# Load tokens
try:
    with open('tokens.json', 'r') as f:
        tokens = json.load(f)
        PAGE_ACCESS_TOKEN = tokens['facebook']['pageToken']
        PAGE_ID = tokens['facebook']['pageId']
except Exception as e:
    print(f"❌ Error loading tokens: {e}")
    sys.exit(1)

FB_GRAPH_URL = "https://graph.facebook.com/v21.0"

# --- CAMPAIGN CONFIG: APP FEATURES ---
# Rotating content based on day of week or simple counter
# 1. Satellite (NDVI)
# 2. Voice (Sevak)
# 3. Weather (Mausam)

FEATURES = [
    {
        "id": "satellite",
        "image": "/home/ubuntu/.openclaw/media/fasal_mockup_sat.png",
        "caption": """🛰️ Apne khet ko space se dekhein! 🛰️

Kya aapke khet mein kahin bimari hai? Ya paani kam hai?
Ab aap Satellite Map se pata laga sakte hain - wo bhi muft! 🟢🔴

✅ Hara rang = Swasth Fasal
🔴 Laal rang = Khatra/Kamzori

Abhi check karein Fasal Seva App par! 👇
📲 Download Link: https://play.google.com/store/apps/details?id=com.fasalseva.app

#SmartFarming #KhetiBadi #SatelliteFarming #FasalSeva #IndianFarmer"""
    },
    {
        "id": "voice",
        "image": "/home/ubuntu/.openclaw/media/fasal_mockup_voice.png",
        "caption": """🗣️ Likhna nahi aata? Bas bol kar puchiye! 🗣️

"Gehu ka bhaav kya hai?"
"Kapas mein kaunsi dawai dalun?"

Ab Sevak AI se apni bhasha mein baat karein. Likhne ki zarurat nahi! 🎙️

Aaj hi try karein 👇
📲 Download Link: https://play.google.com/store/apps/details?id=com.fasalseva.app

#VoiceAI #KisanHelp #FasalSeva #AgriTech #BoloAurJaano"""
    },
    {
        "id": "weather",
        "image": "/home/ubuntu/.openclaw/media/fasal_mockup_weather.png",
        "caption": """🌦️ Baarish aayegi ya sookha padega? 🌦️

Galat mausam anuman se nuksan na hone dein.
Paiye 14 Din Ka Sateek Mausam sirf Fasal Seva App par. ☔🌞

Apni kheti ki planning aaj hi shuru karein! 👇
📲 Download Link: https://play.google.com/store/apps/details?id=com.fasalseva.app

#WeatherUpdate #MausamVibhag #KisanSafety #FasalSeva"""
    }
]

STATE_FILE = "/home/ubuntu/.openclaw/workspaces/main/feature_state.json"

def get_next_index():
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                return state.get('last_index', -1) + 1
    except Exception:
        pass
    return 0

def save_index(index):
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump({'last_index': index}, f)
    except Exception as e:
        print(f"⚠️ Failed to save state: {e}")

def post_feature(feature_index=None):
    if feature_index is None:
        feature_index = get_next_index()
    
    idx = feature_index % len(FEATURES)
    feat = FEATURES[idx]
    print(f"🚀 Posting Feature [{idx}]: {feat['id'].upper()}...")
    
    url = f"{FB_GRAPH_URL}/{PAGE_ID}/photos"
    
    if not os.path.exists(feat['image']):
        print(f"❌ Image missing: {feat['image']}")
        return

    files = {'source': open(feat['image'], 'rb')}
    data = {
        'access_token': PAGE_ACCESS_TOKEN,
        'message': feat['caption'],
        'published': 'true'
    }
    
    try:
        r = requests.post(url, files=files, data=data, timeout=30)
        r.raise_for_status()
        pid = r.json().get('id')
        print(f"✅ Success! Post ID: {pid}")
        print(f"🔗 URL: https://www.facebook.com/{PAGE_ID}/posts/{pid}")
        save_index(idx) # Save successful index
    except Exception as e:
        print(f"❌ Failed: {e}")
        if 'r' in locals():
            print(r.text)

if __name__ == "__main__":
    # Allow manual override
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "satellite": post_feature(0)
        elif arg == "voice": post_feature(1)
        elif arg == "weather": post_feature(2)
        else: post_feature()
    else:
        post_feature()
