from SPARQLWrapper import SPARQLWrapper,JSON
from time import *
wikidata_url = "http://210.28.134.34:8890/sparql"
endpoint = SPARQLWrapper(wikidata_url)
endpoint.setReturnFormat(JSON)

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

def is_exist_example(p):
    results=[]
    query = "SELECT ?a WHERE { ?a ?p1 ?cvt.?cvt <"+p+"> ?c.?cvt ?p2 ?b." \
                             "filter regex (str(?b),\"http://rdf.freebase.com/ns/m\\\\.\")." \
                             "filter regex (str(?a),\"http://rdf.freebase.com/ns/m\\\\.\")}limit 1"
    endpoint.setQuery(query)
    response = endpoint.query().convert()
    results = parse_query_results(response, query)

    query = "SELECT ?a WHERE {?a <" + p + "> ?b.}limit 1"
    endpoint.setQuery(query)
    response = endpoint.query().convert()
    results += parse_query_results(response, query)
    if(len(results)>0):
        return True
    return False

def select_predicate(predicates):
    to_time_predicates = []
    for i in predicates:
        try:
            if(is_exist_example(i)):
                to_time_predicates.append(i)
            # else:
            #     print(i)

        except:
            print(i)
    with open("to_time_statement_predicates.txt", "w+",encoding="utf-8") as f:
        f.write("\n".join(to_time_predicates))
    print(len(to_time_predicates))


def get_label(p):
    query = "SELECT distinct ?label where{<" + p + "> rdfs:label ?label.filter(lang(?label)=\'en\')}"
    result = query_kg(query)
    try:
        return list(result[0].values())[0]
    except:
        print("NO LABEL:" + p)
        return p

def whether_cvt(p):
    query = "ASK where{<" + p + "> rdfs:label ?label.filter(lang(?label)=\'en\')}"
    result = query_kg(query)
    if result == True:
        return False
    else:
        return True

def find_time_predicate(p):
    query = "SELECT distinct  ?a ?p1  ?p2 ?b WHERE " \
            "{ ?a ?p1 ?cvt.?cvt <" + p + "> ?c.?cvt ?p2 ?b. ?cvt ?p2 ?a." \
                                         "?a <http://rdf.freebase.com/ns/type.object.type> ?ac.?b <http://rdf.freebase.com/ns/type.object.type> ?bc." \
                                         "filter regex (str(?b),\"http://rdf.freebase.com/ns/m\\\\.\")." \
                                         "filter regex (str(?a),\"http://rdf.freebase.com/ns/m\\\\.\")}limit 3"
    endpoint.setQuery(query)
    response = endpoint.query().convert()
    results = parse_query_results(response, query)
    return results

def get_class_pairs(p):
    pairs = []
    query = "SELECT ?ac ?bc WHERE " \
              "{ ?a ?p1 ?cvt.?cvt <"+p+"> ?c.?cvt ?p2 ?b." \
                "?a <http://rdf.freebase.com/ns/type.object.type> ?ac.?b <http://rdf.freebase.com/ns/type.object.type> ?bc."\
                 "filter regex (str(?b),\"http://rdf.freebase.com/ns/m\\\\.\")." \
                 "filter regex (str(?a),\"http://rdf.freebase.com/ns/m\\\\.\")}"

    query2 = "SELECT distinct ?ac ?bc WHERE " \
              "{ ?a ?p1 ?cvt.?cvt <"+p+"> ?c.?cvt ?p2 ?b." \
                "?a <http://rdf.freebase.com/ns/type.object.type> ?ac.?b <http://rdf.freebase.com/ns/type.object.type> ?bc."\
                 "filter regex (str(?b),\"http://rdf.freebase.com/ns/m\\\\.\")." \
                 "filter regex (str(?a),\"http://rdf.freebase.com/ns/m\\\\.\")}"
    results = query_kg(query)
    results2 = query_kg(query2)
    # print(len(results))
    if (len(results) > 0):
        # print(len(results))
        # print(len(results2))
        for i in results2:
            num = 0
            for j in results:
                if i == j:
                    num += 1
            # print(num)
            pairs.append([i['ac'].replace("http://rdf.freebase.com/ns/", ""),
                          i['bc'].replace("http://rdf.freebase.com/ns/", ""), num])
    return len(results), pairs

def get_pattern_from_qualifier(p):
    '''
    :param p:
    :return: specific pattern
    '''
    query1 = "SELECT distinct ?p1 Count(?p1)WHERE { ?a ?p1 ?cvt.?cvt <http://rdf.freebase.com/ns/people.marriage.from> ?c.?cvt ?p2 ?b. ?a <http://rdf.freebase.com/ns/type.object.type> ?ac.}ORDER BY DESC(Count(?p1)) limit 5"
    query2 = "SELECT distinct ?p2 Count(?p2)WHERE { ?a ?p1 ?cvt.?cvt <http://rdf.freebase.com/ns/people.marriage.from> ?c.?cvt ?p2 ?b. ?a <http://rdf.freebase.com/ns/type.object.type> ?ac.}ORDER BY DESC(Count(?p2)) limit 5"

    result1 = query_kg(query1)
    result2 = query_kg(query2)
    pattern=[]
    pattern.append(result1)
    pattern.append(result2)
    return pattern

if __name__ == "__main__":
    predicates = []
    # with open("pre_datatime.txt","r",encoding="utf-8") as f:
    #     for line in f.readlines():
    #         l = line.strip()
    #         predicates += l.split("\t")
    # select_predicate(predicates)
    # with open("to_time_statement_predicates.txt","r",encoding="utf-8") as f:
    with open("test.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            predicates.append(line.strip())
    predicate_dict = dict()
    for i in predicates:
        time_predicate=find_time_predicate(i)
        print(i,time_predicate)

    print(len(predicates))
    for i in predicates:
        print(get_pattern_from_qualifier(i))
    # write_file=open("")
    # write_file = open("class_pairs_res.txt","a+",encoding="utf-8")
    # p1 = []
    # p2 = []
    # p3 = []
    # p = []
    # begin_time = time()
    # for i in predicates:
    #     single_begin_time = time()
    #     if(not is_exist_example(i)):
    #         continue
    #     num, pairs = get_class_pairs(i)
    #     single_end_time = time()
    #
    #     print(i, num, single_end_time - single_begin_time)
    #
    #     if (len(pairs) > 0):
    #         pairs = sorted(pairs, key=lambda i: i[2], reverse=True)
    #         # print(pairs)
    #         predicate_dict[i.replace("http://rdf.freebase.com/ns/", "")] = pairs
    #         write_file.write(
    #             i.replace("http://rdf.freebase.com/ns/","") + "\t"  + str(num) + "\t" + str(
    #                 pairs) + "\t" + "\n")
    # end_time = time()
    # run_time = end_time - begin_time
    # print('该循环程序运行时间(s)：', run_time)

