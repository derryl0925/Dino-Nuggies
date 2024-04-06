import tensorflow as tf
from PIL import Image
import numpy as np
import os

# Function to find image by name
def find_image(images_folder, name):
    for folder_name in os.listdir(images_folder):
        if name.lower() in folder_name.lower():
            dino_image_path = os.path.join(images_folder, folder_name, '2.png')
            if os.path.exists(dino_image_path):
                return Image.open(dino_image_path)
    return None

# Function to blend two images
def blend_images(image1, image2):
    # Get the minimum dimensions of both images
    min_width = min(image1.width, image2.width)
    min_height = min(image1.height, image2.height)
    
    # Resize both images to have the same dimensions
    resized_image1 = image1.resize((min_width, min_height))
    resized_image2 = image2.resize((min_width, min_height))
    
    # Convert images to numpy arrays
    arr1 = np.array(resized_image1)
    arr2 = np.array(resized_image2)
    
    # Blend images
    blended_image = (arr1 + arr2) // 2
    
    # Convert back to PIL image
    return Image.fromarray(blended_image.astype(np.uint8))

def generate_new_name(name1, name2):
    # Combine names creatively
    new_name = f"{name1.capitalize()}-{name2.capitalize()}"
    return new_name

def generate_new_image(dino1_image, dino2_image, dino1_name, dino2_name):
    # Blend two dinosaur images
    blended_image = blend_images(dino1_image, dino2_image)
    
    # Generate new dinosaur name
    new_dino_name = generate_new_name(dino1_name, dino2_name)
    
    return blended_image, new_dino_name

def get_user_input():
    dino1 = input("Enter Dinosaur 1 Name: ")
    dino2 = input("Enter Dinosaur 2 Name: ")
    return dino1, dino2

def main():
    # Load Dinosaur Dataset
    images_folder = '/Users/maana/Documents/Dinosss/dino'

    # Get User Input
    dino1_name, dino2_name = get_user_input()

    # Find corresponding images based on user input
    dino1_image = find_image(images_folder, dino1_name)
    dino2_image = find_image(images_folder, dino2_name)

    if dino1_image is None or dino2_image is None:
        print("One or both dinosaurs not found.")
        return

    # Generate New Dinosaur Image
    new_image, new_name = generate_new_image(dino1_image, dino2_image, dino1_name, dino2_name)

    # Generate New Dinosaur Description
    #description = generate_description(dino1_name, dino2_name)

    # Display Results (Image and Description)
    new_image.show()
    print("New Dinosaur Name:", new_name)
    #print("Description:", description)

if __name__ == "__main__":
    main()
