from re import X
from rdflib import Graph, Namespace, Literal, XSD
from rdflib.plugins.sparql import prepareQuery
from SPARQLWrapper import SPARQLWrapper,JSON
from rdflib.term import URIRef
import utm
import math
import PySimpleGUI as sg

############################# BASED ON STREET #################################
def based_on_street(street):
    g = Graph()
    g.parse("pharmacies_full.ttl",format="ttl") #cambiar a GitHub
    wikidata = SPARQLWrapper("https://query.wikidata.org/sparql")
    ns = Namespace("http://pharmacies.odkg.es/group08/ontology/ppg8#")
    owl = Namespace("http://www.w3.org/2002/07/owl#")

    q = prepareQuery('''
        SELECT ?pharmacy ?streetname ?streetnum ?streetkm ?x ?y
        WHERE { 
        ?street ns:hasStreetName ?streetname.
        ?pharmacy ns:hasAddress ?address.
        ?address ns:hasStreet ?street.
        ?address ns:hasX ?x.
        ?address ns:hasY ?y.
        OPTIONAL{?address ns:hasStreetNumber ?streetnum}.
        OPTIONAL{?address ns:hasKM ?streetkm}
        }
        ''',
        initNs = { "ns": ns,"xsd":XSD}
    )
    out = []
    if (any(g.query(q,initBindings={'?streetname':Literal(street,datatype=XSD.string)}))):
        easting = 0.0
        northing = 0.0
        for r in g.query(q,initBindings={'?streetname':Literal(street,datatype=XSD.string)}):
            easting = easting + float(r.x)
            northing = northing + float(r.y)
        userX = easting/len(g.query(q,initBindings={'?streetname':Literal(street,datatype=XSD.string)})) 
        userY = northing/len(g.query(q,initBindings={'?streetname':Literal(street,datatype=XSD.string)}))
        
        out.append("Nearest pharmacies:\n\n")
        for r in g.query(q,initBindings={'?streetname':Literal(street,datatype=XSD.string)}):
            #print("\n",r.pharmacy,"\t",r.streetname)
            out.append(r.pharmacy)
            out.append("\n")
            out.append(r.streetname)
            if r.streetnum != None:
                #print(" ",r.streetnum)
                out.append("No")
                out.append(r.streetnum)
            elif r.streetkm != None:
                #print(" km. ",r.streetkm)
                out.append("km.")
                out.append(r.streetkm)
            out.append("\n----------------------\n")
        out = get_hospitals(out,userX,userY,street,wikidata,ns,owl,g)
    else:
        out.append("Nothing was found")
    return out








################################### BASED ON COORDINATES ###############
def based_on_coordinates(x,y):
    g = Graph()
    g.parse("pharmacies_full.ttl",format="ttl") #cambiar a GitHub
    wikidata = SPARQLWrapper("https://query.wikidata.org/sparql")
    ns = Namespace("http://pharmacies.odkg.es/group08/ontology/ppg8#")
    owl = Namespace("http://www.w3.org/2002/07/owl#")


    u = utm.from_latlon(x,y)
    userX = float(u[0])
    userY = float(u[1])
    dmin = 1000000
    q = prepareQuery('''
            SELECT DISTINCT ?x ?y ?streetname
            WHERE { 
            ?pharmacy ns:hasAddress ?address.
            ?address ns:hasX ?x.
            ?address ns:hasY ?y.
            ?address ns:hasStreet ?street.
            ?street ns:hasStreetName ?streetname
            }
            ''',
            initNs = { "ns": ns,"xsd":XSD}
    )
    for r in g.query(q):
        x = float(r.x)
        y = float(r.y)
        d = math.sqrt((userX-x)**2+(userY-y)**2)
        if d < dmin:
            dmin = d
            street = r.streetname
    
    q = prepareQuery('''
        SELECT ?pharmacy ?streetname ?streetnum ?streetkm
        WHERE { 
        ?street ns:hasStreetName ?streetname.
        ?pharmacy ns:hasAddress ?address.
        ?address ns:hasStreet ?street.
        OPTIONAL{?address ns:hasStreetNumber ?streetnum}.
        OPTIONAL{?address ns:hasKM ?streetkm}
        }
        ''',
        initNs = { "ns": ns,"xsd":XSD}
    )
    out = []
    if (any(g.query(q,initBindings={'?streetname':Literal(street,datatype=XSD.string)}))):   
        out.append("Nearest pharmacies:\n\n")
        for r in g.query(q,initBindings={'?streetname':Literal(street,datatype=XSD.string)}):
            #print("\n",r.pharmacy,"\t",r.streetname)
            out.append(r.pharmacy)
            out.append("\n")
            out.append(r.streetname)
            if r.streetnum != None:
                #print(" ",r.streetnum)
                out.append("No")
                out.append(r.streetnum)
            elif r.streetkm != None:
                #print(" km. ",r.streetkm)
                out.append("km.")
                out.append(r.streetkm)
            out.append("\n----------------------\n")
        out = get_hospitals(out,userX,userY,street,wikidata,ns,owl,g)
    else:
        out.append("Nothing was found")
    return out







################################### GET HOSPITALS ###############
def get_hospitals(out,userX,userY,street,wikidata,ns,owl,g):
    wikidata = SPARQLWrapper("https://query.wikidata.org/sparql")
    q = prepareQuery('''
        SELECT ?pharmacy ?municipality ?wikidata
        WHERE { 
            ?pharmacy ns:hasAddress ?address.
            ?address ns:hasStreet ?street.
            ?street ns:hasStreetName ?streetname.
            ?address ns:hasMunicipality ?municipality.
            ?municipality owl:sameAs ?wikidata
        }
        ''',
        initNs = { "ns": ns,"owl":owl}
        )
    for r in g.query(q,initBindings={'?streetname':Literal(street,datatype=XSD.string)}):
        municipality_wd = r.wikidata.split("/")[-1]

    wikidata.setQuery('''
        SELECT DISTINCT ?item ?itemLabel ?coordinates WHERE {
            ?item p:P131 ?statement0.
            ?statement0 (ps:P131) wd:'''+municipality_wd+'''.
            ?item p:P31 ?statement1.
            ?statement1 (ps:P31) wd:Q16917.
            ?item wdt:P625 ?coordinates
            SERVICE wikibase:label {
                 bd:serviceParam wikibase:language "en" .
            }
        }
        '''
    )

    wikidata.setReturnFormat(JSON)
    results = wikidata.query().convert()
    dmin = 1000000000000
    if any(results["results"]["bindings"]):
        #print("\nNearest hospital in current municipality: ")
        out.append("\n\nNearest hospital in current municipality:\n\n")
        for result in results["results"]["bindings"]:
            coords = result["coordinates"]["value"][6:-1].split(" ")
            hosp_y = float(coords[0])
            hosp_x = float(coords[1])
            u = utm.from_latlon(hosp_x,hosp_y)
            hosp_x = float(u[0])
            hosp_y = float(u[1])
            dist_hosp = math.sqrt((userX-hosp_x)**2+(userY-hosp_y)**2)/1000
            if dist_hosp < dmin:
                hosp = result
                dmin = dist_hosp
        #print(hosp["item"]['value'],hosp["itemLabel"]['value'],"\tDistance: ",round(dmin,2),"km")
        out.append(hosp["item"]['value'])
        out.append(hosp["itemLabel"]['value'])
        out.append(str(round(dmin,2)))
        out.append("km")
    else:
        #print("\nNo hospital in current municipality")
        out.append("No hospitals were found in current municipality")
    return out
            









############################# GUI #############################################
def gui():
    input_column = [
        [
            sg.Text("Street"),
            sg.In(size=(25,1),enable_events=True,key="-STREET-"),
            sg.Button("Search",key="-SEARCHONSTREET-")

        ],
        [
            sg.Text("USER X"),
            sg.In(size=(25,1),enable_events=True,key="-COORDX-"),
            sg.Text("USER Y"),
            sg.In(size=(25,1),enable_events=True,key="-COORDY-"),
            sg.Button("Search",key="-SEARCHONCOORDINATES-")
        ]
    ]
    output_column = [
        [
            sg.Text(enable_events=False,size=(80,60),key="-OUTPUT-")
        ]
    ]
    layout = [
        [
            sg.Column(input_column),
            sg.VSeparator(),
            sg.Column(output_column)
        ]
    ]

    window = sg.Window("Medical APP",layout)

    while True:
        event, values = window.read()
        if event == "-SEARCHONSTREET-":
            try:
                street = values["-STREET-"]
                out = based_on_street(street)
                if any(out):
                    output = ' '.join(out)
                    window["-OUTPUT-"].update(output)
                else:
                    window["-OUTPUT-"].update("Pharmacies not found")
            except:
                window["-OUTPUT-"].update("Something went wrong")
        elif event == "-SEARCHONCOORDINATES-":
            try:
                x = float(values["-COORDX-"])
                y = float(values["-COORDY-"])
                if not(x > 41.3 or x < 39.8 or y > -3 or y < -5):
                    out = based_on_coordinates(x,y)
                    if len(out) != 0:
                        output = ' '.join(out)
                        window["-OUTPUT-"].update(output)
                    else:
                        window["-OUTPUT-"].update("Pharmacies not found")
                else:
                    window["-OUTPUT-"].update("Coordinates are not valid")
            except:
                window["-OUTPUT-"].update("Something went wrong")
        if event == sg.WIN_CLOSED:
            break
    window.close()

    ################################# EXEC ###############
gui()