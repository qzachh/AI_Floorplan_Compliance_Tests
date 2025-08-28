
from PIL import Image, ImageDraw, ImageFont
import json

# Load the floor plan image
image_path = "/Users/kewzeec/Downloads/exampleplan.jpg"
output_path = "/Users/kewzeec/Downloads/Annotated_Floorplan_Perplexity(Claude).jpg"

# Open the image
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# Define the non-compliance issues with coordinates
issues = [
    {"issue": "Insufficient side setback - building too close to boundary", "coordinates": [270, 315, 1030, 600]},
    {"issue": "Insufficient front setback from road", "coordinates": [270, 315, 1030, 400]},
    {"issue": "Insufficient natural ventilation for internal bedroom", "coordinates": [500, 400, 650, 520]},
    {"issue": "Excessive travel distance to fire exit", "coordinates": [650, 400, 900, 520]},
    {"issue": "Staircase width insufficient for fire safety", "coordinates": [420, 440, 480, 520]},
    {"issue": "Site coverage may exceed 50% limit", "coordinates": [270, 315, 1030, 600]}
]

# Define colors for different issue types
colors = ["red", "orange", "yellow", "magenta", "cyan", "green"]

# Try to load a font, fallback to default if not available
try:
    font = ImageFont.truetype("arial.ttf", 12)
except:
    font = ImageFont.load_default()

# Draw rectangles and labels for each issue
for i, issue_data in enumerate(issues):
    x1, y1, x2, y2 = issue_data["coordinates"]
    color = colors[i % len(colors)]

    # Draw rectangle
    draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

    # Create label
    label = f"{i+1}. {issue_data['issue'][:30]}..."

    # Draw label background
    text_bbox = draw.textbbox((x1, y1-20), label, font=font)
    draw.rectangle(text_bbox, fill=color, outline=color)

    # Draw label text
    draw.text((x1, y1-20), label, fill="white", font=font)

# Add legend
legend_x, legend_y = 50, 50
legend_items = [
    "1. Side setback violation",
    "2. Front setback violation", 
    "3. Ventilation issue",
    "4. Fire exit distance",
    "5. Staircase width",
    "6. Site coverage limit"
]

# Draw legend background
legend_height = len(legend_items) * 25 + 20
draw.rectangle([legend_x-10, legend_y-10, legend_x+250, legend_y+legend_height], 
               fill="white", outline="black", width=2)

# Draw legend title
draw.text((legend_x, legend_y), "COMPLIANCE ISSUES:", fill="black", font=font)

# Draw legend items
for i, item in enumerate(legend_items):
    y_pos = legend_y + 20 + (i * 20)
    color = colors[i % len(colors)]

    # Draw color indicator
    draw.rectangle([legend_x, y_pos, legend_x+15, y_pos+15], fill=color, outline=color)

    # Draw text
    draw.text((legend_x+20, y_pos), item, fill="black", font=font)

# Save the annotated image
image.save(output_path)
print(f"Annotated floor plan saved to: {output_path}")

# Display summary
print("\nCOMPLIANCE ANNOTATION COMPLETE")
print("=" * 40)
print(f"Total issues marked: {len(issues)}")
print("Each issue is marked with a colored rectangle and numbered for reference.")
