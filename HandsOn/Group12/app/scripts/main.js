const WIKI = 'http://www.wikidata.org/entity/';

const sparqlWikiData = new Sparql('https://query.wikidata.org/bigdata/namespace/wdq/sparql');
const events = new Events();

function loadDistricts(){
    sparqlWikiData.query(allDistrictsQuery).then(function(districts) {
          generateDistrict(districts);
    })
}

function loadEvents() {
    events.loadEvents(allEventsQuery);
}

function showMoreEvents() {
    events.showMore();
}

function filterByDistrict(){
    districValue = d3.select("#seldist").node().value;
    if (districValue !=='default'){
        distric = districValue.replace(WIKI,'wiki:')
        query = filterByDistrictQuery.replace('FILTRO', distric);
        events.loadEvents(query);
    }else{
        events.loadEvents(allEventsQuery);
    }

}

function generateDistrict(list_districts) {
    //generar option select y append
    for (dist of list_districts) {
        //console.log(dist.districtLabel);
        var x = document.createElement("OPTION"); //Creamos una nueva opcion para el desplegable
        x.setAttribute("value",dist.district); //Le asignamos el valor del dato obtenido
        var t = document.createTextNode(dist.districtLabel); //Le asignamos el nombre del dato obtenido
        x.appendChild(t);
        document.getElementById("seldist").appendChild(x);
    }
}