# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/103U6QO3sBi8TQGrc9KDOnG1WvimB7JE0

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

from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s,p,o)

q1 = prepareQuery('''
  SELECT DISTINCT
    ?sc 

  WHERE { 

    ?sc rdfs:subClassOf  ns:Person. 

  } 
  ''', 
  initNs = { "rdfs": RDFS, "ns": ns}
)
for r in g.query(q1):
  print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

for s,p,o in g.triples((None, RDF.type, ns.Person)):
  print(s)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s1,p1,o1 in g.triples((None, RDF.type, s)):
    print(s1)

q1 = prepareQuery('''
  SELECT 
    ?sc1
  WHERE { 
    { 
      ?sc1 rdf:type ns:Person. 
    } UNION {
      ?sc2 rdfs:subClassOf ns:Person.
      ?sc1 rdf:type ?sc2
    }
  }
  ''',
  initNs = { "rdfs": RDFS,"rdf": RDF, "ns": ns}
)

for r in g.query(q1):
  print(r)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

for s,p,o in g.triples((None, RDF.type, ns.Person)):
  for s1,p1,o1 in g.triples((s, None, None)):
    print(s1,p1,o1)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s1,p1,o1 in g.triples((None, RDF.type, s)):
    for s2,p2,o2 in g.triples((s1, None, None)):
      print(s2,p2,o2)

q1 = prepareQuery('''
  SELECT 
    ?sc ?o ?p
  WHERE { 
    { 
      ?sc rdf:type ns:Person.
      ?sc ?o ?p 
    } UNION {
      ?sc rdf:type ?sc1.
      ?sc ?o ?p.
      ?sc rdfs:subClassOf ns:Person.
      
    }
  }
  ''',
  initNs = { "rdfs": RDFS,"rdf": RDF, "ns": ns}
)

for r in g.query(q1):
  print(r)