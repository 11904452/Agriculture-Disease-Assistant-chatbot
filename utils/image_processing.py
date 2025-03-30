import numpy as np
import cv2 as cv

def preprocess_binary_image(image):
    image = image.resize((256, 256))
    image = np.array(image)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    return image

def preprocess_multiClass_image(image):
    image = image.resize((256, 256))
    image = np.array(image)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    return image