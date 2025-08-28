from PIL import Image, ImageDraw, ImageFont
import os

# File paths
image_path = "/Users/kewzeec/Downloads/exampleplan.jpg"
output_path = "/Users/kewzeec/Downloads/Annotated_Floorplan_Claude_Sonnet_4.jpg"

# Non-compliant areas with coordinates and issues
non_compliant_areas = [
    {"issue": "Front setback insufficient", "coordinates": [270, 314, 1030, 370]},
    {"issue": "Left side setback too small", "coordinates": [270, 314, 320, 610]},
    {"issue": "No defined parking/driveway turning area", "coordinates": [270, 610, 980, 780]},
    {"issue": "Narrow staircase - fire safety concern", "coordinates": [460, 360, 490, 430]},
    {"issue": "Potential ventilation issues in interior rooms", "coordinates": [320, 430, 420, 520]},
    {"issue": "Secondary emergency exit not clearly defined", "coordinates": [850, 430, 980, 520]}
]

def annotate_floor_plan():
    try:
        # Load the image
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        
        # Try to load a font, fall back to default if not available
        try:
            font = ImageFont.truetype("Arial", 12)
        except:
            font = ImageFont.load_default()
        
        # Colors
        box_color = "red"
        text_color = "red"
        text_bg_color = "white"
        
        # Draw bounding boxes and labels
        for i, area in enumerate(non_compliant_areas):
            coords = area["coordinates"]
            issue = area["issue"]
            
            # Draw rectangle
            draw.rectangle(coords, outline=box_color, width=3)
            
            # Prepare label text
            label = f"{i+1}. {issue}"
            
            # Get text bounding box for background
            text_bbox = draw.textbbox((0, 0), label, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Position text near the top-left of the bounding box
            text_x = coords[0]
            text_y = coords[1] - text_height - 5
            
            # Ensure text stays within image bounds
            if text_y < 0:
                text_y = coords[1] + 5
            if text_x + text_width > image.width:
                text_x = image.width - text_width - 10
            
            # Draw text background
            draw.rectangle([text_x - 2, text_y - 2, text_x + text_width + 2, text_y + text_height + 2], 
                         fill=text_bg_color, outline=box_color)
            
            # Draw text
            draw.text((text_x, text_y), label, fill=text_color, font=font)
            
            # Draw number in circle at corner of bounding box
            circle_radius = 15
            circle_center = (coords[0] + circle_radius, coords[1] + circle_radius)
            draw.ellipse([circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                         circle_center[0] + circle_radius, circle_center[1] + circle_radius],
                        fill=box_color, outline="darkred", width=2)
            
            # Draw number in circle
            number_str = str(i + 1)
            number_bbox = draw.textbbox((0, 0), number_str, font=font)
            number_width = number_bbox[2] - number_bbox[0]
            number_height = number_bbox[3] - number_bbox[1]
            draw.text((circle_center[0] - number_width//2, circle_center[1] - number_height//2),
                     number_str, fill="white", font=font)
        
        # Save the annotated image
        image.save(output_path, quality=95)
        print(f"Annotated floor plan saved to: {output_path}")
        
        # Print summary
        print("\nCompliance Issues Found:")
        for i, area in enumerate(non_compliant_areas):
            print(f"{i+1}. {area['issue']}")
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Could not find image file at {image_path}")
        return False
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return False

# Run the annotation
if __name__ == "__main__":
    success = annotate_floor_plan()
    if success:
        print("\nFloor plan successfully annotated with compliance issues.")
    else:
        print("\nFailed to annotate floor plan. Please check file paths and permissions.")