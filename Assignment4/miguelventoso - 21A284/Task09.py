# %%
"""
**Task 09: Data linking**
"""

# %%
!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials/"

# %%
from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g3 = Graph()
g1.parse(github_storage+"rdf/data03.rdf", format="xml")
g2.parse(github_storage+"rdf/data04.rdf", format="xml")

# %%
"""
Busca individuos en los dos grafos y enlázalos mediante la propiedad OWL:sameAs, inserta estas coincidencias en g3. Consideramos dos individuos iguales si tienen el mismo apodo y nombre de familia. Ten en cuenta que las URI no tienen por qué ser iguales para un mismo individuo en los dos grafos.
"""

# %%
#First we set the neccesary parameters, we have different data in the graphs so we will need 2 different Namespace calls
from rdflib.namespace import RDF, RDFS, OWL
ns1=Namespace("http://data.three.org#")
ns2=Namespace("http://data.four.org#")
vcard=Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

# %%
#Now we look for all instances of person in both graphs, we need to nest loops since 
#we need to check all g2 individuals for each g1 individual
for a,b,c in g1.triples((None, RDF.type, ns1.Person)):
    for d,e,f in g2.triples((None, RDF.type, ns2.Person)):
        #Once we have a g1 and g2 individual, we check if they have the same given name AND family name
        if g1.value(a, vcard.Given, None) == g2.value(d, vcard.Given, None) and g1.value(a, vcard.Family, None) == g2.value(d, vcard.Family, None):
            #If both names match, they are the same person. We can now add the triplet on g3
            g3.add((a, OWL.sameAs, d))
            #We can add an extra triplet so nodes are connected both ways
            g3.add((d, OWL.sameAs, a))

# %%
#We check g3 now
for s,p,o in g3.triples((None, None, None)):
    for a,b,c in g3.triples((s, None, None)):
        print(a,b,c)

# %%
#We check g1 and g2 to see if g3 is correctly built
for s,p,o in g1.triples((None, None, None)):
    for a,b,c in g1.triples((s, None, None)):
        print(a,b,c)
print("------------------------------")
for s,p,o in g2.triples((None, None, None)):
    for a,b,c in g2.triples((s, None, None)):
        print(a,b,c)

# %%
"""
Since the only two persons that are repeated on both g1 and g2 are John Doe and Sara Jones, we have succesfully built g3.
"""

# %%
