
// event listeners
$("#search").on("click",update);

$("#district").on("change",()=> console.log('change'));
$("#type").on("change",()=> console.log('change'));
$("#audience").on("change",()=> console.log('change'));



const grid= new gridjs.Grid({
  columns: ['Search an event !!'],
  data: [{}]
  
}).render(document.getElementById("wrapper"))

var endpointUrl = 'http://localhost:9999/blazegraph/sparql',
	sparqlQuery = "prefix : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?description ?date ?price ?url ?address WHERE { ?facility :hasDistrict <http://groupfive.edu/kg/resources/district/Centro> . ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address. ?event :hasFacility ?facility .?event :hasTitle ?title . ?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price . }";
  sparqlQuery2= " prefix : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT DISTINCT ?obj WHERE { ?district :hasDistrict ?obj }"





  






