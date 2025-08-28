from PIL import Image, ImageDraw, ImageFont
import json

# Define input and output paths
image_path = "/Users/kewzeec/Downloads/exampleplan.jpg"
output_path = "/Users/kewzeec/Downloads/Annotated_Floorplan_Qwen.jpg"

# Load image
img = Image.open(image_path)
draw = ImageDraw.Draw(img)

# Define font (use default if custom font not available)
try:
    font = ImageFont.truetype("arial.ttf", 16)
except:
    font = ImageFont.load_default()

# List of non-compliant issues with coordinates
non_compliant_issues = [
    {"issue": "Driveway too narrow and lacks proper turning radius", "coordinates": [350, 700, 450, 780]},
    {"issue": "No dedicated parking area", "coordinates": [750, 670, 850, 750]},
    {"issue": "No ventilation in bedroom", "coordinates": [300, 380, 410, 490]},
    {"issue": "Insufficient ventilation in bathroom", "coordinates": [430, 460, 490, 520]}
]

# Draw red rectangles and labels
for item in non_compliant_issues:
    x1, y1, x2, y2 = item["coordinates"]
    # Draw red rectangle
    draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
    # Add label
    text = item["issue"]
    draw.text((x1, y1 - 20), text, fill="red", font=font)

# Save annotated image
img.save(output_path)
print(f"Annotated image saved to {output_path}")