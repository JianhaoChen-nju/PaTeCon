from SPARQLWrapper import SPARQLWrapper,JSON
from time import *
wikidata_url = "http://114.212.81.217:8890/sparql/"
endpoint = SPARQLWrapper(wikidata_url)
endpoint.setReturnFormat(JSON)
prefixs = "PREFIX wd: <http://www.wikidata.org/entity/>\n"+"PREFIX wds: <http://www.wikidata.org/entity/statement/>\n"+\
         "PREFIX wdt: <http://www.wikidata.org/prop/direct/>\n"+"PREFIX p: <http://www.wikidata.org/prop/>\n "+ \
         "PREFIX ps: <http://www.wikidata.org/prop/statement/>\n"+"PREFIX pq: <http://www.wikidata.org/prop/qualifier/>\n" +\
         "PREFIX wikibase: <http://wikiba.se/ontology#>\n"

def parse_query_results(response, query):
    if 'ASK' in query or 'ask' in query:  # ask
        result = response['boolean']
    elif 'COUNT' in query or 'count' in query:  # count
        result = int(response['results']['bindings'][0]['callret-0']['value'])
    else:
        result = []
        for res in response['results']['bindings']:
            res = {k: v["value"] for k, v in res.items()}
            result.append(res)
    return result

def query_kg(query):
    global endpoint
    endpoint.setQuery(query)
    try:
        response = endpoint.query().convert()
    except Exception as err:
        print(err)
        endpoint = SPARQLWrapper(wikidata_url)
        return []
    result = parse_query_results(response, query)
    return result

def get_label(p):
    query = prefixs + "SELECT distinct ?label where{<"+p+"> rdfs:label ?label.filter(lang(?label)=\'en\')}"
    result = query_kg(query)
    try:
        return list(result[0].values())[0]
    except:
        print("NO LABEL:"+p)
        return p

def read_file(file_name):
    f=open(file_name,"r")
    lines=f.readlines()
    for line in lines:
        line=line.strip()
        l=line.split("\t")
        name=l[0]
        id=l[1]
        num=l[2]
        class_pairs_s=l[3]
        class_pairs_list=class_pairs_s.split("],")
        class_pairs=[]
        for item in class_pairs_list:
            a_pair=[]
            a_pair=item.replace("[","").replace("]","").replace(" ","").replace("'","").split(",")
            class_pairs.append(a_pair)
        print(class_pairs)
        time_predicate_s=l[4]
        time_predicate=time_predicate_s.replace("[","").replace("]","").replace(" ","").replace("'","").split(",")
        # print(time_predicate)
    # print(len(lines))

if __name__ == '__main__':
    read_file("class_pairs_res.txt")