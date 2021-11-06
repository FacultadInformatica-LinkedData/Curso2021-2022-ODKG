## 1.Get all the classes
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
SELECT ?class
WHERE { ?class a rdfs:Class.} 
 [output](http://sandbox.linkeddata.es/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2FGP-onto.fi.upm.es%2Fexercise2%23%3E%0D%0ASELECT+%3Fclass%0D%0AWHERE+%7B+%3Fclass+a+rdfs%3AClass.%7D+&format=text%2Fhtml&timeout=0&debug=on)
## 2. Get all the subclasses of the class Establishment
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
SELECT  ?subclass
WHERE { ?subclass rdfs:subClassOf vocab:Establishment.} 
[output](http://sandbox.linkeddata.es/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2FGP-onto.fi.upm.es%2Fexercise2%23%3E%0D%0ASELECT+%3Fsubclass%0D%0AWHERE+%7B+%3Fsubclass+rdfs%3AsubClassOf++vocab%3AEstablishment.%7D+&format=text%2Fhtml&timeout=0&debug=on)
## 3. Get all instances of the class City

PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
SELECT  ?class
WHERE { ?class a vocab:City.} 

[output](http://sandbox.linkeddata.es/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2FGP-onto.fi.upm.es%2Fexercise2%23%3E%0D%0ASELECT++%3Fclass%0D%0AWHERE+%7B+%3Fclass+a+vocab%3ACity.%7D+&format=text%2Fhtml&timeout=0&debug=on)

## 4. Get the number of inhabitants of Santiago de Compostela

PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
SELECT ?inhabitants
WHERE { vocab:Santiago_de_Compostela vocab:hasInhabitantNumber ?inhabitants.}

Santiago_de_Compostela has **300000 inhabitant**

## 5. Get the number of inhabitants of Santiago de Compostela and of Arzua

PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
SELECT ?san_inhabitants ?ar_inhabitants
WHERE { vocab:Santiago_de_Compostela vocab:hasInhabitantNumber ?san_inhabitants.
        vocab:Arzua vocab:hasInhabitantNumber ?ar_inhabitants.

}

Santiago_de_Compostela has **300000 inhabitant** and Arzua has **38900 inhabitant**


## 6. Get different places with the inhabitants number, ordering the results by name of the place (ascending)
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
SELECT ?place ?inhabitants
WHERE { ?place vocab:hasInhabitantNumber ?inhabitants.
}
ORDER BY ASC(?place)

[output](http://sandbox.linkeddata.es/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2FGP-onto.fi.upm.es%2Fexercise2%23%3E%0D%0ASELECT+%3Fplace+%3Finhabitants%0D%0AWHERE+%7B+%3Fplace+vocab%3AhasInhabitantNumber+%3Finhabitants.%0D%0A%0D%0A%7D%0D%0AORDER+BY+ASC%28%3Fplace%29&format=text%2Fhtml&timeout=0&debug=on)

## 7. Get all the instances of Locality with their inhabitant number (if it exists)
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
SELECT ?locality, ?inhabitants
WHERE {
?locality rdf:type/rdfs:subClassOf vocab:Locality. 
OPTIONAL {?locality vocab:hasInhabitantNumber ?inhabitants}
} 

[output](http://sandbox.linkeddata.es/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2FGP-onto.fi.upm.es%2Fexercise2%23%3E%0D%0ASELECT+%3Flocality%2C+%3Finhabitants%0D%0AWHERE+%7B%0D%0A%3Flocality+rdf%3Atype%2Frdfs%3AsubClassOf+vocab%3ALocality.+%0D%0AOPTIONAL+%7B%3Flocality+vocab%3AhasInhabitantNumber+%3Finhabitants%7D%0D%0A%7D+&format=text%2Fhtml&timeout=0&debug=on)

## 8. Get all the places with more than 200.000 inhabitants
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
SELECT *
WHERE {
 ?places vocab:hasInhabitantNumber ?inhabitants .
 FILTER(xsd:integer(?inhabitants) > 200000)
}

[output](http://sandbox.linkeddata.es/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2FGP-onto.fi.upm.es%2Fexercise2%23%3E%0D%0ASELECT+*%0D%0AWHERE+%7B%0D%0A+%3Fplaces+vocab%3AhasInhabitantNumber+%3Finhabitants+.%0D%0A+FILTER%28xsd%3Ainteger%28%3Finhabitants%29+%3E+200000%29%0D%0A%7D&format=text%2Fhtml&timeout=0&debug=on)

## 9. Get postal data of Pazo_Breogan (street, number, locality, province
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
SELECT *
WHERE {
vocab:Pazo_Breogan vocab:isPlacedIn ?province;
                  vocab:hasAddress ?adress.
        ?adress   vocab:hasStreet ?street;

                  vocab:hasNumber ?number.

}
[output](http://sandbox.linkeddata.es/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2FGP-onto.fi.upm.es%2Fexercise2%23%3E%0D%0ASELECT+*%0D%0AWHERE+%7B%0D%0Avocab%3APazo_Breogan+vocab%3AisPlacedIn+%3Fprovince%3B%0D%0A++++++++++++++++++vocab%3AhasAddress+%3Fadress.%0D%0A++++++++%3Fadress+++vocab%3AhasStreet+%3Fstreet%3B%0D%0A%0D%0A++++++++++++++++++vocab%3AhasNumber+%3Fnumber.%0D%0A%0D%0A%0D%0A%7D&format=text%2Fhtml&timeout=0&debug=on)

## 10. Get the subclasses of class Location
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
SELECT *
WHERE {
?subclass rdfs:subClassOf vocab:Locality
}
[output](http://sandbox.linkeddata.es/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2FGP-onto.fi.upm.es%2Fexercise2%23%3E%0D%0ASELECT+*%0D%0AWHERE+%7B%0D%0A%3Fsubclass+rdfs%3AsubClassOf+vocab%3ALocality%0D%0A%7D&format=text%2Fhtml&timeout=0&debug=on)

## 11. Get the instances of class Locality
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
SELECT *
WHERE {
?instance rdf:type/rdfs:subClassOf vocab:Locality 
}
[output](http://sandbox.linkeddata.es/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2FGP-onto.fi.upm.es%2Fexercise2%23%3E%0D%0ASELECT+*%0D%0AWHERE+%7B%0D%0A%3Finstance+rdf%3Atype%2Frdfs%3AsubClassOf+vocab%3ALocality+%0D%0A%7D&format=text%2Fhtml&timeout=0&debug=on)

## 12. Describe the resource with rdfs:label "Madrid"
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
DESCRIBE *
WHERE {
?resource rdfs:label "Madrid"
}
[OUTPUT](http://sandbox.linkeddata.es/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2FGP-onto.fi.upm.es%2Fexercise2%23%3E%0D%0ADESCRIBE+*%0D%0AWHERE+%7B%0D%0A%3Fresource+rdfs%3Alabel+%22Madrid%22%0D%0A%7D&format=text%2Fturtle&timeout=0&debug=on)

## 13. Construct the RDF(S) graph that directly relates all the touristic places with their respective provinces, using a new property called ”isIn” 
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
CONSTRUCT {
?touristic_places vocab:isIn ?province
}
WHERE {
?touristic_places rdf:type/rdfs:subClassOf vocab:TouristicLocation.
OPTIONAL {
  ?touristic_places vocab:isPlacedIn ?locality.
  ?locality vocab:inProvince ?province.
}
}

## 14. Ask if there is some instance of Town
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
ASK {
?instance rdf:type vocab:Town

}

## 15. Ask if there is some instance of Chapel
PREFIX vocab: <http://GP-onto.fi.upm.es/exercise2#>
ASK {
?instance rdf:type/rdfs:subClassOf vocab:Chapel
}