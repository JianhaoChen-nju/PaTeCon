from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper import SPARQLWrapper
import id2label

endpoint = SPARQLWrapper("http://114.212.81.217:8890/sparql/")


def getPotentialEntities():
    query = '''
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        SELECT ?entity
        WHERE 
        {{
            ?entity wdt:P31/(wdt:P279){1,2} wd:Q26907166.
        }}
        '''
    # print(query)
    endpoint.setQuery(query)
    endpoint.setReturnFormat(JSON)
    response = endpoint.query().convert()
    results = response['results']['bindings']
    entityIdList = []
    for eachEntity in results:
        entityIdList.append(eachEntity['entity']['value'][31:])
    print(len(entityIdList))
    with open('p279andsqr_result.txt', 'w') as f:
        for eachEntityId in entityIdList:
            f.write(eachEntityId)
            f.write("\n")
        f.close()


def getHeadEntityCount(entityId):
    query = '''
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        SELECT DISTINCT ?e ?r
        WHERE
        {{
            wd:{} ?r ?e.
            ?e (wdt:P31|wdt:P279) ?ee
        }}'''.format(entityId)
    # print(query)
    endpoint.setQuery(query)
    endpoint.setReturnFormat(JSON)
    response = endpoint.query().convert()
    results = response['results']['bindings']
    return len(results)


def getTailEntityCount(entityId):
    query = '''
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        SELECT DISTINCT ?e ?r
        WHERE
        {{
            ?e ?r wd:{}.
            ?e (wdt:P31|wdt:P279) ?ee
        }}'''.format(entityId)
    # print(query)
    endpoint.setQuery(query)
    endpoint.setReturnFormat(JSON)
    response = endpoint.query().convert()
    results = response['results']['bindings']
    return len(results)


headSum = 0
tailSum = 0
cnt = 0
res_f = open('p279andsqr_result_stat_converted.txt', 'w')
dict_f = open('id_label_dict.txt', 'a+')
with open('p279andsqr_result.txt', 'r') as f:
    entityIdList = f.read().split("\n")
    for eachEntityId in entityIdList:
        cnt += 1
        if cnt % 100 == 0:
            print("Processing #%d..." % (cnt))
        headCnt = getHeadEntityCount(eachEntityId)
        tailCnt = getTailEntityCount(eachEntityId)
        res_f.write("%s:%s\tHeadEntityCount:%d\tTailEntityCount:%d\n" % (
            eachEntityId, id2label.trans_id_to_label(eachEntityId, dict_f), headCnt, tailCnt))
        headSum += headCnt
        tailSum += tailCnt
        # print("%s\thead:%d\ttail:%d" %(eachEntityId,headCnt,tailCnt))
    f.close()
# headSum:168268  tailSum:1058169
print("headSum:%d\ttailSum:%d" % (headSum, tailSum))
