import requests, json, sys, base64

API_KEY = "AIzaSyDow1UVPt93h9wtV6VBNia4w5LpoHMThdE"

def generate_ultra(prompt, outfile):
    # Try Imagen 3 first (better photorealism)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={API_KEY}"
    
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "1:1",
            "outputOptions": {"mimeType": "image/png"}
        }
    }
    print(f"🎨 Generating ULTRA: {outfile}...")
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
            print(f"❌ Failed (Trying Fast Model): {data}")
            # Fallback
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

# --- THE NEW CINEMATIC PROMPT ---
prompt = "A hyper-realistic, cinematic wide shot of an Indian farmer standing in a golden wheat field at sunset, holding a smartphone. A glowing green holographic shield surrounds the crops, displaying icons for 'Rain', 'Pests', and 'Money'. Text overlay in elegant gold Hindi font: 'फसल सेवा - किसानों का डिजिटल साथी'. 8k resolution, National Geographic style, warm lighting."
outfile = "/home/ubuntu/.openclaw/media/fasal_cinematic_shield.png"

if __name__ == "__main__":
    generate_ultra(prompt, outfile)
