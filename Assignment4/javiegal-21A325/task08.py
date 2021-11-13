from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

g1 = Graph()
g2 = Graph()
g1.parse(github_storage + "/rdf/data01.rdf", format="xml")
g2.parse(github_storage + "/rdf/data02.rdf", format="xml")

print("Graph 1:")
for s, p, o in g1:
  print(s, p, o)


print("\nGraph 2:")
for s, p, o in g2:
  print(s, p, o)

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas."""


ns = Namespace("http://data.org#")

print("\nInstances of class Person")
for sc in list(g1.transitive_subjects(RDFS.subClassOf, ns.Person)):
    for s, p, o in g1.triples((None, RDF.type, sc)):
        print(s)

print("\nAdding properties from graph 2...")
for sc in list(g2.transitive_subjects(RDFS.subClassOf, ns.Person)):
    for s1, p1, o1 in g2.triples((None, RDF.type, sc)):
        for s2, p2, o2 in g2.triples((s1, None, None)):
            if not (s2, p2, o2) in g1:
                print("Adding ", s2, p2, o2)
                g1.add((s2, p2, o2))
