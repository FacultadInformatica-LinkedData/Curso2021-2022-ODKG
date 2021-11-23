from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
import geopy.distance
import numpy as np
from collections import Counter

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
    
    # average trip duration
    # average trip distance
    # most common end community
    # most common start community
    
    
    def get_statistic(self):
        
        query = prepareQuery('''
            SELECT ?trip ?distance ?duration
            WHERE {
                {?trip rdf:type ns:Trip}.
                {?trip ns:hasTripDistance ?distance}.
                {?trip ns:hasTripDuration ?duration}.
            }
        ''', initNs = {"ns": self.ns}
        )
        trips = []
        distances = []
        durations = []
        for trip,distance,duration in self.g.query(query):
            trips.append(trip)
            distances.append(float(distance))
            durations.append(float(duration))
            
           
        
        return {'mean_distance':np.mean(distances),'mean_duration':np.mean(durations)}
    
    def get_monst_common_community(self):
        query = prepareQuery('''
            SELECT ?trip ?start_community ?end_community
            WHERE {
                {?trip rdf:type ns:Trip}.
                {?trip ns:hasStartCommunity ?start_community}.
                {?trip ns:hasEndCommunity ?end_comunity}.
            }
        ''', initNs = {"ns": self.ns}
        )
        trips = []
        start_communities = []
        end_communities = []
        for trip,start_community,end_community in self.g.query(query):
            if start_community != None:
                start_communities.append(start_community)
            if end_community != None:
                end_communities.append(end_community)
            
        
        data1 = Counter(start_communities)
        most_common_start = data1.most_common(1)
        
        data2 = Counter(end_communities)
        most_common_end = data2.most_common(1)
        
        return {'most_common_start':most_common_start,'most_common_end':most_common_end}
        
    
if __name__ == '__main__':
    obj = OpenGraph("mapped_data")
    out = obj.get_monst_common_community()
    print(out)
        
        
        
    
    
    
    
    
    
    