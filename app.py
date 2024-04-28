import io
import json
import os

from flask import Flask, render_template, request, send_file, make_response
from flask_cors import CORS
import cv2 as cv
import numpy as np

app = Flask(__name__, static_folder="static", template_folder="static", static_url_path="/")
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    for fname in request.files:
        f = request.files.get(fname)
        # image_stream = io.BytesIO(f.stream.read())
        # img = cv.imdecode(np.frombuffer(image_stream.read()), cv.IMREAD_COLOR)
        #
        # adjusted = cv.convertScaleAbs(img, alpha=1.5, beta=10)
        # encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 90]
        # result, imgencode = cv.imencode(".jpg", img, encode_param)
        return send_file(io.BytesIO(f.stream.read()), mimetype="image/jpg")


if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.mkdir('./uploads')
    app.run(debug=True, port=9000)
