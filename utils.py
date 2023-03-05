from SPARQLWrapper import SPARQLWrapper, JSON

def sparql_query(arg):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """PREFIX dbr:  <http://dbpedia.org/resource/> \n
     SELECT ?predicate \n
     WHERE {\n?predicate a rdf:Property\n
     FILTER ( REGEX ( STR (?predicate), \"http://dbpedia.org/ontology/\", \"i\" ) )\n
     FILTER ( REGEX ( STR (?predicate), \"""" + arg + """\", \"i\" ) )\n}\n
     ORDER BY ?predicate
     """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]



def get_uri(name: str):
    resource_url = "http://dbpedia.org/resource/" # column value
    ontology_url = "http://dbpedia.org/ontology/" # column name
    return resource_url + name.replace(" ", "_")
