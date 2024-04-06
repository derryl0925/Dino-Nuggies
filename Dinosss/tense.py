import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Reshape, Conv2DTranspose
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img
from PIL import Image
import numpy as np
import os

# Define image dimensions (consider adjusting based on dataset)
IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS = 128, 128, 3
IMG_SHAPE = (IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)

# Function to load and preprocess images
def load_image(image_path):
    img = Image.open(image_path)
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img = img_to_array(img) / 255.0  # Normalize pixel values
    return img

# Function to create the generator model (increased complexity)
def build_generator():
    inputs = Input(shape=(100,))
    x = Dense(64 * 64 * 128, activation='relu')(inputs)
    x = Reshape((64, 64, 128))(x)
    x = Conv2DTranspose(64, kernel_size=5, strides=2, padding='same', activation='relu')(x)
    x = Conv2DTranspose(32, kernel_size=5, strides=2, padding='same', activation='relu')(x)
    x = Conv2DTranspose(16, kernel_size=5, strides=2, padding='same', activation='relu')(x)
    outputs = Conv2DTranspose(IMG_CHANNELS, kernel_size=5, strides=2, padding='same', activation='tanh')(x)
    model = Model(inputs, outputs)
    return model

# Function to generate noise vector (consider adding more variation)
def generate_noise(batch_size):
    noise = np.random.normal(0, 1, (batch_size, 100))  # Random noise with adjustable batch size
    return noise

# Function to generate a new dinosaur image using the generator model
def generate_new_image(generator, noise):
    generated_image = generator.predict(noise)
    generated_image = array_to_img(generated_image[0] * 255.0)  # Assuming batch size of 1
    return generated_image

def get_user_input():
    dino1 = input("Enter Dinosaur 1 Name: ")
    dino2 = input("Enter Dinosaur 2 Name: ")
    return dino1, dino2

def main():
    # Load Dinosaur Dataset (assuming you have a labeled dataset)
    images_folder = '/Users/maana/Documents/Dinosss/dino'  # Replace with your path

    # Get User Input for two dinosaurs
    dino1_name, dino2_name = get_user_input()

    # Find corresponding images based on user input (assuming filenames match names)
    dino1_image = load_image(os.path.join(images_folder, f'{dino1_name.lower()}', '2.png'))
    dino2_image = load_image(os.path.join(images_folder, f'{dino2_name.lower()}', '2.png'))

    if dino1_image is None or dino2_image is None:
        print("One or both dinosaurs not found.")
        return

    # Blend the features of the two dinosaurs (assuming simple averaging)
    blended_image = (dino1_image + dino2_image) / 2.0

    # Display the blended image
    blended_image = array_to_img(blended_image * 255.0)
    blended_image.show()

if __name__ == "__main__":
    main()

