import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Reshape, Conv2DTranspose, Conv2D, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img
from tensorflow.keras.layers import Input, Dense, Reshape, Conv2DTranspose, Conv2D, LeakyReLU, BatchNormalization
import nltk
from namesgenerator import RandomNameGenerator
from PIL import Image
import numpy as np
import os

# Define image dimensions
IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS = 128, 128, 3
IMG_SHAPE = (IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)
LATENT_DIM = 100  # Dimension of noise input to generator

# Function to load and preprocess images
def load_image(image_path):
    img = Image.open(image_path)
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img = img_to_array(img) / 255.0  # Normalize pixel values
    return img

# Define the Generator Model
def build_generator():
    inputs = Input(shape=(LATENT_DIM,))
    # Consider a deeper network or using residual connections
    x = Dense(7 * 7 * 256, use_bias=False, activation='relu')(inputs)
    x = Reshape((7, 7, 256))(x)
    x = BatchNormalization()(x)
    # Experiment with transposed convolution with fractional strides or nearest-neighbor upsampling
    x = Conv2DTranspose(128, kernel_size=3, strides=(2, 2), padding='same', use_bias=False, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Conv2DTranspose(64, kernel_size=3, strides=(2, 2), padding='same', use_bias=False, activation='relu')(x)
    x = BatchNormalization()(x)
    outputs = Conv2DTranspose(IMG_CHANNELS, kernel_size=3, strides=(2, 2), padding='same', activation='tanh')(x)
    model = Model(inputs, outputs)
    return model

# Define the Discriminator Model
def build_discriminator():
    inputs = Input(shape=IMG_SHAPE)
    x = Conv2D(64, kernel_size=3, strides=2, padding='same', activation='leaky_relu')(inputs)
    x = LeakyReLU(alpha=0.2)(x)
    x = Conv2D(128, kernel_size=3, strides=2, padding='same', activation='leaky_relu')(x)
    x = LeakyReLU(alpha=0.2)(x)
    x = Conv2D(256, kernel_size=3, strides=2, padding='same', activation='leaky_relu')(x)
    x = LeakyReLU(alpha=0.2)(x)
    outputs = Conv2D(1, kernel_size=3, strides=1, padding='same', activation='sigmoid')(x)  # Classify real or fake
    model = Model(inputs, outputs)
    return model

# Function to generate noise vector
def generate_noise(batch_size):
    return np.random.normal(0, 1, (batch_size, LATENT_DIM))

# Define Loss Functions and Optimizers
def discriminator_loss(real_output, fake_output):
    crossentropy = BinaryCrossentropy(from_logits=True)
    real_loss = crossentropy(tf.ones_like(real_output), real_output)
    fake_loss = crossentropy(tf.zeros_like(fake_output), fake_output)
    total_loss = (real_loss + fake_loss) / 2
    return total_loss

def generator_loss(fake_output):
    crossentropy = BinaryCrossentropy(from_logits=True)
    return crossentropy(tf.ones_like(fake_output), fake_output)

# Create the GAN Models
generator = build_generator()
discriminator = build_discriminator()

# Set up training (compile separately for training efficiency)
discriminator.compile(loss=discriminator_loss, optimizer=Adam(learning_rate=0.0002))
generator.compile(loss=generator_loss, optimizer=Adam(learning_rate=0.0002))

# Combined training function (consider using dedicated GAN training libraries for advanced features)
def train_gan(epochs, batch_size, dataset):
   batch_count = int(len(dataset) / batch_size)

   for epoch in range(epochs):
       for batch in range(batch_count):
           # Train Discriminator
           real_images = dataset[batch * batch_size:(batch + 1) * batch_size]
           noise = generate_noise(batch_size)
           fake_images = generator.predict(noise)

           discriminator.trainable = True  # Set discriminator as trainable
           discriminator.train_on_batch(real_images, tf.ones((batch_size, 1)))
           discriminator.train_on_batch(fake_images, tf.zeros((batch_size, 1)))

           # Train Generator
           noise = generate_noise(batch_size)
           discriminator.trainable = False  # Freeze discriminator weights for generator training
           generator.train_on_batch(noise, tf.ones((batch_size, 1)))  # Trick discriminator into thinking fakes are real

       print(f"Epoch {epoch + 1}/{epochs}")

   # Save the generator model for future use
   generator.save('trained_generator.h5')

def get_user_input():
    dino1_name = input("Enter Dinosaur 1 Name: ")
    dino2_name = input("Enter Dinosaur 2 Name: ")
    return dino1_name, dino2_name

# Function to generate a new dinosaur name
def generate_new_name(dino1_name, dino2_name):
    # Extract phonemes from names (using nltk)
    name1_phonemes = nltk.corpus.cmudict.cmudict[dino1_name][0]
    name2_phonemes = nltk.corpus.cmudict.cmudict[dino2_name][0]

    # Combine phonemes creatively (replace with your logic)
    combined_phonemes = name1_phonemes[:2] + name2_phonemes[:2]

    # Generate name based on phonemes using a name generator library
    generator = RandomNameGenerator()
    new_name = generator.generate_name(phonemes=combined_phonemes)
    return new_name

# Main function to load images, generate new dinosaur, and display
def main():
    # Load Dinosaur Dataset (assuming you have a labeled dataset)
    images_folder = '/Users/maana/Documents/Dinosss/dino'  # Replace with your path

    # Get Dinosaur Names from User
    dino1_name, dino2_name = get_user_input()

    # Find corresponding images based on user input (assuming filenames match names)
    dino1_image_path = os.path.join(images_folder, f'{dino1_name.lower()}', '2.png')
    dino2_image_path = os.path.join(images_folder, f'{dino2_name.lower()}', '2.png')

    # Check if images exist
    if not (os.path.exists(dino1_image_path) and os.path.exists(dino2_image_path)):
        print("One or both dinosaur images not found.")
        return

    # Load Dinosaur Images
    dino1_image = load_image(dino1_image_path)
    dino2_image = load_image(dino2_image_path)

    # Combine the features of the two dinosaurs (simple averaging)
    blended_image = (dino1_image + dino2_image) / 2.0

    # Generate new dinosaur name
    new_dino_name = generate_new_name(dino1_name, dino2_name)
    print("New Dinosaur Name:", new_dino_name)

    # Display the blended image
    blended_image = array_to_img(blended_image * 255.0)
    blended_image.show()

if __name__ == "__main__":
    main()

