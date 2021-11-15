from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL


github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"

g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage + "rdf/data03.rdf", format="xml")
g2.parse(github_storage + "rdf/data04.rdf", format="xml")

print("Graph 1")
for s, p, o in g1:
    print(s, p, o)

print("\nGraph 2")
for s, p, o in g2:
    print(s, p, o)

"""Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos."""

ns1 = Namespace("http://data.three.org#")
ns2 = Namespace("http://data.four.org#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

given_family_g1 = {}

for sc in list(g1.transitive_subjects(RDFS.subClassOf, ns1.Person)):
    for s, p, o in g1.triples((None, RDF.type, sc)):
        if (s, vcard.Given, None) in g1 and (s, vcard.Family, None) in g1:
            given_family_g1[(g1.value(s, vcard.Given), g1.value(s, vcard.Family))] = s

for sc in list(g2.transitive_subjects(RDFS.subClassOf, ns2.Person)):
    for s, p, o in g2.triples((None, RDF.type, sc)):
        if (s, vcard.Given, None) in g2 and (s, vcard.Family, None) in g2:
            given = g2.value(s, vcard.Given)
            family = g2.value(s, vcard.Family)
            if (given, family) in given_family_g1.keys():
                g3.add((given_family_g1[(given, family)], OWL.sameAs, s))

print("\nGraph 3")
for s, p, o in g3:
    print(s, p, o)
