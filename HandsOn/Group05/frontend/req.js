var endpointUrl = 'http://localhost:9999/blazegraph/sparql',
	sparqlQuery = "prefix : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?description ?date ?price ?url ?address WHERE { ?facility :hasDistrict <http://groupfive.edu/kg/resources/district/Centro> . ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address. ?event :hasFacility ?facility .?event :hasTitle ?title . ?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price . }";
    sparqlQuery2= " prefix : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT DISTINCT ?obj WHERE { ?district :hasDistrict ?obj }"
    sparqlQuery3 = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?eventType WHERE {?eventType rdfs:subClassOf <https://schema.org/Event> .}"
    sparqlQuery4 = "PREFIX : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT DISTINCT ?obj WHERE {?sub :hasAudiance ?obj .}"


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
$("#search").on("click",update)
$("#district").on("change",()=> console.log('change'));
$("#type").on("change",()=> console.log('change'));
$("#audience").on("change",()=> console.log('change'));


function get_district() {
    makeSPARQLQuery( endpointUrl, sparqlQuery2, function( data ) {
        
        
        console.log(data.results.bindings)
        var dt = []
        data.results.bindings.forEach(e => {dt.push(e.obj.value.split('/').splice(-1).join().split("%20").join(" "))})
        w3.displayObject("district", {"dis" : dt});
      }
      );
}
function get_type() {
    makeSPARQLQuery( endpointUrl, sparqlQuery3, function( data ) {
        
        
        var dt = []
        console.log(data.results.bindings[0].eventType.value)
        data.results.bindings.forEach(e => {dt.push(e.eventType.value.split('/').splice(-1).join().split("%20").join(" ").split("#").splice(-1))})
        
        w3.displayObject("type", {"typ" : dt});
      }
      );
}

function get_audience() {
    makeSPARQLQuery( endpointUrl, sparqlQuery4, function( data ) {
        
        
        console.log(data.results.bindings)
        var dt = []
        data.results.bindings.forEach(e => {dt.push(e.obj.value.split('/').splice(-1).join().split("%20").join(" "))})
        w3.displayObject("audience", {"aud" : dt});
      }
      );
}


  function update(){
    var districtname = $( "#district" ).val();
    var type = $( "#type" ).val();
    var audience = $( "#audience" ).val();
    console.log(districtname)
    console.log(type)
    console.log(audience)
    
    var endpointUrl = 'http://localhost:9999/blazegraph/sparql';
        
    if(districtname=="District" && type=="Type" && audience=="Audience" ) {

        var sparqlQuery = "PREFIX : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?facility ?address ?date ?price ?url WHERE {  ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address. ?event :hasTitle ?title .?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price .} limit 10000"
        console.log(sparqlQuery)
    }
    else if (districtname !="District" && type=="Type" && audience=="Audience") {
        var sparqlQuery = "PREFIX : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?facility ?address ?date ?price ?url WHERE {  ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address .?event :hasFacility ?facility .?facility :hasDistrict <http://groupfive.edu/kg/resources/district/" + districtname + ">. ?event :hasTitle ?title  .?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price .}"
        
    } 
    else if (districtname !="District" && type != "Type" && audience=="Audience") {
        var sparqlQuery = "PREFIX : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?facility ?address ?date ?price ?url WHERE {  ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address .?event :hasFacility ?facility .?facility :hasDistrict <http://groupfive.edu/kg/resources/district/" + districtname + "> . ?event a :" + type + " . ?event :hasTitle ?title.?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price .}"

        
    }
    else if (districtname !="District" && type == "Type" && audience!="Audience") {
        var sparqlQuery = "PREFIX : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?facility ?address ?date ?price ?url WHERE {  ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address .?event :hasFacility ?facility .?facility :hasDistrict <http://groupfive.edu/kg/resources/district/" + districtname + "> . ?event :hasTitle ?title . ?event :hasAudiance <http://groupfive.edu/kg/resources/audiance/" + audience+ "> .?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price .}"      
    }
    else if (districtname =="District" && type != "Type" && audience=="Audience") {
        var sparqlQuery = "PREFIX : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?facility ?address ?date ?price ?url WHERE {  ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address .?event :hasFacility ?facility . ?event a :" + type + " . ?event :hasTitle ?title  .?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price .}"
    }
    else if (districtname =="District" && type == "Type" && audience!="Audience") {
        var sparqlQuery = "PREFIX : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?facility ?address ?date ?price ?url WHERE {  ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address .?event :hasFacility ?facility. ?event :hasTitle ?title . ?event :hasAudiance <http://groupfive.edu/kg/resources/audiance/" + audience+ "> .?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price .}"
    }
    else if (districtname =="District" && type != "Type" && audience !="Audience") {
        var sparqlQuery = "PREFIX : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?facility ?address ?date ?price ?url WHERE {  ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address .?event :hasFacility ?facility . ?event a :" + type + " . ?event :hasTitle ?title . ?event :hasAudiance <http://groupfive.edu/kg/resources/audiance/" + audience+ "> .?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price .}"
    }
    else {
        var sparqlQuery = "PREFIX : <http://groupfive.edu/kg/ontology/MadridEvents#> SELECT ?title ?facility ?address ?date ?price ?url WHERE {  ?facility <http://www.w3.org/2006/vcard/ns#hasAddress> ?address .?event :hasFacility ?facility .?facility :hasDistrict <http://groupfive.edu/kg/resources/district/" + districtname + "> . ?event a :" + type + " . ?event :hasTitle ?title . ?event :hasAudiance <http://groupfive.edu/kg/resources/audiance/" + audience+ "> .?event :hasStartingDate ?date . ?event :hasEventUrl ?url . ?event <https://saref.etsi.org/core/hasPrice> ?price .}"

        
    }
    console.log(sparqlQuery)

    makeSPARQLQuery( endpointUrl, sparqlQuery, function( data ) {
          
          
      
      var dt = []
      console.log(data.results.bindings)
      data.results.bindings.forEach(e => {dt.push({"title":e.title.value, "price":e.price.value, "Address":e.address.value.toLowerCase(), "date":e.date.value.substr(0,10), "facility": e.facility.value.split('/').splice(-1).join().split("%20").join(" ").split("%28").join(" ").split("%29").join(" ")}
      )})
      console.log(dt)
      
  
  
      grid.updateConfig({
        // lets update the columns field only
        columns: [{
          id:"title",
          name:"Title"
        },
        {
            id:"facility",
            name:"Facility"
          },
        {
          id:"Address",
          name:"Address"
        },
        {
            id:"price",
            name:"€"
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
  
  
    
  }