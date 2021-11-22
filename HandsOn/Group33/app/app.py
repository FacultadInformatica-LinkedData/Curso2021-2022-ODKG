from flask import Flask, jsonify
from openGraph import *

app = Flask(__name__)
obj = OpenGraph("mapped_data")

@app.route("/")
def index():
    response = jsonify(obj.allPredicats())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/sparql/community')
def getSparqlCommunity():
    response = jsonify(obj.allCommunities())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/rdflib/community')
def getRdflibCommunity():
    response = jsonify(obj.allCommunitiesWithQuery())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/rdflib/position/<latitude>/<longitude>/<max_distance>')
def getPosition(latitude, longitude, max_distance):
    response = jsonify(obj.find_escooters_near(latitude, longitude, max_distance))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/rdflib/statistics_of_distance_and_duration/')
def getStatistics1():
    response = jsonify(obj.get_statistic())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/rdflib/common_start_end_community/')
def getStatistics2():
    response = jsonify(obj.get_monst_common_community())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3100, debug=True)