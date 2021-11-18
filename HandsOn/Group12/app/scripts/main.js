const WIKI = 'http://www.wikidata.org/entity/';

const sparqlWikiData = new Sparql('https://query.wikidata.org/bigdata/namespace/wdq/sparql');
const events = new Events();
let today = new Date();

function loadDistricts(){
    sparqlWikiData.query(allDistrictsQuery).then(function(districts) {
          generateDistrict(districts);
    })
}

function loadEvents() {
    events.loadEvents(mainQuery);
}

function showMoreEvents() {
    events.showMore(3);
}

function filterEvents(){
    let query = bordersQuery.replace('#FILTER', getSelectedDistrict());
    if (d3.select('input[id="nd"]:checked').node()) {
        sparqlWikiData.query(query).then(function(borders) {
            let borderList = borders.flatMap(x => x.borders.replace(WIKI,"wiki:")).toString();
            //console.log(borderList);
            let aux= getFilterByDistrict(borderList);
            //console.log(aux);
            let query = createFilters(aux);
            events.loadEvents(query);
        })
    }else{
        let query = createFilters();
        events.loadEvents(query);
    }
}

function getSelectedDistrict(){
    districValue = d3.select("#seldist").node().value;
    if (districValue !=='default'){
        distric = districValue.replace(WIKI,'wd:')
        return distric;
    }
    return '';
}

function createFilters(aux){
    let query = mainQuery;
    query = query.replace('#FILTERBYDATE', getFilterByDate());
    query = query.replace('#FILTERBYFACILITY', getFilterByFacility());
    query = query.replace('#FILTERBYPRICE', getFilterByPrice());
    query = query.replace('#FILTERBYTYPE', getFilterByType());
    if (aux) {
        query = query.replace('#FILTERBYDISTRICT', aux);
    } else {
        query = query.replace('#FILTERBYDISTRICT', getFilterByDistrict());
    }
    
    return query;
}

function getFilterByDate(){
    let dates = d3.select('input[name="radioDate"]:checked').node()
    if(dates){
        filter = filterByDate.replaceAll('TODAY', today.toISOString().slice(0, 10));
        var date = new Date();
        date.setDate(date.getDate() + Number(dates.value));
        return filter.replaceAll('DATE', date.toISOString().slice(0, 10));
    }
    return '';
}

function getFilterByFacility(){
    let facility = d3.select('input[name="radioFacility"]:checked').node()
    if(facility){
        return filterByFacility.replaceAll('FACILITY', facility.value);
    }
    return '';
}

function getFilterByPrice(){
    let price = d3.select('input[name="radioPrice"]:checked').node()
    if(price){
        return filterByPrice.replaceAll('PRICE', price.value==='free');
    }
    return '';
}

function getFilterByType(){
    let type = d3.select('input[name="radioType"]:checked').node()
    if(type){
        return filterByType.replaceAll('TYPE', type.value);
    }
    return '';
}

function getFilterByDistrict(borderList){
    districValue = d3.select("#seldist").node().value;
    if (districValue !=='default'){
        distric = districValue.replace(WIKI,'wiki:')
        if (borderList) {
            return filterByDistric.replaceAll('DISTRICT', distric+","+borderList);
        } else {
            return filterByDistric.replaceAll('DISTRICT', distric);
        }
        
    }
    return '';
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