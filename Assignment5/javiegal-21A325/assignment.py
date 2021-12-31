from graph_tool.all import *
from kgtk.configure_kgtk_notebooks import ConfigureKGTK
from kgtk.functions import kgtk

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
ck.load_files_into_cache()

"""# About this assignment.
This assignment is based on https://github.com/usc-isi-i2/kgtk-notebooks/tree/main/tutorial. If you have any questions or doubts, it is encouraged to look how the tutorial performs the different operations.

Additional information can be found in https://kgtk.readthedocs.io/

## Simple graph statistics

"""
print('\nLet\'s calculate first some statistics about the KG. Count the number of instances:')
print(kgtk("""
    query -i all
        --match '(instance)-[:P31]->(class)'
        --return 'count(distinct instance) as count_instances'
"""))

print("\nNow, count the number of distinct properties:")
print(kgtk("""
    query -i all
        --match '(instance)-[l {label: property}]->(class)'
        --return 'count(distinct property) as count_property'
"""))

print("\nNow, let's count the frequency of those properties. That is, how many instances we can find with each property")
print(kgtk("""
    query -i all
        --match '(instance)-[l {label: property}]->(class)'
        --return 'l.label, count(distinct instance) as count_instances'
"""))

"""## Simple queries
Some of these queries are simple and will run in the Wikidata endpoint.
Try both of them using SPARQL and Kypher
"""

print("\nWhich actors has Schwarzenegger worked with throughout his career? (Print also the movie)")
print("In SPARQL (first 10 results):")
# SELECT ?actor ?movie ?actorLabel ?movieLabel WHERE {
#   ?movie wdt:P161 wd:Q2685.
#   ?movie wdt:P161 ?actor.
#   FILTER (?actor != wd:Q2685)
#   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
# }
# Link to query:
# https://query.wikidata.org/#SELECT%20%3Factor%20%3Fmovie%20%3FactorLabel%20%3FmovieLabel%20WHERE%20%7B%0A%20%20%3Fmovie%20wdt%3AP161%20wd%3AQ2685.%0A%20%20%3Fmovie%20wdt%3AP161%20%3Factor.%0A%20%20FILTER%20%28%3Factor%20%21%3D%20wd%3AQ2685%29%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%7D
print('''actor	movie	actorLabel	movieLabel
http://www.wikidata.org/entity/Q4490	http://www.wikidata.org/entity/Q45672	Zach Gilford	The Last Stand
http://www.wikidata.org/entity/Q182763	http://www.wikidata.org/entity/Q45672	Forest Whitaker	The Last Stand
http://www.wikidata.org/entity/Q240355	http://www.wikidata.org/entity/Q45672	Genesis Rodriguez	The Last Stand
http://www.wikidata.org/entity/Q253343	http://www.wikidata.org/entity/Q45672	Jaimie Alexander	The Last Stand
http://www.wikidata.org/entity/Q294819	http://www.wikidata.org/entity/Q45672	Rodrigo Santoro	The Last Stand
http://www.wikidata.org/entity/Q295034	http://www.wikidata.org/entity/Q45672	Johnny Knoxville	The Last Stand
http://www.wikidata.org/entity/Q295148	http://www.wikidata.org/entity/Q45672	Peter Stormare	The Last Stand
http://www.wikidata.org/entity/Q314290	http://www.wikidata.org/entity/Q45672	Harry Dean Stanton	The Last Stand
http://www.wikidata.org/entity/Q347395	http://www.wikidata.org/entity/Q45672	Luis Guzmán	The Last Stand''')

print("\nIn Kypher:")
print(kgtk("""
    query -i all
        --match '(:Q2685)<-[:P161]-(movie)-[:P161]->(actor)'
        --where 'actor != "Q2685"'
        --return 'actor, movie'
    / add-labels
"""))

print("\nHow many awards does Schwarzenegger have?")
print("In SPARQL:")
# SELECT (COUNT(?award) AS ?count_awards) WHERE {
#   wd:Q2685 wdt:P166 ?award
# }
# Link to query
# https://query.wikidata.org/#SELECT%20%28COUNT%28%3Faward%29%20AS%20%3Fcount_awards%29%20WHERE%20%7B%0A%20%20wd%3AQ2685%20wdt%3AP166%20%3Faward%0A%7D
print('''count_awards
15''')

print("\nIn Kypher:")
print(kgtk("""
    query -i all
        --match '(:Q2685)-[:P166]->(award)'
        --return 'count(award) as count_awards'
"""))

print("\nRetrieve at least two members of Schwarzenegger's political party. Make sure only persons are returned")
print("In SPARQL (first 10 results):")
# SELECT ?other ?party ?otherLabel ?partyLabel WHERE {
#   wd:Q2685 wdt:P102 ?party.
#   ?other wdt:P102 ?party.
#   ?other wdt:P31 wd:Q5.
#   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
#   FILTER (?other != wd:Q2685)
# }
# Link to query:
# https://query.wikidata.org/#SELECT%20%3Fother%20%3Fparty%20%3FotherLabel%20%3FpartyLabel%20WHERE%20%7B%0A%20%20wd%3AQ2685%20wdt%3AP102%20%3Fparty.%0A%20%20%3Fother%20wdt%3AP102%20%3Fparty.%0A%20%20%3Fother%20wdt%3AP31%20wd%3AQ5.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%20%20FILTER%20%28%3Fother%20%21%3D%20wd%3AQ2685%29%0A%7D
print('''other	party	otherLabel	partyLabel
http://www.wikidata.org/entity/Q171454	http://www.wikidata.org/entity/Q29468	Oral Roberts	Republican Party
http://www.wikidata.org/entity/Q171736	http://www.wikidata.org/entity/Q29468	Robert Duvall	Republican Party
http://www.wikidata.org/entity/Q171989	http://www.wikidata.org/entity/Q29468	James R. Schlesinger	Republican Party
http://www.wikidata.org/entity/Q172155	http://www.wikidata.org/entity/Q29468	Roger Penske	Republican Party
http://www.wikidata.org/entity/Q173797	http://www.wikidata.org/entity/Q29468	William Whitney Rice	Republican Party
http://www.wikidata.org/entity/Q173839	http://www.wikidata.org/entity/Q29468	Tom Cole	Republican Party
http://www.wikidata.org/entity/Q173897	http://www.wikidata.org/entity/Q29468	John Bassett Moore	Republican Party
http://www.wikidata.org/entity/Q173981	http://www.wikidata.org/entity/Q29468	Samuel D. Nicholson	Republican Party
http://www.wikidata.org/entity/Q174037	http://www.wikidata.org/entity/Q29468	Henry Cabot Lodge	Republican Party
http://www.wikidata.org/entity/Q174264	http://www.wikidata.org/entity/Q29468	David Dreier	Republican Party''')

print("\nIn Kypher:")
print(kgtk("""
    query -i all
        --match '(:Q2685)-[:P102]->(party)<-[:P102]-(other)-[:P31]->(:Q5)'
        --where 'other != "Q2685"'
        --return 'other, party'
    / add-labels
"""))

print("\nWhat are the properties that describe an artist?")
# In theory this one is heavy on Wikidata
print("In SPARQL (first 10 results):")
# SELECT DISTINCT ?property WHERE {
#   ?class rdfs:subClassOf* wd:Q483501.
#   ?element wdt:P106 ?class.
#   ?element ?property ?p.
# }
# Link to query:
# https://query.wikidata.org/#SELECT%20DISTINCT%20%3Fproperty%20WHERE%20%7B%0A%20%20%3Fclass%20rdfs%3AsubClassOf%2a%20wd%3AQ483501.%0A%20%20%3Felement%20wdt%3AP106%20%3Fclass.%0A%20%20%3Felement%20%3Fproperty%20%3Fp.%0A%7D
print('''property
http://schema.org/version
http://schema.org/dateModified
http://schema.org/description
http://www.w3.org/1999/02/22-rdf-syntax-ns#type
http://www.w3.org/2000/01/rdf-schema#label
http://www.wikidata.org/prop/P19
http://www.wikidata.org/prop/P20
http://www.wikidata.org/prop/P21
http://www.wikidata.org/prop/P27
http://www.wikidata.org/prop/P31''')

print("\nIn Kypher:")
print(kgtk("""
    query -i all
        --match '()<-[l {label: property}]-(element)-[:P106]->(class)-[:P279star]->(:Q483501)'
        --return 'distinct property'
"""))

print("\nAnd a film director?")
print("In SPARQL (first 10 results):")
# SELECT DISTINCT ?property WHERE {
#         ?class rdfs:subClassOf* wd:Q2526255.
#         ?element wdt:P106 ?class.
#         ?element ?property ?p.
# }
# Link to query:
# https://query.wikidata.org/#SELECT%20DISTINCT%20%3Fproperty%20WHERE%20%7B%0A%20%20%20%20%20%20%20%20%3Fclass%20rdfs%3AsubClassOf%2a%20wd%3AQ2526255.%0A%20%20%20%20%20%20%20%20%3Felement%20wdt%3AP106%20%3Fclass.%0A%20%20%20%20%20%20%20%20%3Felement%20%3Fproperty%20%3Fp.%0A%7D
print('''property
http://schema.org/version
http://schema.org/dateModified
http://schema.org/description
http://www.w3.org/2000/01/rdf-schema#label
http://www.wikidata.org/prop/P345
http://www.wikidata.org/prop/direct/P345
http://www.wikidata.org/prop/P570
http://www.wikidata.org/prop/P569
http://www.wikidata.org/prop/direct/P570
http://www.wikidata.org/prop/direct/P569''')

print("\nIn Kypher:")
print(kgtk("""
    query -i all
        --match '()<-[l {label: property}]-(element)-[:P106]->(class)-[:P279star]->(:Q2526255)'
        --return 'distinct property'
"""))

# Embeddings. Run the noebook https://colab.research.google.com/drive/1A55l10voA4jnjoju3fojJWY3buLfaR4i?usp=sharing.
print("\nWhich are the top 10 similar entities to Schwarzenegger? (list below)")
print('''
    1.- Arnold Schwarzenegger
    2.- Hugh O'Brian
    3.- John Larroquette
    4.- Carl Reiner
    5.- Harvey Fierstein
    6.- Tom Sizemore
    7.- Randy Quaid
    8.- Gene Kelly
    9.- DeForest Kelley
    10.- Robert Stack''')

"""## Network analysis
Print all the paths between Schwarzenegger and Trump

## Note that **you have to create a file `paths.tsv` with the node pairs you want to find the paths for. Upload it in the "content" folder**
"""

kgtk("""
    add-labels -i /tmp/projects/assignment/path.tsv
""")

print("\nCalculate all the paths between Trump and Schwarzenegger (max hops: 3) (\'/tmp/projects/assignment/path.tsv\' file needed)")
print(kgtk("""
    paths -i all
          --path-file /tmp/projects/assignment/path.tsv
          --statistics-only True
          --max_hops 3
"""))

print("\nRetrieve all the family of Schwarzenegger (child/father/mother/sibling/spouse relationships)")
print(kgtk("""
    reachable-nodes -i all
        --root Q2685
        --props P40 P3373 P26 P22 P25
        --label Pextended_family
    / add-labels
"""))

print("\nWhat are the 10 most relevant actors (pagerank) in the graph? (Use graph-statistics command to calculate page rank, and then filter only actors)")
# Hint: do the query after calculating the pagerank. See https://github.com/usc-isi-i2/kgtk-notebooks/blob/main/tutorial/06-kg-network-analysis.ipynb for inspiration
kgtk("""
    graph-statistics -i all -o /tmp/projects/assignment/metadata.pagerank.undirected.tsv.gz
    --compute-pagerank True
    --compute-hits False
    --page-rank-property P_pagerank
    --output-pagerank True
    --output-statistics-only
    --output-hits False
    --undirected True
    --log-file /tmp/projects/assignment/metadata.pagerank.undirected.summary.txt
""")

print(kgtk("""
    query  -i all -i /tmp/projects/assignment/metadata.pagerank.undirected.tsv.gz
        --match '
            all: (actor)-[:P106]->(:Q33999),
            pagerank: (actor)-[:P_pagerank]->(pagerank)'
        --return 'actor as node1, pagerank as node2'
        --order-by 'cast(pagerank, float) desc'
        --limit 10
    / add-labels
"""))
