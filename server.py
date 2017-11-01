from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        file = next(iter(request.files.values()))
        file.save()
    return


if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)
