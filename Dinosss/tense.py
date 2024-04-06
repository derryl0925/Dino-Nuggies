import tensorflow as tf
from PIL import Image
import numpy as np

# Function to find image by name
def find_image(images, name):
    for img_name, img in images.items():
        if name.lower() in img_name.lower():
            return img
    return None

# Function to blend two images
def blend_images(image1, image2):
    # Convert images to numpy arrays
    arr1 = np.array(image1)
    arr2 = np.array(image2)
    
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
    images = 'archive/'

    # Get User Input
    dino1_name, dino2_name = get_user_input()

    # Find corresponding images based on user input
    dino1_image = find_image(images, dino1_name)
    dino2_image = find_image(images, dino2_name)

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