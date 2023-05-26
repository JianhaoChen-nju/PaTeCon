import argparse

import Constraint_Mining
import Graph_Structure
import Conflict_Detection
import os

relation_number={"GDELT":240,"ICEWS14":230,"ICEWS05-15":251,"ICEWS18":256,"WIKI":24,"YAGO":10}

confidence_threshold=0.97
def pre_process():
    file="data"
    for root, dirs, files in os.walk(file):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            f1=os.path.join(root, f)
            file1=open(f1,"r",encoding="utf-8")
            pfi = "processed_" + f1
            file2 = open(pfi, "w", encoding="utf-8")
            lines=file1.readlines()
            new_lines=[]

            for line in lines:
                line=line.replace(" ","_").replace(",","")
                new_lines.append(line)

            file2.writelines(new_lines)
                # head=line.split("\t")[0]
                # relation=line.split("\t")[1]
                # tail=line.split("\t")[2]
            print(os.path.join(root, f))

        # 遍历所有的文件夹

        # for d in dirs:
        #     print(os.path.join(root, d))


def read_file(filename):
    f=open(filename,"r",encoding="utf-8")
    lines=f.readlines()
    f.close()
    facts=[]
    for line in lines:
        line=line.strip()
        line=line.replace(",\t",",").replace("[[", "").replace("[","")
        line=line.replace(",]]", "").replace(",]","")
        # line = line.replace("[", "").replace(",]","")
        fact=line.split("\t")
        process_fact = [fact[0], fact[1], fact[2], fact[3], fact[4]]
        # process_fact=[fact[1],fact[2],fact[3],fact[4]]
        facts.append(process_fact)

    return facts

def Entity_Prediction_Metrics(facts):
    l=len(facts)
    rank=[]
    for i in range(l):
        tails=facts[i][2].split(",")
        heads = facts[i][0].split(",")
        if len(heads)!=1:
            rank.append(len(heads))
        elif len(tails)!=1:
            rank.append(len(tails))
        else:
            rank.append(1)
    nMrr=0
    hit1 = 0
    hit3=0
    hit10=0
    for i in range(l):
        nMrr+=1.0/float(rank[i])
        if rank[i]==1:
            hit1+=1
        if rank[i]<=3:
            hit3+=1
        if rank[i]<=10:
            hit10+=1

    # for i in range(half):
    #     nMrr += 1.0 / float(mrr[i])
    # print(rank)
    # print(facts[0])
    # print(facts[100000])
    return nMrr/l,float(hit1)/l,float(hit3)/l,float(hit10)/l

def Relation_Prediction_Metrics(facts):
    l=len(facts)
    rank=[]
    for i in range(l):
        if len(facts[i])==5:
            mid=facts[i][2].split(",")
        else:
            mid=facts[i][1].split(",")
        rank.append(len(mid))
    nMrr=0
    hit1 = 0
    hit3=0
    hit10=0
    for i in range(l):
        nMrr+=1.0/float(rank[i])
        if rank[i]==1:
            hit1+=1
        if rank[i]<=3:
            hit3+=1
        if rank[i]<=10:
            hit10+=1

    return nMrr/l,float(hit1)/l,float(hit3)/l,float(hit10)/l

def GoldMetrics(facts):
    # gold rank
    nMrr = 0
    hit1 = 0
    hit3 = 0
    hit10 = 0
    for i in range(len(facts)):
        rank=int(facts[i][0])
        nMrr += 1.0 / float(rank)
        if rank == 1:
            hit1 += 1
        if rank <= 3:
            hit3 += 1
        if rank <= 10:
            hit10 += 1

    #
    # l=len(facts)
    # # print(facts[0])
    # rank=[]
    # # half=int(l/2)
    # # print(l,half)
    # for i in range(l):
    #     tails=facts[i][3].split(",")
    #     # gold=tails[len(tails)-1]
    #     rank.append(len(tails))
    # # print(rank)
    # nMrr=0
    # hit1 = 0
    # hit3=0
    # hit10=0
    # for i in range(l):
    #     nMrr+=1.0/float(rank[i])
    #     if rank[i]==1:
    #         hit1+=1
    #     if rank[i]<=3:
    #         hit3+=1
    #     if rank[i]<=10:
    #         hit10+=1
    return nMrr / len(facts), float(hit1) / len(facts), float(hit3) / len(facts), float(hit10) / len(facts)

def NoEndTraintSet(g):
    for i in g.sVertexList.keys():
        statementList = g.sVertexList[i]
        for j in statementList:
            end = j.getEndTime()
            if end==g.maxTime:
                j.end=-1
            # print(head, relation, tail, start, end,  weight, truth)

def streaming_detection(filename,knowledgebase,original_set,constraint_filename):
    detected_facts=[]
    fact_truth={}
    # if filename.__contains__("WIKI") or filename.__contains__("wikidata"):
    #     knowledgebase="wikidata"
    # elif filename.__contains__("freebase"):
    #     knowledgebase="freebase"
    # else:
    #     knowledgebase="other"
    relation_n=0
    if filename.__contains__("WIKI"):
        relation_n=relation_number['WIKI']
    elif filename.__contains__("YAGO"):
        relation_n=relation_number['YAGO']
    elif filename.__contains__("ICEWS14"):
        relation_n=relation_number['ICEWS14']
    elif filename.__contains__("ICEWS18"):
        relation_n=relation_number['ICEWS18']
    elif filename.__contains__("GDELT"):
        relation_n=relation_number['GDELT']
    elif filename.__contains__("ICEWS05-15"):
        relation_n=relation_number['ICEWS05-15']
    facts_dict={}
    g=Graph_Structure.Graph()
    g.ConstructThroughTsv(original_set, knowledgebase)
    constraint_set=Conflict_Detection.read_constraints(constraint_filename)
    # print(constraint_set)
    filtered_constraints=[]
    for c in constraint_set:
        confidence=float(c.split("|")[1])
        if confidence>=confidence_threshold:
            filtered_constraints.append(c)
    # print(filtered_constraints)
    # the max end time means the fact has not ended

    NoEndTraintSet(g)
    # g.iterateOverGraph()
    facts=read_file(filename)
    # print(facts)

    conflict_file = open(filename.replace(".txt",".conflict"), "w", encoding="UTF-8")
    index = 0
    for i in range(len(facts)):
        predicted_facts = []
        mid=facts[i][2].split(",")
        gold= mid[len(mid)-1]
        # print(gold)

        # print(facts[i])
        if len(mid)>20:
            detected_facts.append(facts[i])
            continue
        for m in mid:
            fact=[facts[i][1],m,facts[i][3],facts[i][4],facts[i][4]]
            predicted_facts.append(fact)

        # loop input
        Conflict_Free_Relation=[]
        for fact in predicted_facts:
            # print(fact)
            inverse=False
            index += 1
            if index % 10000 == 0:
                print("have detected", index, "predicted facts")

            #process inverse relation
            relation = fact[1]
            if int(relation)>=relation_n:
                inverse=True
                head = fact[2]
                tail = fact[0]
                relation= str(int(relation)-relation_n)

            else:
                head = fact[0]
                tail = fact[2]

            start = fact[3]
            end = fact[4]
            fact=[head,relation,tail,start,end]
            # print(fact)
            e1 = g.add_eVertex(head)
            e2 = g.add_eVertex(tail)
            svertex = g.add_sVertex(relation, start, end)
            g.add_e2s_Edge(e1, svertex)
            g.add_s2e_Edge(svertex, e2)
            sg = g.select_subgraph(head, tail)
            Conflict_Set = Conflict_Detection.Conflict_Detection(sg, filtered_constraints, filename, knowledgebase,False,'')
            hasConflict=False
            for conflict in Conflict_Set:
                str_fact=fact[0]+","+fact[1]+","+fact[2]+","+fact[3]+","+fact[4]
                if inverse == True:
                    original_fact = fact[2] + "," + str(int(fact[1]) + relation_n) + "," + fact[0] + "," + fact[
                        3] + "," + fact[4]
                else:
                    original_fact=str_fact
                if conflict.__contains__(str_fact):
                    # print(original_fact)
                    hasConflict=True
                    conflict=conflict.replace(str_fact,original_fact)
                    conflict_file.write(conflict)
                    conflict_file.write("\n")
            # print(Conflict_Set)
            g.delete_sVertex(fact, svertex)
            del sg
            if hasConflict==False:
                # No conflict
                if inverse==True:
                    Conflict_Free_Relation.append(str(int(relation)+relation_n))
                else:
                    Conflict_Free_Relation.append(relation)

        # print(Conflict_Free_Entity)
        # splice back
        fact = predicted_facts[0]
        if len(Conflict_Free_Relation)==0:
            Conflict_Free_Fact= [fact[0],Conflict_Free_Relation,fact[2],fact[3]]
            print(Conflict_Free_Fact)
        else:
            Relation=Conflict_Free_Relation[0]
            # print(Conflict_Free_Relation[len(Conflict_Free_Relation)-1])
            if Conflict_Free_Relation[len(Conflict_Free_Relation)-1]!=gold:
                print(facts[i])
            for j in range(1, len(Conflict_Free_Relation)):
                Relation = Relation + "," + Conflict_Free_Relation[j]

            Conflict_Free_Fact = [fact[0],Relation,fact[2],fact[3]]
            # fact = predicted_facts[0]
            # Conflict_Free_Fact=fact
        detected_facts.append(Conflict_Free_Fact)
        # print("len(predicted_facts)",len(predicted_facts))
    conflict_file.close()
    return detected_facts

    # entity prediction version
    # for i in range(len(facts)):
    #     predicted_facts = []
    #     heads=facts[i][0].split(",")
    #     tails=facts[i][2].split(",")
    #     position=0
    #     if len(heads)!=1:
    #         position=0
    #         if len(heads)>20:
    #             detected_facts.append(facts[i])
    #             continue
    #         for h in heads:
    #             fact=[h,facts[i][1],facts[i][2],facts[i][3],facts[i][3]]
    #             predicted_facts.append(fact)
    #     elif len(tails)!=1:
    #         position=2
    #         if len(tails)>20:
    #             detected_facts.append(facts[i])
    #             continue
    #         for t in tails:
    #             fact = [facts[i][0], facts[i][1], t, facts[i][3], facts[i][3]]
    #             predicted_facts.append(fact)
    #     else:
    #         position=1
    #         fact=[facts[i][0],facts[i][1],facts[i][2],facts[i][3],facts[i][3]]
    #         predicted_facts.append(fact)
    #
    #     # loop input
    #
    #     Conflict_Free_Entity=[]
    #     for fact in predicted_facts:
    #         index += 1
    #         if index % 10000 == 0:
    #             print("have detected", index, "predicted facts")
    #
    #         head = fact[0]
    #         relation = fact[1]
    #         tail = fact[2]
    #         start = fact[3]
    #         end = fact[4]
    #         e1 = g.add_eVertex(head)
    #         e2 = g.add_eVertex(tail)
    #         svertex = g.add_sVertex(relation, start, end)
    #         g.add_e2s_Edge(e1, svertex)
    #         g.add_s2e_Edge(svertex, e2)
    #         sg = g.select_subgraph(head, tail)
    #         Conflict_Set = Conflict_Detection.Conflict_Detection(sg, filtered_constraints, filename, knowledgebase)
    #         hasConflict=False
    #         for conflict in Conflict_Set:
    #             str_fact=fact[0]+","+fact[1]+","+fact[2]+","+fact[3]+","+fact[4]
    #             if conflict.__contains__(str_fact):
    #                 hasConflict=True
    #                 conflict_file.write(conflict)
    #                 conflict_file.write("\n")
    #         # print(Conflict_Set)
    #         g.delete_sVertex(fact, svertex)
    #         del sg
    #         if hasConflict==False:
    #             # No conflict
    #             if position==0:
    #                 e=head
    #                 Conflict_Free_Entity.append(e)
    #             elif position==2:
    #                 e=tail
    #                 Conflict_Free_Entity.append(e)
    #
    #     # print(Conflict_Free_Entity)
    #     # splice back
    #     if position == 0:
    #         fact = predicted_facts[0]
    #         Entity=Conflict_Free_Entity[0]
    #         for j in range(1, len(Conflict_Free_Entity)):
    #             Entity = Entity + "," + Conflict_Free_Entity[j]
    #
    #         Conflict_Free_Fact = [Entity,fact[1],fact[2],fact[3],fact[4]]
    #     elif position == 2:
    #         fact = predicted_facts[0]
    #         # print(fact)
    #         Entity = Conflict_Free_Entity[0]
    #         for j in range(1, len(Conflict_Free_Entity)):
    #             Entity = Entity + "," + Conflict_Free_Entity[j]
    #         Conflict_Free_Fact = [fact[0], fact[1], Entity, fact[3], fact[4]]
    #     else:
    #         fact = predicted_facts[0]
    #         Conflict_Free_Fact=fact
    #     detected_facts.append(Conflict_Free_Fact)
    #     # print(len(predicted_facts))
    # return detected_facts
def detection(filename,knowledgebase):
    facts=read_file(filename)
    print("len of facts:",len(facts))
    print("Mrr,hit@1,hit@3,hit@10:",Relation_Prediction_Metrics(facts))

    trainset=""
    if filename.__contains__("WIKI"):
        trainset = "processed_data/WIKI/time_merged_train.tsv"
    elif filename.__contains__("YAGO"):
        trainset = "processed_data/YAGO/time_merged_train.tsv"
    elif filename.__contains__("ICEWS14"):
        trainset = "processed_data/ICEWS14/time_merged_train.tsv"
    elif filename.__contains__("ICEWS18"):
        trainset = "processed_data/ICEWS18/time_merged_train.tsv"
    elif filename.__contains__("GDELT"):
        trainset = "processed_data/GDELT/time_merged_train.tsv"
    elif filename.__contains__("ICEWS05-15"):
        trainset = "processed_data/ICEWS05-15/time_merged_train.tsv"
    constraint_filename = trainset.replace(".tsv",".rules")
    detected_facts=streaming_detection(filename,knowledgebase,trainset,constraint_filename)
    # print(detected_facts)
    # # calculate new metrics
    print("len(detected_facts)",len(detected_facts))
    print("Mrr,hit@1,hit@3,hit@10:",Relation_Prediction_Metrics(detected_facts))

    # print(GoldMetrics(facts))
    return


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Constraint Mining')
    # parser.add_argument('--dataset', metavar='FILE', default='', help='KG to be mined')
    # parser.add_argument('--knowledgegraph', metavar='KG', default='wikidata', help='which type of kg')
    # args = parser.parse_args()
    # filename= args.dataset
    # knowledgebase=args.knowledgegraph

    # filename = "TiRGN_predicted/relation/YAGO_filtered_predict_res_relpred1.txt"
    # filename = "TiRGN_predicted/relation/YAGO_filtered_predict_res_relpred1_test.txt"
    filename = "TiRGN_predicted/relation/RE-CGN_YAGO_filtered_predict_res_relpred1.txt"
    '''
    Mrr,hit@1,hit@3,hit@10: (0.9768747150858567, 0.9622484069990898, 0.989051279457874, 0.9982552847173055)
    Mrr,hit@1,hit@3,hit@10: (0.9775953022410595, 0.963664407808233, 0.9890765651866087, 0.9982552847173055)
    Mrr,hit@1,hit@3,hit@10: (0.9776093498681343, 0.9636896935369678, 0.9890765651866087, 0.9982552847173055)
    '''

    # filename = "TiRGN_predicted/YAGO_filtered_predict_res_relpred-test.txt"
    # filename = "TiRGN_predicted/relation/WIKI_filtered_predict_res_relpred1.txt"
    # filename = "TiRGN_predicted/relation/ICEWS14_filtered_predict_res_relpred1.txt"
    # filename = "TiRGN_predicted/relation/ICEWS18_filtered_predict_res_relpred1.txt"
    # filename = "TiRGN_predicted/relation/ICEWS05-15_filtered_predict_res_relpred1.txt"
    # filename = "TiRGN_predicted/relation/GDELT_filtered_predict_res_relpred1.txt"
    knowledgebase="other"
    detection(filename,knowledgebase)