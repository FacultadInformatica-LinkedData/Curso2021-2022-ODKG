function makeSPARQLQuery( endpointUrl, sparqlQuery, doneCallback ) {
	var settings = {
		// headers: { Accept: 'application/sparql-results+json',
    // 'Access-Control-Allow-Origin': '*' }
    headers: { Accept: 'application/sparql-results+json' },
    data: {query: sparqlQuery}
	};
	return $.ajax( endpointUrl, settings ).then( doneCallback );
}
// event listeners
$("#district-select").on("change", update)
$("#audience-select").on("change", update)




const district = $("#district-select").val()


const grid= new gridjs.Grid({
  columns: ['district'],
  data: [
    
  ]
}).render(document.getElementById("wrapper"))

var endpointUrl = 'http://localhost:9999/blazegraph/sparql',
	sparqlQuery = "prefix : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?description ?date ?price ?url ?address WHERE { ?facility :hasDistrict <http://groupfive.edu/kg/resources/district/Centro> . ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address. ?event :hasFacility ?facility .?event :hasTitle ?title . ?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price . }";
  sparqlQuery2= " prefix : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT DISTINCT ?obj WHERE { ?district :hasDistrict ?obj }"

makeSPARQLQuery( endpointUrl, sparqlQuery2, function( data ) {
  $( 'body' ).append( $( '<pre>' ).text( JSON.stringify( data ) ) );
  
  var dt = []
  console.log(data.results.bindings)
  data.results.bindings.forEach(e => {dt.push(e.obj.value.split('/').splice(-1).join().split("%20").join(" "))})
  console.log(dt)
}
);

  makeSPARQLQuery( endpointUrl, sparqlQuery, function( data ) {
		$( 'body' ).append( $( '<pre>' ).text( JSON.stringify( data ) ) );
    
    var dt = []
    console.log(data.results.bindings[0].title)
    data.results.bindings.forEach(e => {dt.push(e.title)})
    console.log(district)
    
	}
);
function update(){
    // filter data based on selections
  const district = $("#district-select").val()
  const audience = $("#audience-select").val()
  const category = $("#category-select").val()

  var endpointUrl = 'http://localhost:9999/blazegraph/sparql',
	sparqlQuery = "prefix : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?description ?date ?price ?url ?address WHERE { ?facility :hasDistrict <http://groupfive.edu/kg/resources/district/Centro> . ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address. ?event :hasFacility ?facility .?event :hasTitle ?title . ?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price . }";
  console.log(sparqlQuery)


  
}

  makeSPARQLQuery( endpointUrl, sparqlQuery, function( data ) {
		$( 'body' ).append( $( '<pre>' ).text( JSON.stringify( data ) ) );
    
    var dt = []
    console.log(data)
    data.results.bindings.forEach(e => {dt.push({"title":e.title.value, "price":e.price.value, "Address":e.address.value.toLowerCase(), "date":e.date.value.substr(0,10)}
    )})
    console.log(dt)
    console.log(district)


    grid.updateConfig({
      // lets update the columns field only
      columns: [{
        id:"title",
        name:"Title"
      },
      {
        id:"price",
        name:"Price"
      },
      {
        id:"Address",
        name:"Address"
      },{
        id:"date",
        name:"Date"
      }],
      pagination: {
        limit: 10
      },
      search: true,
      resizable: true,
      sort: true,
      data:dt
    }).forceRender();

	}
);






