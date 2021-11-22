function Sparql(endpoint){
  this.endpoint = endpoint;
  this.version = "sparql.js version 2021-11-05";
  this.debug = true;  // set to true for showing debug information
  var xmlSchema = 'http://www.w3.org/2001/XMLSchema#';
  var fetch
  if (typeof window !== 'undefined') {
    fetch = window.fetch
  } else {
    fetch = require('isomorphic-fetch')
  }

    /*
    Execute a SPARQL query and get the result
    Example:
    [0 … 99]
      0:
      item: "http://www.wikidata.org/entity/Q30600575"
      itemLabel: "Orlando"
    1:
      item: "http://www.wikidata.org/entity/Q42442324"
      itemLabel: "Kiisu Miisu"
  */
  this.query = function (query, options) {
    return this.get(this.endpoint, query, options).then(this.parseResponse)
  }

    /*
    Execute a get request to a end-point and get the result in json
    Example:
    data:
      head:
        vars: Array(2)
        0: "item"
        1: "itemLabel"
      results:
        bindings: Array(152)
        0:
          item: {type: 'uri', value: 'http://www.wikidata.org/entity/Q30600575'}
          itemLabel: {xml:lang: 'en', type: 'literal', value: 'Orlando'}
        1:
          item: {type: 'uri', value: 'http://www.wikidata.org/entity/Q42442324'}
          itemLabel: {xml:lang: 'en', type: 'literal', value: 'Kiisu Miisu'}
  */
  this.get = function (endpoint, query, options) {
    url = parseURL(endpoint,query)
    if (this.debug) { console.log(url) }
    var defaultOptions = {
      method: 'GET',
      headers: {
        'Accept': 'application/sparql-results+json'
      }
    }
    Object.assign(defaultOptions, options)
    return fetch(url, defaultOptions)
      .then(function (response) {
        return response.json()
      })
  }

  this.parseResponse = function(json) {
    return json.results.bindings.map(function (row) {
      var rowObject = {}
      Object.keys(row).forEach(function (column) {
        rowObject[column] = dataTypeToJS(row[column])
      })
      return rowObject
    })
  }

  function parseURL(endpoint, query) {
    return endpoint + '?query=' + encodeURIComponent(query)
  }

  function dataTypeToJS (value) {
    var v = value.value
    if (typeof value.datatype === 'string') {
      var dt = value.datatype.replace(xmlSchema, '')
      switch (dt) {
        case 'string':
          v = String(v); break
        case 'boolean':
          v = Boolean(v === 'false' ? false : v); break
        case 'float':
        case 'integer':
        case 'long':
        case 'double':
        case 'decimal':
        case 'nonPositiveInteger':
        case 'nonNegativeInteger':
        case 'negativeInteger':
        case 'int':
        case 'unsignedLong':
        case 'positiveInteger':
        case 'short':
        case 'unsignedInt':
        case 'byte':
        case 'unsignedShort':
        case 'unsignedByte':
          v = Number(v); break
        case 'date':
        case 'dateTime':
          v = new Date(v); break
        case 'time':
          v = String(v); break
      }
    }
    return v
  }
}
