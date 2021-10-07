#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[1]:


get_ipython().system('pip install rdflib ')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"


# Leemos el fichero RDF de la forma que lo hemos venido haciendo

# In[3]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**

# In[36]:


from rdflib.plugins.sparql import prepareQuery
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
ns = Namespace("http://somewhere#")

for s, p, o in g:
  print(s,p,o)

#RDFLib
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s)


# SPARQL
q1 = prepareQuery('''
  SELECT ?Subject WHERE { 
    ?Subject RDFS:subClassOf NS:Person.
  }
  ''',
  initNs = { "RDFS": RDFS, "NS": ns}
)


for r in g.query(q1):
  print(r.Subject)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[68]:


#RDFLib
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  print(s)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for si, pi, oi in g.triples((None, RDF.type, s)):
    print(si)

# SPARQL
q1 = prepareQuery('''
  SELECT ?Subject WHERE { 

    {
        ?Subject RDFS:subClassOf NS:Person.
    }
    UNION
    {
        ?Subject RDF:type ?s2.
        ?s2 RDFS:subClassOf NS:Person.
    }
  }
  ''',
                  initNs={"RDFS": RDFS, "NS": ns, "RDF": RDF}
                  )

for r in g.query(q1):
  print(r.Subject)
# Visualize the results


# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
# 

# In[80]:


for s, p, o in g.triples((None, RDF.type, ns.Person)):
  for si, pi, oi in g.triples((s, None, None)):
    print(s, pi, oi)

for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):  # Individuals of one of the subclasses of Person (SC)
  for si, pi, oi in g.triples((None, RDF.type, s)):
    for ss, pp, oo in g.triples((si, None, None)):
      print(ss, pp, oo)

# SPARQL
q1 = prepareQuery('''
  SELECT ?individual ?pro ?value WHERE { 
    {
        ?individual RDF:type NS:Person.
        ?individual ?pro ?value.
    }
    UNION 
    {
        ?individual ?pro ?value.
        ?individual RDF:type ?subclass.
        ?subclass RDFS:subClassOf NS:Person.      
    }
  }
  ''',
                  initNs={"RDFS": RDFS, "NS": ns, "RDF": RDF}
                  )

print()

for r in g.query(q1):
  print(r.individual, r.pro, r.value)


# In[ ]:




