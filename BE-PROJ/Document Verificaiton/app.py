from flask import Flask, render_template, request
import numpy as np
import os
from pathlib import Path
import pickle
import matplotlib.pyplot as plt
import keras
import tensorflow as tf
from tensorflow.keras.utils import load_img

app = Flask(__name__)


svm_classifier = pickle.load(open("finalized_model.h5", 'rb'))




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save('inp.png')
      print("image saved")
      image_data = []
      img = keras.utils.load_img('inp.png', target_size=(64,64))
      print("image loaded")
      img_array = keras.utils.img_to_array(img)
      print("image converted to array")
      image_data.append(img_array)
      image_data = np.array(image_data, dtype='float32')/255.0
      M = image_data.shape[0]
      image_data = image_data.reshape(M,-1)

      print("image appended to array")
      print(image_data.shape)
      pred = svm_classifier.predict(image_data)
      print("image predicted", pred)
      return render_template('index.html', pred = pred)

if __name__ == '__main__':
    app.run(debug=True)