import read_datasets
import random
import time
from SPARQLWrapper import SPARQLWrapper,JSON

def supplementary_sample_dict():
    return dict

def sample_wiki_annotated_data():
    supplement = True
    if supplement==False:
        wiki_write_file = open("resource/WD27M_SAMPLED.tsv", "w", encoding="utf-8")
    else:
        wiki_write_file = open("resource/WD27M_SAMPLED_supplement.tsv", "w", encoding="utf-8")
    wikidata_prefix = "wd:"
    wd_predicate_file = open("resource/wikidata_predicates_list.tsv", "r", encoding="UTF-8")
    wd_predicate_list = {}
    wd_predicate_file.readline()
    wd_predicates = wd_predicate_file.readlines()
    '''compute sampling percentage'''
    wiki_facts_num = {}
    wiki_sampling = {}
    sample_numbers = 10000
    for item in wd_predicates:
        item = item.strip()
        elements = item.split("\t")
        # if elements[2]=="True":
        #     wd_predicate_list.append
        predicate = elements[0]
        facts = int(elements[3])
        isTemporal = elements[2]
        wd_predicate_list[predicate] = facts
        # 7471929
        wiki_temporal_facts = 7471929
        if isTemporal == "True":
            num = int(facts * 1.0 * sample_numbers / wiki_temporal_facts)
            if num == 0:
                num = 1
            wiki_sampling[predicate] = num
            wiki_facts_num[predicate] = facts
    for item in wiki_sampling.keys():
        print(item.replace("wd:","")+"\t"+str(wiki_sampling[item]))
    # print(wiki_sampling)
    print(sum(wiki_sampling.values()))

    '''supplement'''
    if supplement==True:
        dict = {}
        file = "resource/wiki_sup.txt"
        with open(file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            max_sup_number = 10000
            for line in lines:
                p = "wd:" + line.split("\t")[0]
                # print(p)

                # if wiki_facts_num[p]<max_sup_number:
                #     dict[p]=wiki_facts_num[p]
                # else:
                #     dict[p] = max_sup_number
                # print(wiki_facts_num[p])
                dict[p]=int(line.strip().split("\t")[1])
        wiki_sampling=dict

    # print(wiki_sampling)

    '''smapling'''
    wiki_sampling_index = {}
    for key in wiki_sampling:
        wiki_sampling_index[key] = random.sample(range(0, wiki_facts_num[key]), wiki_sampling[key])
    # print(wiki_sampling_index)

    WIKIDATA = "resource/WD27M.tsv"
    utkg_wiki = read_datasets.read_file(WIKIDATA)
    # print(utkg_wiki[0])
    # ['Q27067701', 'P735', 'Q3133296', 'null', 'null']
    wiki_sampling_pointer = {}
    for key in wiki_sampling:
        wiki_sampling_pointer[key]=-1
    wiki_sampled_dataset = []
    for quad in utkg_wiki:
        predicate=wikidata_prefix+quad[1]
        if predicate in wiki_sampling:
            wiki_sampling_pointer[predicate]+=1
            if wiki_sampling_pointer[predicate] in wiki_sampling_index[predicate]:
                wiki_sampled_dataset.append(quad)
    # print(sum(wd_predicate_list.values()))

    for quad in wiki_sampled_dataset:
        line = quad[0] + "\t" + quad[1] + "\t" + quad[2] + "\t" + quad[3] + "\t" + quad[4] + "\n"
        wiki_write_file.write(line)

def sample_free_annotated_data():
    freebase_prefix = "fb:"
    free_facts_num = {}
    fb_predicate_file = open("resource/freebase_predicates_list.tsv", "r", encoding="UTF-8")
    fb_predicate_list = {}
    free_sampling = {}
    fb_predicate_file.readline()
    fb_predicates = fb_predicate_file.readlines()
    sample_numbers = 128
    for item in fb_predicates:
        item = item.strip()
        elements = item.split("\t")
        # if elements[2]=="True":
        #     wd_predicate_list.append
        predicate = elements[0]
        facts = int(elements[3])
        isTemporal = elements[2]
        fb_predicate_list[predicate] = facts
        # 2989799
        free_temporal_facts = 2989799
        if isTemporal == "True":
            num = int(facts * 1.0 * sample_numbers / free_temporal_facts)
            num += 1
            free_sampling[predicate] = num
            free_facts_num[predicate] = facts
    print(free_sampling)
    print(sum(free_sampling.values()))

    # List=random.sample(range(0,10),10)
    # print(List)

    free_sampling_index = {}
    for key in free_sampling:
        free_sampling_index[key] = random.sample(range(0, free_facts_num[key]), free_sampling[key])
    # print(free_sampling_index)
    FREEBASE = "resource/FB37M.tsv"
    free_sampling_pointer = {}
    '''initiate pointer'''

    for key in free_sampling:
        free_sampling_pointer[key] = -1
    free_sampled_dataset = []

    utkg_free = read_datasets.read_file(FREEBASE)
    for quad in utkg_free:
        predicate = freebase_prefix + quad[1]
        if predicate in free_sampling:
            free_sampling_pointer[predicate] += 1
            if free_sampling_pointer[predicate] in free_sampling_index[predicate]:
                free_sampled_dataset.append(quad)
        # else:
        #     print(predicate)
    # print(sum(fb_predicate_list.values()))

    free_write_file = open("resource/FB37M_SAMPLED.tsv", "w", encoding="utf-8")
    for quad in free_sampled_dataset:
        line = quad[0] + "\t" + quad[1] + "\t" + quad[2] + "\t" + quad[3] + "\t" + quad[4] + "\n"
        free_write_file.write(line)

def sample_annotated_data():
    sample_wiki_annotated_data()
    # sample_free_annotated_data()
    # wikidata_prefix = "wd:"
    # wd_predicate_file = open("resource/wikidata_predicates_list.tsv", "r", encoding="UTF-8")
    # wd_predicate_list = {}
    # wd_predicate_file.readline()
    # wd_predicates = wd_predicate_file.readlines()
    # filename="resource/.tsv"
    # utkg=read_file(filename)
    # print(wd_predicates)
    '''initiate dictionary'''
    # for item in wd_predicates:
    #     item=item.strip()
    #     elements=item.split("\t")
    #     # if elements[2]=="True":
    #     #     wd_predicate_list.append
    #     predicate=elements[0]
    #     wd_predicate_list[predicate]=0
    # fb_predicate_file.readline()
    # fb_predicates=fb_predicate_file.readlines()
    # for item in fb_predicates:
    #     item=item.strip()
    #     elements=item.split("\t")
    #     # if elements[2]=="True":
    #     #     wd_predicate_list.append
    #     predicate=elements[0]
    #     fb_predicate_list[predicate]=0

    # print(wd_predicate_list)
    # print(fb_predicate_list)

    # print(len(wd_predicate_list))
    # print(len(fb_predicate_list))

    '''count facts'''
    # WIKIDATA = "resource/WD27M.tsv"
    # FREEBASE = "resource/FB37M.tsv"
    #
    # utkg_wiki=read_file(WIKIDATA)
    # # print(utkg_wiki[0])
    # # ['Q27067701', 'P735', 'Q3133296', 'null', 'null']
    # for quad in utkg_wiki:
    #     predicate=wikidata_prefix+quad[1]
    #     wd_predicate_list[predicate]+=1
    # # print(sum(wd_predicate_list.values()))
    #
    # utkg_free=read_file(FREEBASE)
    # for quad in utkg_free:
    #     predicate=freebase_prefix+quad[1]
    #     if predicate in fb_predicate_list:
    #         fb_predicate_list[predicate]+=1
    #     else:
    #         print(predicate)
    # print(sum(fb_predicate_list.values()))
    # KeyError: 'http://www.w3.org/2000/01/rdf-schema#range'
    # KeyError: 'http://www.w3.org/2000/01/rdf-schema#domain'

    # wd_predicate_file.close()
    # fb_predicate_file.close()

    '''rewrite file'''
    # write_wiki_predicates=open("resource/wikidata_predicates_list.tsv","w",encoding="UTF-8")
    # write_free_predicates=open("resource/freebase_predicates_list.tsv","w",encoding="UTF-8")
    # write_wiki_predicates.write("predicate"+"\t"+"label"+"\t"+"?temporal_predicate"+"\t"+"facts"+"\n")
    # write_free_predicates.write("predicate" + "\t" + "label" + "\t" + "?temporal_predicate" + "\t" + "facts" + "\n")
    # for item in wd_predicates:
    #     item=item.strip()
    #     elements=item.split("\t")
    #     # if elements[2]=="True":
    #     #     wd_predicate_list.append
    #     predicate=elements[0]
    #     item=item+"\t"+str(wd_predicate_list[predicate])+"\n"
    #     write_wiki_predicates.write(item)
    #
    # for item in fb_predicates:
    #     item=item.strip()
    #     elements=item.split("\t")
    #     # if elements[2]=="True":
    #     #     wd_predicate_list.append
    #     predicate=elements[0]
    #     item=item+"\t"+str(fb_predicate_list[predicate])+"\n"
    #     write_free_predicates.write(item)

def query_wikidata():
    '''
    human(Q5)
    sports team (Q12973014)
    human-geographic territorial entity (Q15642541)
    human settlement (Q486972)
    '''


    # Set up the SPARQL endpoint URL
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    # Define the Wikidata query to retrieve information about Albert Einstein
    query = """
    SELECT ?property ?value WHERE {
      wd:Q937 ?property ?value .
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    }
    """.format()

    # Set the query and return format
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and parse the results
    results = sparql.query().convert()

    # Print the results
    for result in results["results"]["bindings"]:
        print(result["property"]["value"], result["value"]["value"])

def reformat_time(t):
    #YYYYY/MM/DD
    #"2013-01-31T00:00:00Z"^^xsd:dateTime
    #"-0220-01-01T00:00:00Z"^^xsd:dateTime
    DD=t.__getitem__(len(t)-2)+t.__getitem__(len(t)-1)
    MM=t.__getitem__(len(t)-4)+t.__getitem__(len(t)-3)
    YY=t[0:len(t)-4]
    DATE=YY+"-"+MM+"-"+DD
    # print(DATE)
    dateTime="\""+DATE+"T00:00:00Z\"^^xsd:dateTime"
    # print(dateTime)
    return dateTime

def select_mutiple_wiki():
    # incomplete
    wiki_file="resource/wiki_annotated_file.tsv"
    mutiple_values=[]
    with open(wiki_file,"r",encoding="utf-8") as file:
        lines= file.readlines()
        for line in lines:
            ele = line.split("\t")
            label =ele[0]
            if label=="-1":
                mutiple_values.append(ele)

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    for fact in mutiple_values:
        s = fact[1]
        p = fact[2]
        o = fact[3]
        start = fact[4]
        # end = fact[4]
        year=o.split("-")[0]

def truth_verification_wiki():
    supplement=False
    if supplement==False:
        wiki_to_verify = "resource/WD27M_SAMPLED.tsv"
        wiki_annotated_file = open("resource/wiki_annotated_file.tsv", "a", encoding="utf-8")
    else:
        wiki_to_verify = "resource/WD27M_SAMPLED_supplement.tsv"
        wiki_annotated_file = open("resource/wiki_supplement_annotated_file.tsv", "a", encoding="utf-8")
    # p580 start time
    # p582 end time
    # p585 point in time

    wiki_file = open(wiki_to_verify, "r", encoding="utf-8")
    delay_time = 1

    temporal_binding = open("resource/wikidata_temporal_property_type.tsv", "r", encoding="utf-8")
    temporal_binding.readline()
    temporal_types = temporal_binding.readlines()
    temporal_binding_dict = {}
    for item in temporal_types:
        item = item.strip()
        item_s = item.split("\t")
        predicate = item_s[0]
        temporal_type = item_s[1]
        temporal_binding_dict[predicate] = temporal_type
        # period point
    temporal_binding_dict["P569"] = "point"
    temporal_binding_dict["P570"] = "point"

    wiki_lines = wiki_file.readlines()

    # # TEST 1
    # s = "Q10520"
    # p = "P54"
    # o = "Q483020"
    # # o maybe str
    # start=""2013-01-31T00:00:00Z"^^xsd:dateTime"
    # end=""2013-05-17T00:00:00Z"^^xsd:dateTime"

    # wiki_annotated_file.write("label\ts\tp\to\tst\ted\n")
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    # if old version consistent to the current one
    count = 0
    for line in wiki_lines:
        # count+=1
        # if count==2:
        #     break
        line = line.strip()
        fact = line.split("\t")
        s = fact[0]
        p = fact[1]
        o = fact[2]
        start = fact[3]
        end = fact[4]
        temporal_type = temporal_binding_dict[p]
        # switch case
        if p.__eq__("P569") or p.__eq__("P570"):
            start_time = reformat_time(start)
            query = """SELECT ?s WHERE {{wd:{} wdt:{} ?s.}}""".format(s, p)
        elif o[0] != "Q":
            if start.__eq__("null") and end.__eq__("null"):
                continue
            elif start.__eq__("null"):
                end_time = reformat_time(end)
                query = """
                        SELECT ?s
                        WHERE {{
                            wd:{} p:{} ?s.
                            ?s pq:P582 {}.
                        }}
                        """.format(s, p, end_time)
            elif end.__eq__("null"):
                start_time = reformat_time(start)
                query = """
                                    SELECT ?s
                                    WHERE {{
                                        wd:{} p:{} ?s.
                                        ?s pq:P580 {}.
                                    }}
                                    """.format(s, p, start_time)
            else:
                start_time = reformat_time(start)
                end_time = reformat_time(end)
                if temporal_type == "period":
                    query = """
                                                    SELECT ?s
                                                    WHERE {{
                                                        wd:{} p:{} ?s.
                                                        ?s pq:P580 {}.
                                                        ?s pq:P582 {}.
                                                    }}
                                                    """.format(s, p, start_time, end_time)
                else:
                    # temporal type = point
                    query = """
                                                                    SELECT ?s
                                                                    WHERE {{
                                                                        wd:{} p:{} ?s.
                                                                        ?s pq:P585 {}.
                                                                    }}
                                                                    """.format(s, p, start_time)
        else:
            if start.__eq__("null") and end.__eq__("null"):
                continue
            elif start.__eq__("null"):
                end_time = reformat_time(end)
                query = """
                        SELECT ?s
                        WHERE {{
                            wd:{} p:{} ?s.
                            ?s ps:{} wd:{}.
                            ?s pq:P582 {}.
                        }}
                        """.format(s, p, p, o, end_time)
            elif end.__eq__("null"):
                start_time = reformat_time(start)
                query = """
                                    SELECT ?s
                                    WHERE {{
                                        wd:{} p:{} ?s.
                                        ?s ps:{} wd:{}.
                                        ?s pq:P580 {}.
                                    }}
                                    """.format(s, p, p, o, start_time)
            else:
                start_time = reformat_time(start)
                end_time = reformat_time(end)
                if temporal_type == "period":
                    query = """
                                                    SELECT ?s
                                                    WHERE {{
                                                        wd:{} p:{} ?s.
                                                        ?s ps:{} wd:{}.
                                                        ?s pq:P580 {}.
                                                        ?s pq:P582 {}.
                                                    }}
                                                    """.format(s, p, p, o, start_time, end_time)
                else:
                    # temporal type = point
                    query = """
                                                                    SELECT ?s
                                                                    WHERE {{
                                                                        wd:{} p:{} ?s.
                                                                        ?s ps:{} wd:{}.
                                                                        ?s pq:P585 {}.
                                                                    }}
                                                                    """.format(s, p, p, o, start_time)

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        # 执行查询并检查结果是否存在
        try:
            results = sparql.query().convert()
        except Exception as e:
            print(e)
            print("retrying......")
            time.sleep(60)
            results = sparql.query().convert()
        if len(results["results"]["bindings"]) > 0:
            if p.__eq__("P569") or p.__eq__("P570"):
                start_time = reformat_time(start)
                DATE = start_time.split("\"")[1]
                exist = 0
                for result in results["results"]["bindings"]:
                    # print(result["s"]["value"])
                    # print(start_time)
                    if result["s"]["value"] == DATE:
                        exist = 1
                if exist == 1:
                    if len(results["results"]["bindings"]) > 1:
                        line = "-1\t" + line + "\n"
                    else:
                        line = "1\t" + line + "\n"
                else:
                    line = "0\t" + line + "\n"
            else:
                line = "1\t" + line + "\n"
            # return True
        else:
            line = "0\t" + line + "\n"
            # return False
        wiki_annotated_file.write(line)
        time.sleep(delay_time)

def truth_verification_free():
    # freebase
    # date_of_birth P569
    # date_of_death P570
    # teams P54
    # spouse_s  P26
    # employment_history    P108
    # coaches   P286
    # free_to_verify = "resource/selected_fb_facts.tsv"
    free_to_verify= "resource/FB37M_SAMPLED.tsv"
    # free_to_verify = "resource/temp.txt"
    free_file=open(free_to_verify,"r",encoding="utf-8")
    free_lines = free_file.readlines()
    delay_time = 1
    relation_map={}
    relation_map["people.deceased_person.date_of_death"]="P570"
    relation_map["people.person.date_of_birth"]="P569"
    relation_map["sports.pro_athlete.teams"] = "P54"
    relation_map["people.person.spouse_s"] = "P26"
    relation_map["people.person.employment_history"] = "P108"
    relation_map["sports.sports_team.coaches"] = "P286"

    temporal_binding_dict = {}
    temporal_binding_dict["P569"] = "point"
    temporal_binding_dict["P570"] = "point"
    temporal_binding_dict["P54"] = "period"
    temporal_binding_dict["P26"] = "period"
    temporal_binding_dict["P108"] = "period"
    temporal_binding_dict["P286"] = "period"

    # # TEST 1
    # s = "Q10520"
    # p = "P54"
    # o = "Q483020"
    # # o maybe str
    # start=""2013-01-31T00:00:00Z"^^xsd:dateTime"
    # end=""2013-05-17T00:00:00Z"^^xsd:dateTime"
    id_maps={}
    with open("resource/FBids_to_WDids.tsv","r",encoding="utf-8") as id_maps_file:
        lines=id_maps_file.readlines()
        for pair in lines:
            pair=pair.strip()
            fbid=pair.split("\t")[0]
            wdid=pair.split("\t")[1]
            id_maps[fbid]=wdid


    free_annotated_file = open("resource/temp_free_annotated_file.tsv", "a", encoding="utf-8")
    # free_annotated_file.write("label\ts\tp\to\tst\ted\n")
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    # if old version consistent to the current one
    count = 0
    for line in free_lines:
        # count+=1
        # if count==10:
        #     break
        line = line.strip()
        fact = line.split("\t")

        if fact[0] in id_maps:
            s=id_maps[fact[0]]
        else:
            continue
        #relation map
        p = relation_map[fact[1]]
        if p!="P569" and p!="P570":
            if fact[2] in id_maps:
                o=id_maps[fact[2]]
            else:
                continue
        start = fact[3]
        end = fact[4]
        temporal_type = temporal_binding_dict[p]
        # switch case
        if p.__eq__("P569") or p.__eq__("P570"):
            start_time = reformat_time(start)
            query = """SELECT ?s WHERE {{wd:{} wdt:{} ?s.}}""".format(s, p)
        else:
            if start.__eq__("null") and end.__eq__("null"):
                continue
            elif start.__eq__("null"):
                end_time = reformat_time(end)
                query = """
                            SELECT ?s
                            WHERE {{
                                wd:{} p:{} ?s.
                                ?s ps:{} wd:{}.
                                ?s pq:P582 {}.
                            }}
                            """.format(s, p, p, o, end_time)
            elif end.__eq__("null"):
                start_time = reformat_time(start)
                query = """
                                        SELECT ?s
                                        WHERE {{
                                            wd:{} p:{} ?s.
                                            ?s ps:{} wd:{}.
                                            ?s pq:P580 {}.
                                        }}
                                        """.format(s, p, p, o, start_time)
            else:
                start_time = reformat_time(start)
                end_time = reformat_time(end)
                if temporal_type == "period":
                    query = """
                                                        SELECT ?s
                                                        WHERE {{
                                                            wd:{} p:{} ?s.
                                                            ?s ps:{} wd:{}.
                                                            ?s pq:P580 {}.
                                                            ?s pq:P582 {}.
                                                        }}
                                                        """.format(s, p, p, o, start_time, end_time)
                else:
                    # temporal type = point
                    query = """
                                                                        SELECT ?s
                                                                        WHERE {{
                                                                            wd:{} p:{} ?s.
                                                                            ?s ps:{} wd:{}.
                                                                            ?s pq:P585 {}.
                                                                        }}
                                                                        """.format(s, p, p, o, start_time)


        sparql.setQuery(query)

        sparql.setReturnFormat(JSON)
        # 执行查询并检查结果是否存在
        try:
            results = sparql.query().convert()

        except Exception as e:
            print(e)
            print("retrying......")
            time.sleep(60)
            results = sparql.query().convert()

        if len(results["results"]["bindings"]) > 0:
            if p.__eq__("P569") or p.__eq__("P570"):
                start_time = reformat_time(start)
                DATE = start_time.split("\"")[1]
                exist = 0
                for result in results["results"]["bindings"]:
                    # print(result["s"]["value"])
                    # print(start_time)
                    if result["s"]["value"] == DATE:
                        exist = 1
                if exist == 1:
                    if len(results["results"]["bindings"]) > 1:
                        line = "-1\t" + line + "\n"
                    else:
                        line = "1\t" + line + "\n"
                else:
                    line = "0\t" + line + "\n"
            else:
                line = "1\t" + line + "\n"
            # return True
        else:
            line = "0\t" + line + "\n"
            # return False
        free_annotated_file.write(line)
        time.sleep(delay_time)

def truth_verification():
    truth_verification_wiki()
    # truth_verification_free()

def deduplicate_annotated_files():
    filename="resource/wiki_annotated_file.tsv"
    filename="resource/wiki_right.txt"
    with open(filename, "r", encoding="utf-8") as file:
        # file.readline()
        unique_lines = set(file.readlines())

    # Write the unique lines to a new file
    new_filename="resource/unique_wiki_a.tsv"
    with open(new_filename, "w",encoding="utf-8") as unique_file:
        # unique_file.write("label\ts\tp\to\tst\ted\n")
        unique_file.writelines(unique_lines)


def fbid_to_wdid():
    # Replace with the Freebase ID you want to query
    fb_ids=open("resource/entities_to_map.tsv","r",encoding="utf-8")
    lines = fb_ids.readlines()
    sparql = SPARQLWrapper("http://114.212.81.217:8890/sparql/")

    # id_map={}
    map_files=open("resource/FBids_to_WDids.tsv","a",encoding="utf-8")

    count=0
    for freebase_id in lines:
        # count+=1
        # if count==20:
        #     break
        freebase_id=freebase_id.strip()
        new_freebase_id="/"+freebase_id.replace(".","/")
        # print(freebase_id)
        # Construct the SPARQL query
        query = """
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        SELECT ?item WHERE {{
          ?item wdt:P646 "{}".
        }}
        """.format(new_freebase_id)

        # Send the SPARQL query to the Wikidata API

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        response = sparql.query().convert()

        # Parse the response and extract the entity information
        if len(response["results"]["bindings"])>0:
            item_id = response["results"]["bindings"][0]["item"]["value"]
            # print(item_id)
            map_files.write(freebase_id+"\t"+item_id.replace("http://www.wikidata.org/entity/","")+"\n")
    map_files.close()

def entity_in_temporal_fact():
    utkg=read_datasets.read_file("resource/FB37M.tsv")
    temporal_entity=set()

    for fact in utkg:
        if fact[3]!="null" or fact[4]!="null":
            if fact.__contains__("m."):
                temporal_entity.add(fact[0])
            if fact[2].__contains__("m."):
                temporal_entity.add(fact[2])

    has_mapped_entitiy=set()
    with open("resource/FBids_to_WDids.tsv","r",encoding="utf-8") as file:
        lines=file.readlines()
        for line in lines:
            line=line.strip()
            id=line.split("\t")[0]
            has_mapped_entitiy.add(id)

    difference=temporal_entity-has_mapped_entitiy
    with open("resource/entities_to_map.tsv","w",encoding="utf-8") as file1:
        for i in difference:
            file1.write(i+"\n")

def auto_evaluate_wiki():
    # wiki_dict={}
    std_confidence=False
    if std_confidence==True:
        conflict_file = "Std_results/Conflicts in WD27M.txt"
    else:
        conflict_file = "output/WD27M.all_conflicts"
    wiki_annotated_set = set()
    wiki_wrong="resource/WD27M_wrong_facts.tsv"
    with open(wiki_wrong, "r", encoding="utf-8") as wikitest:
        wikitest.readline()
        test_lines = wikitest.readlines()
        for line in test_lines:
            line = line.strip()
            # print(line)
            ele = line.split("\t")
            fact = ele[1] + "," + ele[2] + "," + ele[3] + "," + ele[4] + "," + ele[5]
            if ele[0] == "-1" or ele[0] == "0":
                # wiki_dict[fact]=ele[0]
                wiki_annotated_set.add(fact)
    # print(wiki_annotated_set)

    detected_set = set()
    temporal_represenation_file="output/WD27M.temporal_representation_conflicts"
    with open(temporal_represenation_file,"r",encoding="utf-8") as tr:
        conflict_lines=tr.readlines()
        for line in conflict_lines:
            line=line.strip()
            detected_set.add(line)

    with open(conflict_file, "r", encoding="utf-8") as wdconflict:
        conflict_lines = wdconflict.readlines()
        for line in conflict_lines:
            line = line.strip()
            ele = line.split("\t")
            fact1 = ele[1]
            fact2 = ele[2]
            fact_ele = fact1.split(",")
            if len(fact_ele) == 7:
                # if len(fact_ele[3].split("*"))!=1:
                fact_ele[3]=fact_ele[3].split("*")[0]
                fact1 = fact_ele[2] + "," + fact_ele[3] + "," + fact_ele[4] + "," + fact_ele[5] + "," + fact_ele[6]
            else:
                fact_ele[1] = fact_ele[1].split("*")[0]
                fact1 = fact_ele[0] + "," + fact_ele[1] + "," + fact_ele[2] + "," + fact_ele[3] + "," + fact_ele[4]
            fact_ele = fact2.split(",")
            if len(fact_ele) == 7:
                # if len(fact_ele[3].split("*"))!=1:
                fact_ele[3] = fact_ele[3].split("*")[0]
                fact2 = fact_ele[2] + "," + fact_ele[3] + "," + fact_ele[4] + "," + fact_ele[5] + "," + fact_ele[6]
            else:
                fact_ele[1] = fact_ele[1].split("*")[0]
                fact2 = fact_ele[0] + "," + fact_ele[1] + "," + fact_ele[2] + "," + fact_ele[3] + "," + fact_ele[4]

            detected_set.add(fact1)
            detected_set.add(fact2)

    # print(detected_set)
    # for item in detected_set:
    #     if item.__contains__("*"):
    #         print("yes")
    covered_set = detected_set.intersection(wiki_annotated_set)
    recall = len(covered_set) * 1.0 / len(wiki_annotated_set)
    print(len(wiki_annotated_set))
    print(recall)

def auto_evaluate_wiki_aaai17():
    # wiki_dict={}
    wiki_annotated_set = set()
    wiki_wrong = "resource/WD27M_wrong_facts.tsv"
    with open(wiki_wrong, "r", encoding="utf-8") as wikitest:
        wikitest.readline()
        test_lines = wikitest.readlines()
        for line in test_lines:
            line = line.strip()
            # print(line)
            ele = line.split("\t")
            if ele[4]=="-1":
                ele[4]=ele[5]
            if ele[5]=="-1":
                ele[5]=ele[4]
            ele[4] = ele[4][0:4]
            ele[5] = ele[5][0:4]
            fact = ele[1] + "," + ele[2] + "," + ele[3] + "," + ele[4] + "," + ele[5]
            if ele[0] == "-1" or ele[0] == "0":
                # wiki_dict[fact]=ele[0]
                wiki_annotated_set.add(fact)
    # print(wiki_annotated_set)
    conflict_file = "tecore/WDconflict_web.cons"
    detected_set=set()
    with open(conflict_file, "r", encoding="utf-8") as wdconflict:
        conflict_lines = wdconflict.readlines()
        for line in conflict_lines:
            line = line.strip()
            ele = line.split("\t")
            fact = ele[0] + "," + ele[1] + "," + ele[2] + "," + ele[3] + "," + ele[4]
            detected_set.add(fact)

    covered_set = detected_set.intersection(wiki_annotated_set)
    # for item in covered_set:
    #     print(item)
    # print(covered_set)
    recall = len(covered_set) * 1.0 / len(wiki_annotated_set)
    print(len(wiki_annotated_set))
    print(recall)

def auto_evaluate_free():
    # free_dict={}
    free_annotated_set = set()
    detected_set = set()
    wrong_file="resource/FB37M_wrong_facts.tsv"
    with open(wrong_file, "r", encoding="utf-8") as freetest:
        freetest.readline()
        test_lines = freetest.readlines()
        for line in test_lines:
            line = line.strip()
            ele = line.split("\t")
            # if ele[3][0:2]!="m.":
            #     # print(ele[3])
            #     ele[3]="T"
            fact = ele[1] + "," + ele[2] + "," + ele[3] + "," + ele[4] + "," + ele[5]
            # free_dict[fact]=ele[0]
            if ele[0] == "-1" or ele[0] == "0":
                # wiki_dict[fact]=ele[0]
                free_annotated_set.add(fact)
    # print(free_annotated_set)

    detected_set = set()
    temporal_represenation_file="output/FB37M.temporal_representation_conflicts"
    with open(temporal_represenation_file,"r",encoding="utf-8") as tr:
        conflict_lines=tr.readlines()
        for line in conflict_lines:
            line=line.strip()
            detected_set.add(line)

    conflict_file="output/FB37M.all_conflicts"
    # conflict_file = "Std_results/Conflicts in FB37M.txt"
    with open(conflict_file, "r", encoding="utf-8") as fbconflict:
        conflict_lines = fbconflict.readlines()
        for line in conflict_lines:
            line = line.strip()
            ele = line.split("\t")
            fact1 = ele[1]
            fact2 = ele[2]
            fact_ele = fact1.split(",")

            if len(fact_ele) == 7:
                fact1 = fact_ele[2] + "," + fact_ele[3] + "," + fact_ele[4] + "," + fact_ele[5] + "," + fact_ele[6]
            else:
                fact1=fact_ele[0] + "," + fact_ele[1] + "," + fact_ele[2] + "," + fact_ele[3] + "," + fact_ele[4]
            fact_ele = fact2.split(",")
            if len(fact_ele) == 7:
                fact2 = fact_ele[2] + "," + fact_ele[3] + "," + fact_ele[4] + "," + fact_ele[5] + "," + fact_ele[6]
            else:
                fact2 = fact_ele[0] + "," + fact_ele[1] + "," + fact_ele[2] + "," + fact_ele[3] + "," + fact_ele[4]

            detected_set.add(fact1)
            detected_set.add(fact2)
    # print(detected_set)
    covered_set = detected_set.intersection(free_annotated_set)
    print(len(covered_set))
    for item in covered_set:
        print(item)
    recall = len(covered_set) * 1.0 / len(free_annotated_set)
    print(len(free_annotated_set))
    print(recall)

def auto_evaluate_free_aaai17():
    # free_dict={}
    free_annotated_set = set()
    detected_set = set()
    wrong_file = "resource/FB37M_wrong_facts.tsv"
    with open(wrong_file, "r", encoding="utf-8") as freetest:
        freetest.readline()
        test_lines = freetest.readlines()
        for line in test_lines:
            line = line.strip()
            ele = line.split("\t")

            # special process
            if ele[4]=="-1":
                ele[4]=ele[5]
            if ele[5]=="-1":
                ele[5]=ele[4]
            ele[4]=ele[4][0:4]
            ele[5] = ele[5][0:4]

            fact = ele[1] + "," + ele[2] + "," + ele[3] + "," + ele[4] + "," + ele[5]
            # free_dict[fact]=ele[0]
            if ele[0] == "-1" or ele[0] == "0":
                # wiki_dict[fact]=ele[0]
                free_annotated_set.add(fact)
    # print(free_annotated_set)

    relation_map={}
    relation_map["P570"] = "people.deceased_person.date_of_death"
    relation_map["P569"] = "people.person.date_of_birth"
    relation_map["P54"] = "sports.pro_athlete.teams"
    relation_map["P26"] = "people.person.spouse_s"
    relation_map["P108"] = "people.person.employment_history"
    relation_map["P286"] = "sports.sports_team.coaches"
    conflict_file = "tecore/FBconflict_web.cons"
    with open(conflict_file, "r", encoding="utf-8") as fbconflict:
        conflict_lines = fbconflict.readlines()
        for line in conflict_lines:
            line = line.strip()
            ele = line.split("\t")
            ele[1]=relation_map[ele[1]]
            fact=ele[0]+ "," + ele[1] + "," + ele[2] + "," + ele[3] + "," + ele[4]
            detected_set.add(fact)
    # print(detected_set)
    covered_set = detected_set.intersection(free_annotated_set)
    for item in covered_set:
        print(item)
    # print(covered_set)
    recall = len(covered_set) * 1.0 / len(free_annotated_set)
    print(len(free_annotated_set))
    print(recall)

def automatic_evaluate():
    # 411
    # 0.5790754257907542
    # 411
    # 0.23114355231143552
    auto_evaluate_wiki()
    auto_evaluate_wiki_aaai17()

    # 128
    # 0.1953125
    # 128
    # 0.0859375
    auto_evaluate_free()
    auto_evaluate_free_aaai17()

def select_all_mapped_facts():
    ids_map={}
    with open("resource/FBids_to_WDids.tsv","r",encoding="utf-8") as file:
        lines=file.readlines()
        for line in lines:
            line = line.strip()
            ele=line.split("\t")
            ids_map[ele[0]]=ele[1]

    free_utkg=read_datasets.read_file("resource/FB37M.tsv")
    selected_facts=[]
    for fact in free_utkg:
        s=fact[0]
        o=fact[2]
        st=fact[3]
        ed=fact[4]
        if st!="null" or ed!="null":
            if s in ids_map:
                if o[1]==".":
                    if o in ids_map:
                        str_fact=fact[0]+"\t"+fact[1]+"\t"+fact[2]+"\t"+fact[3]+"\t"+fact[4]
                        selected_facts.append(str_fact)
                else:
                    str_fact = fact[0] + "\t" + fact[1] + "\t" + fact[2] + "\t" + fact[3] + "\t" + fact[4]
                    selected_facts.append(str_fact)
    with open("resource/selected_fb_facts.tsv","w",encoding="utf-8") as file1:
        file1.write("\n".join(selected_facts))

def tranlate():
    relation_map = {}
    relation_map["people.deceased_person.date_of_death"] = "P570"
    relation_map["people.person.date_of_birth"] = "P569"
    relation_map["sports.pro_athlete.teams"] = "P54"
    relation_map["people.person.spouse_s"] = "P26"
    relation_map["people.person.employment_history"] = "P108"
    relation_map["sports.sports_team.coaches"] = "P286"

    id_maps = {}
    with open("resource/FBids_to_WDids.tsv", "r", encoding="utf-8") as id_maps_file:
        lines = id_maps_file.readlines()
        for pair in lines:
            pair = pair.strip()
            fbid = pair.split("\t")[0]
            wdid = pair.split("\t")[1]
            id_maps[fbid] = wdid
    filename="resource/FB37M_wrong_facts.tsv"
    filename="resource/FB-128.tsv"
    with open(filename,"r",encoding="utf-8") as file:
        file.readline()
        samples=file.readlines()

    translated_lines=[]
    for line in samples:
        line = line.strip()
        sample = line.split("\t")
        s = sample[1]
        p = sample[2]
        o = sample[3]
        st = sample[4]
        ed = sample[5]
        new_sample=sample[0:6]
        maped_s=id_maps[s]
        maped_p=relation_map[p]
        if o[1]==".":
            maped_o=id_maps[o]
        else:
            maped_o=o
        mapped_fact=[maped_s,maped_p,maped_o,st,ed]
        translated_line="\t".join(new_sample)+"\t"+"|"+"\t"+"\t".join(mapped_fact)+"\n"
        translated_lines.append(translated_line)

    with open("resource/temp_free_mapped_annotated_file.tsv","w",encoding="utf-8") as file1:
        file1.write("label\ts\tp\to\tst\ted\t|\ts(WDid)\tp(WDid)\to(WDid)\tst\ted\n")
        file1.writelines(translated_lines)

def count_statistic():
    file="resource/WD27M_wrong_facts.tsv"
    # file = "resource/FB37M_wrong_facts.tsv"
    file="resource/unique_wiki_a.tsv"
    with open(file,"r",encoding="UTF-8") as f:
        f.readline()
        lines=f.readlines()
    dict={}
    for line in lines:
        # print(line)
        p=line.split("\t")[2]
        if p not in dict:
            dict[p]=1
        else:
            dict[p]+=1
    print("predicates",len(dict))
    print("len",sum(dict.values()))
    for item in dict.keys():
        print(item+"\t"+str(dict[item]))
    # print(dict)
    return

def compare_difference():
    file1="output/WD27M.all_constraints"
    file1_std="Std_results/WD27M.tsv_all_constraints"
    file2="output/FB37M.all_constraints"
    file2_std="Std_results/FB37M.tsv_all_constraints"
    wd_set=set()
    wd_std_set=set()
    with open(file1,"r",encoding="utf-8") as f1:
        lines=f1.readlines()
        for line in lines:
            wd_set.add(line.split("|")[0])

    with open(file1_std,"r",encoding="utf-8") as f1_std:
        lines=f1_std.readlines()
        for line in lines:
            wd_std_set.add(line.split("|")[0])

    print(len(wd_set))
    print(len(wd_std_set))

    print(len(wd_set.intersection(wd_std_set)))
    print(len(wd_std_set.union(wd_set)))

    fb_set = set()
    fb_std_set = set()
    with open(file2, "r", encoding="utf-8") as f2:
        lines = f2.readlines()
        for line in lines:
            fb_set.add(line.split("|")[0])

    with open(file2_std, "r", encoding="utf-8") as f2_std:
        lines = f2_std.readlines()
        for line in lines:
            fb_std_set.add(line.split("|")[0])


    print(len(fb_set))
    print(len(fb_std_set))

    print(len(fb_set.intersection(fb_std_set)))
    print(len(fb_std_set.union(fb_set)))

def correct_supplement_wiki():
    supple_dict = {}
    file = "resource/wiki_sup.txt"
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line = line.split("\t")
            supple_dict[line[0]] = int(line[1])

    file1 = "resource/wiki_annotated_file.tsv"
    # file1="resource/selected_fb_facts.tsv"
    with open(file1,"r",encoding="utf-8") as f1:
        lines=f1.readlines()
        for line in lines:
            line=line.strip()
            line=line.split("\t")
            if line[0]=="1":
                if line[2] in supple_dict:
                    if supple_dict[line[2]]>0:
                        print(line)
                        supple_dict[line[2]]-=1

    for item in supple_dict.keys():
        print(item,supple_dict[item])
    # print(supple_dict)

def correct_supplement_free():
    supple_dict={}
    file="resource/free_sup.txt"
    with open(file,"r",encoding="utf-8") as f:
        lines=f.readlines()
        for line in lines:
            line=line.strip()
            line=line.split("\t")
            supple_dict[line[0]]=int(line[1])

    file1 = "resource/temp_free_annotated_file.tsv"
    # file1="resource/selected_fb_facts.tsv"
    with open(file1,"r",encoding="utf-8") as f1:
        lines=f1.readlines()
        for line in lines:
            line=line.strip()
            line=line.split("\t")
            if line[0]=="1":
                if supple_dict[line[2]]>0:
                    print(line)
                    supple_dict[line[2]]-=1

    print(supple_dict)


def correct_supplement():
    correct_supplement_wiki()
    # correct_supplement_free()

def test():
    # automatic_evaluate()
    # tranlate()
    # sample_annotated_data()
    # truth_verification()
    # fbid_to_wdid()
    # entity_in_temporal_fact()
    # deduplicate_annotated_files()
    # automatic_evaluate()
    # select_all_mapped_facts()
    count_statistic()
    # compare_difference()
    # correct_supplement()

if __name__ == '__main__':
    test()