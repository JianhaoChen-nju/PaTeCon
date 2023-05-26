import os
import random
import time

def pre_process(tsvFile):
    file=open(tsvFile, "r", encoding="utf-8")
    lines = file.readlines()
    processed_file=[]
    for line in lines:
        fact=line.strip().replace("<","").replace(">","").split("\t")
        str_fact=fact[0]+"\t"+fact[1]+"\t"+fact[2]+"\t"+fact[3]+"\t"+fact[4]
        processed_file.append(str_fact)
    file.close()
    file = open(tsvFile, "w", encoding="utf-8")
    file.writelines("\n".join(processed_file))
    file.close()

def temporal_representation_constraint(tsvFile,utkg):
    # a pre_process of data
    Conflicting_facts = []
    Conflict_free_facts=[]
    for temporal_fact in utkg:
        if temporal_fact[3]=="null" or temporal_fact[4]=="null":
            Conflict_free_facts.append(temporal_fact)
            continue
        start = int(temporal_fact[3])
        end = int(temporal_fact[4])
        if start > end:
            f=temporal_fact[0]+","+temporal_fact[1]+","+temporal_fact[2]+","+temporal_fact[3]+","+temporal_fact[4]
            Conflicting_facts.append(f)
        else:
            Conflict_free_facts.append(temporal_fact)
    print("there are ",len(Conflicting_facts)," facts whose start > end and they have been removed")
    file=open(tsvFile.replace("resource","output").replace(".tsv",".temporal_representation_conflicts"),"w",encoding="utf-8")
    file.writelines("\n".join(Conflicting_facts))

    return Conflict_free_facts

def read_footballdb_csv():
    footballdb = "football"
    filedir = os.listdir(footballdb)
    for i in range(len(filedir)):
        # if i==15:
        f = open(footballdb + "/" + filedir[i], "r", encoding="utf-8")
        lines=f.readlines()
        new_lines = []
        for line in lines:
            if line.__contains__("sameAs"):
                continue
            post_line=line.strip().replace(" ","").replace("pinstConf(","").replace(")","").replace("\"","")
            tuples=post_line.split(",")
            new_line="<"+tuples[0]+">\t<"+tuples[1]+">\t<"+tuples[2]+">\t<"+tuples[3]+">\t<"+tuples[4]+">\t<"+tuples[5]+">\t<"+tuples[6]+">"
            new_lines.append(new_line)

        f.close()
        f1=open(footballdb+ "_tsv/" + filedir[i].replace("db","tsv"),"w",encoding="utf-8")
        f1.write("\n".join(new_lines))
        f1.close()

def read_wikidata_csv():
    wikidata = "wikidata_dataset"
    filedir = os.listdir(wikidata)
    for i in range(len(filedir)):
        # if i==15:

        f = open(wikidata + "/" + filedir[i], "r", encoding="utf-8")
        lines = f.readlines()
        new_lines = []
        for line in lines:
            if line.__contains__("sameAs"):
                continue
            post_line = line.strip().replace(" ", "").replace("pinstConf(", "").replace(")", "").replace("\"", "")
            tuples = post_line.split(",")
            new_line = "<" + tuples[0] + ">\t<" + tuples[1] + ">\t<" + tuples[2] + ">\t<" + tuples[3] + ">\t<" + tuples[
                4] + ">\t<" + tuples[5] + ">\t<" + tuples[6] + ">"
            new_lines.append(new_line)

        f.close()
        f1 = open(wikidata + "_tsv/" + filedir[i].replace("csv", "tsv"), "w", encoding="utf-8")
        f1.write("\n".join(new_lines))
        f1.close()

def read_testfile():
    testfile = "rockit_wikidata_0_250k.tsv"

    f = open(testfile, "r", encoding="utf-8")
    lines = f.readlines()
    new_lines = []
    for line in lines:
        tuples = line.split("\t")
        new_line = tuples[0] + "\t" + tuples[1] + "\t" + tuples[2]
        new_lines.append(new_line)

    f.close()
    f1 = open("test_"+testfile, "w", encoding="utf-8")
    f1.write("\n".join(new_lines))
    f1.close()

def assgin_weight(datasetname):
    # Nottodo football那边需要重排序一下，排序好删掉此备注
    dataset = read_dataset(datasetname)
    utkg_full=dataset[5]
    percent_list=["0","10","25","50","75"]
    lines=[]
    for i in range(len(utkg_full)):
        if utkg_full[i][5]=="<true>":
            # 0.8-1
            weight2 = round(random.random() / 5 + 0.8,4)
            utkg_full[i][6]="<"+str(weight2)+">"
        else:
            # 0.5-1
            weight1 = round(random.random() / 2 + 0.5,4)
            utkg_full[i][6] = "<" + str(weight1) + ">"
    for line in utkg_full:
        lines.append("\t".join(line))
    if datasetname == "footballdb_tsv":
        f = open("player_team_year_rockit_100.tsv", "w", encoding="utf-8")
        f.write("\n".join(lines))
        f.close()
    else:
        f = open("rockit_wikidata_100_50k.tsv", "w", encoding="utf-8")
        f.write("\n".join(lines))
        f.close()
    for i in range(5):
        lines=[]
        utkg=dataset[i]
        for j in range(len(utkg)):
            for k in range(j,len(utkg_full)):
                if utkg[j][0].__eq__(utkg_full[k][0]) & utkg[j][1].__eq__(utkg_full[k][1]) & utkg[j][2].__eq__(utkg_full[k][2]) \
                & utkg[j][3].__eq__(utkg_full[k][3])  & utkg[j][4].__eq__(utkg_full[k][4]) & utkg[j][5].__eq__(utkg_full[k][5]):
                    utkg[j][6]=utkg_full[k][6]
                    break
        for line in utkg:
            lines.append("\t".join(line))
        if datasetname == "footballdb_tsv":
            f = open("player_team_year_rockit_"+percent_list[i]+".tsv", "w", encoding="utf-8")
            f.write("\n".join(lines))
            f.close()
        else:
            f = open("rockit_wikidata_" + percent_list[i] + "_50k.tsv", "w", encoding="utf-8")
            f.write("\n".join(lines))
            f.close()

    # datasetname = "footballdb_tsv"
    # # datasetname="wikidata_dataset_tsv"
    # dataset = read_dataset(datasetname)
    # 0-1
    weight0=random.random()

def read_file(filename):
    f = open(filename, "r", encoding="utf-8")
    starttime=time.time()
    lines = f.readlines()
    endtime=time.time()
    runningtime=endtime-starttime
    print("readlines running time is:",runningtime,"s")
    utkg = []
    starttime2 = time.time()
    deduplicate_utkg = set(lines)
    endtime2 = time.time()
    runningtime2 = endtime2 - starttime2
    print("duplicate running time is:", runningtime2, "s")
    print("len of file is",len(lines))
    print("len of NonDuplicate utkg is", len(deduplicate_utkg))

    f.close()
    for line in deduplicate_utkg:
        line=line.strip().split("\t")
        utkg.append(line)
    return utkg


# Function has been deprecated.
def read_dataset(datasetname):
    # output: utkg_list
    # 0:0% 1:10% 2:25% 3:50% 4:75% 5:100%
    inject_percent = ["0", "10", "25", "50", "75", "100"]
    testfile = []
    if datasetname == "wikidata_dataset_tsv":
        for i in inject_percent:
            file = "wikidata_dataset_tsv/rockit_wikidata_" + i + "_50k.tsv"
            testfile.append(file)
    else:  # footballdb
        for i in inject_percent:
            file = "footballdb_tsv/player_team_year_rockit_" + i + ".tsv"
            testfile.append(file)
    utkg_list = []
    for filename in testfile:
        utkg=read_file(filename)
        utkg_list.append(utkg)
    # for i in utkg_list:
    #     print(len(i))
    return utkg_list



if __name__ == '__main__':
    # read_footballdb()
    # read_wikidata()
    # read_testfile()
    # datasetname="footballdb_tsv"
    # datasetname="wikidata_dataset_tsv"
    # read_dataset(datasetname)
    # assgin_weight("wikidata_dataset_tsv")
    filename="wikidata_dataset_tsv/rockit_wikidata_0_50k.tsv"
    utkg=read_file(filename)
    # print(utkg[0])
    # pre_process(filename)

