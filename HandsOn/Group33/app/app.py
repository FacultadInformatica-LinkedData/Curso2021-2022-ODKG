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

@app.route('/rdflib/position/<latitude>/<longitude>/<max_distance>')
def getPosition(latitude, longitude, max_distance):
    return jsonify(obj.find_escooters_near(latitude, longitude, max_distance))

@app.route('/rdflib/statistics_of_distance_and_duration/')
def getStatistics1():
    return jsonify(obj.get_statistic())

@app.route('/rdflib/common_start_end_community/')
def getStatistics2():
    return jsonify(obj.get_monst_common_community())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3100, debug=True)