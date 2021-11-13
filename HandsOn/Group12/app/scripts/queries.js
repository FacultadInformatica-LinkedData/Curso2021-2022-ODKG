var allDistrictsQuery = `
    SELECT ?district ?districtLabel 
    WHERE {
      wd:Q2807  wdt:P150 ?district
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
    }ORDER BY ?districtLabel
    `;

var allEventsQuery = `
        PREFIX schema: <http://schema.org/>
        PREFIX va: <http://code-research.eu/ontology/visual-analytics#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ns: <https://data.eventsatmadrid.org/ontology#>
        PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
        PREFIX shema: <http://schema.org/>
        PREFIX evt: <https://data.eventsatmadrid.org/resource/Event/>
        SELECT * WHERE {
           ?Events rdf:type ns:Event.
           ?Events rdfs:label ?Label.
           ?Events vcard:additional-name ?Title.
           ?Events ns:hasPrice ?Price.
           ?Events ns:eventType ?Type.
           ?Events schema:startDate ?StartDate.
           OPTIONAL { ?Events schema:startDate ?FinishDate}.
           ?Events schema:doorTime ?Hour.
           ?Events ns:hasTargetAudience ?TargetAudience.
           OPTIONAL { ?Events ns:hasDaysOfWeek ?Days}.
           OPTIONAL {?Events ns:exceptDates ?ExcludedDays}.
           ?Events vcard:hasURL ?URL.
           ?Events ns:isHeldAt ?facility.
           ?facility rdfs:label ?HeldIn
        } LIMIT 50
        `

var mainQuery = `
    PREFIX schema: <http://schema.org/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns: <https://data.eventsatmadrid.org/ontology#>
    PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
    PREFIX wiki: <https://wikidata.org/entity/>
    PREFIX evt: <https://data.eventsatmadrid.org/resource/Event/>
    SELECT * WHERE {
      ?Events rdf:type ns:Event.
      ?Events rdfs:label ?Label.
      OPTIONAL {?Events vcard:additional-name ?Title}.
      ?Events ns:hasPrice ?Price.
      ?Events schema:isAccessibleForFree ?isFree.
      ?Events ns:eventType ?Type.
      OPTIONAL {?Events schema:startDate ?StartDate}.
      OPTIONAL { ?Events schema:startDate ?FinishDate}.
      OPTIONAL {?Events schema:doorTime ?Hour}.
      OPTIONAL {?Events ns:hasTargetAudience ?TargetAudience}.
      OPTIONAL { ?Events ns:hasDaysOfWeek ?Days}.
      OPTIONAL {?Events ns:exceptDates ?ExcludedDays}.
      ?Events vcard:hasURL ?URL.
      ?Events ns:isHeldAt ?facility.
      ?facility rdfs:label ?HeldIn.
      ?facility ns:isInDistrict ?distric.
      ?distric owl:sameAs ?wikidata.
      
      #FILTERBYDATE
      #FILTERBYFACILITY
      #FILTERBYPRICE
      #FILTERBYTYPE
      #FILTERBYDISTRICT
     
      #FILTER (?StartDate >= "2021-11-21"^^xsd:date && ?StartDate <= "2021-11-21"^^xsd:date)
      #FILTER (strstarts(str(?HeldIn), 'B'))
      #FILTER (contains(?TargetAudience, "Niños"))
      #FILTER (?isFree = FILTRO)
      #FILTER (?wikidata = wiki:Q656196)
      
    } LIMIT 100
        `
var filterByDate = 'FILTER (?StartDate >= "TODAY"^^xsd:date && ?StartDate <= "DATE"^^xsd:date)';
var filterByFacility = 'FILTER (strstarts(str(?HeldIn), "FACILITY"))';
var filterByType = 'FILTER (contains(?TargetAudience, "TYPE") || contains(?Type, "TYPE"))';
var filterByPrice = 'FILTER (?isFree = PRICE)';
var filterByDistric = 'FILTER (?wikidata = DISTRICT)';