import io
import json
import os

from flask import Flask, render_template, request, send_file, make_response
from flask_cors import CORS
import cv2 as cv
import numpy as np
import sys
import torch
from PIL import Image
from skimage.transform import resize
from train import ConvNet
from utils import read_image, cvt2Lab, upsample, cvt2rgb

app = Flask(__name__, static_folder="static", template_folder="static", static_url_path="/")
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})

MODEL_PATH = "model/image_colorization_model.pt"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    for fname in request.files:
        photo = request.files.get(fname)
        in_memory_file = io.BytesIO()
        photo.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv.imdecode(data, color_image_flag)
        result = img
        colorized = request.form.get('colorize')
        sharpen = request.form.get('sharpen')
        remove_glare = request.form.get('removeGlare')
        if colorized:
            result = np.array(colorize(result))

        #   TODO
        # if sharpen:
        #     result = np.array(sharpen(result))

        #   TODO
        # if remove_glare:
        #     result = np.array(remove_glare(result))

        image_bytes = cv.imencode('.jpg', result)[1].tobytes()
        return send_file(io.BytesIO(image_bytes), mimetype="image/jpg")


def get_model():
    model = ConvNet()
    model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
    return model


def preprocess_image(image):
    img, real_size = (image, image.shape[:2])
    img_light, _ = cvt2Lab(img)
    img_input = np.expand_dims(img_light, axis=0)
    img_input = np.expand_dims(img_input, axis=0)
    img_input = torch.autograd.Variable(torch.from_numpy(img_input).float(), requires_grad=False)
    print(str(img_light.shape) + 'preprocess')
    return img_light, img_input, real_size


def process_image(img, img_light):
    img = np.squeeze(img, axis=0)
    img = np.transpose(img.astype(float), (1, 2, 0))
    img = upsample(img)
    print(str(img.shape) + 'after upscale')
    img = np.insert(img, 0, img_light, axis=2)
    img = (cvt2rgb(img) * 255.).astype(np.uint8)
    return img


def colorize(image):
    model = get_model()

    img_light, img_input, real_size = preprocess_image(image)

    img = model(img_input).cpu().data.numpy()
    img = process_image(img, img_light)
    img_result = Image.fromarray(img)
    img_result = img_result.resize((real_size[1], real_size[0]))
    return img_result


if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.mkdir('./uploads')
    app.run(debug=True, port=9000)
