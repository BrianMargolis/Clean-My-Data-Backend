import random
import string

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager

from Cleaner import Cleaner

app = Flask(__name__)
login_manager = LoginManager()


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # error handling
        if len(request.files) <= 0:
            return {"message": "No file provided"}, 400
        elif len(request.files) > 1:
            return {"message": "{0} files is too many. Send 1.".format(len(request.files))}, 400

        file = next(iter(request.files.values()))  # get the single file
        file_name = get_file_name()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        return jsonify({"file_name": file_name})


@app.route("/identify_errors", methods=['POST'])
def identify_errors():
    if request.method == "POST":
        json = request.json
        file_name = json["file_name"]
        options = json["options"]
        cleaner = Cleaner(file_name, options)
        cleaner.identify_errors()

        download = "download" in json and json["download"]
        if download:
            return send_from_directory(app.config['UPLOAD_FOLDER'], file_name)
        else:
            # get bad line numbers from cleaner
            pass


@app.route("/clean_data", methods=['POST'])
def clean_data():
    if request.method == "POST":
        json = request.json
        file_name = json["file_name"]
        errors = json["errors"]
        cleaner = Cleaner(file_name, {})
        cleaner.clean_data(errors)

        download = "download" in json and json["download"]
        if download:
            return send_from_directory(app.config['UPLOAD_FOLDER'], file_name)
        else:
            # get bad line numbers from cleaner
            pass

def get_file_name():
    N = 15
    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    return id + ".csv"


if __name__ == '__main__':
    login_manager.init_app(app)
    CORS(app)
    app.config['UPLOAD_FOLDER'] = app.root_path + '/uploads'
    app.run(debug=True)
