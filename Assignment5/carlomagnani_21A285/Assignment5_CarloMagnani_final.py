#!/usr/bin/env python
# coding: utf-8


get_ipython().system('pip install kgtk==1.0.1')


get_ipython().system('echo "deb http://downloads.skewed.de/apt bionic main" >> /etc/apt/sources.list')
get_ipython().system('apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25')
get_ipython().system('apt-get update')
get_ipython().system('apt-get install python3-graph-tool python3-cairo python3-matplotlib')
get_ipython().system('apt-get install libcairo2-dev ')


# ## Preamble: set up the environment and files used in the assignment (remember to restart runtime)


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


# The following command will download all the files you  need for the assignment:


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


# The KGTK setup command defines environment variables for all the files so that you can reuse the Jupyter notebook when you install it on your local machine.

ck.print_env_variables()

get_ipython().run_cell_magic('time', '', 'ck.load_files_into_cache()')


# # About this assignment.
# This assignment is based on https://github.com/usc-isi-i2/kgtk-notebooks/tree/main/tutorial. If you have any questions or doubts, it is encouraged to look how the tutorial performs the different operations.
# 
# Additional information can be found in https://kgtk.readthedocs.io/

# ## Simple graph statistics
# 
# Let's calculate first some statistics about the KG. Count the number of instances:
# 


kgtk(""" 
    query -i all
        --match \'(p)-[r]->(n)\'\
        --return \'count(p) as instances_num\'
""")


# Now, count the number of distinct properties: 
# 


kgtk("""
    query -i all
    --match \'(p)-[r]->(n)\'
    --return \'count(distinct r.label) as properties\'
""")


# Now, let's count the frequency of those properties. That is, how many instances we can find with each property


kgtk("""
     query -i all
    --match \'(p)-[r]->(n)\' 
    --return \'r.label, count(n) as frequency\'
""")


# ## Simple queries
# Some of these queries are simple and will run in the Wikidata endpoint. 
# Try both of them using SPARQL and Kypher


# Which actors has Schwarzenegger worked with throughout his career? (Print also the movie)

# (in SPARQL)

#select distinct ?movie ?actors{
#  ?movie wdt:P161 wd:Q2685.
#  ?movie wdt:P161 ?actors
#}LIMIT 100

# In Kypher:
kgtk("""
    query -i all \
    --match '(a)<-[:P161]-(f)-[:P161]->(:Q2685)'
    --return 'f as film, a as actor'
    / add-labels
""")


# How many awards does Schwarzenegger have?

# SPARQL:

#select distinct ?award{
#  wd:Q2685 wdt:P166 ?award
#}LIMIT 100

# Kypher:
kgtk("""
    query -i all \
    --match '(:Q2685)-[:P166]->(awards)' \
    --return 'count(awards) as Number_of_awards'
""")


# Retrieve at least two members of Schwarzenegger's political party. Make sure only persons are returned
# SPARQL:

#select ?politician 
#where{
#    wd:Q2685 wdt:P102 ?party.
#    ?politician wdt:P102 ?party.
#    ?politician wdt:P31  wd:Q5      
#}LIMIT 2

# Kypher:
kgtk("""
    query -i all \
    --match '(:Q2685)-[:P102]->(party)<-[:P102]-(politician)-[:P31]->(:Q5)' \
    --return 'politician as politician'
    --limit 2
    / add-labels
""")


# What are the properties that describe an artist?

# In theory this one is heavy on Wikidata

# SPARQL: 

#select distinct ?prop 
#where{
# ?artist wdt:P106 wd:Q483501.
# ?artist ?prop ?values
#}


# In Kypher:
kgtk("""
    query -i all \
    --match '(:Q483501)<-[:P31]-(artist)-[p]->()' \
    --return 'distinct p.label as Property'
    / add-labels
""")


# And a film director?
# SPARQL: 

#select distinct ?prop 
#where{
# ?director wdt:P106 wd:Q2526255.
# ?director ?prop ?values
#}

# In Kypher:
kgtk("""
    query -i all \
    --match '(:Q2526255)<-[:P106]-(director)-[p]->()' \
    --return 'distinct p.label as Property'
    / add-labels
""")


# Embeddings. Run the noebook https://colab.research.google.com/drive/1A55l10voA4jnjoju3fojJWY3buLfaR4i?usp=sharing. 
# Which are the top 10 similar entities to Schwarzenegger? (list below) 

#1) Arnold Schwarzenegger (himeslf); 2) Hugh O'Brian; 3) John Larroquette; 4) Carl Reiner; 5) Harvey Fierstein; 6) Tom Sizemore; 7) Randy Quaid; 8) Gene Kelly; 9) DeForest Kelley; 10) Robert Stack

#########################################################################
#########################################################################

# ## Network analysis
# Print all the paths between Schwarzenegger and Trump
# 
# ## Note that **you have to create a file `paths.tsv` with the node pairs you want to find the paths for. Upload it in the "content" folder**
# 


#%%bash
#cat <<EOF >$TEMP/path-query.tsv
#node1	node2	label
#Q2685	Q22686	path


kgtk("""
    add-labels -i $TEMP/path-query.tsv
""")


# Calculate all the paths between Trump and Schwarzenegger (max hops: 3)
# TO DO    
kgtk("""
    paths -i all
        --verbose False
        --statistics-only True
        --path-file $TEMP/path-query.tsv
        --max_hops 3
    -o $TEMP/path-results.tsv
""")

#!head $TEMP/path-results.tsv


# Retrieve all the family of Schwarzenegger (child/father/mother/sibling/spouse relationships)

kgtk("""
    query -i all \
        --match '(:Q2685)-[p]->(rel)' \
        --where 'p.label in ["P22","P25","P3373","P26","P40"]' \
        --return 'p.label as Relationship, rel as Relative'
    / add-labels
""")


# What are the 10 most relevant actors (pagerank) in the graph? (Use graph-statistics command to calculate page rank, and then filter only actors)

kgtk("""
    graph-statistics -i all -o $TEMP/pagerank-results.tsv\
      --compute-pagerank True \
      --compute-hits False \
      --page-rank-property Pdirected_pagerank \ 
      --vertex-in-degree-property Pindegree \
      --vertex-out-degree-property Poutdegree \
      --output-degrees True \
      --output-pagerank True \
      --output-hits False \
      --output-statistics-only \
      --undirected True \
      --log-file $TEMP/metadata.pagerank.undirected.summary.txt
""")
#!head $TEMP/pagerank-results.tsv


# TO DO: Hint: do the query after calculating the pagerank. See https://github.com/usc-isi-i2/kgtk-notebooks/blob/main/tutorial/06-kg-network-analysis.ipynb for inspiration
kgtk("""
      query -i all -i $TEMP/pagerank-results.tsv \
        --match '(pr)<-[:Pdirected_pagerank]-(actor)-[:P106]->(:Q33999)' \
        --return 'actor as Actor, pr as PageRank' \
        --order-by 'cast(pr, float) desc' \
        --limit '10'
        / add-labels
""") 


