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