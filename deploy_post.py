import requests, json, sys, time

# --- CONFIG ---
PAGE_TOKEN = "EAAVZC3DLbbioBQwDRvRtZC232OSP7MA6Xx9Qjpt8ZCF9CefZBifDVtcdfZA1LCSeYLfmQ3FHBRq43fprurtI7S7ijkI7bCV4jW167NA5hBMKdgJblW5DRE5i1NM3YVt2gQynZCZA6jkii1LyFJ2V0TAqYDDuH86QMIQz8zdQ3mAhZBO63EAd1bmPZBaXjZBhjZBg8FRgV3XpuYZD"
PAGE_ID = "105858594332788"
IG_USER_ID = "17841480076010977"
IMAGE_PATH = "/home/ubuntu/.openclaw/media/fasal-seva-student-1.png"

CAPTION = """Namaste India! 🇮🇳

We are engineering students building Fasal Seva - a 100% FREE app for our farmers. 🌾

✅ Satellite Farm View
✅ Weather Updates
✅ AI Crop Advice

We need your support to reach every kisan.
Download Now: https://play.google.com/store/apps/details?id=com.fasalseva.app

#FasalSeva #StudentInitiative #IndianFarmer #Kisan #AgriTech #JaiKisan"""

def deploy():
    print("🚀 Starting Deployment...")

    # 1. Upload to Facebook (Local File)
    print("📤 Uploading to Facebook...")
    fb_url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/photos"
    
    # We open the file in binary mode
    files = {
        'source': open(IMAGE_PATH, 'rb')
    }
    data = {
        'access_token': PAGE_TOKEN,
        'message': CAPTION,
        'published': 'true'
    }
    
    r = requests.post(fb_url, files=files, data=data)
    
    if r.status_code == 200:
        fb_id = r.json().get('id')
        print(f"✅ Facebook Post Success! ID: {fb_id}")
        
        # 2. Get the High-Res URL from Facebook to give to Instagram
        # We need the 'source' field (full size image)
        print("🔄 Fetching image URL for Instagram...")
        info_url = f"https://graph.facebook.com/v21.0/{fb_id}?fields=images,source&access_token={PAGE_TOKEN}"
        r_info = requests.get(info_url)
        if r_info.status_code == 200:
            # Prefer 'source' or the largest image
            public_img_url = r_info.json().get('source')
            print(f"   Got URL: {public_img_url[:30]}...")
            
            # 3. Post to Instagram
            print("📤 Uploading to Instagram...")
            # Step A: Container
            ig_cont_url = f"https://graph.facebook.com/v21.0/{IG_USER_ID}/media"
            ig_payload = {
                'access_token': PAGE_TOKEN,
                'image_url': public_img_url,
                'caption': CAPTION
            }
            r_ig = requests.post(ig_cont_url, data=ig_payload)
            
            if r_ig.status_code == 200:
                cont_id = r_ig.json().get('id')
                print(f"   Container Created: {cont_id}")
                
                # Step B: Publish
                print("   Publishing Container...")
                ig_pub_url = f"https://graph.facebook.com/v21.0/{IG_USER_ID}/media_publish"
                ig_pub_payload = {
                    'access_token': PAGE_TOKEN,
                    'creation_id': cont_id
                }
                # Wait briefly for processing
                time.sleep(5)
                r_pub = requests.post(ig_pub_url, data=ig_pub_payload)
                
                if r_pub.status_code == 200:
                    print(f"✅ Instagram Post Success! ID: {r_pub.json().get('id')}")
                else:
                    print(f"❌ Instagram Publish Failed: {r_pub.text}")
            else:
                print(f"❌ Instagram Container Failed: {r_ig.text}")
        else:
            print("❌ Could not retrieve Facebook image source.")
    else:
        print(f"❌ Facebook Upload Failed: {r.text}")

if __name__ == "__main__":
    deploy()
