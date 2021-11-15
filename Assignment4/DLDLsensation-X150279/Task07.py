#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[1]:


get_ipython().system('pip install rdflib ')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"


# Leemos el fichero RDF de la forma que lo hemos venido haciendo

# In[2]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**

# In[3]:


# TO DO
from rdflib.plugins.sparql import prepareQuery
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
ns = Namespace("http://somewhere#")

#RDFLib
for subject, propiedad, objeto in g.triples((None, RDFS.subClassOf, ns.Person)):
    print(subject)


# SPARQL
#Las 3 comillas dentro del prepareQuery son para poder hacer una consulta de más de una #linea

q1 = prepareQuery('''
  SELECT ?subject WHERE { 
    ?subject RDFS:subClassOf* ns:Person.
  }
  ''',
  initNs = { "RDFS": RDFS, "ns": ns}
)

# Visualize the results
print("Now lets see the SPARQL")
for r in g.query(q1):
    print(r)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[4]:


# TO DO
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
ns = Namespace("http://somewhere#")

#RDFLib
for subject, propiedad, objeto in g.triples((None, RDF.type, ns.Person)):
    print(subject)
for subject, propiedad, objeto in g.triples((None, RDFS.subClassOf, ns.Person)):
#Sacamos cada subclase primero, y luego de cada subclase, todos los individuos
  for subjectBuc, propiedadBuc, objetoBuc in g.triples((None, RDF.type, subject)):
    print(subjectBuc)

# SPARQL
q1 = prepareQuery('''
  SELECT ?subject WHERE { 
    {
        ?subject RDFS:subClassOf ns:Person.
    }
    UNION
    {
        ?subject RDF:type ?subjectBuc.
        ?subjectBuc RDFS:subClassOf* ns:Person.
    }
  }
  ''',
                  initNs={"RDFS": RDFS, "ns": ns, "RDF": RDF}
                  )
# Visualize the results
print("Now lets see the SPARQL")
for r in g.query(q1):
    print(r)


# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
# 

# In[5]:


# TO DO
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
ns = Namespace("http://somewhere#")

#RDFLib
for subject, propiedad, objeto in g.triples((None, RDF.type, ns.Person)):
    for subjectBuc, propiedadBuc, objetoBuc in g.triples((subject, None, None)):
        print(subject, propiedadBuc, objetoBuc)

for subject, propiedad, objeto in g.triples((None, RDFS.subClassOf, ns.Person)):  
#Sacamos cada subclase primero, y luego de cada subclase, todos los individuos
  for subjectBuc, propiedadBuc, objetoBuc in g.triples((None, RDF.type, subject)):
#Sacamos de cada uno de los individuos sus propiedades
    for subjectBuc2, propiedadBuc2, objetoBuc2 in g.triples((subjectBuc, None, None)):
          print(subjectBuc2, propiedadBuc2, objetoBuc2)

# SPARQL
q1 = prepareQuery('''
  SELECT ?subjectBuc ?prop ?value WHERE { 
    {
        ?subjectBuc rdf:type ns:Person.
        ?subjectBuc ?prop ?value.
    }
    UNION 
    {
        ?subjectBuc ?prop ?value.
        ?subjectBuc rdf:type ?subclass.
        ?subclass RDFS:subClassOf ns:Person.      
    }
  }
  ''',
                  initNs={"RDFS": RDFS, "ns": ns, "RDF": RDF}
                  )


# Visualize the results
print("Now lets see the SPARQL")

for r in g.query(q1):
  print(r.subjectBuc, r.prop, r.value)


# In[ ]:




