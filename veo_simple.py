import requests, json, sys, os

API_KEY = "AIzaSyDow1UVPt93h9wtV6VBNia4w5LpoHMThdE"
MODEL = "veo-3.0-fast-generate-001"

def generate_video(prompt, output_file):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predictLongRunning?key={API_KEY}"
    
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9" # 16:9 or 9:16
        }
    }

    print(f"🚀 Requesting {MODEL}...")
    try:
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        op_name = r.json().get("name")
        print(f"⏳ Op: {op_name}")
        
        while True:
            time.sleep(5)
            poll = requests.get(f"https://generativelanguage.googleapis.com/v1beta/{op_name}?key={API_KEY}").json()
            if poll.get("done"):
                # Handle response structure
                if "response" in poll:
                    vid_uri = poll["response"].get("generateVideoResponse", {}).get("generatedSamples", [{}])[0].get("video", {}).get("uri")
                    if vid_uri:
                        print(f"⬇️ Downloading: {vid_uri}")
                        # Important: Append API Key to download URL if needed? Usually not for public bucket but let's see.
                        # Actually, previous success required appending key? No, curl worked with key in params?
                        # The URI usually has a token or is public for short time.
                        # Let's try direct first.
                        v_data = requests.get(vid_uri).content
                        with open(output_file, "wb") as f:
                            f.write(v_data)
                        print(f"✅ Saved: {output_file}")
                        return
                print("❌ Failed to extract video URI.")
                print(poll)
                return
            print(".", end="", flush=True)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import time
    if len(sys.argv) < 3:
        print("Usage: python3 veo_simple.py <prompt> <output.mp4>")
        sys.exit(1)
    generate_video(sys.argv[1], sys.argv[2])
