import tensorflow as tf
import keras as kr
from os.path import abspath

path = "C:\\sebin\\lab\\ecg2\\git\\ecg_data_wfdb\\model\\03\\0118\\"
model = kr.models.load_model(path + "model01_train_80.h5")
converter = tf.lite.TFLiteConverter.from_keras_model(model)

tflite_model = converter.convert()


open(path+"model01.tflite", "wb").write(tflite_model)