# from PIL import Image, ImageDraw, ImageFont
# import os

# def generate_image_from_text(text, output_image_path, font_size=28, image_size=(800, 700), bg_color=(255, 255, 255), text_color=(0, 0, 0)):
#     image = Image.new("RGB", image_size, bg_color)
#     draw = ImageDraw.Draw(image)
#     font = ImageFont.truetype("arial.ttf", font_size)  # You can specify your own font here if needed
#     draw.text((10, 10), text, fill=text_color, font=font)
#     image.save(output_image_path)

# def generate_images_from_text_file(input_text_file, output_folder):
#     with open(input_text_file, 'r') as file:
#         data = file.read()

#     samples = data.split("//")

#     # Create the output folder if it doesn't exist
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     for i, sample in enumerate(samples):
#         if sample.strip():  # Skip empty samples
#             output_image_path = os.path.join(output_folder, f"paperNotes_{i}.png")
#             generate_image_from_text(sample.strip(), output_image_path)

# # Example usage
# input_text_file = "fake_data.txt"
# output_folder = "output_images"

# generate_images_from_text_file(input_text_file, output_folder)


from PIL import Image, ImageDraw, ImageFont
import os

def generate_image_from_text(text, output_image_path, font_size=28, image_size=(800, 700), bg_color=(255, 255, 255), text_color=(0, 0, 0)):
    image = Image.new("RGB", image_size, bg_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", font_size)  # You can specify your own font here if needed
    draw.text((10, 10), text, fill=text_color, font=font)
    image.save(output_image_path)

def generate_images_from_text_file(input_text_file, output_folder, start_index=250, end_index=500):
    with open(input_text_file, 'r') as file:
        data = file.read()

    samples = data.split("//")

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, sample in enumerate(samples, start=start_index):
        if sample.strip():  # Skip empty samples
            output_image_path = os.path.join(output_folder, f"paperNote_{i}.png")
            generate_image_from_text(sample.strip(), output_image_path)

# Example usage
input_text_file = "fake_data.txt"
output_folder = "output_images"

generate_images_from_text_file(input_text_file, output_folder, start_index=250, end_index=500)
