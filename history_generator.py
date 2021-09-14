import os
import tensorflow as tf
import datetime
import matplotlib.pyplot as plt

import time
from geotiff import GeoTiff
import cv2 as cv
import numpy as np

PATH = "history_test/" # Location of input data, organized in folder as S1, S2 (images are 1024 * 512 pixels)

"""
    Load and Preprocess Data
"""


def normalize(real_image):
	real_image = (real_image / 127.5) - 1
	return real_image


def load(image_file):
	image = tf.io.read_file(image_file)
	image = tf.image.decode_png(image)
	image = tf.image.rgb_to_grayscale(image)
	#     image = tf.cast(image, tf.float32)

	img_partitions = [img for img in tf.split(image, num_or_size_splits=2, axis=1)]
	img_partitions = [tf.cast(img, tf.float32) for img in img_partitions]

	return img_partitions[0], img_partitions[1]


def load_image_train_s2(image_file):
	current, historical = load(image_file)
	current, historical = normalize(current), normalize(historical)
	return current, historical


def load_tiff(filename):
	geoTiff = GeoTiff(filename)
	array = geoTiff.read()

	sigma0_vv = array[:, :, 1]
	sigma0_vh = array[:, :, 2]
	cohvv = array[:, :, 3]
	cohvh = array[:, :, 4]

	sigma0_vv_pct = np.where(sigma0_vv > np.percentile(sigma0_vv, 98), 0, sigma0_vv)
	sigma0_vh_pct = np.where(sigma0_vh > np.percentile(sigma0_vh, 98), 0, sigma0_vh)

	cohvv_n = np.where(cohvv < -5000, 0, cohvv)
	cohvh_n = np.where(cohvh < -5000, 0, cohvh)

	sigma0_vv_pct = np.interp(sigma0_vv_pct, (sigma0_vv_pct.min(), sigma0_vv_pct.max()), (-1, +1))
	sigma0_vh_pct = np.interp(sigma0_vh_pct, (sigma0_vh_pct.min(), sigma0_vh_pct.max()), (-1, +1))

	cohvv_n = np.interp(cohvv_n, (cohvv_n.min(), cohvv_n.max()), (-1, +1))
	cohvh_n = np.interp(cohvh_n, (cohvh_n.min(), cohvh_n.max()), (-1, +1))

	# Stack in correct dimensions
	bands_array = np.stack((sigma0_vv_pct, sigma0_vh_pct, cohvv_n, cohvh_n), axis=-1)
	bands_tensor = tf.convert_to_tensor(bands_array, dtype=tf.float32)

	return bands_tensor


def load_all_train():
	for filename in os.listdir(PATH + "S1/"):
		s2_equivalent = filename.split("colwith_")[1]
		s2_equivalent = s2_equivalent.split(".")[0]
		s2_paths = os.listdir(PATH + "S2/")
		s2_file = [f for f in s2_paths if f.startswith(s2_equivalent)]
		if len(s2_file) != 0:
			s2_file = s2_file[0]
			c, h = load_image_train_s2(PATH + "S2/" + s2_file)
			yield load_tiff(PATH + "S1/" + filename), c, h

def save_images(s1, predicted, target, history, epoch):
    
    s1_display = s1[0]
    s1_display = s1_display[:, :, 0]
    
    predicted = predicted[0] * 0.5 + 0.5
    target = target[0] * 0.5 + 0.5
    
    stackedImg = np.concatenate((predicted, target), axis=1) 
    tf.keras.preprocessing.image.save_img(path=f'./300821/fullimage/image_{epoch}.png', x=stackedImg)
    
def display_images(s1, predicted, target, history, epoch):
    s1_display = s1[0]
    s1_display = np.stack((s1_display[:, :, 0], s1_display[:, :, 1], s1_display[:, :, 2]), axis=-1)

    titles = ["S1 Input", "Predicted", "Target", "History"]
    display_list = [s1_display, predicted[0], target[0], history[0]]

    plt.figure(figsize=(20, 10))

    for i in range(4):
        plt.subplot(1, 4, i + 1)
        plt.title(titles[i])
        if i == 0:
            plt.imshow(display_list[i] * 0.5 + 0.5)
        else:
            plt.imshow(display_list[i] * 0.5 + 0.5, cmap='gray')
        plt.axis('off')
    plt.show()
    plt.savefig("history_test/images/epoch_{epoch}.png")
    
def generate_images(model, formatted_inp, inp, tar, hist, epoch=0):
    predicted = model(formatted_inp, training=True)
    display_images(inp, predicted, tar, hist, epoch)

def custom_edge(x):
	return cv.Canny(x, 100, 200)


@tf.function(input_signature=[tf.TensorSpec(None, tf.uint8)])
def tf_function(input):
	y = tf.numpy_function(custom_edge, [input], tf.uint8)
	return y


def mapped_edge_generator(s1_input, image, target):
	x_image = image
	b = tf.ones(x_image.shape)
	c = tf.constant(127.5, shape=x_image.shape)
	x_image = (x_image + b)
	x_image = (x_image * c)

	x_image = tf.dtypes.cast(x_image, tf.uint8)
	x_image = tf.reshape(x_image, [512, 512])

	im_edge = tf_function(x_image)
	im_edge = tf.cast(im_edge, tf.float32)
	im_edge = (im_edge / 127.5) - 1

	im_edge = tf.expand_dims(im_edge, -1)

	# Formatted input, S1 original, S2 Historical, S2 Target
	return s1_input, image, im_edge, target

from tensorflow import keras
import datetime

ep = keras.models.load_model("ep")
fe = keras.models.load_model("fe")
generator = keras.models.load_model("generator")

test_dataset = tf.data.Dataset.from_generator(load_all_train, \
                                               output_signature=(
                                                   tf.TensorSpec(shape=(512, 512, 4), dtype=tf.float32),
                                                   tf.TensorSpec(shape=(512, 512, 1), dtype=tf.float32),
                                                   tf.TensorSpec(shape=(512, 512, 1), dtype=tf.float32)))

test_dataset = test_dataset.map(mapped_edge_generator)
test_dataset = test_dataset.shuffle(800)
test_dataset = test_dataset.batch(1)

# Generate Synthetic images

for n, (s1, s2, s2_edge, target) in test_dataset.enumerate():
    epoch = f"test_{n}"
    fs2 = ep([s2_edge, s2])
    formatted_input = fe([s1, fs2])
    generate_images(generator, formatted_input, s1, target, s2, epoch)
