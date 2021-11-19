# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vTj3hOyIYaCCAnm4hT-8V65Wu_wVkXoP

**Task 07: Querying RDF(s)**
"""

!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

for s, p, o in g:
  print(s,p,o)

# TO DO
ns = Namespace("http://somewhere#")
#RDFLib
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  # Visualize the results
  print(s)

#SPARQL
from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?Subject rdfs:subClassOf ns:Person. 
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": ns}
)
  # Visualize the results
for r in g.query(q1):
  print(r.Subject)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
#RDFLib
for s1,p1,o1 in g.triples((None, RDF.type, ns.Person)):
    print(s1)
for s2,p2,o2 in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s3,p3,o3 in g.triples((None, RDF.type, s2)):
    print(s3)

#SPARQL
q2 = prepareQuery('''
  SELECT ?Subject WHERE { 
    {?Subject rdf:type ns:Person} UNION
    {?Subclass rdfs:subClassOf ns:Person.
    ?Subject rdf:type ?Subclass.}
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": ns, "rdf": RDF}
)
  # Visualize the results
for r in g.query(q2):
  print(r.Subject)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

# TO DO
#RDFLib
for s1,p1,o1 in g.triples((None, RDF.type, ns.Person)):
  for s2,p2,o2 in g.triples((s1, None, None)):
    print(s2,p2,o2)

for s1,p1,o1 in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s2,p2,o2 in g.triples((None, RDF.type, s1)):
    for s3,p3,o3 in g.triples((s2, None, None)):
      print(s3,p3,o3)
#SPARQL
q3 = prepareQuery('''
  SELECT ?Subject ?p ?o WHERE { 
    {?Subject rdf:type ns:Person.
    ?Subject ?p ?o} UNION
    {?Subclass rdfs:subClassOf ns:Person.
    ?Subject rdf:type ?Subclass.
    ?Subject ?p ?o}
  }
  ''',
  initNs = { "rdfs": RDFS, "ns": ns, "rdf": RDF}
)
  # Visualize the results
for r in g.query(q3):
  print(r.Subject, r.p, r.o)
# Visualize the results