package handson;


import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;

import java.net.URLDecoder;
import java.util.ArrayList;

public class QueryHandler {

	Model model = ModelFactory.createDefaultModel();
	
	public QueryHandler() {
            
        }
	
	public ArrayList<String> getMunicipality() { 
		
		ArrayList<String> municipios = new ArrayList<String>();
		String centro;
		
		model.read("resources/output.ttl");
		
		String q1 = "PREFIX properties: <http://linkeddata.es/group15/ontology/studyCentersMadrid/properties#> \r\n"
				+ "  PREFIX classes: <http://linkeddata.es/group15/ontology/studyCentersMadrid/classes#> \r\n"
				+ "  PREFIX individuals: <http://linkeddata.es/group15/ontology/studyCentersMadrid/individuals/municipalities/>\r\n"
				+ "\r\n" + "  SELECT DISTINCT ?municipio \r\n" + "  WHERE { \r\n"
				+ "    ?municipio a classes:Municipality\r\n}";

		Query query1 = QueryFactory.create(q1);
		QueryExecution query1exec = QueryExecutionFactory.create(query1, model);
		ResultSet results = query1exec.execSelect();

		while (results.hasNext()) {
			QuerySolution soln = results.nextSolution();
			centro = soln.get("municipio").toString();
			municipios.add(decodedFun(centro));			
		}
		return municipios;
	}

	public ArrayList<String> execQuery(String lista[]) {

		ArrayList<String> centros = new ArrayList<String>();
		String centro;
		model.read("resources/output.ttl");

		String q1 = "PREFIX properties: <http://linkeddata.es/group15/ontology/studyCentersMadrid/properties#> \r\n"
				+ "  PREFIX classes: <http://linkeddata.es/group15/ontology/studyCentersMadrid/classes#> \r\n"
				+ "  PREFIX individuals: <http://linkeddata.es/group15/ontology/studyCentersMadrid/individuals/municipalities/>\r\n"
				+ "  PREFIX owl: <http://www.w3.org/2002/07/owl#> \r\n"
				+ "\r\n" + "  SELECT DISTINCT ?centrosNombre ?link \r\n" + "  WHERE { \r\n"
				+ "    ?centros properties:located individuals:" + lista[0] + " .\r\n"
				+ "	   ?centros properties:titularity " + lista[1] + " .\r\n"
				+ "    ?centros  properties:centerName ?centrosNombre .\r\n"
				+ "	   individuals:" + lista[0] + " owl:sameAs ?link\r\n}";
		
		String q2 = "PREFIX properties: <http://linkeddata.es/group15/ontology/studyCentersMadrid/properties#> \r\n"
				+ "  PREFIX classes: <http://linkeddata.es/group15/ontology/studyCentersMadrid/classes#> \r\n"
				+ "  PREFIX individuals: <http://linkeddata.es/group15/ontology/studyCentersMadrid/individuals/municipalities/>\r\n"
				+ "  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\r\n"
				+ "\r\n" + "  SELECT DISTINCT ?centrosNombre \r\n" + "  WHERE { \r\n"
				+ "    ?centros properties:located individuals:" + lista[0] + " .\r\n"
				//+ "    ?centros properties:titularity \"PRIVADO\"^^string .\r\n"
				+ "    ?centros  properties:centerName ?centrosNombre .\r\n"
				+ "    ?municipio  a classes:Municipality\r\n}";

		Query query1 = QueryFactory.create(q2);

		QueryExecution query1exec = QueryExecutionFactory.create(query1, model);

		ResultSet results = query1exec.execSelect();

		if (!results.hasNext())
			System.out.println("No se ha encontrado ningun centro");

		while (results.hasNext()) {
			QuerySolution soln = results.nextSolution();
			centro = soln.get("centrosNombre").toString();
			centros.add(decodedFun(centro));			
		}
		return centros;
	}
	
	private String decodedFun(String centro) {
		String result="Error";
		try {
			result = URLDecoder.decode(centro, "UTF-8");
			result = result.substring(result.lastIndexOf('/') + 1);
			System.out.println(result);			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return result;
	}
        
        public ArrayList<RecycleBin> query(String district, Integer capacity, String wasteType, String state){
            
            ArrayList<RecycleBin> bins = new ArrayList<>();
            model.read("resources/output.nt");
            int cont = 0;
            if(state.equals("FULL"))state = "LLENA";
            
            String q = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \r\n" + 
            "  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \r\n" +
            "  PREFIX vocab: <http://opendatagroup03.com/smartbins/ontology/ont#> \r\n" +
            "  PREFIX owl: <http://www.w3.org/2002/07/owl#> \r\n\r\n" + 
            "  SELECT DISTINCT ?nombreDistrito ?direccion ?tipoResiduo ?nivel ?state ?hora \r\n"; 
            
            String where = "  WHERE{ \r\n" +
            "  ?rb a vocab:RecycleBin.\r\n" +
            "  ?rb vocab:hasStatus ?state.\r\n" +
            "  ?rb vocab:hasCapacity ?nivel.\r\n" +
            "  ?rb vocab:residueType ?tipoResiduo.\r\n" +
            "  ?rb vocab:isLocatedIn ?loc .\r\n" +
            "  ?loc vocab:isInDistrict ?dis .\r\n" +
            "  ?loc vocab:hasAddress ?direccion .\r\n" +
            "  ?loc vocab:isInNeighborhood ?barrio .\r\n" +
            "  ?rb vocab:lastUpdate ?hora . \r\n" +
            "  ?dis vocab:hasName ?nombreDistrito . \r\n" +
            "  \r\n";
            
            
            String filter = "";
            
            //state
            if(!state.equals("Any")) {
                filter = filter.concat("FILTER( \r\n\t?state = "+"'"+state+"'");
                cont = 1;
            }
            //capacity
            if(capacity != -1 && cont == 0){
                filter = filter.concat("FILTER( \r\n\t?nivel = "+capacity.toString());
                cont = 1;
            }
            else if (capacity != -1 && cont != 0){
                filter = filter.concat("\r\n\t&& ?nivel = "+capacity.toString());
            }
            //waste type
            if(!(wasteType.equals("Any")) && cont == 0){
                filter = filter.concat("FILTER( \r\n\t?tipoResiduo = "+"'"+wasteType+"'");
                cont = 1;
            }
            else if (!(wasteType.equals("Any")) && cont != 0){
                filter = filter.concat("\r\n\t&& ?tipoResiduo = "+"'"+wasteType+"'");
            }
            //district
            if(!(district.equals("Any")) && cont == 0){
                filter = filter.concat("FILTER( \r\n\t?nombreDistrito = "+"'"+district+"'");
                cont = 1;
            }
            else if (!(district.equals("Any")) && cont != 0){
                filter = filter.concat("\r\n\t&& ?nombreDistrito = "+"'"+district+"'");
            }
            
            if(cont==1) filter = filter.concat("\r\n)");
            
            q = q.concat(where);
            q = q.concat(filter);
            q = q.concat("}");
            
            Query query = QueryFactory.create(q);
            QueryExecution qx = QueryExecutionFactory.create(query, model);
            ResultSet results = qx.execSelect();
            
            while (results.hasNext()) {
                QuerySolution r = results.next();
                
                
                String binCapacityString = r.get("nivel").toString();
                String [] parts = binCapacityString.split("\\^");
                String binCapacity = parts[0];
                String binDireccion = r.get("direccion").toString();
                String binDistrict = r.get("nombreDistrito").toString();
                String binWasteType = r.get("tipoResiduo").toString();
                if(binWasteType.equals("envases"))binWasteType = "Plastic";
                else binWasteType = "Organic";
                String binState = r.get("state").toString();
                if(binState.equals("LLENA"))binState="FULL";
                String binLastUpdateString = r.get("hora").toString();
                String [] parts2 = binLastUpdateString.split("\\^");
                String binLastUpdate = parts2[0];
                RecycleBin bin = new RecycleBin(binCapacity, binDireccion, binDistrict, binWasteType, binState, binLastUpdate);
                bins.add(bin);
            }
            
            return bins;
        }
}


