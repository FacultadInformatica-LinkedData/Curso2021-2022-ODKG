from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
import geopy.distance

class OpenGraph:
      
    def __init__(self, name_of_file):  
        self.g = Graph()
        self.ns = Namespace("http://e-scooter.com/ontology#")
        self.g.namespace_manager.bind('ns', Namespace("http://e-scooter.com/ontology#"), override=False)
        # self.g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
        self.g.parse("./rdf/{}.ttl".format(name_of_file), format="turtle")
      
    def allPredicats(self):
        predicats = []
        for s, p, o in self.g:
            print(s, p, o)
            predicats.append(p)
        return predicats
    
    def allCommunities(self):
        communities = []
        for s, p ,o in self.g.triples((None, RDF.type, self.ns.Community)):
            communities.append(s)
        return communities

    def allCommunitiesWithQuery(self):
        communities = []
        query = prepareQuery('''
            SELECT distinct ?Community
            WHERE {
                {?Community rdf:type ns:Community}
            }
        ''', initNs = {"ns": self.ns}
        )

        for result in self.g.query(query):
            communities.append(result[0])
            print(result)
        return communities

    def find_escooters_near(self, latitude, longitude, max_distance):#, latitude, longitude, max_distance
        # Query all escooter instances and then calculate distance to user
        query = prepareQuery('''
            SELECT ?trip ?latitude ?longitude
            WHERE {
                {?trip rdf:type ns:Trip}.
                {?trip ns:hasEndCentroid ?centroid}.
                {?centroid ns:hasLocation ?location}.
                {?location ns:hasLatitude ?latitude}.
                {?location ns:hasLongitude ?longitude}
            }
        ''', initNs = {"ns": self.ns}
        )
        res = []
        for result in self.g.query(query):
            res.append(result)

        out = []
        for scooter in res:
            latitude_target = scooter[1].toPython()
            longitude_target = scooter[2].toPython()
            dst = geopy.distance.distance((float(latitude), float(longitude)), (latitude_target,longitude_target)).km
            if (dst <= float(max_distance)):
                out.append([scooter[0].toPython(), latitude_target, longitude_target, dst])
        return out