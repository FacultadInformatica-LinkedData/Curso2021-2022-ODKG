## 1. Get all the properties that can be applied to instances of the Politician class
PREFIX vocab: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?prop WHERE {
?instance a vocab:Politician;
       ?prop ?value.
}

## 2. Get all the properties, except rdf:type, that can be applied to instances of the Politician class
PREFIX vocab: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?prop WHERE {
?instance a vocab:Politician;
       ?prop ?value.
FILTER(?prop != rdf:type)
}

## 3. Which different values exist for the properties, except rdf:type, of the instances of the Politician class?
PREFIX vocab: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?value WHERE {
?instance a vocab:Politician;
       ?prop ?value.
FILTER(?prop != rdf:type)
}

## 4. For each of the properties, except rdf:type, that can be applied to instances of the Politician class, which different values do they take in those instances?
PREFIX vocab: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?prop?value WHERE {
?instance a vocab:Politician;
       ?prop ?value.
FILTER(?prop != rdf:type)
}

## 5. For each of the properties, except rdf:type, that can be applied to instances of the Politician class, how many distinct values do they take in hose instances?
PREFIX vocab: <http://dbpedia.org/ontology/>
SELECT DISTINCT  COUNT(DISTINCT ?value) WHERE {
?instance a vocab:Politician;
       ?prop ?value.
FILTER(?prop != rdf:type)
}