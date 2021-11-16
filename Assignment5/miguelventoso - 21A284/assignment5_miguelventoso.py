!pip install kgtk==1.0.1

!echo "deb http://downloads.skewed.de/apt bionic main" >> /etc/apt/sources.list
!apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25
!apt-get update
!apt-get install python3-graph-tool python3-cairo python3-matplotlib
!apt-get install libcairo2-dev

import io
import os
import subprocess
import sys
from rdflib.plugins.sparql import prepareQuery

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
# #P31 is the predicate "instance of"
# print(kgtk("""
#     query -i all
#     --match '(instance)-[:P31]->()'
#     --return 'count(distinct instance) as n_instances'
# """))

"""Now, count the number of distinct properties: 

"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# #Output with print to avoid exception 'NotebookFormatter' object has no attribute 'get_result'
# print(kgtk("""
#     query -i all
#     --match '()-[{label: property}]->()'
#     --return 'count(distinct property) as n_properties'
# """))

"""Now, let's count the frequency of those properties. That is, how many instances we can find with each property"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# print(kgtk("""
#     query -i all
#     --match '(instance)-[p {label: property}]->()'
#     --return 'p.label, count(distinct instance) as frequency'
# """))

"""## Simple queries
Some of these queries are simple and will run in the Wikidata endpoint. 
Try both of them using SPARQL and Kypher
"""

# Which actors has Schwarzenegger worked with throughout his career? (Print also the movie)

# (in SPARQL)
# TO DO 
'''
SELECT ?actor ?movie ?movieLabel ?actorLabel WHERE {
   ?movie wdt:P161 wd:Q2685.
   ?movie wdt:P161 ?actor.
   SERVICE wikibase:label { 
     bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". 
   }
   FILTER (?actor != wd:Q2685)
}
'''
#Link to the result: https://w.wiki/4Pp6


# In Kypher:
print(kgtk("""
    query -i all
    --match '(:Q2685)<-[:P161]-(movie)-[:P161]->(actor)'
    --where 'actor != "Q2685"'
     --return 'actor as actor, movie as movie'
    / add-labels
"""))

# How many awards does Schwarzenegger have?

# SPARQL:
# TO DO
'''
SELECT (
  COUNT(DISTINCT ?awards) as ?num_awards
)  
WHERE {
  wd:Q2685 wdt:P166 ?awards.
}
'''

#Link to result: https://w.wiki/4Pp8

# Kypher:
print(kgtk("""
    query -i all 
    --match '(:Q2685)-[:P166]->(awards)' 
    --return 'count(distinct awards) as num_awards' 
"""))

# Retrieve at least two members of Schwarzenegger's political party. Make sure only persons are returned
# SPARQL:
# TO DO

#We can retrieve all of them, also checking which of both republican and democrat parties is Arnold enrolled.
'''
SELECT ?member ?memberLabel  
WHERE {
  wd:Q2685 wdt:P102 ?party.
  ?member wdt:P102 ?party.
  ?member wdt:P31 wd:Q5
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en" .
   }
 FILTER(?member != wd:Q2685)
}
'''

#Link to result https://w.wiki/4PpD

# Kypher:
print(kgtk("""
    query -i all
    --match '(:Q2685)-[:P102]->(party)<-[:P102]-(member)-[:P31]->(:Q5)'
    --where 'member != "Q2685"'
    --return 'member as member, party as party'
    / add-labels
"""))

# What are the properties that describe an artist?

# In theory this one is heavy on Wikidata

# SPARQL: 
# TO DO
#Setting a 100 limit, because otherwise the query takes a lot of time to process
'''
SELECT DISTINCT ?property WHERE {
   ?artist wdt:P106/rdfs:subClassOf* wd:Q483501.
   ?artist ?property ?o.
}
LIMIT 100
'''

#Link to result: https://w.wiki/4Ppi


# In Kypher:
#It is much faster in Kypher!
print(kgtk("""
     query -i all
     --match '()<-[property]-(element)-[:P106]->(class)-[:P279star]->(:Q483501)'
     --return 'distinct property.label as property'
     / add-labels
"""))

# And a film director?
# SPARQL: 
# TO DO

#same but with Q2526255
'''
SELECT DISTINCT ?property  WHERE {
  ?director wdt:P106/rdfs:subClassOf* wd:Q2526255. 
  ?director ?property ?o       
}
LIMIT 100
'''

#Link to result: https://w.wiki/4Ppj

# In Kypher:
print(kgtk("""
     query -i all
     --match '()<-[property]-(element)-[:P106]->(director)-[:P279star]->(:Q2526255)'
     --return 'distinct property.label as property'
     / add-labels
"""))

# Embeddings. Run the noebook https://colab.research.google.com/drive/1A55l10voA4jnjoju3fojJWY3buLfaR4i?usp=sharing. 
# Which are the top 10 similar entities to Schwarzenegger? (list below) 
# TO DO
print("0. Arnold Schwarzenegger")
print("1. Hugh O\'Brian")
print("2. John Larroquette" )
print("3. Carl Reiner")
print("4. Harvey Fierstein")
print("5. Tom Sizemore ")
print("6. Randy Quaid ")
print("7. Gene Kelly")
print("8. DeForest Kelley")
print("9. Robert Stack")

"""## Network analysis
Print all the paths between Schwarzenegger and Trump

## Note that **you have to create a file `paths.tsv` with the node pairs you want to find the paths for. Upload it in the "content" folder**

"""

# Commented out IPython magic to ensure Python compatibility.
# %%bash
# cat <<EOF >$TEMP/path-query.tsv
# node1	node2	label
# Q2685	Q22686	path

print(kgtk("""
    add-labels -i $TEMP/path-query.tsv
"""))

# Calculate all the paths between Trump and Schwarzenegger (max hops: 3)
# TO DO
print(kgtk("""
    paths -i all
          --path-file $TEMP/path-query.tsv
          --statistics-only True
          --max_hops 3
"""))

# Retrieve all the family of Schwarzenegger (child/father/mother/sibling/spouse relationships)
# TO DO  
print(kgtk("""
    reachable-nodes -i all
        --root Q2685
        --props P40 P3373 P26 P22 P25
    / add-labels
"""))

# What are the 10 most relevant actors (pagerank) in the graph? (Use graph-statistics command to calculate page rank, and then filter only actors)
# TO DO  
print(kgtk("""
    graph-statistics -i all -o /tmp/odkg/metadata.pagerank.undirected.tsv.gz
    --compute-pagerank True
    --compute-hits False
    --page-rank-property P_pagerank
    --output-pagerank True
    --output-statistics-only
    --output-hits False 
    --undirected True
    --log-file /tmp/odkg/metadata.pagerank.undirected.summary.txt
"""))

# TO DO: Hint: do the query after calculating the pagerank. See https://github.com/usc-isi-i2/kgtk-notebooks/blob/main/tutorial/06-kg-network-analysis.ipynb for inspiration
print(kgtk("""
    query -i item -i /tmp/odkg/metadata.pagerank.undirected.tsv.gz
        --match '
            item: (actor)-[:P106]->(:Q33999),
            pagerank: (actor)-[:P_pagerank]->(pagerank)'
        --return 'actor as node1, pagerank as node2'
        --order-by 'cast(pagerank, float) desc'
        --limit 10
    / add-labels
""")
)