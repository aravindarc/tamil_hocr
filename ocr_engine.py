import keras
from keras.models import model_from_json
import numpy as np
import tensorflow as tf

from PIL import Image
import cv2

# the dimensions of the image is fixed
# the model has been constructed and trained
# for a 65 x 65 image, this cannot be changed
# if a different size image is to be used
# crop and resize to 65 x 65 first
IMAGE_HEIGHT = 65   
IMAGE_WIDTH = 65                   

# this is the path to the model dir
MODEL_DIR = '../model/'     

json_file = open(MODEL_DIR + 'model.json', 'r')
model = json_file.read()
json_file.close()
model = model_from_json(model)
model.load_weights(MODEL_DIR + "model.h5")
print("Loaded model from disk")
model.compile(loss=keras.losses.categorical_crossentropy,
            optimizer=keras.optimizers.Adam(),
            metrics=['accuracy'])
print("Model compiled")
graph = tf.get_default_graph()

def recognize(fileName):
    img = Image.open(fileName)

    imgArray = np.array(img)

    # the image is resized to 65 x 65, make sure the original image is square shaped
    # to avoid any skewing, if not possible crop to a square shape and then use
    imgArray = cv2.resize(imgArray, (IMAGE_HEIGHT, IMAGE_WIDTH), interpolation=cv2.INTER_AREA)

    imgArray = cv2.cvtColor(imgArray, cv2.COLOR_BGR2GRAY)
    imgArray = ~imgArray

    imgArray = imgArray.astype('float')
    imgArray /= 255

    tempArr = imgArray.reshape(1, 65, 65, 1)
    with graph.as_default():
        y = model.predict_classes(tempArr)[0]
    return(y)
