

# **Task 07: Querying RDF(s)**

get_ipython().system('pip install rdflib ')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"


# Leemos el fichero RDF de la forma que lo hemos venido haciendo

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**

# TO DO
ns=Namespace("http://somewhere#")
# Visualize the results: rdflib
for s,p,o in g.triples((None,RDFS.subClassOf,ns.Person)):
    print(s)
#  sparql
print("SPAQRL soltion:")
q1=prepareQuery('''
SELECT ?s
WHERE {?s rdfs:subClassOf ns:Person.}''', 
initNs={'rdfs':RDFS, 'ns':ns}
)
for r in g.query(q1):

    print(r.s)

# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

# TO DO
#Visualize the results: rdflib
for s,_,_ in g.triples((None,RDF.type,ns.Person)):
    print(s)
for s2,_,_ in g.triples((None,RDFS.subClassOf,ns.Person)):
    for s3,_,_ in g.triples((None,RDF.type, s2)):
        print(s3)
# SPARQL
q1=prepareQuery("""
SELECT ?s
WHERE {
 ?s rdf:type/rdfs:subClassOf* ns:Person.
}""", initNs={'rdf':RDF,'ns':ns, 'rdfs':RDFS} )
print("SPAQRL soltion:")
for r in g.query(q1):
    print(r.s)

# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
# TO DO
#Visualize the results: rdflib
for s,_,_ in g.triples((None,RDF.type,ns.Person)):
    for s_,p,o in g.triples((s,None,None)):
     print(s_,p,o)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s1,p1,o1 in g.triples((None, RDF.type, s)):
    for s2,p2,o2 in g.triples((s1, None, None)):
      print(s2,p2,o2)

# SPARQL
q1=prepareQuery("""
SELECT ?sub ?prop ?obj
WHERE {
 ?sub rdf:type/rdfs:subClassOf* ns:Person;
    ?prop ?obj.
 
}""", initNs={'rdf':RDF,'ns':ns, 'rdfs':RDFS} )
print("SPAQRL soltion:")
for r in g.query(q1):
    print(r.sub,r.prop, r.obj)




