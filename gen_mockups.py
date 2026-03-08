import requests, json, sys, base64

API_KEY = "AIzaSyDow1UVPt93h9wtV6VBNia4w5LpoHMThdE"

def generate_app_mockup(prompt, outfile):
    # Using Imagen 3 for high-quality mockups
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={API_KEY}"
    
    # Fallback to fast model if needed
    # url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={API_KEY}"
    
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
        r = requests.post(url, json=payload, timeout=60)
        data = r.json()
        if "predictions" in data:
            img_b64 = data["predictions"][0]["bytesBase64Encoded"]
            with open(outfile, "wb") as f:
                f.write(base64.b64decode(img_b64))
            print(f"✅ Saved: {outfile}")
            return True
        else:
            print(f"❌ Failed: {data}")
            # Try Fast model fallback
            url_fast = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={API_KEY}"
            r2 = requests.post(url_fast, json=payload, timeout=60)
            data2 = r2.json()
            if "predictions" in data2:
                img_b64 = data2["predictions"][0]["bytesBase64Encoded"]
                with open(outfile, "wb") as f:
                    f.write(base64.b64decode(img_b64))
                print(f"✅ Saved (Fast Model): {outfile}")
                return True
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# --- PROMPTS ---
p_sat = "A smartphone displaying a satellite map of a farm field with red and green zones indicating crop health (NDVI). The interface is modern, clean, and in Hindi/English. Text on screen: 'Fasal Seva'. Background is a blurred green field. Photorealistic."
p_voice = "Close up of a smartphone screen showing a large microphone button with sound waves. Text bubbles in Hindi: 'Gehu ka bhaav kya hai?' and AI reply: '₹2275/qtl'. Clean UI, green color theme. App name 'Fasal Seva' visible."
p_weather = "Smartphone screen showing a 14-day weather forecast app with sun, rain, and cloud icons. Hindi text for days. 'Fasal Seva' branding at the top. Farmer holding the phone in a field."

if __name__ == "__main__":
    generate_app_mockup(p_sat, "/home/ubuntu/.openclaw/media/fasal_mockup_sat.png")
    generate_app_mockup(p_voice, "/home/ubuntu/.openclaw/media/fasal_mockup_voice.png")
    generate_app_mockup(p_weather, "/home/ubuntu/.openclaw/media/fasal_mockup_weather.png")
