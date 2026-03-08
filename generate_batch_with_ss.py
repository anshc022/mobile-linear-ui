import requests, base64, time
from PIL import Image, ImageOps

API_KEY = "AIzaSyDow1UVPt93h9wtV6VBNia4w5LpoHMThdE"
SS_PATH = "/home/ubuntu/.openclaw/media/fasal-seva-ad-ss-1.png"

# 1. GENERATE BACKGROUNDS
def generate_bg(prompt, outfile):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={API_KEY}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": "1:1", "outputOptions": {"mimeType": "image/png"}}
    }
    print(f"🎨 Generating BG: {outfile}...")
    try:
        r = requests.post(url, json=payload, timeout=60)
        data = r.json()
        if "predictions" in data:
            with open(outfile, "wb") as f:
                f.write(base64.b64decode(data["predictions"][0]["bytesBase64Encoded"]))
            return True
    except Exception as e:
        print(f"Error: {e}")
    return False

# 2. COMPOSITE
def composite(bg_path, out_path):
    try:
        bg = Image.open(bg_path).convert("RGBA")
        ss = Image.open(SS_PATH).convert("RGBA")
        
        # Resize SS to be appropriate size (e.g. 65% of height)
        bg = bg.resize((1024, 1024))
        target_h = int(1024 * 0.65)
        ratio = ss.width / ss.height
        target_w = int(target_h * ratio)
        ss = ss.resize((target_w, target_h))
        
        # Add border (Phone frame)
        border = 25
        frame = Image.new("RGBA", (target_w + 2*border, target_h + 2*border), (10, 10, 10, 255))
        frame.paste(ss, (border, border))
        
        # Center it
        bg_w, bg_h = bg.size
        fw, fh = frame.size
        x = (bg_w - fw) // 2
        y = (bg_h - fh) // 2
        
        bg.paste(frame, (x, y), frame)
        bg.convert("RGB").save(out_path)
        print(f"✅ Composite Saved: {out_path}")
    except Exception as e:
        print(f"Composite Error: {e}")

# --- EXECUTE ---
prompts = [
    ("A photorealistic close-up of a hand holding a generic black smartphone in the center of the frame. Background is a beautiful blurred green wheat field in India. Soft sunlight.", "/home/ubuntu/.openclaw/media/fasal_post_1_field.png"),
    ("A flat-lay photography style. A smartphone lying on a rustic wooden table next to fresh vegetables and soil samples. The phone screen is facing up in the center.", "/home/ubuntu/.openclaw/media/fasal_post_2_table.png"),
    ("A modern digital art style poster. A smartphone floating in the center with a glowing green digital aura. Background is a high-tech data grid map of a farm.", "/home/ubuntu/.openclaw/media/fasal_post_3_tech.png")
]

for p, path in prompts:
    bg_temp = path.replace(".png", "_bg.png")
    if generate_bg(p, bg_temp):
        composite(bg_temp, path)
    time.sleep(2)

