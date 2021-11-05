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
        "selector": "#ResCol"
      }

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

    //This is dummy data json parsed reponse with 10 events
    console.log(jsonResponseExample);
    jsonParsed = sparql.parseResponse(jsonResponseExample)
    toEvents(jsonParsed, config)

}

function toEvents(jsonParsed){
   /* <div class="row" id="cardrow">
     <div className="card" style="width: 18rem;">
        <div className="card-body">
            <h5 className="card-title">Event title</h5>
            <p className="card-text">Date</p>
            <p className="card-text">Facility</p>
            <p className="card-text">Price</p>
            <a href="#" className="btn btn-primary">Event page</a>
        </div>
    </div>*/
    var opts = {
        "selector": config.selector || null
    }

    var eventos = d3.select(opts.selector, "div")
    eventoCard = eventos.append("div").attr("class", "row").attr("id", "cardrow")
    eventoCard.selectAll("div")
        .data(jsonParsed)
        .enter()
        .append("div").attr("class", "card").attr("style", "width: 18rem")
        .append("div").attr("class", "card-body")
        .append("h5").attr("class", "card-title").text(function(col) { return col.Label })
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

