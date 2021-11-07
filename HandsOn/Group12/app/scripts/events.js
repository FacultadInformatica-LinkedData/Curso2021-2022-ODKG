var endpointdummy = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
var querydummy = `SELECT ?item ?itemLabel WHERE {
                        ?item wdt:P31 wd:Q146.
                        ?item rdfs:label ?itemLabel.
                        FILTER(LANG(?itemLabel) = 'en')
                      }
            `

var endpoint = 'http://localhost:9000/sparql'

var queryEvents = `
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns: <https://data.eventsatmadrid.org/ontology#>
    PREFIX evt: <https://data.eventsatmadrid.org/resource/Event/>
    SELECT * WHERE {
        ?Events rdf:type ns:Event.
        OPTIONAL { ?Events rdfs:label ?Label} .
        OPTIONAL { ?Events ns:hasTitle ?Title} .
        OPTIONAL { ?Events ns:hasDescription ?Description} .
        OPTIONAL { ?Events ns:hasPrice ?Price} .
        OPTIONAL { ?Events ns:hasType ?Type} .
        OPTIONAL { ?Events ns:hasStartDate ?StartDate} .
        OPTIONAL { ?Events ns:hasFinishDate ?FinishDate} .
        OPTIONAL { ?Events ns:hasHour ?Hour} .
        OPTIONAL { ?Events ns:hasTargetAudience ?TargetAudience} .
        OPTIONAL { ?Events ns:hasDays ?Days} .
        OPTIONAL {?Events ns:hasExcludedDays ?ExcludedDays} .
        OPTIONAL { ?Events ns:hasURL ?URL} .
        OPTIONAL { ?Events ns:isHeldIn ?HeldIn }
    } LIMIT 10
    `
var config = {
        "selector": "#result"
      }

var list_events = [];
var number_events = 2;

function loadEvents() {
    //this is dummy example
    result = sparql.get(endpointdummy, querydummy).then(function(data) {
      console.log(data)
      //htmltable(data, config)
    })

    //this is a query for events
    result = sparql.query(endpoint, queryEvents).then(function(data) {
      console.log(data)
    })

    console.log(jsonResponseExample);
    list_events = sparql.parseResponse(jsonResponseExample)
    loadMoreEvents(true) //render the first (number_events) events in HTML, deleting the previous
}

function loadMoreEvents(reset=false) {
    events = list_events.slice(0, number_events) //get a sublist of the first n(number_events) elements of events
    renderEvents(events, config, reset)//render the events in HTML
    list_events.splice(0,number_events)//delete the fist n(number_events) elements of events from original list
}

/*
Render the list of events in HTML similar to the template
if reset is true then previous events in DOM are deleted
 */
function renderEvents(events_json, config, reset=false){
   /* This is the template created dinamicaly
   <div class="card-body">
        <h5 class="card-title">Las palabras desnudas</h5>
        <h6 class="card-subtitle mb-2 text-muted">Fortificación y ciudad. 29 maquetas</h6>
        <p class="card-text"><small>Un hombre vive sumido en unaprofunda crisis tras varios añosseparado de la que fue su parejasentimental. La culpa, los remordimientosy la nostalgia, le mantienensumido en un estado de ansiedadconstante que le llevará a rozar lalocura. De ese período oscuronace la necesidad de escribir undiario personal. Lo que comenzócomo un ejercicio catártico, poco apoco se va convirtiendo en laaventura más fascinante de suvida? La que le llevará a encontrarun amor que jamás había conocido. 60 minutos</small></p>
        <span class="badge bg-success">CursosTalleres</span>
        <span class="badge bg-success">Mujeres</span>
        <hr class="col-12">
        <ul class="list-group list-group-flush">
            <li class="list-group-item"><i class="bi bi-calendar-range-fill" title="Date range"></i> 2021-10-05 - 2021-10-06 </li>
            <li class="list-group-item"><i class="bi bi-calendar-x-fill" title="Excluded days"></i> 12/10/2021</li>
            <li class="list-group-item"><i class="bi bi-calendar-week-fill" title="Days"></i> M,T,W,S,F</li>
            <li class="list-group-item"><i class="bi bi-clock-fill" title="Hour"></i> 20:00:00</li>
            <li class="list-group-item"><i class="bi bi-geo-alt-fill" title="Held in"></i> Centro cultural</li>
        </ul>
        <hr class="col-12">

        <i class="bi bi-currency-euro" title="Price"></i>
        <small class="text-muted">Gratuito</small>

        <div class="card-footer text-center">
           <a class="btn btn-primary" href="http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&amp;vgnextoid=785be0464605c710VgnVCM1000001d4a900aRCRD">Ver más</a>
        </div>
    </div>
   * */
    var opts = {
        "selector": config.selector || null
    }

    if(reset){
        d3.select(opts.selector).selectAll("*").remove();
    }

    var eventosDiv = d3.select(opts.selector, "div")
    var eventosRow = eventosDiv.append("div").attr("class", "row")
    var events = eventosRow.selectAll(".card-body")
        .data(events_json)
        .enter()
        .append("div").attr("class", "col col-xl-6 col-lg-12 col-md-12 col-sm-12")
        .append("div").attr("class", "card")
        .append("div").attr("class", "card-body")

    events.append("h5").attr("class", "card-title")
        .text(function(col) { return col.Label })
    events.append("h6").attr("class", "card-subtitle mb-2 text-muted")
        .text(function(col) { return col.Title })
    events.append("p").attr("class", "card-text")
        .style("height", "30vh").style("overflow", "auto")
        .append("small")
        .text(function(col) { return col.Description })

    events.append("span").attr("class", "badge bg-success me-1")
        .text(function(col) { return col.Type })
    events.append("span").attr("class", "badge bg-success")
        .text(function(col) { return col.TargetAudience })

    events.append("hr").attr("class", "col-12")

    properties = events.append("ul").attr("class", "list-group list-group-flush")
    properties.append("li").attr("class", "list-group-item")
        .append("i").attr("class", "bi bi-calendar-range-fill").attr("title", "Date range")
        .text(function(col)
            {
                var dateString = " "
                if(col.StartDate){
                    dateString += col.StartDate.toISOString().slice(0, 10);
                    if(col.FinishDate){
                        dateString += " - " + col.FinishDate.toISOString().slice(0, 10)
                    }
                }
                return dateString

            })
    properties.append("li").attr("class", "list-group-item")
        .append("i").attr("class", "bi bi-calendar-x-fill").attr("title", "Excluded days")
        .text(function(col)
            {
                if(col.ExcludedDays){
                    return " " + col.ExcludedDays
                }
                return ""
            })

    properties.append("li").attr("class", "list-group-item")
        .append("i").attr("class", "bi bi-calendar-week-fill").attr("title", "Days")
        .text(function(col)
            {
                if(col.Days){
                    return " " + col.Days
                }
                return ""
            })

    properties.append("li").attr("class", "list-group-item")
        .append("i").attr("class", "bi bi-clock-fill").attr("title", "Hour")
        .text(function(col)
            {
                if(col.Hour){
                    return " " + col.Hour
                }
                return ""
            })

    properties.append("li").attr("class", "list-group-item")
        .append("i").attr("class", "bi bi-geo-alt-fill").attr("title", "Held in")
        .text(function(col)
            {
                if(col.HeldIn){
                    return " " + col.HeldIn
                }
                return ""
            })

    events.append("hr").attr("class", "col-12")

    events.append("i").attr("class", "bi bi-currency-euro").attr("title", "Price")

    events.append("small").attr("class", "text-muted")
        .text(function(col) { return col.Price })

    events.append("div").attr("class", "card-footer text-center")
        .append("a").attr("class", "btn btn-primary")
        .attr("href", function(col) { return col.URL }).text("Ver más")

}

function htmltable(json, config) {
  config = config || {}

  var head = json.head.vars
  var data = json.results.bindings

  var opts = {
    "selector": config.selector || null
  }

  var table = d3.select(opts.selector, "htmltable").append("table").attr("class", "table table-bordered")
  var thead = table.append("thead")
  var tbody = table.append("tbody")
  thead.append("tr")
    .selectAll("th")
    .data(head)
    .enter()
    .append("th")
    .text(function(col) { return col })
  var rows = tbody.selectAll("tr")
    .data(data)
    .enter()
    .append("tr")
  var cells = rows.selectAll("td")
    .data(function(row) {
      return head.map(function(col) {
        return row[col] ? row[col].value : ""
      })
    })
    .enter()
    .append("td")
    .text(function(val) { return val })

  // default CSS
  table.style({
    "margin": "10px"
  })
  table.selectAll("th").style({
    "background": "#eeeeee",
    "text-transform": "capitalize",
  })
}

