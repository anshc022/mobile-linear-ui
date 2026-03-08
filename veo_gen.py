import requests
import json
import time
import sys
import base64
import os

API_KEY = "AIzaSyDow1UVPt93h9wtV6VBNia4w5LpoHMThdE"
MODEL = "veo-3.0-fast-generate-001"
# MODEL = "veo-2.0-generate-001" # Alternative if 3.0 fails

def generate_video(prompt, output_file, image_path=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:predictLongRunning?key={API_KEY}"
    
    inputs = [{"text": prompt}]
    
    if image_path:
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode("utf-8")
            inputs.append({
                "inlineData": {
                    "mimeType": "image/png",
                    "data": img_b64
                }
            })
            print(f"🖼️  Attached image: {image_path}")
        else:
            print(f"⚠️  Image not found: {image_path}")

    payload = {
        "instances": [
            {
                "prompt": prompt
            }
        ],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9"
        }
    }

    print(f"🚀 Sending request to {MODEL}...")
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        op_data = response.json()
        
        op_name = op_data.get("name")
        if not op_name:
            print("❌ No operation name returned.")
            print(op_data)
            return

        print(f"⏳ Operation started: {op_name}")
        
        # Poll for completion
        while True:
            time.sleep(5)
            poll_url = f"https://generativelanguage.googleapis.com/v1beta/{op_name}?key={API_KEY}"
            poll_resp = requests.get(poll_url)
            poll_data = poll_resp.json()
            
            if poll_data.get("done"):
                print("✅ Generation complete!")
                if "error" in poll_data:
                    print(f"❌ Error in operation: {poll_data['error']}")
                    return
                
                # Extract video URI
                # The response structure can vary, usually response.result.videos[0].uri
                try:
                    # Check for generateVideoResponse (Veo style)
                    if "response" in poll_data:
                        response_data = poll_data["response"]
                        # Handle type.googleapis.com wrapper if present (implicitly handled by dict access?)
                        # Direct access
                        if "generateVideoResponse" in response_data:
                            video_uri = response_data["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
                            print(f"⬇️  Downloading video from {video_uri}...")
                            vid_data = requests.get(video_uri).content
                            with open(output_file, "wb") as f:
                                f.write(vid_data)
                            print(f"💾 Saved to {output_file}")
                            return

                    # Check different possible paths
                    # Standard: response -> result -> videos -> uri
                    # Or: response -> response -> videos...
                    
                    # Inspect the payload structure in 'response' key if present
                    res_payload = poll_data.get("response")
                    if not res_payload:
                        # Sometimes it's directly in metadata or elsewhere?
                        # For now, let's dump if we can't find it
                        print("⚠️  No 'response' field in done operation.")
                        print(poll_data)
                        return

                    # Handle case where 'result' might be wrapped
                    predictions = res_payload.get("predictions") # Vertex style?
                    # Or candidates?
                    
                    # Let's try to find the video bytes or URI
                    # For some Gemini video endpoints, it returns a URI to download
                    
                    # Common pattern for Veo on this API:
                    video_uri = None
                    if "videos" in res_payload:
                        video_uri = res_payload["videos"][0]["uri"]
                    elif "predictions" in res_payload:
                         # Sometimes it returns base64 directly?
                         pass
                    
                    # If we have a URI, download it
                    if video_uri:
                        print(f"⬇️  Downloading video from {video_uri}...")
                        vid_data = requests.get(video_uri).content
                        with open(output_file, "wb") as f:
                            f.write(vid_data)
                        print(f"💾 Saved to {output_file}")
                        return
                    
                    # Fallback check for assets/bytes
                    print("⚠️  Could not find video URI in response.")
                    print(poll_data)
                    return

                except Exception as e:
                    print(f"❌ Error parsing result: {e}")
                    print(poll_data)
                    return
            
            print(".", end="", flush=True)

    except Exception as e:
        print(f"❌ Request failed: {e}")
        if 'response' in locals():
            print(response.text)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python veo_gen.py <prompt> <output.mp4> [image_path]")
        sys.exit(1)
    
    prompt = sys.argv[1]
    output = sys.argv[2]
    img = sys.argv[3] if len(sys.argv) > 3 else None
    
    generate_video(prompt, output, img)
