# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ODKXYb24F_yaAjoSiT5I4nXGwQFLfdFe

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

#visualization of the RDF file
for s,p,o in g:
  print(s,p,o)

#Serialization in ttl format for a better visualization
print(g.serialize(format="ttl"))

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

#Define the namespace
ns = Namespace("http://somewhere#")

#RDFLib
print("-- RDFLib --")
#Researcher is a subclass of Person
for s,p,o in g.triples((None,RDFS.subClassOf,ns.Person)):
  print(s)
#PhDstudent is a subclass of Researcher, which is a subclass of person, so it must be listed too
for a,b,c in g.triples((None,RDFS.subClassOf,s)):
  print(a)


#SPARQL
print("\n-- SPARQL --")
#Import of prepareQuery in order to be able to make a query with SPARQL
from rdflib.plugins.sparql import prepareQuery
#Prepare query1 selecting all the subjects that are subclass of person
q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?Subject rdfs:subClassOf/rdfs:subClassOf* ns:Person .
  }
  ''',
  initNs = { "ns": ns})

for r in g.query(q1):
  print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

#RDFLib
print("-- RDFLib --")
#We list the individuals of Person, but subclasses are not included
for s,p,o in g.triples((None,RDF.type,ns.Person)):
  print(s)
#Now let's include subclasses of Person in order to have all the individuals of Person
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
 for a,b,c in g.triples((None, RDF.type, s)):
    print(a)

#SPARQL
print("\n-- SPARQL --")
#Prepare a query selecting all the individuals of Person. Subclasses included
q2 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?Subject rdf:type/rdfs:subClassOf* ns:Person .
  }
  ''',
  initNs = { "ns": ns})
for r in g.query(q2):
  print(r)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

#RDFLib
print("-- RDFLib --")
#We list the individuals of Person and all their properties, but subclasses are not included
for s,p,o in g.triples((None,RDF.type,ns.Person)):
  for s1,p1,o1 in g.triples((s,None,None)):
      print(s1,p1,o1)
#Now let's include the subclasses and all their properties as well
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
 for a,b,c in g.triples((None, RDF.type, s)):
    for s2,p2,o2 in g.triples((a, None,None)):
      print(s2,p2,o2)

#SPARQL
print("\n-- SPARQL --")
#Prepare a query selecting all the individuals of Person. Subclasses included
q3 = prepareQuery('''
  SELECT ?s ?p ?o WHERE { 
    ?s rdf:type/rdfs:subClassOf* ns:Person .
    ?s ?p ?o .
  }
  ''',
  initNs = { "ns": ns})
for r in g.query(q3):
  print(r)