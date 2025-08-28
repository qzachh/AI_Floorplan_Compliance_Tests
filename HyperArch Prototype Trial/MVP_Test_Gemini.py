from PIL import Image, ImageDraw, ImageFont

def annotate_floor_plan(image_path, output_path, non_compliant_areas):
    """
    Loads a floor plan image, draws bounding boxes and labels for non-compliant
    areas, and saves the annotated image.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the annotated output image.
        non_compliant_areas (list): A list of dictionaries, each containing
                                    an 'issue' and 'coordinates'.
    """
    try:
        # Load the base image
        base_image = Image.open(image_path).convert("RGBA")
        draw = ImageDraw.Draw(base_image)

        # Try to load a font, otherwise use the default
        try:
            # You may need to change the font path depending on your system
            font = ImageFont.truetype("Arial.ttf", 15)
        except IOError:
            print("Arial font not found. Using default font.")
            font = ImageFont.load_default()

        # Loop through each non-compliant issue
        for area in non_compliant_areas:
            coords = area["coordinates"]
            issue_text = area["issue"]

            # Draw the red bounding box
            draw.rectangle(coords, outline="red", width=2)

            # Create a small background for the text for better readability
            text_position = (coords[0], coords[1] - 20) # Position text above the box
            text_bbox = draw.textbbox(text_position, issue_text, font=font)
            
            # Add a small padding to the text background
            text_bg_coords = (text_bbox[0] - 2, text_bbox[1] - 2, text_bbox[2] + 2, text_bbox[3] + 2)
            draw.rectangle(text_bg_coords, fill="black")
            
            # Draw the text label
            draw.text(text_position, issue_text, fill="white", font=font)

        # Save the final annotated image
        base_image.convert("RGB").save(output_path)
        print(f"Annotated image saved successfully to: {output_path}")

    except FileNotFoundError:
        print(f"Error: The file was not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # --- Input Data ---
    
    # Paths for input and output images
    image_path = "/Users/kewzeec/Downloads/exampleplan.jpg"
    output_path = "/Users/kewzeec/Downloads/Annotated_Floorplan_Gemini.jpg"

    # JSON data for non-compliant areas
    non_compliant_data = [
      {
        "issue": "Lack of natural ventilation",
        "coordinates": [285, 478, 385, 614]
      },
      {
        "issue": "Lack of natural ventilation",
        "coordinates": [467, 478, 520, 614]
      },
      {
        "issue": "Lack of natural ventilation",
        "coordinates": [595, 478, 647, 614]
      },
      {
        "issue": "Lack of natural ventilation",
        "coordinates": [610, 650, 675, 725]
      },
      {
        "issue": "Excessive travel distance to exit (>20m)",
        "coordinates": [230, 365, 385, 478]
      },
      {
        "issue": "Insufficient side and rear setbacks (<2m)",
        "coordinates": [205, 345, 1295, 365]
      },
      {
        "issue": "Insufficient front setback (<7.5m)",
        "coordinates": [205, 740, 1295, 765]
      },
      {
        "issue": "Insufficient parking maneuvering space",
        "coordinates": [1080, 770, 1270, 890]
      }
    ]

    # Run the annotation function
    annotate_floor_plan(image_path, output_path, non_compliant_data)