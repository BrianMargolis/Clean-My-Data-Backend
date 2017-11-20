import random
import string

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager

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
        file_id = get_file_id()
        file.save(file_id)
        return jsonify({"file_id": file_id})

@app.route("/outlier_detection", methods=['POST'])
def outlier_detection():
    if request.method == "POST":
        a = request.query_string
        print(a)
        return "asdf"

def get_file_id():
    N = 15
    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    return id + ".csv"

if __name__ == '__main__':
    login_manager.init_app(app)
    CORS(app)
    app.run(debug=True)
