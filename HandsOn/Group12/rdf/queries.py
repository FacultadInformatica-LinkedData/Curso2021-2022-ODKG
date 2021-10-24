#!/usr/bin/python
# coding: iso-8859-15

from rdflib import Graph, Namespace, Literal
from rdflib.plugins.sparql import prepareQuery

"""Creamos un grafo vac�o"""

g = Graph()
g.parse("data.nt", format="ntriples")

#for subj, pred, obj in g:
#  print(subj,pred,obj)

NS = Namespace("https://data.eventsatmadrid.org/ontology#")

#All the facilities
q1 = prepareQuery('''
  SELECT ?Facility ?Neighborhood ?District WHERE { 
    ?Facility ns:isLocatedAt ?Neighborhood .
    ?Neighborhood ns:isInDistrict ?District  }
  ''',
  initNs = { "ns": NS}
)

for r in g.query(q1):
  print(r)

#All districts
q2 = prepareQuery('''
  SELECT distinct ?District WHERE { 
    ?Facility ns:isLocatedAt ?Neighborhood .
    ?Neighborhood ns:isInDistrict ?District  }
  ''',
  initNs = { "ns": NS}
)

for r in g.query(q2):
  print(r.District)

#All the events in a distric
q3 = prepareQuery('''
  SELECT distinct ?Events WHERE { 
    ?Events ns:isHeldIn ?Facility .
    ?Facility ns:isLocatedAt ?Neighborhood .
    ?Neighborhood ns:isInDistrict ?District .
    ?District ns:hasName "LATINA"}
  ''',
  initNs = { "ns": NS}
)

for r in g.query(q3):
  print(r)

#All the events in a facility
q4 = prepareQuery('''
  SELECT distinct ?Events WHERE { 
    ?Events ns:isHeldIn ?Facility .
    ?Facility ns:hasName "Teatro Circo Price"}
  ''',
  initNs = { "ns": NS}
)

for r in g.query(q4):
  print(r)

#All the events in a neighborhood with free access
q5 = prepareQuery('''
  SELECT distinct ?Events WHERE { 
    ?Events ns:hasPrice "Gratuito" .
    ?Events ns:isHeldIn ?Facility .
    ?Facility ns:isLocatedAt ?Neighborhood .
    ?Neighborhood ns:hasName "PUERTA DEL ANGEL"}
  ''',
  initNs = { "ns": NS}
)

for r in g.query(q5):
  print(r)

#All the events  for FAMILIAS and CODIGO POSTAL
q6 = prepareQuery('''
  SELECT distinct ?Events WHERE { 
    ?Events ns:hasType "Familias" .
    ?Events ns:isHeldIn ?Facility .
    ?Facility ns:hasAddress ?Address .
    ?Address ns:hasPostalCode "28047"^^xsd:int}
  ''',
  initNs = { "ns": NS}
)

for r in g.query(q6):
  print(r)

#All the events in certain postal code
q7 = prepareQuery('''
  SELECT distinct ?Events WHERE { 
    ?Events ns:isHeldIn ?Facility .
    ?Facility ns:hasAddress ?Address .
    ?Address ns:hasPostalCode "28047"^^xsd:int}
  ''',
  initNs = { "ns": NS}
)

for r in g.query(q7):
  print(r)

#All the events between two dates
q8 = prepareQuery('''
  SELECT ?title ?startDate WHERE { 
    ?Events ns:hasTitle ?title.
    ?Events ns:hasStartDate ?startDate.
    ?Events ns:hasFinishDate ?finishDate.
    FILTER  (?startDate > "2021-10-21"^^xsd:date)
    FILTER  (?finishDate < "2021-10-25"^^xsd:date)
    FILTER  (?finishDate = ?startDate)
    }
  ''',
  initNs = { "ns": NS}
)

for r in g.query(q8):
  print(r)

#how many free events are there in each distric for the next month?
q9 = prepareQuery('''
  SELECT ?District (COUNT(?Events) AS ?ccount) WHERE {
    ?Events ns:hasStartDate ?startDate.
    ?Events ns:hasFinishDate ?finishDate.
    ?Events ns:isHeldIn ?Facility .
    ?Events ns:hasPrice "Gratuito" .
    ?Facility ns:isLocatedAt ?Neighborhood .
    ?Neighborhood ns:isInDistrict ?District .
    FILTER  (?startDate >= "2021-10-21"^^xsd:date)
    FILTER  (?startDate <= "2021-11-21"^^xsd:date)
    }
   GROUP BY ?District
  ''',
  initNs = { "ns": NS}
)

for r in g.query(q9):
  print(r)


#Events tomorrow after 6:pm
q10 = prepareQuery('''
  SELECT ?title ?hour WHERE {
    ?Events ns:hasTitle ?title.
    ?Events ns:hasHour ?hour.
    ?Events ns:hasStartDate ?startDate.
    ?Events ns:hasFinishDate ?finishDate.
    ?Events ns:isHeldIn ?Facility .
    ?Facility ns:isLocatedAt ?Neighborhood .
    ?Neighborhood ns:isInDistrict ?District .
    FILTER  (?startDate = "2021-10-22"^^xsd:date)
    FILTER  (?startDate = ?finishDate)
    FILTER  (?hour >= "18"^^xsd:int)
    }
  ''',
  initNs = { "ns": NS}
)

for r in g.query(q10):
  print(r)


#Get the facilities and the number of free Events they have
q11 = prepareQuery('''
SELECT ?Facility ?freeEvents {
    SELECT ?Facility (COUNT(?Events) AS ?freeEvents)  WHERE {
      ?Events ns:isHeldIn ?Facility .
      ?Events ns:hasPrice ?price
      FILTER  (?price >= "Gratuito"^^xsd:string)
      }
      GROUP BY ?Facility
    }
    ORDER BY ?freeEvents DESC(?freeEvents)
  ''',
  initNs = { "ns": NS}
)

for r in g.query(q11):
  print(r)
