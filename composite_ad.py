from PIL import Image, ImageOps, ImageDraw

# Paths
bg_path = "/home/ubuntu/.openclaw/media/fasal_cinematic_shield.png"
ss_path = "/home/ubuntu/.openclaw/media/fasal-seva-ad-ss-1.png" # Assuming this is the main map view
out_path = "/home/ubuntu/.openclaw/media/fasal_final_ad.png"

try:
    # Load images
    bg = Image.open(bg_path).convert("RGBA")
    ss = Image.open(ss_path).convert("RGBA")

    # Resize background to standard post size if needed (e.g. 1024x1024)
    bg = bg.resize((1024, 1024))

    # Resize screenshot to fit nicely (e.g. phone size)
    # Let's make it look like a floating phone in the center-right or just center
    # Target height: 60% of background
    ss_ratio = ss.width / ss.height
    new_h = int(1024 * 0.75)
    new_w = int(new_h * ss_ratio)
    ss = ss.resize((new_w, new_h))

    # Add a black phone border (rounded rectangle feeling)
    border = 20
    phone = Image.new("RGBA", (new_w + 2*border, new_h + 2*border), (20, 20, 20, 255))
    # Paste screenshot inside
    phone.paste(ss, (border, border))
    
    # Place phone in the center (or slightly offset if the farmer is on one side)
    # Assuming centered for safety
    bg_w, bg_h = bg.size
    ph_w, ph_h = phone.size
    x = (bg_w - ph_w) // 2
    y = (bg_h - ph_h) // 2

    # Paste phone onto background (with alpha composite)
    bg.paste(phone, (x, y), phone)

    # Save
    bg.convert("RGB").save(out_path)
    print(f"✅ Composite created: {out_path}")

except Exception as e:
    print(f"❌ Error compositing: {e}")
