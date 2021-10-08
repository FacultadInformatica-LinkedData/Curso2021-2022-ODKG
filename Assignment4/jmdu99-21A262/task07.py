# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tV5j-DRcpPtoJGoMj8v2DSqR_9wyXeiE

**Task 07: Querying RDF(s)**
"""

# !pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/resources/example6.rdf", format="xml")
'''
# Para ver el grafo inicialmente
print("\nGrafo completo")
for s, p, o in g:
  print(s,p,o)
  '''
from rdflib.plugins.sparql import prepareQuery

ns = Namespace("http://somewhere#")

# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**
print("\nTASK 7.1: List all subclasses of Person with RDFLIB")

for s,p,o in g.triples((None,RDFS.subClassOf,ns.Person)):
    print(s)

print("\nTASK 7.1: List all subclasses of Person with SPARQL")

q1 = prepareQuery('''
  SELECT 
    ?Subject
  WHERE { 
    ?Subject rdfs:subClassOf ns:Person
  }
  ''',
  initNs = { "ns": ns, "rdfs": RDFS}
  )
for r in g.query(q1):
  print(r.Subject)

  
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

print("\nTASK 7.2: List all individuals of Person with RDFLIB")

for s,p,o in g.triples((None,RDF.type,ns.Person)):
    print(s)
for s,p,o in g.triples((None,RDFS.subClassOf,ns.Person)):
    for s2,p2,o2 in g.triples((None,RDF.type,s)):
        print(s2)


print("\nTASK 7.2: List all individuals of Person with SPARQL")

q2 = prepareQuery('''
  SELECT 
    ?Subject
  WHERE { 
    {?Subject rdf:type ns:Person} 
    UNION
    {
     ?Subject2 rdfs:subClassOf ns:Person.
     ?Subject  rdf:type ?Subject2 
    }
  }
  ''',
  initNs = { "ns": ns, "rdf": RDF}
  )

for r in g.query(q2):
  print(r.Subject)

# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
print("\nTASK 7.3: List all individuals of Person and all their properties including their class with RDFLib")

for s,p,o in g.triples((None,RDF.type,ns.Person)):
    for s2,p2,o2 in g.triples((s,None,None)):
        print(s2,p2,o2)
        
for s,p,o in g.triples((None,RDFS.subClassOf,ns.Person)):
    for s2,p2,o2 in g.triples((None,RDF.type,s)):
        for s3,p3,o3 in g.triples((s2,None,None)):
            print(s3,p3,o3)

print("\nTASK 7.3: List all individuals of Person and all their properties including their class with SPARQL")
q3 = prepareQuery('''
  SELECT 
    ?Subject ?Predicate ?Object
  WHERE {
      {
    ?Subject rdf:type ns:Person.
    ?Subject ?Predicate ?Object
    }
    UNION
    {
    ?Subject1 rdfs:subClassOf ns:Person.
    ?Subject rdf:type ?Subject1.
    ?Subject ?Predicate ?Object
    } 
  }
  ''',
  initNs = { "ns": ns, "rdf": RDF}
  )
      
for r in g.query(q3):
  print(r)