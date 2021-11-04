# %%
"""
**Task 07: Querying RDF(s)**
"""

# %%
!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

# %%
"""
Leemos el fichero RDF de la forma que lo hemos venido haciendo
"""

# %%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# %%
"""
**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**
"""

# %%
#RDFlib
ns = Namespace("http://somewhere#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

for s, p, o in g.triples((None,RDFS.subClassOf,ns.Person)):
    print(s)

# %%
#SPARQL
from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
SELECT ?subclasses
WHERE {
    ?subclasses rdfs:subClassOf ns:Person.
}
''',
initNs = {"ns":ns, "rdfs":RDFS}
)

for r in g.query(q1):
    print(r)

# %%
"""
**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# %%
#RDFlib
#First we print all the Persons
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    print(s) 
#Then we look for its subclasses one by one (in this case it's only one, but works too) and print their individuals
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    #We need to put the object of the second loop the same as the subject of the first loop.
    for a,b,c in g.triples((None, RDF.type, s)):
        print(a)

# %%
#SPARQL
from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
SELECT ?individual
WHERE {
    {
        ?individual rdf:type ns:Person.
    }
    UNION
    {
        ?subclasses rdfs:subClassOf ns:Person.
        ?individual rdf:type ?subclasses
    }
}
''',
initNs = {"ns":ns, "rdfs":RDFS, "rdf": RDF}
)

for r in g.query(q1):
    print(r)

# %%
"""
**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

# %%
#RDFlib
#As we have to take into account the subclasses, first we loop over Person, and then, over its subclasses
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    #To get all their properties, just query all triplets that have each individual as a subject
    for a,b,c in g.triples((s, None, None)):
        print(a,b,c)

for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for a,b,c in g.triples((None, RDF.type, s)):
        for x,y,z in g.triples((a, None, None)):
            print(x,y,z)

# %%
#SPARQL
from rdflib.plugins.sparql import prepareQuery
#Adding a line on each query asking for the properties and object is enough
q1 = prepareQuery('''
SELECT ?subject ?property ?object
WHERE {
    {
        ?individual rdf:type ns:Person.
        ?individual ?property ?object
    }
    UNION
    {
        ?subclasses rdfs:subClassOf ns:Person.
        ?individual rdf:type ?subclasses.
        ?individual ?property ?object
    }
}
''',
initNs = {"ns":ns, "rdfs":RDFS, "rdf": RDF}
)

for r in g.query(q1):
    print(r)

# %%
