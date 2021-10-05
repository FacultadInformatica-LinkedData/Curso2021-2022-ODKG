# -*- coding: utf-8 -*-
"""Task08 - Completing Missing Data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13PTZ9Zaj4S8NwdPRnMKh6gMKtpAByAZF

**Task 08: Completing missing data**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas.

### List of all elements in class Person of the first graph (data01.rdf)
"""

# Initial glance of g1
for s, p, o in g1:
  print(s, p, o)

# Find out the namespaces in use
props = set()
for s, p, o in g1:
  props.add(str(s).partition("#")[0]+"#")
  props.add(str(p).partition("#")[0]+"#")

for prop in props:
  print(prop)

from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

data = Namespace("http://data.org#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
# g1.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
# g1.namespace_manager.bind('data', Namespace("http://data.org#"), override=False)

q1 = prepareQuery('''
  SELECT  ?subject 
  WHERE { 
    ?subject rdf:type/rdfs:subClassOf* data:Person. 
  }
  ''',
  initNs = { "rdf": RDF, "rdfs": RDFS, "vcard": vcard, "data": data}
)

# Visualize the results
for r in g1.query(q1):
 print(r)

"""### Fill up empty fields (given name, family name, email) of first graph with data of the second graph (data02.rdf)

"""

print("The following triplets were added:")
flag = bool()
for s2, p2, o2 in g2:
  flag = True
  for s1, p1, o1 in g1:
    if (s2,p2,o2) == (s1,p1,o1):
      flag = False
  if flag:
    if any(x in str(p2) for x in ['#Given', '#FN', '#EMAIL', "#Family"]):
      g1.add((s2,p2,o2))
      print(s2,p2,o2)