from SPARQLWrapper import SPARQLWrapper,JSON
from time import *
wikidata_url = "http://114.212.81.217:8890/sparql/"
endpoint = SPARQLWrapper(wikidata_url)
endpoint.setReturnFormat(JSON)
prefixs = "PREFIX wd: <http://www.wikidata.org/entity/>\n"+"PREFIX wds: <http://www.wikidata.org/entity/statement/>\n"+\
         "PREFIX wdt: <http://www.wikidata.org/prop/direct/>\n"+"PREFIX p: <http://www.wikidata.org/prop/>\n "+ \
         "PREFIX ps: <http://www.wikidata.org/prop/statement/>\n"+"PREFIX pq: <http://www.wikidata.org/prop/qualifier/>\n" +\
         "PREFIX wikibase: <http://wikiba.se/ontology#>\n"
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
    id = p.replace("http://www.wikidata.org/entity/", "")
    ItemCheckQuery = "SELECT DISTINCT ?p WHERE { wd:"+id+" wikibase:propertyType ?p.}"
    # print(query_kg(ItemCheckQuery)[0]['p'])
    if query_kg(ItemCheckQuery)[0]['p']!="http://wikiba.se/ontology#WikibaseItem":
        return 0,pairs


    query = prefixs + "SELECT ?ac ?bc WHERE " \
                      "{ ?a p:" + id+ " ?statement." \
                        "?statement ps:" + id+ " ?b. " \
                        "?statement ?pq ?t FILTER regex (STR(?pq),\"prop/qualifier/P58\") FILTER (datatype(?t)=xsd:dateTime) ." \
                        "?a wdt:P31 ?ac. ?b wdt:P31 ?bc." \
                        "}"


    query2 = prefixs + "SELECT distinct ?ac ?bc WHERE " \
                  "{ ?a p:" + id + " ?statement." \
                    "?statement ps:" + id + " ?b. " \
                    "?statement ?pq ?t FILTER regex (STR(?pq),\"prop/qualifier/P58\") FILTER (datatype(?t)=xsd:dateTime) ." \
                    "?a wdt:P31 ?ac. ?b wdt:P31 ?bc." \
                    "}"
    results = query_kg(query)
    results2= query_kg(query2)
    # print(len(results))
    if (len(results) > 0):
        # print(len(results))
        # print(len(results2))
        for i in results2:
            num=0
            for j in results:
                if i==j:
                    num+=1
            # print(num)
            pairs.append([i['ac'].replace("http://www.wikidata.org/entity/",""),i['bc'].replace("http://www.wikidata.org/entity/",""),num])
    return len(results),pairs

if __name__ == "__main__":
    predicates = []
    with open("to_time_statement_predicates(1).txt","r",encoding="utf-8") as f:
    # with open("test.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            predicates.append(line.strip())
    predicate_dict = dict()
    write_file = open("class_pairs_res.txt","a+",encoding="utf-8")
    p1 = []
    p2 = []
    p3 = []
    p = []
    begin_time = time()
    for i in predicates:
        single_begin_time=time()
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
        num,pairs = get_class_pairs(i)
        single_end_time=time()

        print(i,num,single_end_time-single_begin_time)

        if (len(pairs) > 0):
            pairs = sorted(pairs, key=lambda i: i[2], reverse=True)
            # print(pairs)
            predicate_dict[i.replace("http://www.wikidata.org/entity/", "")] = pairs
            write_file.write(
                get_label(i) + "\t" + i.replace("http://www.wikidata.org/entity/", "") + "\t" + str(num) + "\t" + str(pairs) + "\t" + str(pqs) +"\n" )
    end_time = time()
    run_time = end_time - begin_time
    print('该循环程序运行时间(s)：', run_time)


