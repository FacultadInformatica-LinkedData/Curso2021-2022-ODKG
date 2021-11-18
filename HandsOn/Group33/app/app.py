from flask import Flask, jsonify
from openGraph import *

app = Flask(__name__)
obj = OpenGraph("mapped_data")

@app.route("/")
def index():
    return jsonify(obj.allPredicats())

@app.route('/sparql/community')
def getSparqlCommunity():
    return jsonify(obj.allCommunities())

@app.route('/rdflib/community')
def getRdflibCommunity():
    return jsonify(obj.allCommunitiesWithQuery())
