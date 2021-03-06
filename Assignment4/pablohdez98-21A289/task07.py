# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hiGbUYySIO6yOrHzvCIjqmjCS7JdsROr

**Task 07: Querying RDF(s)**
"""

# !pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

from rdflib.plugins.sparql import prepareQuery

ns = Namespace("http://somewhere#")

# RDFLib
print('**TASK 7.1: List all subclasses of "Person" with RDFLib**')
def getSubClassesRecursive(x):
  for s,p,o in g.triples((None, RDFS.subClassOf, x)):
    print(s)
    getSubClassesRecursive(s)

getSubClassesRecursive(ns.Person)

# SPARQL
print('**TASK 7.1: List all subclasses of "Person" with SPARQL**')
q1 = prepareQuery('''
  SELECT ?s WHERE {
    ?s rdfs:subClassOf+ ns:Person
  }
  ''',
  initNs = { "ns": ns}
)
# Visualize the results
for r in g.query(q1):
  print(r.s)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**"""

# RDFLib
print('**TASK 7.2: List all individuals of "Person" with RDFLib (remember the subClasses)**')
def getAllIndividualsRecursive(x):
  for s1,_,_ in g.triples((None, RDFS.subClassOf, x)):
    for s2,_,_ in g.triples((None, RDF.type, s1)):
      print(s2)
    getAllIndividualsRecursive(s1)

for s,_,_ in g.triples((None, RDF.type, ns.Person)):
  print(s)

getAllIndividualsRecursive(ns.Person)

# SPARQL
print('**TASK 7.2: List all individuals of "Person" with SPARQL (remember the subClasses)**')
q2 = prepareQuery('''
  SELECT ?s WHERE {
    ?s rdf:type/rdfs:subClassOf* ns:Person
  }
  ''',
  initNs = { "ns": ns}
)
# Visualize the results
for r in g.query(q2):
  print(r.s)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**"""

# RDFLib
print('**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib**')
def getAllRecursive(x):
  for s1,_,_ in g.triples((None, RDFS.subClassOf, x)):
    for s2,_,_ in g.triples((None, RDF.type, s1)):
      for s3,p3,o3 in g.triples((s2, None, None)):
        print(s3,p3,o3)
    getAllRecursive(s1)

for s1,_,_ in g.triples((None, RDF.type, ns.Person)):
  for s2,p2,o2 in g.triples((s1, None, None)):
    print(s2,p2,o2)

getAllRecursive(ns.Person)

# SPARQL
print('**TASK 7.3: List all individuals of "Person" and all their properties including their class with SPARQL**')
q3 = prepareQuery('''
  SELECT * WHERE {
    ?s rdf:type/rdfs:subClassOf* ns:Person.
    ?s ?p ?o
  }
  ''',
  initNs = { "ns": ns}
)
# Visualize the results
for r in g.query(q3):
  print(r.s, r.p, r.o)