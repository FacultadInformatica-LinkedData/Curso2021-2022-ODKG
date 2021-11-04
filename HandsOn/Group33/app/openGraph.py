from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS

class OpenGraph:
      
    def __init__(self, name_of_file):  
        self.g = Graph()
        # self.ns = Namespace("http://e-scooter.com/ontology#")

        # self.g.namespace_manager.bind('ns', Namespace("http://e-scooter.com/ontology#"), override=False)
        # self.g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
        self.g.parse("./rdf/{}.ttl".format(name_of_file), format="turtle")
      
    def allPredicats(self):
        # self.g.add((self.ns.Researcher, RDF.type, RDFS.Class))
        predicats = []
        for s, p, o in self.g:
            print(s, p, o)
            predicats.append(p)
        return predicats
