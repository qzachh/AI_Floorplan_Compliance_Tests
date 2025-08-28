from PIL import Image, ImageDraw

# Reload the original plan
img_path = '/Users/kewzeec/Downloads/exampleplan.jpg'
img = Image.open(img_path)

# Create drawing overlay
draw = ImageDraw.Draw(img)

# Example highlights (approximate coordinates)
# Parking/Driveway missing
parking_box = [(150, 1150), (450, 1350)]
draw.rectangle(parking_box, outline="red", width=5)
draw.text((150, 1120), "No driveway/parking", fill="red")

# Setback unclear (top boundary)
setback_line = [(50, 50), (1050, 50)]
draw.line(setback_line, fill="red", width=5)
draw.text((60, 30), "Setback not dimensioned", fill="red")

# Single escape route (entrance)
escape_box = [(880, 950), (1050, 1100)]
draw.rectangle(escape_box, outline="red", width=5)
draw.text((880, 920), "Single exit point", fill="red")

# Save annotated output
output_path = '/Users/kewzeec/Downloads/Annotated_Floorplan.jpg'
img.save(output_path)

output_path
