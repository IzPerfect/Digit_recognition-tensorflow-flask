from flask import Flask, request, jsonify, render_template
from PIL import Image, ImageOps

import tensorflow as tf
import numpy as np
import os
from cnn_model import *

app = Flask(__name__)

def imgToData(data):
    canvas_img = Image.open(data)
    canvas_img = canvas_img.resize((28, 28), Image.LANCZOS)
    img = Image.new("L", canvas_img.size, (255))
    img.paste(canvas_img, canvas_img)
    img = ImageOps.invert(img)
    return img

@app.route('/')
def home():
    return render_template('canvas_home.html')

@app.route('/classify', methods=['POST'])
def getAnswer():
    img = imgToData(request.files["image"])
    input = (np.asarray(img, dtype = np.float32)).reshape(1,784)

    pred_result = pred(input)
    return jsonify(prediction = str(pred_result))

if __name__=='__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(port=5100)
