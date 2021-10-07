🔹 1. Get all the properties that can be applied to instances of the Politician class (<http://dbpedia.org/ontology/Politician>)

``` 
PREFIX vocab: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?props
WHERE
{?pol a <http://dbpedia.org/ontology/Politician> .
	?pol ?props ?data
}
``` 

[Result: #1 ](https://es.dbpedia.org/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0A%0D%0ASELECT+DISTINCT+%3Fprops%0D%0AWHERE%0D%0A%7B%3Fpol+a+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2FPolitician%3E+.%0D%0A%09%3Fpol+%3Fprops+%3Fdata%0D%0A%7D&should-sponge=&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+)

🔹 2. Get all the properties, except rdf:type, that can be applied to instances of the Politician class

``` 
PREFIX vocab: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?props
WHERE
{?pol a <http://dbpedia.org/ontology/Politician> .
?pol ?props ?data.
FILTER (?props != rdf:type)
}
``` 

[Result: #2 ](https://es.dbpedia.org/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0ASELECT+DISTINCT+%3Fprops%0D%0AWHERE%0D%0A%7B%3Fpol+a+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2FPolitician%3E+.%0D%0A%3Fpol+%3Fprops+%3Fdata.%0D%0AFILTER+%28%3Fprops+%21%3D+rdf%3Atype%29%0D%0A%7D&should-sponge=&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+)

🔹 3. Which different values exist for the properties, except for rdf:type, applicable to the instances of Politician?

``` 
PREFIX vocab: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?data
WHERE
{?pol a <http://dbpedia.org/ontology/Politician> .
?pol ?props ?data.
FILTER (?props != rdf:type)
}
``` 

[Result: #3 ](https://es.dbpedia.org/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0ASELECT+DISTINCT+%3Fdata%0D%0AWHERE%0D%0A%7B%3Fpol+a+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2FPolitician%3E+.%0D%0A%3Fpol+%3Fprops+%3Fdata.%0D%0AFILTER+%28%3Fprops+%21%3D+rdf%3Atype%29%0D%0A%7D&should-sponge=&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+)

🔹 4. For each of these applicable properties, except for rdf:type, which different values do they take globally for all those instances?

``` 
PREFIX vocab: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?props?data
WHERE
{?pol a <http://dbpedia.org/ontology/Politician> .
?pol ?props ?data.
FILTER (?props != rdf:type)
}
``` 
[Result: #4 ](https://es.dbpedia.org/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0ASELECT+DISTINCT+%3Fprops%3Fdata%0D%0AWHERE%0D%0A%7B%3Fpol+a+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2FPolitician%3E+.%0D%0A%3Fpol+%3Fprops+%3Fdata.%0D%0AFILTER+%28%3Fprops+%21%3D+rdf%3Atype%29%0D%0A%7D&should-sponge=&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+)

🔹 5. For each of these applicable properties, except for rdf:type, how many distinct values do they take globally for all those instances?

``` 
PREFIX vocab: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?props COUNT(DISTINCT ?data)
WHERE
{?pol a <http://dbpedia.org/ontology/Politician> .
?pol ?props ?data.
FILTER (?props != rdf:type)
}
``` 

[Result: #5 ](https://es.dbpedia.org/sparql?default-graph-uri=&query=PREFIX+vocab%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0ASELECT+DISTINCT+%3Fprops+COUNT%28DISTINCT+%3Fdata%29%0D%0AWHERE%0D%0A%7B%3Fpol+a+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2FPolitician%3E+.%0D%0A%3Fpol+%3Fprops+%3Fdata.%0D%0AFILTER+%28%3Fprops+%21%3D+rdf%3Atype%29%0D%0A%7D&should-sponge=&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+)
