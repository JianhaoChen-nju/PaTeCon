from SPARQLWrapper import SPARQLWrapper, JSON
from time import *
wikidata_url = "http://114.212.81.217:8890/sparql/"
endpoint = SPARQLWrapper(wikidata_url)
endpoint.setReturnFormat(JSON)
prefixs = "PREFIX wd: <http://www.wikidata.org/entity/>\n"+"PREFIX wds: <http://www.wikidata.org/entity/statement/>\n" +\
    "PREFIX wdt: <http://www.wikidata.org/prop/direct/>\n"+"PREFIX p: <http://www.wikidata.org/prop/>\n " + \
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
    query = prefixs + \
        "SELECT distinct ?label where{wd:"+p + \
        " rdfs:label ?label.filter(lang(?label)=\'en\')}"
    result = query_kg(query)
    try:
        return list(result[0].values())[0]
    except:
        # print("NO LABEL:"+p)
        return p


def trans_id_to_label(id, dict_file, dict_enabled=True):
    if dict_enabled:
        dict_file.seek(0, 0)
        line = dict_file.readline()
        while line:
            id_label_pair = line.strip().split("\t")
            dict_id = id_label_pair[0]
            dict_label = id_label_pair[1]
            if dict_id == id:
                return dict_label
            line = dict_file.readline()
    label_name = get_label(id)
    if dict_enabled:
        dict_file.seek(0, 2)
        dict_file.write("%s\t%s\n" % (id, label_name))
    return label_name


def read_file(raw_filename, res_filename, dict_filename, dict_enabled=True):
    raw_f = open(raw_filename, "r")
    res_f = open(res_filename, "w")
    dict_f = open(dict_filename, "a+")
    time_start = time()

    lines = raw_f.readlines()
    line_cnt = 0
    for line in lines:
        line_cnt += 1
        if line_cnt % 5 == 0:
            time_now = time()
            print("Processing #%d...\tPeriod time Cost:%f" %
                  (line_cnt, time_now-time_start))
            time_start = time_now
        line = line.strip()
        l = line.split("\t")
        name = l[0]
        id = l[1]
        num = l[2]
        class_pairs_s = l[3]
        class_pairs_list = class_pairs_s.split("],")
        class_pairs = []
        for item in class_pairs_list:
            a_pair = []
            a_pair = item.replace("[", "").replace("]", "").replace(
                " ", "").replace("'", "").split(",")
            a_pair_converted = [trans_id_to_label(a_pair[0], dict_f, dict_enabled), trans_id_to_label(
                a_pair[1], dict_f, dict_enabled), a_pair[2]]
            class_pairs.append(a_pair_converted)
        # print(class_pairs)
        time_predicate_s = l[4]
        time_predicate = time_predicate_s.replace("[", "").replace(
            "]", "").replace(" ", "").replace("'", "").split(",")
        time_predicate_converted = []
        for p in time_predicate:
            time_predicate_converted.append(
                trans_id_to_label(p, dict_f, dict_enabled))
        # print(time_predicate)
        res_f.write("%s\t%s\t%s\t%s\t%s\n" % (name, id, num, str(
            class_pairs), str(time_predicate_converted)))
        # break
    raw_f.close()
    res_f.close()
    dict_f.close()
    # print(len(lines))

def split_results():
    rawf=open("class_pairs_res_converted.txt","r")
    res_f1=open("class_pairs_res_0_100.txt","w")
    res_f2=open("class_pairs_res_100_1000.txt","w")
    res_f3=open("class_pairs_res_1000+.txt","w")

    line=rawf.readline()
    while line:
        nowsum=int(line.split("\t")[2])
        if nowsum<100:
            res_f1.write(line)
        elif nowsum<1000:
            res_f2.write(line)
        else:
            res_f3.write(line)
        line=rawf.readline()
    rawf.close()
    res_f1.close()
    res_f2.close()
    res_f3.close()

if __name__ == '__main__':
    read_file("class_pairs_res.txt",
              "class_pairs_res_converted.txt", "id_label_dict.txt")
    # split_results()
