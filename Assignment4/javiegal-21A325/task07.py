from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery


github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage + "/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

print("Task 7.1")
# RDFLib
ns = Namespace("http://somewhere#")

print("RDFLib:")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
    print(s)

# SPARQL
print("\nSPARQL")
q1 = prepareQuery('''
  SELECT ?subClass WHERE {
    ?subClass rdfs:subClassOf ns:Person.
  }
  ''',
                  initNs={"ns": ns, "rdfs": RDFS}
                  )

for r in g.query(q1):
    print(r.subClass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""
print("\nTask 7.2")

# RDFLib
print("RDFLib")
for sc in list(g.transitive_subjects(RDFS.subClassOf, ns.Person)):
    for s, p, o in g.triples((None, RDF.type, sc)):
        print(s)

# SPARQL
q1 = prepareQuery('''
  SELECT ?individual WHERE {
    ?individual rdf:type ?x.
    ?x rdfs:subClassOf* ns:Person
  }
  ''',
                  initNs={"ns": ns, "rdf": RDF, "rdfs": RDFS}
                  )

print("\nSPARQL")
for r in g.query(q1):
    print(r.individual)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

print("\nTask 7.3")
# RDFLib
print("RDFLib")
for sc in list(g.transitive_subjects(RDFS.subClassOf, ns.Person)):
    for s1, p1, o1 in g.triples((None, RDF.type, sc)):
        for s2, p2, o2 in g.triples((s1, None, None)):
            print(s2, p2, o2)

# SPARQL
q1 = prepareQuery('''
  SELECT ?individual ?p ?o WHERE {
    ?individual rdf:type ?x.
    ?x rdfs:subClassOf* ns:Person.
    ?individual ?p ?o
  }
  ''',
                  initNs={"ns": ns, "rdf": RDF, "rdfs": RDFS}
                  )

print("\nSPARQL")
for r in g.query(q1):
    print(r.individual, r.p, r.o)
