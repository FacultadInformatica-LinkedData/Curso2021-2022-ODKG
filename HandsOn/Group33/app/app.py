from flask import Flask, jsonify
from openGraph import *

app = Flask(__name__)

@app.route("/")
def index():
    obj = OpenGraph("mapped_data")
    return jsonify(obj.allPredicats())
