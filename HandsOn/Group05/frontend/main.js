

function makeSPARQLQuery( endpointUrl, sparqlQuery, doneCallback ) {
	var settings = {
		headers: { Accept: 'application/sparql-results+json' },
		data: { query: sparqlQuery }
	};
	return $.ajax( endpointUrl, settings ).then( doneCallback );
}
// event listeners
$("#district-select").on("change", update)
$("#audience-select").on("change", update)



var endpointUrl = 'https://query.wikidata.org/sparql',
	sparqlQuery = "#Chats\n" +
        "SELECT ?item ?itemLabel \n" +
        "WHERE \n" +
        "{\n" +
        "  ?item wdt:P31 wd:Q146. # doit avoir comme nature chat\n" +
        "  SERVICE wikibase:label { bd:serviceParam wikibase:language \"[AUTO_LANGUAGE],en\". } # le label viendra de préférence dans votre langue, et autrement en anglais\n" +
        "}";

const district = $("#district-select").val()
  

const grid= new gridjs.Grid({
  columns: ['district'],
  data: [
    
  ]
}).render(document.getElementById("wrapper"))

function update(){
    // filter data based on selections
  const district = $("#district-select").val()
  const audience = $("#audience-select").val()
  const category = $("#category-select").val()

  var endpointUrl = 'https://query.wikidata.org/sparql',
	sparqlQuery = "#Chats\n" +
        "SELECT ?item ?itemLabel \n" +
        "WHERE \n" +
        "{\n" +
        "  ?item wdt:P31 wd:Q146. # doit avoir comme nature chat\n" +
        "  SERVICE wikibase:label { bd:serviceParam wikibase:language \"[AUTO_LANGUAGE],en\". } # le label viendra de préférence dans votre langue, et autrement en anglais\n" +
        "}";


  makeSPARQLQuery( endpointUrl, sparqlQuery, function( data ) {
		$( 'body' ).append( $( '<pre>' ).text( JSON.stringify( data ) ) );
    
    var dt = []
    console.log(dt)
    data.results.bindings.forEach(e => {dt.push(e.itemLabel)})
    console.log(dt)
    console.log(district)

    grid.updateConfig({
      // lets update the columns field only
      columns: [{
        id:district,
        name:district
      },
      {
        id:district,
        name:district
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

}





