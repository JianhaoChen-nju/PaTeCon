from SPARQLWrapper import SPARQLWrapper,JSON
wikidata_url = "http://114.212.81.217:8890/sparql/"
endpoint = SPARQLWrapper(wikidata_url)
endpoint.setReturnFormat(JSON)
prefixs = "PREFIX wd: <http://www.wikidata.org/entity/>\n"+"PREFIX wds: <http://www.wikidata.org/entity/statement/>\n"+\
         "PREFIX wdt: <http://www.wikidata.org/prop/direct/>\n"+"PREFIX p: <http://www.wikidata.org/prop/>\nPREFIX " \
                                                                "pq: <http://www.wikidata.org/prop/qualifier/>\n"
# p580 start time p582 end time p585 point in time


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

def get_full_predicates():
    query = prefixs + "select distinct(?p) where {?p wdt:P31 ?c.?c wdt:P279* wd:Q18616576 }"
    endpoint.setQuery(query)
    response = endpoint.query().convert()
    results = parse_query_results(response,query)
    predicates = []
    for i in results:
        predicates += i.values()
    return predicates
    # with open("full_predicates.txt","w+", encoding="utf-8") as f:
    #     f.write("\n".join(predicates))

def is_to_time_statement(p):
    pqs = ['P580','P582','P585']
    tem_predicates=[]
    for i in pqs:
        query = prefixs + "SELECT distinct count(?a) WHERE { ?a p:"+p.replace("http://www.wikidata.org/entity/","")+" ?c.?c pq:"+i+" ?d}limit 1"
        endpoint.setQuery(query)
        response = endpoint.query().convert()
        results = parse_query_results(response, query)
        if(results>0):
            tem_predicates.append(i)
    return tem_predicates

def select_predicate():
    predicates = get_full_predicates()
    to_time_predicates = []
    for i in predicates:
        if(is_to_time_statement(i)):
            to_time_predicates.append(i)
    with open("to_time_statement_predicates.txt", "w+",encoding="utf-8") as f:
        f.write("\n".join(to_time_predicates))
    print(len(to_time_predicates))

def get_label(p):
    query = prefixs + "SELECT distinct ?label where{<"+p+"> rdfs:label ?label.filter(lang(?label)=\'en\')}"
    result = query_kg(query)
    try:
        return list(result[0].values())[0]
    except:
        print("NO LABEL:"+p)
        return p

def get_class_pairs(p):
    pairs = []
    query = prefixs + "SELECT distinct count(?a) WHERE { ?a wdt:" + p.replace("http://www.wikidata.org/entity/",
                                                                        "") + " ?b.?a wdt:P31 ?ac.?b wdt:P31 ?bc.}"
    if(query_kg(query)>0):
        print(query_kg)
        query = prefixs + "SELECT distinct ?ac WHERE { ?a wdt:" + p.replace("http://www.wikidata.org/entity/",
                                                                                "") + " ?b.?a wdt:P31 ?ac.?b wdt:P31 ?bc.}"
        a_class = []
        results = query_kg(query)
        for i in results:
            a_class += i.values()
        query = prefixs + "SELECT distinct ?bc WHERE { ?a wdt:" + p.replace("http://www.wikidata.org/entity/",
                                                                            "") + " ?b.?b wdt:P31 ?bc.?a wdt:P31 ?ac.}"
        b_class = []
        results = query_kg(query)
        for i in results:
            b_class += i.values()
        for a in a_class:
            for b in b_class:
                query = prefixs + "SELECT distinct count(?a) WHERE {?a wdt:"+ p.replace("http://www.wikidata.org/entity/",
                                            "") + " ?b.?a wdt:P31 <"+a+">.?b wdt:P31 <"+b+">.}"
                num = query_kg(query)
                if(num>0):
                    pairs.append([get_label(a),get_label(b),num])
    return pairs

if __name__ == "__main__":
    predicates = []
    # with open("to_time_statement_predicates.txt","r",encoding="utf-8") as f:
    with open("test.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            predicates.append(line.strip())
    predicate_dict = dict()
    write_file = open("class_pairs_res.txt","a+",encoding="utf-8")
    p1 = []
    p2 = []
    p3 = []
    p = []
    for i in predicates:
        pqs = is_to_time_statement(i)
        # print(pqs)
        # if(len(pqs)==3):
        #     p3.append(i)
        # elif(len(pqs)==2 and 'P585' in pqs):
        #     p2.append(i)
        # elif(len(pqs)==1):
        #     p1.append(i)
        # else:
        #     p.append(i)
        pairs = get_class_pairs(i)
        print(pairs)
        if (len(pairs) > 0):
            pairs = sorted(pairs, key=lambda i: i[2], reverse=True)
            predicate_dict[i.replace("http://www.wikidata.org/entity/", "")] = pairs
            write_file.write(
                get_label(i) + "\t" + i.replace("http://www.wikidata.org/entity/", "") + "\t" + str(pairs) + "\t" + str(pqs) +"\n" )

    # print(p)


