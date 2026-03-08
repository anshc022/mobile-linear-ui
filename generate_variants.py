import requests, json, sys, base64, time

API_KEY = "AIzaSyDow1UVPt93h9wtV6VBNia4w5LpoHMThdE"

def generate(prompt, outfile):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={API_KEY}"
    # Fallback to fast if needed
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

# --- VARIANT 1: MINIMALIST TECH (Clean Green) ---
p1 = "Minimalist flat design poster. A simple green vector tractor icon in the center on a white background. Below it, a sleek smartphone showing a 'Check Weather' button. Text: 'Smart Farming Simplified'. Modern, clean, Apple-style aesthetic."
out1 = "/home/ubuntu/.openclaw/media/fasal_variant_minimal.png"

# --- VARIANT 2: FUTURISTIC DRONE (Sci-Fi / High Tech) ---
p2 = "Cyberpunk agriculture style. A drone flying over a neon-lit green field at night. The drone projects a holographic map of the farm onto the ground. Text: 'Satellite Vision for Every Farmer'. Dark, moody, glowing green/blue."
out2 = "/home/ubuntu/.openclaw/media/fasal_variant_drone.png"

# --- VARIANT 3: COMMUNITY / PEOPLE (Trust) ---
p3 = "Warm photography style. A group of 3 happy Indian farmers (one elder, two young) looking at a smartphone screen together and smiling. Background is a lush green sugarcane field. Natural sunlight. Text: 'Join the Revolution'. Authentic, emotional."
out3 = "/home/ubuntu/.openclaw/media/fasal_variant_community.png"

if __name__ == "__main__":
    generate(p1, out1)
    time.sleep(2)
    generate(p2, out2)
    time.sleep(2)
    generate(p3, out3)
