from PIL import Image, ImageDraw, ImageFont

# Define paths
image_path = "/Users/kewzeec/Downloads/exampleplan.jpg"
output_path = "/Users/kewzeec/Downloads/Annotated_Floorplan_DeepSeek.jpg"  # Replaced [model_name]

# Load the image
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# Try to load a font, use default if not available
try:
    font = ImageFont.truetype("arial.ttf", 20)
except IOError:
    font = ImageFont.load_default()
    print("Default font used; for better labels, ensure 'arial.ttf' is available.")

# Define issues and their coordinates (You MUST adjust these coordinates!)
# Tip: Use image.size to get its dimensions (width, height) and estimate positions.
issues = [
    {"issue": "Driveway lacks turning radius (min. 6m required)", "coordinates": [50, 150, 250, 200]},
    {"issue": "Habitable room (J) has no ventilation opening", "coordinates": [400, 50, 550, 150]}
]

# Draw bounding boxes and labels for each issue
for item in issues:
    coords = item["coordinates"]
    label = item["issue"]
    
    # Draw the red rectangle
    draw.rectangle(coords, outline="red", width=3)
    
    # Calculate position for the label (just above the top-left of the box)
    text_x = coords[0]
    text_y = coords[1] - 25  # Place text 25 pixels above the box
    # Ensure text doesn't go off the top of the image
    if text_y < 0:
        text_y = coords[3] + 5  # If it does, place it below the box
    
    # Draw a white background for the text for better readability
    text_bbox = draw.textbbox((text_x, text_y), label, font=font)
    padding = 2
    draw.rectangle(
        [text_bbox[0] - padding, text_bbox[1] - padding, text_bbox[2] + padding, text_bbox[3] + padding],
        fill="white"
    )
    # Draw the text
    draw.text((text_x, text_y), label, fill="red", font=font)

# Save the annotated image
image.save(output_path)
print(f"Annotated image saved to: {output_path}")
print("Please note: You may need to adjust the 'coordinates' in the code to match the features in your specific image.")