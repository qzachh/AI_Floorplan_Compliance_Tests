from PIL import Image, ImageDraw, ImageFont

# --- Inputs ---
IMAGE_PATH = "/Users/kewzeec/Downloads/pueblo-mio-planta-baja-6.jpg"  # update if your path differs
OUTPUT_PATH = "/Users/kewzeec/Downloads/annotated_non_compliant_front_setback.png"

# --- Load and inspect image ---
img = Image.open(IMAGE_PATH).convert("RGBA")
W, H = img.size
print("Image size:", (W, H))  # Should print (1414, 1000)

# --- Non-compliant area bounding box (inside image bounds) ---
# Bottom-right curved entrance area (assumed nearest to front boundary)
NON_COMPLIANT_BOX = (1080, 760, 1330, 960)  # (x1, y1, x2, y2)

# --- Draw overlay ---
overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Very visible semi-transparent red fill + thick outline
draw.rectangle(NON_COMPLIANT_BOX, fill=(255, 0, 0, 110), outline=(255, 0, 0, 255), width=12)

# Callout line + label (to make it obvious on any viewer background)
x1, y1, x2, y2 = NON_COMPLIANT_BOX
callout_start = (x2, (y1 + y2) // 2)
callout_mid = (x2 + 20, (y1 + y2) // 2 - 30)
callout_end = (min(W - 10, x2 + 160), min(H - 10, (y1 + y2) // 2 - 60))
draw.line([callout_start, callout_mid, callout_end], fill=(255, 0, 0, 255), width=6)

try:
    font = ImageFont.load_default()
except:
    font = None

label = "Nearest point to assumed front boundary (non-compliant)"
# Nudge label so it stays on-canvas
label_x = max(10, callout_end[0] - 155)
label_y = max(10, callout_end[1] - 18)
draw.text((label_x, label_y), label, fill=(255, 0, 0, 255), font=font)

# --- Merge and save ---
annotated = Image.alpha_composite(img, overlay)
annotated.save(OUTPUT_PATH)

print(f"Saved annotated image to: {OUTPUT_PATH}")