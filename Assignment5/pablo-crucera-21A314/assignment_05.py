# -*- coding: utf-8 -*-
"""Assignment_05.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x7ZFm1guZqOtwlqDFxCd0eUQssEfjvxf
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
#         --match '(instance)-[:P31]->(class)'
#         --return 'count(distinct instance) as count_instances'
# """)

"""Now, count the number of distinct properties: 

"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# kgtk("""
#     query -i all
#         --match '(instance)-[l {label: property}]->(class)'
#         --return 'count(distinct property) as count_property'
# """)

"""Now, let's count the frequency of those properties. That is, how many instances we can find with each property"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# kgtk("""
#     query -i all
#         --match '(instance)-[l {label: property}]->()'
#         --return 'property as Prop, count(instance) as frequency'
#         --order-by 'cast(frequency, int)'
# """)

"""## Simple queries
Some of these queries are simple and will run in the Wikidata endpoint. 
Try both of them using SPARQL and Kypher
"""

# Which actors has Schwarzenegger worked with throughout his career? (Print also the movie)

# In SPARQL
"""
SELECT DISTINCT ?mateName ?filmName WHERE {
  ?film wdt:P161 wd:Q2685.
  ?film wdt:P161 ?mate.
  ?mate rdfs:label ?mateName.
  ?film rdfs:label ?filmName.
  FILTER(?mate != wd:Q2685).
  FILTER(LANG(?mateName) = 'en')
  FILTER(LANG(?filmName) = 'en')
}
"""

# In Kypher:
kgtk("""
    query -i all
        --match '
          (film)-[:P161]->(:Q2685), 
          (film)-[:P161]->(mate)'
        --where 'mate != "Q2685"'
        --return 'distinct mate as Actors, film as Movie'
        / add-labels
""")

# How many awards does Schwarzenegger have?

# SPARQL:
# TO DO
"""
SELECT (COUNT(?award) as ?numberOfAwards) WHERE {
  wd:Q2685 wdt:P166 ?award.
}
"""

# Kypher:
kgtk("""
    query -i all
        --match '(:Q2685)-[:P166]->(award)'
        --return 'count(award) as count_awards'
""")

# Retrieve at least two members of Schwarzenegger's political party. Make sure only persons are returned
# SPARQL:
# TO DO
"""
SELECT DISTINCT ?memberName WHERE {
  wd:Q2685 wdt:P102 ?party.
  ?member wdt:P102 ?party.
  ?member wdt:P31 wd:Q5.
  ?member rdfs:label ?memberName
  FILTER(LANG(?memberName) = 'en')
}
"""

# Kypher:
kgtk("""
    query -i all
        --match '
            (:Q2685)-[:P102]->(party),
            (member)-[:P102]->(party),
            (member)-[:P31]->(:Q5)'
        --where 'member != "Q2685"'
        --return 'distinct member as Members'
    / add-labels
""")

# What are the properties that describe an artist?

# In theory this one is heavy on Wikidata

# SPARQL: 
# TO DO
"""
SELECT DISTINCT ?property WHERE {
  ?subclassOfArtist rdfs:subClassOf* wd:Q483501.
  ?instanceOfArtist wdt:P106 ?subclassOfArtist.
  ?instanceOfArtist ?property ?prop.
}
"""


# In Kypher:
kgtk("""
    query -i all
      --match '
        (subclassOfArtist)-[:P279star]->(:Q483501),
        (instanceOfArtist)-[:P106]->(subclassOfArtist),
        (instanceOfArtist)-[l {label: property}]->()'
      --return 'distinct property as Properties'
    / add-labels
""")

# And a film director?
# SPARQL: 
# TO DO
"""
SELECT DISTINCT ?property WHERE {
  ?instanceOfFilmDir wdt:P106 wd:Q2526255.
  ?instanceOfFilmDir ?property ?prop.
}
"""

# In Kypher:
kgtk("""
    query -i all
      --match '
        (instanceOfFilmDir)-[:P106]->(:Q2526255),
        (instanceOfFilmDir)-[l {label: property}]->()'
      --return 'distinct property as Properties'
    / add-labels
""")

# Embeddings. Run the noebook https://colab.research.google.com/drive/1A55l10voA4jnjoju3fojJWY3buLfaR4i?usp=sharing. 
# Which are the top 10 similar entities to Schwarzenegger? (list below) 
# TO DO
# 1 - Arnold Schwarzenegger
# 2 - Hugh O'Brian
# 3 - John Larroquette
# 4 - Carl Reiner
# 5 - Harvey Fierstein
# 6 - Tom Sizemore
# 7 - Randy Quaid
# 8 - Gene Kelly
# 9 - DeForest Kelley
# 10 - Robert Stack

"""## Network analysis
Print all the paths between Schwarzenegger and Trump

## Note that **you have to create a file `paths.tsv` with the node pairs you want to find the paths for. Upload it in the "content" folder**

"""

# Commented out IPython magic to ensure Python compatibility.
# %%bash
# cat <<EOF >$TEMP/path-query.tsv
# node1	node2	label
# Q2685	Q22686	path

kgtk("""
    add-labels -i $TEMP/path-query.tsv
""")

# Calculate all the paths between Trump and Schwarzenegger (max hops: 3)
# TO DO    
kgtk("""
    paths -i all
        --path-file $TEMP/path-query.tsv
        --statistics-only True
        --max-hops 3
""")

# Retrieve all the family of Schwarzenegger (child/father/mother/sibling/spouse relationships)
# TO DO  
kgtk("""
    reachable-nodes -i all
        --root Q2685
        --props P40 P22 P25 P3373 P26
        --label Family
    / add-labels
""")

# What are the 10 most relevant actors (pagerank) in the graph? (Use graph-statistics command to calculate page rank, and then filter only actors)
# TO DO  
kgtk("""
    graph-statistics -i all -o $OUT/metadata.pagerank.undirected.tsv.gz 
    --compute-pagerank True 
    --compute-hits False 
    --page-rank-property Pdirected_pagerank 
    --vertex-in-degree-property Pindegree
    --vertex-out-degree-property Poutdegree    
    --output-degrees True
    --output-pagerank True 
    --output-hits False \
    --output-statistics-only 
    --undirected True 
    --log-file $TEMP/metadata.pagerank.undirected.summary.txt
""")

# TO DO: Hint: do the query after calculating the pagerank. See https://github.com/usc-isi-i2/kgtk-notebooks/blob/main/tutorial/06-kg-network-analysis.ipynb for inspiration
kgtk("""
    query -i item -i $OUT/metadata.pagerank.undirected.tsv.gz
        --match '
            item: (actor)-[:P106]->(:Q33999),
            pagerank: (actor)-[:Pdirected_pagerank]->(pagerank)'
        --return 'actor as node1, pagerank as node2'
        --order-by 'cast(pagerank, float) desc'
        --limit 10
    / add-labels
""")