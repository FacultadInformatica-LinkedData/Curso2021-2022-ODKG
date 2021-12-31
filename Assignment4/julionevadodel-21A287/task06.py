# -*- coding: utf-8 -*-
"""Task06.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U5lvSizmik7jjvH6AeTpxjjVSK2etJMV

**Task 06: Modifying RDF(s)**
"""

#!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")

"""Create a new class named Researcher"""

ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.1: Create a new class named "University"**

"""

# TO DO
ns = Namespace("http://somewhere#")
g.add((ns.University, RDF.type, RDFS.Class))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.2: Add "Researcher" as a subclass of "Person"**"""

# TO DO
ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.3: Create a new individual of Researcher named "Jane Smith"**"""

# TO DO
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
fullName = Literal("Jane Smith")
resource1 = (ns.Jane,VCARD.FN,fullName)
resource2 = (ns.Jane,RDF.type,ns.Researcher)
g.add(resource1)
g.add(resource2)
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.4: Add to the individual JaneSmith the fullName, given and family names**"""

# TO DO
given = Literal("Jane")
family = Literal("Smith")
resource1 = (ns.Jane,VCARD.Given,given)
resource2 = (ns.Jane,VCARD.Family,family)
g.add(resource1)
g.add(resource2)
# Visualize the results
for s, p, o in g:
  print(s,p,o)

"""**TASK 6.5: Add UPM as the university where John Smith works**"""

# TO DO
resource = (ns.Jane,VCARD.Work,ns.UPM)
g.add(resource)
# Visualize the results
for s, p, o in g:
  print(s,p,o)