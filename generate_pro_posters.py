import requests, base64, time
from PIL import Image

API_KEY = "AIzaSyDow1UVPt93h9wtV6VBNia4w5LpoHMThdE"
SS_PATH = "/home/ubuntu/.openclaw/media/fasal-seva-ad-ss-1.png"

def generate_bg(prompt, outfile):
    # Using Imagen 3 for best text rendering
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={API_KEY}"
    # Fallback to fast
    # url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={API_KEY}"
    
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": "3:4", "outputOptions": {"mimeType": "image/png"}}
    }
    print(f"🎨 Generating Base: {outfile}...")
    try:
        r = requests.post(url, json=payload, timeout=60)
        data = r.json()
        if "predictions" in data:
            with open(outfile, "wb") as f:
                f.write(base64.b64decode(data["predictions"][0]["bytesBase64Encoded"]))
            return True
        else:
            print(f"Gen Failed, trying fast model... {data}")
            # Fallback
            url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={API_KEY}"
            r = requests.post(url, json=payload, timeout=60)
            data = r.json()
            if "predictions" in data:
                with open(outfile, "wb") as f:
                    f.write(base64.b64decode(data["predictions"][0]["bytesBase64Encoded"]))
                return True
    except Exception as e:
        print(f"Error: {e}")
    return False

def composite(bg_path, out_path):
    try:
        bg = Image.open(bg_path).convert("RGBA")
        ss = Image.open(SS_PATH).convert("RGBA")
        
        # Target: Center placement, vertical
        bg_w, bg_h = bg.size
        
        # Desired phone height is roughly 50-60% of the poster
        target_h = int(bg_h * 0.55)
        ratio = ss.width / ss.height
        target_w = int(target_h * ratio)
        ss = ss.resize((target_w, target_h))
        
        # Create a sleek phone frame
        border = 20
        frame = Image.new("RGBA", (target_w + 2*border, target_h + 2*border + 40), (20, 20, 20, 255)) # +40 for chin
        # Draw screen
        frame.paste(ss, (border, border))
        
        # Composite center
        x = (bg_w - frame.width) // 2
        y = (bg_h - frame.height) // 2 + 50 # Slightly lower to leave room for header text
        
        bg.paste(frame, (x, y), frame)
        bg.save(out_path)
        print(f"✅ Composite Saved: {out_path}")
    except Exception as e:
        print(f"Composite Error: {e}")

# --- PROMPTS BASED ON USER UPLOADS ---

# 1. "The Innovation" (Dark/Green Tech)
p1 = "High-quality vertical poster. Dark gradient background (black to deep green). Top text in bold white sans-serif: 'Fasal Seva: The Seed of Innovation'. Bottom text: 'Built by Students. Used by Farmers.' In the center, leave empty space for a smartphone. Glowing green tech lines and satellite icons in the background. Professional UI/UX portfolio style."
f1 = "/home/ubuntu/.openclaw/media/fasal_pro_innovation.png"

# 2. "The Smart Farm" (Clean/White)
p2 = "Clean vertical advertisement poster. White background. Top text in bold black: 'What if farmers could see their fields from space?'. Subtext in green: 'We made it happen.' Center empty space for phone. Bottom icons: Satellite, AI Voice, IoT Sensors. Minimalist Apple style."
f2 = "/home/ubuntu/.openclaw/media/fasal_pro_clean.png"

# 3. "The Hindi Direct" (Field/Nature)
p3 = "Vertical poster. Blurred green wheat field background. Top text in bold Hindi font (Devanagari): 'अब खेती होगी स्मार्ट'. Center empty space for phone. Bottom text in English: 'FREE for Indian Farmers'. High contrast, bright lighting."
f3 = "/home/ubuntu/.openclaw/media/fasal_pro_hindi.png"

jobs = [(p1, f1), (p2, f2), (p3, f3)]

for p, f in jobs:
    bg_temp = f.replace(".png", "_bg.png")
    if generate_bg(p, bg_temp):
        composite(bg_temp, f)
    time.sleep(3)
