# -*- coding: utf-8 -*-
"""Copia de Assignment-Notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J2d8CwNmo_xItoT7oPEovJG7AhY3x88m
"""

!pip install kgtk==1.0.1

!echo "deb http://downloads.skewed.de/apt bionic main" >> /etc/apt/sources.list
!apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25
!apt-get update
!apt-get install python3-graph-tool python3-cairo python3-matplotlib
!apt-get install libcairo2-dev

"""## Preamble: set up the environment and files used in the assignment (remember to restart runtime)"""

import io
import os
import subprocess
import sys

import math
import numpy as np
import pandas as pd
from graph_tool.all import *
from IPython.display import display, HTML

from kgtk.configure_kgtk_notebooks import ConfigureKGTK
from kgtk.functions import kgtk, kypher

# Parameters

# Folder on local machine where to create the output and temporary folders
input_path = None
output_path = "/tmp/projects"
project_name = "assignment"

"""The following command will download all the files you  need for the assignment:"""

files = [
    "all",
    "label",
    "alias",
    "description",
    "external_id",
    "monolingualtext",
    "quantity",
    "string",
    "time",
    "item",
    "wikibase_property",
    "qualifiers",
    "datatypes",
    "p279",
    "p279star",
    "p31",
    "in_degree",
    "out_degree",
    "pagerank_directed",
    "pagerank_undirected"
]
ck = ConfigureKGTK(files)
ck.configure_kgtk(input_graph_path=input_path,
                  output_path=output_path,
                  project_name=project_name)

"""The KGTK setup command defines environment variables for all the files so that you can reuse the Jupyter notebook when you install it on your local machine."""

ck.print_env_variables()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# ck.load_files_into_cache()

"""# About this assignment.
This assignment is based on https://github.com/usc-isi-i2/kgtk-notebooks/tree/main/tutorial. If you have any questions or doubts, it is encouraged to look how the tutorial performs the different operations.

Additional information can be found in https://kgtk.readthedocs.io/

## Simple graph statistics

Let's calculate first some statistics about the KG. Count the number of instances:
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# kgtk("""
#     query -i all
#         --match '(inst)-[:P31]->(class)'
#         --return 'count(distinct inst) as Instances'
# """)

"""Now, count the number of distinct properties: 

"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# kgtk("""
#     query -i all
#         --match '(a)-[prop {label: property}]->(b)'
#         --return 'count(distinct property) as Properties'
# """)

"""Now, let's count the frequency of those properties. That is, how many instances we can find with each property"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# kgtk("""
#     query -i all
#         --match '(inst)-[prop {label: property}]->(class)'
#         --return 'prop.label as Property, count(distinct inst) as Frequency' 
# """)

"""## Simple queries
Some of these queries are simple and will run in the Wikidata endpoint. 
Try both of them using SPARQL and Kypher
"""

##Import packages to work with SPARQL
!pip install sparqlwrapper
from SPARQLWrapper import SPARQLWrapper, JSON

## To show both SPARQL and Kypher outputs
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'

# Which actors has Schwarzenegger worked with throughout his career? (Print also the movie)

# (in SPARQL)
endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?actor ?film ?actorLabel ?filmLabel WHERE {
  ?film wdt:P161 wd:Q2685.
  ?film wdt:P161 ?actor.
  FILTER (?actor != wd:Q2685)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}ORDER BY ?filmLabel"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)
for result in results["results"]["bindings"]:
    print(result.get("actor").get("value"),result.get("film").get("value"),result.get("actorLabel").get("value"),result.get("filmLabel").get("value"))



# In Kypher:
kgtk("""
    query -i all \
     --match '(movie)-[:P161]->(:Q2685),
              (movie)-[:P161]->(actor)' \
     --return 'actor as Actor, movie as Movie'
    / add-labels
""")

# How many awards does Schwarzenegger have?

# SPARQL:
endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT (COUNT(?award) AS ?NumberOfAwards) WHERE {
  wd:Q2685 wdt:P166 ?award
}"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result.get("NumberOfAwards").get("value"))


# Kypher:
kgtk("""
    query -i all
        --match '(:Q2685)-[:P166]->(award)'
        --return 'count(award) as NumberOfAwards'
""")

# There is one missing in Wikidata !!!

# Retrieve at least two members of Schwarzenegger's political party. Make sure only persons are returned
# SPARQL:
endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?member ?party ?memberLabel ?partyLabel WHERE {
  wd:Q2685 wdt:P102 ?party.
  ?member wdt:P102 ?party.
  ?member wdt:P31 wd:Q5.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  FILTER (?member != wd:Q2685)
}LIMIT 20"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result.get("member").get("value"),result.get("memberLabel").get("value"))


# In Kypher:
kgtk("""
    query -i all \
     --match '(:Q2685)-[:P102]->(parties),
              (members)-[:P102]->(parties),
              (members)-[:P31]->(:Q5)' \
     --return 'members' 
    / add-labels
""")

# What are the properties that describe an artist?

# In theory this one is heavy on Wikidata

# SPARQL: 
endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT DISTINCT ?property ?propertyLabel WHERE {
  ?subclasses rdfs:subClassOf* wd:Q483501.
  ?artist wdt:P106 ?subclasses.
  ?artist ?property ?prop.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} LIMIT 20"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result.get("property").get("value"))


# In Kypher:
kgtk("""
    query -i all
        --match '()<-[prop {label: property}]-(element)-[:P106]->(class)-[:P279*]->(:Q483501)'
        --return 'distinct property'
""")

# And a film director?
# SPARQL: 
endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT DISTINCT ?property WHERE {
        ?subclasses rdfs:subClassOf* wd:Q2526255.
        ?director wdt:P106 ?subclasses.
        ?director ?property ?prop.
}LIMIT 20"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result.get("property").get("value"))


# In Kypher:
kgtk("""
    query -i all
        --match '()<-[prop {label: property}]-(element)-[:P106]->(class)-[:P279*]->(:Q2526255)'
        --return 'distinct property'
""")

# Embeddings. Run the notebook https://colab.research.google.com/drive/1A55l10voA4jnjoju3fojJWY3buLfaR4i?usp=sharing. 
# Which are the top 10 similar entities to Schwarzenegger? (list below) 
print("""
    From an already run cell in the embeddings file:
    1) Arnold Schwarzenegger
    2) Hugh O'Brian
    3) John Larroquette
    4) Carl Reiner
    5) Harvey Fierstein
    6) Tom Sizemore
    7) Randy Quaid
    8) Gene Kelly
    9) DeForest Kelley
    10) Robert Stack""")

"""## Network analysis
Print all the paths between Schwarzenegger and Trump

## Note that **you have to create a file `paths.tsv` with the node pairs you want to find the paths for. Upload it in the "content" folder**

"""

# Commented out IPython magic to ensure Python compatibility.
# %%bash
# cat <<EOF >$TEMP/path-query.tsv
# node1	node2	label
# Q2685	Q22686	path
#

kgtk("""
    add-labels -i $TEMP/path-query.tsv
""")

# Calculate all the paths between Trump and Schwarzenegger (max hops: 3)    
kgtk("""
    paths -i all
        --verbose False
        --shortest-path True
        --statistics-only True
        --path-file $TEMP/path-query.tsv
        --max_hops 3
    -o $TEMP/path-results.tsv
""")

## Display ideas from the tutorial 

!head $TEMP/path-results.tsv

kgtk("""
    query -i all -i $TEMP/path-results.tsv
        --match '
            path: (path)-[segment]->(edge),
            all: (n1)-[edge {label: property}]->(n2)'
        --return 'n1 as node1, property as label, n2 as node2, path as path, segment as segment'
        --order-by 'path, segment'
    / add-labels
""")

# Retrieve all the family of Schwarzenegger (child/father/mother/sibling/spouse relationships)  
kgtk("""
    reachable-nodes -i $item
        --root Q2685
        --props P40 P3373 P26 P451 P22 P25
        --label Pextended_family
    / add-labels
""")

# Commented out IPython magic to ensure Python compatibility.
# # What are the 10 most relevant actors (pagerank) in the graph? (Use graph-statistics command to calculate page rank, and then filter only actors)
# # Item istead of all avoids to compute the graph wthout literals and qualifiers in order to save time
# 
# #This is used to obtain a graph with the pagerank information
# %%time
# kgtk("""
#     graph-statistics -i "$item" -o $OUT/metadata.pagerank.undirected.tsv.gz 
#     --compute-pagerank True 
#     --compute-hits False 
#     --page-rank-property Pdirected_pagerank 
#     --vertex-in-degree-property Pindegree
#     --vertex-out-degree-property Poutdegree
#     --output-degrees True 
#     --output-pagerank True 
#     --output-hits False \
#     --output-statistics-only 
#     --undirected True 
#     --log-file $TEMP/metadata.pagerank.undirected.summary.txt
# """)

# TO DO: Hint: do the query after calculating the pagerank. See https://github.com/usc-isi-i2/kgtk-notebooks/blob/main/tutorial/06-kg-network-analysis.ipynb for inspiration
kgtk("""
    query -i item -i $OUT/metadata.pagerank.undirected.tsv.gz
        --match '
            item: (actor)-[:P106]->(:Q33999),
            pagerank: (actor)-[:Pdirected_pagerank]->(pagerank)'
        --return 'actor as node1, pagerank as node2'
        --order-by 'cast(pagerank, float) desc'
        --limit '10'
    / add-labels
""")