from graph_tool.all import *
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
#         --match '()-[:P31]->(class)'
#         --return 'count(distinct n) as N_instances'
# """)

"""Now, count the number of distinct properties: 

"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# kgtk("""
#     query -i all
#         --match '(n)-[l {label: property}]->(class)'
#         --return 'count(distinct property) as N_properties'
# """)

"""Now, let's count the frequency of those properties. That is, how many instances we can find with each property"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# kgtk("""
#     query -i all
#         --match '(n)-[l {label: property}]->(class)'
#         --return 'l.label, count(distinct n) as N_instances'
# """)

"""## Simple queries
Some of these queries are simple and will run in the Wikidata endpoint. 
Try both of them using SPARQL and Kypher
"""

# Which actors has Schwarzenegger worked with throughout his career? (Print also the movie)

# (in SPARQL)
# TO DO
q1 = '''
SELECT ?actor ?movie ?actorLabel ?movieLabel WHERE {
  ?movie wdt:P161 ?actor.
  ?movie wdt:P161 wd:Q2685.
  FILTER (?actor != wd:Q2685)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
'''

# In Kypher:
kgtk("""
    query -i all
        --match '(:Q2685)<-[:P161]-(movie)-[:P161]->(actor)'
        --where 'actor != "Q2685"'
        --return 'actor as Actor, movie as Movie'
    / add-labels
""")

# How many awards does Schwarzenegger have?

# SPARQL:
# TO DO
q2 = '''
    SELECT (COUNT(?award) AS ?N_awards)
    WHERE {
      wd:Q2685 wdt:P166 ?award
    }
'''
# Kypher:
kgtk("""
    query -i all
        --match '(:Q2685)-[:P166]->(award)'
        --return 'count(award) as N_awards'
""")

# Retrieve at least two members of Schwarzenegger's political party. Make sure only persons are returned
# SPARQL:
# TO DO
q3= '''
SELECT ?member ?party ?memberLabel ?partyLabel WHERE {
  wd:Q2685 wdt:P102 ?party.
  ?member wdt:P102 ?party.
  ?member wdt:P31 wd:Q5.
  FILTER (?member != wd:Q2685)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
'''

# Kypher:
kgtk("""
    query -i all
         --match ' 
            (:Q2685)-[:P102]->(party),
            (member)-[:P102]->(party),
            (member)-[:P31]->(:Q5)'
         --where 'member != "Q2685"'
         --return 'distinct member as Member, party as Party' 
    / add-labels
""")

# What are the properties that describe an artist?

# In theory this one is heavy on Wikidata

# SPARQL: 
# TO DO
q4 = '''
SELECT DISTINCT ?p WHERE {
  ?subclasses rdfs:subClassOf* wd:Q483501.
  ?director wdt:P106 ?subclasses.
  ?director ?p ?o
}
'''

# In Kypher:
kgtk("""
    query -i all
      --match '
        (subclasses)-[:P279star]->(:Q483501),
        (director)-[:P106]->(subclasses),
        (director)-[l {label: p}]->()'
      --return 'distinct p as Property'
    / add-labels
""")

# And a film director?
# SPARQL: 
# TO DO
q5 = '''
SELECT DISTINCT ?p WHERE {
  ?subclasses rdfs:subClassOf* wd:Q2526255.
  ?director wdt:P106 ?c.
  ?director ?prop ?o.
}
'''


# In Kypher:
kgtk("""
    query -i all
      --match '
        (subclasses)-[:P106]->(:Q2526255),
        (s)-[l {label: p}]->()'
      --return 'distinct p as Properties'
    / add-labels
""")

# Embeddings. Run the noebook https://colab.research.google.com/drive/1A55l10voA4jnjoju3fojJWY3buLfaR4i?usp=sharing. 
# Which are the top 10 similar entities to Schwarzenegger? (list below) 
# TO DO

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