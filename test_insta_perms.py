import requests, json

token = "EAAVZC3DLbbioBQz8rUMeAyZBCmoFQJL5GVpl3wxhLqQOLtnjK8GgR8Xnl6x3CRu0dVBhLroZCJ7WgqjGEyWhgKnk8Up2mDWHcMzdlZBvyjV6ZAEZANZAZCkKmO2R3fyg5TfyQRjs4S5ZAk7OL1Uz7qmDtUmZBufIN8xmAj4vo1yUfrQwBA81yV5i0YcXH9rSxg"

# Get permissions
print("Checking permissions...")
try:
    r = requests.get("https://graph.facebook.com/v21.0/me/permissions", params={"access_token": token})
    if r.status_code != 200:
        print(f"Error fetching permissions: {r.text}")
    else:
        perms = r.json().get("data", [])
        insta_perms = [p for p in perms if "instagram" in p["permission"]]
        print("Instagram Permissions:")
        for p in insta_perms:
            print(f"  {p['permission']}: {p['status']}")
except Exception as e:
    print(f"Exception during permission check: {e}")

# Get Instagram account info
print("\nChecking Instagram Account...")
try:
    r2 = requests.get("https://graph.facebook.com/v21.0/17841480076010977", params={"access_token": token, "fields": "id,username,name,profile_picture_url,followers_count,media_count"})
    if r2.status_code != 200:
        print(f"Error fetching account info: {r2.text}")
    else:
        print("Instagram Account:", json.dumps(r2.json(), indent=2))
except Exception as e:
    print(f"Exception during account check: {e}")
