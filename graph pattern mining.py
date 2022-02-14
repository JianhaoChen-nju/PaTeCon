from SPARQLWrapper import SPARQLWrapper,JSON
from SPARQLWrapper import SPARQLWrapper
import os
import time

endpoint = SPARQLWrapper("http://114.212.81.217:8890/sparql/")

'''
human(Q5)
sports team (Q12973014)
human-geographic territorial entity (Q15642541)
human settlement (Q486972)
'''
def whether_some_class(entity,category):
    query = '''
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        ASK  {{
                {{wd:{} wdt:P31 wd:{}.}}
                UNION
                {{
                    wd:{} wdt:P31 ?type.
                    ?type (wdt:P279)+ wd:{}.
                }}
        }}'''.format(entity,category,entity,category)
    # print(query)
    endpoint.setQuery(query)
    endpoint.setReturnFormat(JSON)
    response = endpoint.query().convert()
    result = response['boolean']

    return result

if __name__ == '__main__':
    whether_some_class()