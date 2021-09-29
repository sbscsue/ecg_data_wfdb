import tensorflow as tf
import keras as kr
from os.path import abspath

model = kr.models.load_model("C:\\sebin\\lab\\ecg\\ecg_data_wfdb\\test\\02\\07\\model02.h5")
converter = tf.lite.TFLiteConverter.from_keras_model(model)

tflite_model = converter.convert()


open("C:\\sebin\\lab\\ecg\\ecg_data_wfdb\\lite\\converted_model.tflite", "wb").write(tflite_model)