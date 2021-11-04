# %%
"""
**Task 08: Completing missing data**
"""

# %%
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

# %%
from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

# %%
"""
Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.
"""

# %%
#List all elements of Person in the first graph
from rdflib.namespace import RDF, RDFS
ns=Namespace("http://data.org#")
for s,p,o in g1.triples((None, RDF.type, ns.Person)):
    for a,b,c in g1.triples((s, None, None)):
        print(a,b,c)

# %%
#Now we iterate over the second graph and add the subject properties to the first
for s,p,o in g2.triples((None, RDF.type, ns.Person)):
    for a,b,c in g2.triples((s, None, None)):
        g1.add((a,b,c))

# %%
#Checking g2 elements
for s,p,o in g2.triples((None, RDF.type, ns.Person)):
    for a,b,c in g2.triples((s, None, None)):
        print(a,b,c)

# %%
#Checking if g1 elements are the same as g2 elements
for s,p,o in g1.triples((None, RDF.type, ns.Person)):
    for a,b,c in g1.triples((s, None, None)):
        print(a,b,c)

# %%
"""
G1 graph missing data has been filled with g2 data since both graphs hace same data, so task is completed.
"""

# %%
