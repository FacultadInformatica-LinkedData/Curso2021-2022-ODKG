# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/Coffode/Curso2021-2022-ODKG/blob/master/Assignment4/course_materials/notebooks/Task07.ipynb

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

# TO DO
ns = Namespace("http://somewhere#")

# Assuring the structure
for s, p, o in g:
  print(s,p,o)

# RDFLib
print('RDFLib')
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s)

########################
# SPARQL  
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?Subject rdfs:subClassOf  NS:Person. 
  }
  ''',
  initNs = {"NS": ns}
)


print('SPARQL')
for r in g.query(q1):
  print(r.Subject)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
ns = Namespace("http://somewhere#")

# RDFLib
print('RDFLib')
for s,p,o in g.triples((None, RDF.type, ns.Person)):
  print(s, p )
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s1, p1, o1 in g. triples((None, RDF.type,s))):  
        print(s1, p1 )

########################
# SPARQL  
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT ?Subject ?subClass WHERE { 
    ?Subject ?rdf:type  NS:Person. 
  }
  UNION
  {
    ?Subject1 rdfs:subClassOf NS:Person.
    ?Subject rdf:type ?Subject1
    
  }
  ''',
  initNs = {"NS": ns, "rdfs": RDFS, "rdf":RDF}
)


print('SPARQL')
for r in g.query(q1):
  print(r.Subject, r.subClass)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

# TO DO
ns = Namespace("http://somewhere#")

# RDFLib
print('RDFLib')
for s,p,o in g.triples((None, RDF.type, ns.Person)):
  #print(s, p, o )
  for s1,p1,o1 in g.triples((s, None, None)):
    print(s1, p1, o1)

for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  #print('spo:',s, p, o )
  for s1,p1,o1 in g.triples((None, RDF.type, s)):
    #print('spo1:',s1, p1, o1)
    for s2,p2,o2 in g.triples((s1, None, None)):
      print(s2, p2, o2)

########################
# SPARQL  
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT ?Subject ?property ?value  WHERE {
  {    
    ?Subject RDF:type  NS:Person. 
    ?Subject ?property ?value.
  }
  UNION 
  {
    ?Subject ?property ?value.
    ?Subject RDF:type ?subclass.
    ?subclass RDFS:subClassOf NS:Person.      
  }
  }
  ''',
  initNs = {"NS": ns, "RDFS": RDFS,"RDF": RDF }
)


print('SPARQL')
for r in g.query(q1):
  print(r.Subject, r.property, r.value)
