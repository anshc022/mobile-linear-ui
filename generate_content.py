import requests, json, sys, base64

API_KEY = "AIzaSyDow1UVPt93h9wtV6VBNia4w5LpoHMThdE"

def generate_image(prompt, outfile):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={API_KEY}"
    # Fallback to fast model if needed
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={API_KEY}"
    
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "1:1",
            "outputOptions": {"mimeType": "image/png"}
        }
    }
    print(f"🎨 Generating: {outfile}...")
    try:
        r = requests.post(url, json=payload, timeout=120)
        data = r.json()
        if "predictions" in data:
            img_b64 = data["predictions"][0]["bytesBase64Encoded"]
            with open(outfile, "wb") as f:
                f.write(base64.b64decode(img_b64))
            print(f"✅ Saved: {outfile}")
            return True
        else:
            print(f"❌ Failed: {data}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# --- DAY 1: WEATHER HACK ---
prompt_day1 = "Split screen realistic image. Left side: Indian farmer looking worried at dark storm clouds in a wheat field. Right side: Smartphone screen showing a bright sunny weather forecast app with the text 'NO RAIN'. High contrast, cinematic lighting."
outfile_day1 = "/home/ubuntu/.openclaw/media/fasal_day1_weather.png"

# --- DAY 2: MANDI PRICE ---
prompt_day2 = "Infographic style image. Background is a busy Indian grain market (Mandi). Overlay text in bold yellow and white: 'WHEAT PRICES TODAY'. Show comparison: 'Punjab: 2275' vs 'MP: 2400'. Green upward arrow graphic."
outfile_day2 = "/home/ubuntu/.openclaw/media/fasal_day2_mandi.png"

if __name__ == "__main__":
    generate_image(prompt_day1, outfile_day1)
    generate_image(prompt_day2, outfile_day2)
