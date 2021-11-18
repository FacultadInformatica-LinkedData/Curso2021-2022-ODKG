from flask import Flask, jsonify, render_template
from openGraph import *

app = Flask(__name__)
obj = OpenGraph("mapped_data")

@app.route("/", methods=["GET"])
def index():
    title = "E-scooter project"
    return render_template("layouts/index.html", title=title)

@app.route("/results/", methods=["GET"])
def results():
    title = "Results"
    datalist = ["a", "2", "4"]
    return render_template("layouts/results.html", title=title, datalist=datalist)

@app.route("/sparql/predicates")
def getSparqlPredicates():
    return jsonify(obj.allPredicats())

@app.route('/sparql/community')
def getSparqlCommunity():
    return jsonify(obj.allCommunities())

@app.route('/rdflib/community')
def getRdflibCommunity():
    return jsonify(obj.allCommunitiesWithQuery())
