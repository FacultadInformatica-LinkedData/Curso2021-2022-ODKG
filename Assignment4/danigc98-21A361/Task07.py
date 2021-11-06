#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[1]:


# !pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"


# Leemos el fichero RDF de la forma que lo hemos venido haciendo

# In[2]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# In[9]:


# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**

print('  ----------------------------------SPARQL-------------------------------')
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import RDF, RDFS

ns = Namespace("http://somewhere#")
q1 = prepareQuery('''
  SELECT DISTINCT ?subclass WHERE { 
    ?subclass rdfs:subClassOf ns:Person. 
  }
  ''',
    initNs = {"rdfs": RDFS, "ns":ns}
)
for r in g.query(q1):
 print(r)


print(' ---------------------------------RDFLIB---------------------------------')


for subclass, pred, p in g.triples((None, RDFS.subClassOf, ns.Person)):
    print(subclass)


# In[12]:


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

print('  ----------------------------------SPARQL-------------------------------')
q2 = prepareQuery('''
  SELECT ?person WHERE { 
    ?subclass rdfs:subClassOf* ns:Person.
    ?person a ?subclass
  }
  ''',
    initNs = {"rdfs": RDFS, "ns":ns}
)
for r in g.query(q2):
 print(r)


print(' ---------------------------------RDFLIB---------------------------------')

for person, rel, p in g.triples((None, RDF.type, ns.Person)):
    print(person)
for subclass, pred, p in g.triples((None, RDFS.subClassOf, ns.Person)):
    for person, rel, s in g.triples((None, RDF.type, subclass)):
        print(person)


# In[15]:


# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
# 
print('  ----------------------------------SPARQL-------------------------------')

q3 = prepareQuery('''
  SELECT ?person ?predicate ?value WHERE { 
    ?subclass rdfs:subClassOf* ns:Person.
    ?person a ?subclass.
    ?person ?predicate ?value.
  }
  ''',
    initNs = {"rdfs": RDFS, "ns":ns}
)
for r in g.query(q3):
 print(r)


print(' ---------------------------------RDFLIB---------------------------------')
for person, rel, p in g.triples((None, RDF.type, ns.Person)):
    for pers, pred, val in g.triples((person, None, None)):
        print((pers, pred, val))
        
for subclass, pred, p in g.triples((None, RDFS.subClassOf, ns.Person)):
    for person, rel, s in g.triples((None, RDF.type, subclass)):
        for pers, pred, val in g.triples((person, None, None)):
            print((pers, pred, val))


# In[ ]:




