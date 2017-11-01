from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello, World!'
