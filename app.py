from flask import Flask, render_template, request, jsonify
import json
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="dist/spa", template_folder="dist/spa", static_url_path="/dist/spa")
# This is necessary because QUploader uses an AJAX request
# to send the file.jpg
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")


@app.route("/increment/<int:count>")
def increment(count):
    return f"{count + 1}"


@app.route("/image", methods=["POST"])
def processing():
    f = request.data
    print(f)
    return {
        "image": json.loads(f).get("image"),
    }


@app.route('/upload', methods=['POST'])
def upload():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
        f.save('./uploads/%s' % secure_filename(fname))

    return 'Okay!'


if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.mkdir('./uploads')
    app.run(debug=True, port=9000)
