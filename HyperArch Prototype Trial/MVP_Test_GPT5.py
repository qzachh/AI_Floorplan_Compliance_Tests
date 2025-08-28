from PIL import Image, ImageDraw, ImageFont
import os

# ---- Inputs ----
image_path = "/Users/kewzeec/Downloads/exampleplan.jpg"
model_name = "GPT-5 Thinking"
output_path = f"/Users/kewzeec/Downloads/Annotated_Floorplan_{model_name}.jpg"

# Non-compliance boxes (copy/paste from JSON above)
boxes = [
    {"issue": "Internal bathroom lacks window/MV", "coordinates": [540, 445, 595, 500]},
    {"issue": "Internal bathroom lacks window/MV", "coordinates": [665, 445, 725, 500]},
    {"issue": "Internal bathroom lacks window/MV", "coordinates": [790, 445, 850, 505]},
    {"issue": "Common WC lacks window/MV", "coordinates": [385, 560, 450, 620]},
    {"issue": "Pool setback risk (<2.0m) — verify", "coordinates": [315, 95, 760, 200]}
]

# ---- Draw ----
im = Image.open(image_path).convert("RGB")
draw = ImageDraw.Draw(im)

# Try a basic font; will fall back if not found
try:
    font = ImageFont.truetype("arial.ttf", 18)
except:
    font = ImageFont.load_default()

for b in boxes:
    x1, y1, x2, y2 = b["coordinates"]
    # rectangle
    draw.rectangle([x1, y1, x2, y2], outline="red", width=4)
    # label background
    text = b["issue"]
    tw, th = draw.textbbox((0,0), text, font=font)[2:]
    pad = 4
    # place label at top-left of the box
    label_rect = [x1, max(0, y1 - th - 2*pad), x1 + tw + 2*pad, y1]
    draw.rectangle(label_rect, fill="red")
    draw.text((label_rect[0] + pad, label_rect[1] + pad), text, fill="white", font=font)

# ---- Save ----
im.save(output_path, quality=95)
print(f"Saved: {output_path}")
