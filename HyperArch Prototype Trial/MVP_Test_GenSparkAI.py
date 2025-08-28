from PIL import Image, ImageDraw, ImageFont
import os

# Load the image
image_path = "/Users/kewzeec/Downloads/exampleplan.jpg"
output_path = "/Users/kewzeec/Downloads/Annotated_Floorplan_GenSparkAI.jpg"

# Open the image
img = Image.open(image_path)
draw = ImageDraw.Draw(img)

# Try to load a font, fallback to default if not available
try:
    font = ImageFont.truetype("Arial.ttf", 12)
except:
    font = ImageFont.load_default()

# Define non-compliant areas with coordinates and labels
issues = [
    {"issue": "No parking provision shown", "coordinates": [200, 500, 400, 650]},
    {"issue": "Missing setback dimensions - front", "coordinates": [130, 200, 810, 250]},
    {"issue": "Missing setback dimensions - rear", "coordinates": [130, 480, 810, 520]},
    {"issue": "Missing setback dimensions - left", "coordinates": [130, 200, 180, 520]},
    {"issue": "Missing setback dimensions - right", "coordinates": [760, 200, 810, 520]},
    {"issue": "No fire escape route marked", "coordinates": [300, 280, 700, 450]}
]

# Draw red rectangles and labels for each non-compliant area
for i, item in enumerate(issues):
    coords = item["coordinates"]
    issue_text = item["issue"]
    
    # Draw red rectangle
    draw.rectangle(coords, outline="red", width=3)
    
    # Calculate text position (above the rectangle)
    text_x = coords[0]
    text_y = coords[1] - 20 if coords[1] > 20 else coords[1] + 5
    
    # Draw issue number and text
    label = f"{i+1}. {issue_text}"
    
    # Draw text background for better readability
    bbox = draw.textbbox((text_x, text_y), label, font=font)
    draw.rectangle([bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2], fill="white", outline="red")
    
    # Draw the text
    draw.text((text_x, text_y), label, fill="red", font=font)

# Add legend
legend_text = "COMPLIANCE ISSUES:\n1. No parking provision\n2-5. Missing setback dimensions\n6. No fire escape routes marked"
draw.text((20, 20), legend_text, fill="red", font=font)

# Save the annotated image
img.save(output_path)
print(f"Annotated floor plan saved to: {output_path}")
