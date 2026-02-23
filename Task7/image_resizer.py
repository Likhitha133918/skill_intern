import os
from PIL import Image

base_path = os.path.dirname(os.path.abspath(__file__))

input_folder = os.path.join(base_path, "input_folder")
output_folder = os.path.join(base_path, "output_images")

new_width = 800
new_height = 600
output_format = "JPEG"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Supported formats
supported_formats = (".jpg", ".jpeg", ".png", ".webp", ".bmp")

# Check if input folder exists
if not os.path.exists(input_folder):
    print(" Input folder not found!")
    print("Expected location:", input_folder)
    exit()

# Process images
for filename in os.listdir(input_folder):

    if filename.lower().endswith(supported_formats):

        input_path = os.path.join(input_folder, filename)

        try:
            with Image.open(input_path) as img:

                resized_img = img.resize((new_width, new_height))

                name_without_ext = os.path.splitext(filename)[0]
                output_filename = name_without_ext + "." + output_format.lower()
                output_path = os.path.join(output_folder, output_filename)

                resized_img.convert("RGB").save(output_path, output_format)

                print("Resized:", output_filename)

        except Exception as e:
            print(" Error processing", filename, ":", e)

print(" All images processed successfully!")