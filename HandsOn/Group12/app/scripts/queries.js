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

var filterByDistrictQuery = `
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ns: <https://data.eventsatmadrid.org/ontology#>
        PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
        PREFIX schema: <http://schema.org/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX evt: <https://data.eventsatmadrid.org/resource/Event/>
        PREFIX wiki: <https://wikidata.org/entity/>
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
          ?facility rdfs:label ?HeldIn.
          ?facility ns:isInDistrict ?distric.
          ?distric owl:sameAs ?wikidata
          FILTER (?wikidata = FILTRO).
        } LIMIT 100
        `