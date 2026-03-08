import requests
import json
import sys

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

# Post IDs (from previous successful deployments)
POST_IDS = [
    "933913235994488",  # Video Post (Note: Video object ID might differ from Feed Post ID, but let's try direct)
    "954024617136247"   # Image Post
]

def check_engagement():
    print("📊 Checking Engagement Metrics...")
    
    for pid in POST_IDS:
        # Construct the full ID (PageID_PostID) usually required for Feed API, 
        # but sometimes Object ID works directly for likes. Let's try Object ID first.
        
        # Try fetching likes summary
        url = f"{FB_GRAPH_URL}/{pid}?fields=likes.summary(true),comments.summary(true),shares&access_token={PAGE_ACCESS_TOKEN}"
        
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                data = r.json()
                likes = data.get('likes', {}).get('summary', {}).get('total_count', 0)
                comments = data.get('comments', {}).get('summary', {}).get('total_count', 0)
                shares = data.get('shares', {}).get('count', 0)
                
                print(f"🔹 Post ID: {pid}")
                print(f"   👍 Likes: {likes}")
                print(f"   💬 Comments: {comments}")
                print(f"   🔄 Shares: {shares}")
            else:
                # If direct ID fails, try PageID_PostID format (common FB Graph requirement)
                full_id = f"{PAGE_ID}_{pid}"
                url2 = f"{FB_GRAPH_URL}/{full_id}?fields=likes.summary(true),comments.summary(true),shares&access_token={PAGE_ACCESS_TOKEN}"
                r2 = requests.get(url2, timeout=30)
                if r2.status_code == 200:
                    data = r2.json()
                    likes = data.get('likes', {}).get('summary', {}).get('total_count', 0)
                    comments = data.get('comments', {}).get('summary', {}).get('total_count', 0)
                    shares = data.get('shares', {}).get('count', 0)
                    
                    print(f"🔹 Post ID: {full_id} (via Composite ID)")
                    print(f"   👍 Likes: {likes}")
                    print(f"   💬 Comments: {comments}")
                    print(f"   🔄 Shares: {shares}")
                else:
                    print(f"❌ Failed to fetch {pid}: {r.status_code} / {r2.status_code}")
                    # print(r.text) # Debug only
        except Exception as e:
            print(f"❌ Error checking {pid}: {e}")

if __name__ == "__main__":
    check_engagement()
