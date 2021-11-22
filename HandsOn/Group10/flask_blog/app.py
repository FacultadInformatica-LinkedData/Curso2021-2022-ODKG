from flask import Flask, render_template
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, FOAF
from rdflib.plugins.sparql import prepareQuery
from flask import request
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
import datetime
import re

app = Flask(__name__)

@app.route('/madridEvents',methods=["GET", "POST"] )

def index():

	headers = ['Event Title','Init Date','End Date','Type of Event','Location','Price','Link']
	table = 0
	if request.method == 'POST':
		req = request.form.get("init")
		req1 = request.form.get("fin")
		req2 = request.form.get("grat")
		req3 = request.form.get("local")
		table = queries(gratuito=req2, fecha_in=req, fecha_ax=req1, tipo=req3)
		return render_template('index.html',headers=headers, objects=table)
	else:
		table = query_inicial()			
		return render_template('index.html',headers=headers, objects=table)
		
		


def dateTimeToString(dateTime):
	day, time = dateTime.split("T")
	day = day.replace("-","/")
	time = time.split("+")[0]
	return("Day: " + day + '\n' + "Time: " + time)
		
def query_inicial():
	RDFsource = "https://raw.githubusercontent.com/pablo-crucera/Curso2021-2022-ODKG/master/HandsOn/Group10/rdf/eventosfinal-deverdad.ttl"
	g = Graph()
	g.namespace_manager.bind('ns', Namespace("http://www.example.org#"), override=False)
	g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
	g.namespace_manager.bind('xsd', Namespace("http://www.w3.org/2001/XMLSchema#"), override=False)
	g.namespace_manager.bind('smart', Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#"), override=False)
	g.parse(RDFsource, format="ttl")
	smart = Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#")
	xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
	q = prepareQuery('''
		SELECT ?title ?startDate ?endDate ?typeEvent ?location ?price ?link WHERE {
		?event a smart:Event.
		?event smart:title ?title.
		?event smart:startDate ?startDate.
		?event smart:takesPlaceIn ?facility.
		?facility smart:name ?location.
		?event smart:endDate ?endDate.
		?event smart:price ?price.
		?event smart:URI ?link.
		?event smart:isA ?category.
		?category smart:name ?typeEvent
		}
		''',
		initNs = { "smart": smart, "xsd": xsd}
	)

	queryOut = g.query(q)
	queryOut = [(title, dateTimeToString(startDate), dateTimeToString(endDate),' '.join(re.findall('[A-Z][a-z]*',typeEvent)), location, price, URL) for title, startDate, endDate, typeEvent , location, price, URL in queryOut]
	return queryOut





def queries(gratuito=None, fecha_in=None, fecha_ax=None, tipo=None):
	RDFsource = "https://raw.githubusercontent.com/pablo-crucera/Curso2021-2022-ODKG/master/HandsOn/Group10/rdf/eventosfinal-deverdad.ttl"
	g = Graph()
	g.namespace_manager.bind('ns', Namespace("http://www.example.org#"), override=False)
	g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
	g.namespace_manager.bind('xsd', Namespace("http://www.w3.org/2001/XMLSchema#"), override=False)
	g.namespace_manager.bind('smart', Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#"), override=False)
	g.parse(RDFsource, format="ttl")
	smart = Namespace("http://smartcity.linkeddata.es/lcc/ontology/MadridEvents#")
	xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

	if fecha_in == "":
		fecha_min = "2020-01-01T00:00:00Z"
	else:
		day_month_year = fecha_in.split('-')
		fecha_min = str(datetime.datetime(int(day_month_year[0]), int(day_month_year[1]), int(day_month_year[2]))).replace(" ","T") + "Z"
			
	if fecha_ax == "":
		fecha_max = "2023-01-01T00:00:00Z"
	else:
		day_month_year = fecha_ax.split('-')
		fecha_max = str(datetime.datetime(int(day_month_year[0]), int(day_month_year[1]), int(day_month_year[2]))).replace(" ","T") + "Z"

	if gratuito == "gratis":
		grat = True
	else:
		grat = False
	
	if tipo == "Todas":
		buscaPorTipo = False
	else:
		buscaPorTipo = True

	q = '''
	SELECT ?title ?startDate ?endDate ?typeEvent ?location ?price ?link WHERE {
		?event a smart:Event.
		?event smart:title ?title.
		?event smart:startDate ?startDate.
		?event smart:takesPlaceIn ?facility.
		?facility smart:name ?location.
		?event smart:endDate ?endDate.
		?event smart:price ?price.
		?event smart:URI ?link.
		
		FILTER(?startDate > "''' + fecha_min + '''"^^xsd:dateTime && ?endDate < "''' + fecha_max + '''"^^xsd:dateTime)
	    '''
	
	if grat:
		q = q + '''?event smart:free "true"^^xsd:boolean.
			'''

	if buscaPorTipo:
		q = q + '''?event smart:isA ?category.
			?category smart:name "''' + tipo + '''".
			?category smart:name ?typeEvent.
			'''
	else:
		q = q + '''?event smart:isA ?category.
			?category smart:name ?typeEvent.
			'''
	
	q = q + '''}'''
	
	q = prepareQuery(q, initNs = { "smart": smart, "xsd": xsd})

	queryOut = g.query(q)
	queryOut = [(title, dateTimeToString(startDate), dateTimeToString(endDate),' '.join(re.findall('[A-Z][a-z]*',typeEvent)), location, price, URL) for title, startDate, endDate, typeEvent , location, price, URL in queryOut]
	return queryOut
