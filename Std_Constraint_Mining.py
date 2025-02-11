import argparse
import gc
import Refinement_Mining
import read_datasets
import Interval_Relations
import Graph_Structure
import time
import os
import Conflict_Detection
from multiprocessing.dummy import Pool as ThreadPool
import Std_Refinement_Mining
from Constraint_Mining import MergeConstraint


# prune2_begin_percent=0.1
candidate_threshold=0.5
confidence_threshold=0.9
mutual_exclusion_threshold= 0.95
truncate_threshold=0.9
support_threshold=20
pruned_threshold=0.8*candidate_threshold
pruned_instances=0.5*support_threshold
relation_prune_threshold=10*support_threshold
# relation_prune_threshold=100
# relation_prune_threshold=100000000

def Mutual_Exclusion_mining(graph):
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets
    # possible_subgraph = 0
    print("Mutual_Exclusion_mining......")
    st = time.time()
    # output_filename = "functional_conflict.txt"
    # a quick index dict
    index_dict={}
    Mutual_Exclusion_constraint = []

    for i in range(len(graph.temporalRelationList)):
        index_dict[graph.temporalRelationList[i]]=i
    F_relations = graph.temporalRelationList.copy()


    if len(graph.eVertexList)<=50000:
        mutual_exclusion_threshold = 0.96
    else:
        mutual_exclusion_threshold = 0.98
    # index_dict["P54"] = 0
    # F_relations =["P54"]
    F_relations_statistics=[]
    for r in F_relations:
        F_relations_statistics.append([r,0,0])
        #relation consistent_subset total_subset
        #[[P1,0,0]]
    vertex_count=0
    pre = time.time()


    for i in graph.eVertexList:
        vertex_count += 1
        if vertex_count % 1000000 == 0:
            ed = time.time()
            print("have traversed nodes:", vertex_count)
            print("time cost:", ed - pre, "s")
        v = graph.eVertexList[i]
        if v.isLiteral == True:
            # return
            continue
        # if len(v.hasStatement)<2:
        #     continue
        all_relation_pairs = {}

        for s in v.hasStatement:
            i1 = s.getStartTime()
            i2 = s.getEndTime()
            # we only care temporal facts
            tail=s.hasValue.getId()
            if i1 != -1 or i2 != -1:
                relation = s.getId()
                if index_dict.__contains__(relation):
                    index = index_dict[relation]
                    all_relation_pairs.setdefault(index, []).append(s)
        for j in all_relation_pairs.keys():
            # hasRelation=true
            # total subsets+=1
            # if len(all_relation_pairs[j])==1:
            #     continue
            F_relations_statistics[j][2] += 1
            consistent = True
            exist = False
            if len(all_relation_pairs[j])!=1:
                consistent=False
            # possible_subgraph += len(all_relation_pairs[j])*(len(all_relation_pairs[j])-1)/2
            if consistent == True:
                # consistent subsets+=1
                F_relations_statistics[j][1] += 1
        all_relation_pairs.clear()
    for f in F_relations_statistics:
        total_subsets=f[2]
        consistent_subsets=f[1]
        relation=f[0]
        if total_subsets == 0:
            confidence = 0
        else:
            confidence = consistent_subsets * 1.0 / total_subsets
        print(relation, consistent_subsets, total_subsets, confidence)
        if confidence > mutual_exclusion_threshold and consistent_subsets > support_threshold:
        # if confidence > confidence_threshold and consistent_subsets > support_threshold:
            constraint = "(a," + relation + ",b,t1,t2) & (a," + relation + ",c,t3,t4) => MutualExclusion|" + str(
                confidence)
            print(constraint)
            Mutual_Exclusion_constraint.append(constraint)

        # x relation1 y & x relation2 z t1(t1=start time) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1
    ed = time.time()
    print("Mutual_Exclusion_Mining time is", ed - st, "s")
    # print(possible_subgraph)
    return Mutual_Exclusion_constraint


def functional_mining(graph):
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets
    # possible_subgraph = 0
    print("functional_mining......")
    st = time.time()
    # output_filename = "functional_conflict.txt"
    # a quick index dict
    index_dict={}
    functional_constraint = []

    for i in range(len(graph.temporalRelationList)):
        index_dict[graph.temporalRelationList[i]]=i
    F_relations = graph.temporalRelationList.copy()

    # index_dict["P54"] = 0
    # F_relations =["P54"]
    F_relations_statistics=[]
    for r in F_relations:
        F_relations_statistics.append([r,0,0])
        #relation consistent_subset total_subset
        #[[P1,0,0]]
    vertex_count=0
    pre = time.time()

    for i in graph.eVertexList:
        vertex_count += 1
        if vertex_count % 1000000 == 0:
            ed = time.time()
            print("have traversed nodes:", vertex_count)
            print("time cost:", ed - pre, "s")
        v = graph.eVertexList[i]
        if v.isLiteral == True:
            # return
            continue
        if len(v.hasStatement)<2:
            continue

        if len(v.hasStatement) >1000:
            continue
        all_relation_pairs = {}

        for s in v.hasStatement:
            i1 = s.getStartTime()
            i2 = s.getEndTime()
            # we only care temporal facts
            tail=s.hasValue.getId()
            if i1 != -1 or i2 != -1:
                relation = s.getId()
                if index_dict.__contains__(relation):
                    index = index_dict[relation]
                    all_relation_pairs.setdefault(index, []).append(s)
                #fill index into a set
        for j in all_relation_pairs.keys():
            # hasRelation=true
            # total subsets+=1
            # if len(all_relation_pairs[j])==1:
            #     continue

            # F_relations_statistics[j][2] += 1
            consistent = True
            negative = False
            # possible_subgraph += len(all_relation_pairs[j]) * (len(all_relation_pairs[j]) - 1) / 2
            for k in range(len(all_relation_pairs[j])):
                vertex1 = all_relation_pairs[j][k]
                flag = True
                for l in range(k + 1, len(all_relation_pairs[j])):
                    # possible_subgraph +=1
                    vertex2 = all_relation_pairs[j][l]
                    start1 = vertex1.getStartTime()
                    end1 = vertex1.getEndTime()
                    start2 = vertex2.getStartTime()
                    end2 = vertex2.getEndTime()
                    tail1 = vertex1.hasValue.getId()
                    tail2 = vertex2.hasValue.getId()

                    # confidence = positive+unknown/positive+unknown+negative
                    # if Interval_Relations.disjoint(start1, end1, start2, end2) == -1:
                    #     consistent = False
                    #     flag = False
                    #     break

                    #confidence = positive/positive+negative
                    result=Interval_Relations.disjoint(start1, end1, start2, end2)
                    if result == -1:
                        consistent = False
                        flag = False
                        negative=True
                        F_relations_statistics[j][2] += 1

                    elif result==1:
                        #result==1
                        F_relations_statistics[j][1] += 1
                        F_relations_statistics[j][2] += 1

        all_relation_pairs.clear()
    for f in F_relations_statistics:
        total_subsets=f[2]
        consistent_subsets=f[1]
        relation=f[0]
        if total_subsets == 0:
            confidence = 0
        else:
            confidence = consistent_subsets * 1.0 / total_subsets
        print(relation, consistent_subsets, total_subsets, confidence)
        if confidence > candidate_threshold and consistent_subsets > support_threshold:
        # if confidence > confidence_threshold and consistent_subsets > support_threshold:
            constraint = "(a," + relation + ",b,t1,t2) & (a," + relation + ",c,t3,t4) => disjoint(t1,t2,t3,t4)|" + str(
                confidence)
            print(constraint)
            functional_constraint.append(constraint)

        # x relation1 y & x relation2 z t1(t1=start time) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1
    ed = time.time()
    print("functional_mining time is", ed - st, "s")
    # print(possible_subgraph)
    return functional_constraint


def inverse_functional_mining(graph):
    # possible_subgraph=0
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets
    print("inverse_functional_mining......")
    st=time.time()

    inverse_functional_constraint = []
    index_dict = {}
    for i in range(len(graph.temporalRelationList)):
        index_dict[graph.temporalRelationList[i]] = i

    IF_relations = graph.temporalRelationList.copy()
    IF_relations_statistics = []
    for r in IF_relations:
        IF_relations_statistics.append([r, 0, 0])
        # relation consistent_subset total_subset
        # [[P1,0,0]]
    vertex_count=0
    pre=time.time()
    for i in graph.eVertexList:
        vertex_count+=1
        if vertex_count%1000000==0:
            ed=time.time()
            print("have traversed nodes:",vertex_count)
            print("time cost:",ed-pre,"s")
        v = graph.eVertexList[i]
        if len(v.bePointedTo)<2:
            continue
        if v.isLiteral==True:
            continue

        all_relation_pairs={}
        if len(v.bePointedTo)>1000:
            continue
        for s in v.bePointedTo:
            i1 = s.getStartTime()
            i2 = s.getEndTime()
            # we only care temporal facts
            if i1 != -1 or i2 != -1:
                relation = s.getId()
                index = index_dict[relation]
                all_relation_pairs.setdefault(index, []).append(s)

                # [[P54,e,e,e],[P286,e,e,e]]
        for j in all_relation_pairs.keys():
            # if len(all_relation_pairs[j])==1:
            #     continue
            # IF_relations_statistics[j][2] += 1
            consistent = True
            negative = False
            # possible_subgraph += len(all_relation_pairs[j]) * (len(all_relation_pairs[j]) - 1) / 2
            for k in range(len(all_relation_pairs[j])):
                vertex1 = all_relation_pairs[j][k]
                flag=True
                for l in range(k + 1, len(all_relation_pairs[j])):
                    # possible_subgraph +=1
                    vertex2 = all_relation_pairs[j][l]
                    start1 = vertex1.getStartTime()
                    end1 = vertex1.getEndTime()
                    start2 = vertex2.getStartTime()
                    end2 = vertex2.getEndTime()

                    # if Interval_Relations.disjoint(start1, end1, start2, end2) == -1:
                    #     consistent = False
                    #     flag=False
                    #     break

                    # confidence = positive/positive+negative
                    result=Interval_Relations.disjoint(start1, end1, start2, end2)
                    if result == -1:
                        consistent = False
                        flag = False
                        negative = True
                        IF_relations_statistics[j][2] += 1

                    elif result == 1:
                        # consistent subsets+=1
                        IF_relations_statistics[j][1] += 1
                        # confidence = positive/positive+negative
                        IF_relations_statistics[j][2] += 1

    for f in IF_relations_statistics:
        total_subsets = f[2]
        consistent_subsets = f[1]
        relation = f[0]
        if total_subsets == 0:
            confidence = 0
        else:
            confidence = consistent_subsets * 1.0 / total_subsets
        print(relation, consistent_subsets, total_subsets, confidence)
        if confidence > candidate_threshold and consistent_subsets > support_threshold:
        # if confidence > confidence_threshold and consistent_subsets > support_threshold:
            constraint = "(a," + relation + ",b,t1,t2) & (c," + relation + ",b,t3,t4) => disjoint(t1,t2,t3,t4)|"+str(confidence)
            print(constraint)
            inverse_functional_constraint.append(constraint)

        # x relation1 y & x relation2 z t1(t1=start time) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1
    ed=time.time()
    print("inverse_functional_mining time is",ed-st,"s")
    # print(possible_subgraph)
    return inverse_functional_constraint

def Single_Entity_Temporal_Order(graph,pruned_relation):
    # transitivity
    # before include start finish overlap disjoint
    print("Single Entity Temporal Order Mining......")
    possible_subgraph = 0
    st = time.time()
    index_dict = {}
    Single_Entity_Temporal_Order_Constraint = []
    ZH_relations = []
    ZH_relations_statistics=[]
    cou=0
    for i in range(len(graph.temporalRelationList)):
        for j in range(i+1,len(graph.temporalRelationList)):
            ZH_relation1 = graph.temporalRelationList[i]
            ZH_relation2 = graph.temporalRelationList[j]
            relation_pair1 = [ZH_relation1, ZH_relation2]
            relation_pair2 = [ZH_relation2, ZH_relation1]
            ZH_relations.append(relation_pair1)
            ZH_relations_statistics.append([ZH_relation1,ZH_relation2,0,0,0,0,0,0,0,0])
            key=ZH_relation1+"*"+ZH_relation2
            index_dict[key]=cou
            cou+=1
            #before include start finish total
            ZH_relations.append(relation_pair2)
            ZH_relations_statistics.append([ZH_relation2, ZH_relation1, 0, 0, 0, 0, 0,0,0,0])
            key = ZH_relation2 + "*" + ZH_relation1
            index_dict[key] = cou
            cou+=1

            # [[P54,P569,before],[P54,P570,before]]
    vertex_count = 0

    pre = time.time()
    # pool=ThreadPool(4)
    # def single_subgraph_traverse(i):

    #how to prune1?
    #n * n complexity, we can prune at the first layer
    # relation_temporal_order_score=[]
    # for i in graph.temporalRelationList:
    #     #relation,has_order,entity_subgraph
    #     record=[i,0,0]
    #     relation_temporal_order_score.append(record)
    # print(relation_temporal_order_score)
    possible_subgraph_set=set()
    pruned_subgraph_set=set()
    relation_in_possible_set={}
    # relation_in_pruned_set=set()

    relation_in_howmany_entities={}

    for r in graph.temporalRelationList:
        relation_in_possible_set[r]=0
        relation_in_howmany_entities[r]=0
    # print(relation_in_possible_set)

    # prune_begin_number = prune2_begin_percent * len(graph.eVertexList)
    for i in graph.eVertexList:
        relation_temporal_order_true=set()
        relation_temporal_order_exist=set()
        cou+=1
        # print(cou)
        vertex_count += 1
        if vertex_count % 1000000 == 0:
            ed = time.time()
            print("have traversed nodes:", vertex_count)
            print("time cost:", ed - pre, "s")
        # prune_step2=False
        # if prune_step2==False:
        #     if vertex_count > prune_begin_number:
        #         prune_step2=True

        v = graph.eVertexList[i]
        # print(v.getId())
        if v.isLiteral==True:
            continue
            # return
        if len(v.hasStatement) < 2:
            continue
            # return
        else:
            all_relation_pairs={}
            # time0=time.time()
            relation_set=set()
            for j in range(len(v.hasStatement)):
                s1 = v.hasStatement[j]
                relation1 = s1.getId()
                start1 = s1.getStartTime()
                end1 = s1.getEndTime()
                if start1 != -1 or end1 != -1:
                    #prune
                    # if vertex_count>prune_begin_number:
                    #     continue
                    # if relation1 in pruned_relation:
                    #     continue
                    relation_set.add(relation1)
                    for k in range(j+1,len(v.hasStatement)):
                            s2 = v.hasStatement[k]
                            if s1.getId().__eq__(s2.getId()):
                                continue
                            start2 = s2.getStartTime()
                            end2 = s2.getEndTime()
                            relation2 = s2.getId()
                            if start2 != -1 or end2 != -1:
                                # if relation2 in pruned_relation:
                                #     continue
                                key1=relation1+"*"+relation2
                                key2=relation2+"*"+relation1
                                index1=index_dict[key1]
                                index2=index_dict[key2]
                                #prune
                                # if key1 not in pruned_subgraph_set:
                                all_relation_pairs.setdefault(index1, []).append(s1)
                                all_relation_pairs.setdefault(index1, []).append(s2)
                                    # if key1 not in possible_subgraph_set:
                                    #     possible_subgraph_set.add(key1)
                                    #     relation_in_possible_set[relation1]+=1
                                    #     relation_in_possible_set[relation2]+=1

                                # if key2 not in pruned_subgraph_set:
                                all_relation_pairs.setdefault(index2, []).append(s2)
                                all_relation_pairs.setdefault(index2, []).append(s1)
                                    # if key2 not in possible_subgraph_set:
                                    #     possible_subgraph_set.add(key2)
                                    #     relation_in_possible_set[relation1] += 1
                                    #     relation_in_possible_set[relation2] += 1
            # time1=time.time()
            # print("choose time is",time1-time0,"s")
            for j in all_relation_pairs.keys():
                before_consistent = True
                include_consistent = True
                start_consistent = True
                finish_consistent = True
                before_negative = False
                include_negative = False
                start_negative = False
                finish_negative = False
                flag1 = True
                flag2 = True
                flag3 = True
                flag4 = True
                # total subsets+=1
                # 1
                # ZH_relations_statistics[j][6]+=1
                # step=2
                for k in range(0,len(all_relation_pairs[j]), 2):
                    vertex1 = all_relation_pairs[j][k]
                    vertex2 = all_relation_pairs[j][k + 1]
                    start1 = vertex1.getStartTime()
                    end1 = vertex1.getEndTime()
                    start2 = vertex2.getStartTime()
                    end2 = vertex2.getEndTime()
                    # choose which interval relation is
                    possible_subgraph +=1
                    result1=Interval_Relations.before(start1, end1, start2, end2)
                    result2=Interval_Relations.include(start1, end1, start2, end2)
                    result3=Interval_Relations.start(start1, end1, start2, end2)
                    result4=Interval_Relations.finish(start1, end1, start2, end2)
                    if result1== -1:
                        ZH_relations_statistics[j][6] += 1
                    elif result1==1:
                        # before_consistent_subsets += 1
                        ZH_relations_statistics[j][2] += 1
                        # confidence = positive/positive+negative
                        ZH_relations_statistics[j][6] += 1

                    if result2 == -1:
                        ZH_relations_statistics[j][7] += 1
                    elif result2 == 1:
                        # include_consistent_subsets +=1
                        ZH_relations_statistics[j][3] += 1
                        # confidence = positive/positive+negative
                        ZH_relations_statistics[j][7] += 1

                    if result3 == -1:
                        ZH_relations_statistics[j][8] += 1
                    elif result3 == 1:
                        # start_consistent_subsets +=1
                        ZH_relations_statistics[j][4] += 1
                        # confidence = positive/positive+negative
                        ZH_relations_statistics[j][8] += 1

                    if result4 == -1:
                        ZH_relations_statistics[j][9] += 1
                    elif result4 == 1:
                        # finish_consistent_subsets +=1
                        ZH_relations_statistics[j][5] += 1
                        # confidence = positive/positive+negative
                        ZH_relations_statistics[j][9] += 1

                    # if flag1==False and flag2==False and flag3==False and flag4==False:
                    #     break

                #prune
                #Bernoulli law of large numbers
                relation1 = ZH_relations_statistics[j][0]
                relation2 = ZH_relations_statistics[j][1]
                before_consistent_subsets = ZH_relations_statistics[j][2]
                include_consistent_subsets = ZH_relations_statistics[j][3]
                start_consistent_subsets = ZH_relations_statistics[j][4]
                finish_consistent_subsets = ZH_relations_statistics[j][5]
                before_total_subsets = ZH_relations_statistics[j][6]
                include_total_subsets = ZH_relations_statistics[j][7]
                start_total_subsets = ZH_relations_statistics[j][8]
                finish_total_subsets = ZH_relations_statistics[j][9]

                if before_total_subsets == 0:
                    before_confidence = 0
                else:
                    before_confidence = before_consistent_subsets * 1.0 / before_total_subsets
                if include_total_subsets == 0:
                    include_confidence = 0
                else:
                    include_confidence = include_consistent_subsets * 1.0 / include_total_subsets
                if start_total_subsets == 0:
                    start_confidence = 0
                else:
                    start_confidence = start_consistent_subsets * 1.0 / start_total_subsets
                if finish_total_subsets == 0:
                    finish_confidence = 0
                else:
                    finish_confidence = finish_consistent_subsets * 1.0 / finish_total_subsets

                if before_total_subsets >=pruned_instances or include_total_subsets>=pruned_instances or \
                    start_total_subsets>=pruned_instances or finish_total_subsets>=pruned_instances:
                    if before_confidence<=pruned_threshold and include_confidence<=pruned_threshold and \
                    start_confidence<=pruned_threshold and finish_confidence<=pruned_threshold:
                        # print("pruned")
                        pruned_subgraph = relation1 + "*" + relation2
                        pruned_subgraph_set.add(pruned_subgraph)
                        if pruned_subgraph in possible_subgraph_set:
                            relation_in_possible_set[relation1]-=1
                            relation_in_possible_set[relation2]-=1

                support_percent=0.4
                if before_confidence > candidate_threshold and before_consistent_subsets > support_percent*support_threshold:
                    key=relation1 + "*" + relation2
                    if key not in possible_subgraph_set:
                        possible_subgraph_set.add(key)
                        relation_in_possible_set[relation1] += 1
                        relation_in_possible_set[relation2] += 1
                elif include_confidence > candidate_threshold and include_consistent_subsets > support_percent*support_threshold:
                    key=relation1 + "*" + relation2
                    if key not in possible_subgraph_set:
                        possible_subgraph_set.add(key)
                        relation_in_possible_set[relation1] += 1
                        relation_in_possible_set[relation2] += 1
                elif start_confidence > candidate_threshold and start_consistent_subsets > support_percent*support_threshold:
                    key=relation1 + "*" + relation2
                    if key not in possible_subgraph_set:
                        possible_subgraph_set.add(key)
                        relation_in_possible_set[relation1] += 1
                        relation_in_possible_set[relation2] += 1
                elif finish_confidence > candidate_threshold and finish_consistent_subsets > support_percent*support_threshold:
                    key=relation1 + "*" + relation2
                    if key not in possible_subgraph_set:
                        possible_subgraph_set.add(key)
                        relation_in_possible_set[relation1] += 1
                        relation_in_possible_set[relation2] += 1

            #prune
            for r in relation_set:
                relation_in_howmany_entities[r]+=1
                if relation_in_howmany_entities[r]>=relation_prune_threshold:
                    if relation_in_possible_set[r]==0:
                        pruned_relation.add(r)
    # print(relation_in_possible_set)

    for f in ZH_relations_statistics:
        relation1=f[0]
        relation2=f[1]
        # 1
        # before_total_subsets= f[6]
        before_consistent_subsets=f[2]
        include_consistent_subsets=f[3]
        start_consistent_subsets = f[4]
        finish_consistent_subsets = f[5]
        before_total_subsets = f[6]
        include_total_subsets = f[7]
        start_total_subsets = f[8]
        finish_total_subsets = f[9]

        # 2
        if before_total_subsets==0:
            before_confidence = 0
        else:
            before_confidence = before_consistent_subsets * 1.0 / before_total_subsets
        if include_total_subsets == 0:
            include_confidence = 0
        else:
            include_confidence = include_consistent_subsets * 1.0 / include_total_subsets
        if start_total_subsets == 0:
            start_confidence = 0
        else:
            start_confidence = start_consistent_subsets * 1.0 / start_total_subsets
        if finish_total_subsets == 0:
            finish_confidence = 0
        else:
            finish_confidence = finish_consistent_subsets * 1.0 / finish_total_subsets

        # if before_consistent_subsets != 0:
        #     print("before relation", relation1, relation2, before_consistent_subsets, before_total_subsets, before_confidence)
        # if include_consistent_subsets != 0:
        #     print("include relation", relation1, relation2, include_consistent_subsets, include_total_subsets, include_confidence)
        # if start_consistent_subsets != 0:
        #     print("start relation", relation1, relation2, start_consistent_subsets, start_total_subsets, start_confidence)
        # if finish_consistent_subsets != 0:
        #     print("finish relation", relation1, relation2, finish_consistent_subsets, finish_total_subsets, finish_confidence)

        # if before_confidence > confidence_threshold and before_consistent_subsets > support_threshold:
        if before_confidence > candidate_threshold and before_consistent_subsets > support_threshold:
            constraint = "(a," + relation1 + ",b,t1,t2) & (a," + relation2 + ",c,t3,t4) => before(t1,t2,t3,t4)|" + str(
                before_confidence)
            print(constraint)
            Single_Entity_Temporal_Order_Constraint.append(constraint)
        # elif include_confidence > confidence_threshold and include_consistent_subsets > support_threshold:
        elif include_confidence > candidate_threshold and include_consistent_subsets > support_threshold:
            constraint = "(a," + relation1 + ",b,t1,t2) & (a," + relation2 + ",c,t3,t4) => include(t1,t2,t3,t4)|" + str(
                include_confidence)
            print(constraint)
            Single_Entity_Temporal_Order_Constraint.append(constraint)
        elif start_confidence > candidate_threshold and start_consistent_subsets > support_threshold:
            constraint = "(a," + relation1 + ",b,t1,t2) & (a," + relation2 + ",c,t3,t4) => start(t1,t2,t3,t4)|" + str(
                start_confidence)
            print(constraint)
            Single_Entity_Temporal_Order_Constraint.append(constraint)
        elif finish_confidence > candidate_threshold and finish_consistent_subsets > support_threshold:
            constraint = "(a," + relation1 + ",b,t1,t2) & (a," + relation2 + ",c,t3,t4) => finish(t1,t2,t3,t4)|" + str(
                finish_confidence)
            print(constraint)
            Single_Entity_Temporal_Order_Constraint.append(constraint)
    print(relation_in_howmany_entities)
    ed=time.time()
    print("Single Entity Temporal Order Mining time is",ed-st,"s")
    print("checked subgraph",possible_subgraph)
    return Single_Entity_Temporal_Order_Constraint

def Mutiple_Entity_Temporal_Order(graph,pruned_relation):
    print("Mutiple Entity Temporal Order Mining......")
    st = time.time()
    Mutiple_Entity_Temporal_Order_Constraint = []
    index_dict = {}
    OH_relations = []
    OH_relations_statistics = []
    cou = 0
    possible_subgraph=0
    for i in range(len(graph.temporalRelationList)):
        OH_relation1 = graph.temporalRelationList[i]
        for j in range(len(graph.relationList)):
            OH_relation2 = graph.relationList[j]
            if OH_relation2.__eq__(OH_relation1):
                continue
            for k in range(len(graph.temporalRelationList)):
                OH_relation3 = graph.temporalRelationList[k]
                if OH_relation3.__eq__(OH_relation2):
                    continue
                relation_pair1 = [OH_relation1, OH_relation2,OH_relation3]

                OH_relations.append(relation_pair1)
                OH_relations_statistics.append([OH_relation1, OH_relation2,OH_relation3,0,0,0,0,0,0,0,0,0,0,0,0,0])
                # before inverse_before include inverse_include start finish total
                key = OH_relation1 + "*" + OH_relation2+"*"+OH_relation3
                index_dict[key] = cou
                cou += 1

    possible_subgraph_set = set()
    pruned_subgraph_set = set()
    relation_in_possible_set = {}
    # relation_in_pruned_set=set()

    relation_in_howmany_entities = {}
    relationList=set(graph.relationList)
    temporalrelationList=set(graph.temporalRelationList)
    nonTemporalList=relationList.difference(temporalrelationList)
    for r in nonTemporalList:
        relation_in_possible_set[r] = 0
        relation_in_howmany_entities[r] = 0

    vertex_count = 0
    pre=time.time()
    for i in graph.eVertexList:
        # cou+=1
        # print(cou)
        vertex_count += 1
        if vertex_count % 1000000 == 0:
            ed = time.time()
            print("have traversed nodes:", vertex_count)
            print("time cost:", ed - pre, "s")
        v = graph.eVertexList[i]
        if v.isLiteral==True:
            continue
        if len(v.hasStatement) < 2:
            continue
        else:
            all_relation_pairs={}
            relation_set = set()
            for j in range(len(v.hasStatement)):
                s1 = v.hasStatement[j]
                start1 = s1.getStartTime()
                end1 = s1.getEndTime()
                relation1=s1.getId()
                if start1 != -1 or end1 != -1:
                    # if relation1 in pruned_relation:
                    #     continue

                    for k in range(len(v.hasStatement)):
                        if j==k:
                            continue
                        s2 = v.hasStatement[k]
                        one_hop=s2.getId()

                        if relation1.__eq__(one_hop):
                            continue
                        # if one_hop in pruned_relation:
                        #     continue
                        if one_hop in nonTemporalList:
                            relation_set.add(one_hop)
                        for l in range(len(s2.hasValue.hasStatement)):
                            s3=s2.hasValue.hasStatement[l]
                            relation2=s3.getId()
                            if one_hop.__eq__(relation2):
                                continue
                            # if relation2 in pruned_relation:
                            #     continue
                            start2 = s3.getStartTime()
                            end2 = s3.getEndTime()
                            if start2 != -1 or end2 != -1:
                                key1 = relation1 + "*" + one_hop+"*"+relation2
                                index1 = index_dict[key1]
                                # if key1 not in pruned_subgraph_set:
                                all_relation_pairs.setdefault(index1, []).append(s1)
                                all_relation_pairs.setdefault(index1, []).append(s3)
            for j in all_relation_pairs.keys():
                before_consistent = True
                inverse_before_consistent=True
                include_consistent = True
                inverse_include_consistent=True
                start_consistent = True
                finish_consistent = True
                before_negative = False
                inverse_before_negative = False
                include_negative = False
                inverse_include_negative = False
                start_negative = False
                finish_negative = False
                flag1 = True
                flag2 = True
                flag3 = True
                flag4 = True
                flag5 = True
                flag6 = True

                # total subsets+=1
                # OH_relations_statistics[j][9] += 1
                # step=2
                for k in range(0, len(all_relation_pairs[j]), 2):
                    # print(len(all_relation_pairs[j]))
                    vertex1 = all_relation_pairs[j][k]
                    vertex2 = all_relation_pairs[j][k + 1]
                    start1 = vertex1.getStartTime()
                    end1 = vertex1.getEndTime()
                    start2 = vertex2.getStartTime()
                    end2 = vertex2.getEndTime()
                    possible_subgraph += 1
                    # choose which interval relation is
                    result1=Interval_Relations.before(start1, end1, start2, end2)
                    result2 = Interval_Relations.before(start2, end2, start1, end1)
                    result3 = Interval_Relations.include(start1, end1, start2, end2)
                    result4 = Interval_Relations.include(start2, end2, start1, end1)
                    result5 = Interval_Relations.start(start1, end1, start2, end2)
                    result6 = Interval_Relations.finish(start1, end1, start2, end2)
                    if  result1== -1:
                        before_consistent = False
                        before_negative=True
                        flag1=False
                        OH_relations_statistics[j][9] += 1
                    elif result1==1:
                        # before_consistent_subsets += 1
                        OH_relations_statistics[j][3] += 1
                        # confidence = positive/positive+negative
                        OH_relations_statistics[j][9] += 1

                    if  result2== -1:
                        inverse_before_consistent = False
                        inverse_before_negative = True
                        flag2 = False
                        OH_relations_statistics[j][10] += 1
                    elif result2 == 1:
                        # inverse_before_consistent_subsets +=1
                        OH_relations_statistics[j][4] += 1
                        # confidence = positive/positive+negative
                        OH_relations_statistics[j][10] += 1

                    if  result3== -1:
                        include_consistent = False
                        include_negative = True
                        flag3 = False
                        OH_relations_statistics[j][11] += 1
                    elif result3 == 1:
                        # include_consistent_subsets +=1
                        OH_relations_statistics[j][5] += 1
                        # confidence = positive/positive+negative
                        OH_relations_statistics[j][11] += 1

                    if  result4== -1:
                        inverse_include_consistent = False
                        inverse_include_negative = True
                        flag4 = False
                        OH_relations_statistics[j][12] += 1
                    elif result4 == 1:
                        # inverse_include_consistent_subsets +=1
                        OH_relations_statistics[j][6] += 1
                        # confidence = positive/positive+negative
                        OH_relations_statistics[j][12] += 1

                    if  result5== -1:
                        start_consistent = False
                        start_negative = True
                        flag5 = False
                        OH_relations_statistics[j][13] += 1
                    elif result5 == 1:
                        # start_consistent_subsets +=1
                        OH_relations_statistics[j][7] += 1
                        # confidence = positive/positive+negative
                        OH_relations_statistics[j][13] += 1

                    if  result6== -1:
                        finish_consistent = False
                        finish_negative = True
                        flag6 = False
                        OH_relations_statistics[j][14] += 1
                    elif result6 == 1:
                        # finish_consistent_subsets +=1
                        OH_relations_statistics[j][8] += 1
                        # confidence = positive/positive+negative
                        OH_relations_statistics[j][14] += 1


                relation1 = OH_relations_statistics[j][0]
                one_hop = OH_relations_statistics[j][1]
                relation2 = OH_relations_statistics[j][2]
                # 1
                # total_subsets = f[9]
                before_consistent_subsets = OH_relations_statistics[j][3]
                inverse_before_consistent_subsets = OH_relations_statistics[j][4]
                include_consistent_subsets = OH_relations_statistics[j][5]
                inverse_include_consistent_subsets = OH_relations_statistics[j][6]
                start_consistent_subsets = OH_relations_statistics[j][7]
                finish_consistent_subsets = OH_relations_statistics[j][8]
                before_total_subsets = OH_relations_statistics[j][9]
                inverse_before_total_subsets = OH_relations_statistics[j][10]
                include_total_subsets = OH_relations_statistics[j][11]
                inverse_include_total_subsets = OH_relations_statistics[j][12]
                start_total_subsets = OH_relations_statistics[j][13]
                finish_total_subsets = OH_relations_statistics[j][14]

                # 2
                if before_total_subsets == 0:
                    before_confidence = 0
                else:
                    before_confidence = before_consistent_subsets * 1.0 / before_total_subsets
                if inverse_before_total_subsets == 0:
                    inverse_before_confidence = 0
                else:
                    inverse_before_confidence = inverse_before_consistent_subsets * 1.0 / inverse_before_total_subsets
                if include_total_subsets == 0:
                    include_confidence = 0
                else:
                    include_confidence = include_consistent_subsets * 1.0 / include_total_subsets
                if inverse_include_total_subsets == 0:
                    inverse_include_confidence = 0
                else:
                    inverse_include_confidence = inverse_include_consistent_subsets * 1.0 / inverse_include_total_subsets
                if start_total_subsets == 0:
                    start_confidence = 0
                else:
                    start_confidence = start_consistent_subsets * 1.0 / start_total_subsets
                if finish_total_subsets == 0:
                    finish_confidence = 0
                else:
                    finish_confidence = finish_consistent_subsets * 1.0 / finish_total_subsets

                if before_total_subsets >=pruned_instances or include_total_subsets>=pruned_instances or \
                    start_total_subsets>=pruned_instances or finish_total_subsets>=pruned_instances or \
                    inverse_before_total_subsets>=pruned_instances or inverse_include_total_subsets>=pruned_instances:
                    if before_confidence<=pruned_threshold and include_confidence<=pruned_threshold and \
                    start_confidence<=pruned_threshold and finish_confidence<=pruned_threshold and \
                    inverse_before_confidence<=pruned_threshold and inverse_include_confidence<=pruned_threshold:
                        # print("pruned")
                        pruned_subgraph = relation1 + "*" +one_hop+"*"+ relation2
                        pruned_subgraph_set.add(pruned_subgraph)
                        if pruned_subgraph in possible_subgraph_set:
                            relation_in_possible_set[one_hop]-=1

                support_percent=0.4
                if one_hop in nonTemporalList:
                    if before_confidence > candidate_threshold and before_consistent_subsets > support_percent*support_threshold:
                        key = relation1 + "*" +one_hop+"*"+ relation2
                        if key not in possible_subgraph_set:
                            possible_subgraph_set.add(key)
                            relation_in_possible_set[one_hop] += 1
                    elif inverse_before_confidence > candidate_threshold and inverse_before_consistent_subsets > support_percent*support_threshold:
                        key = relation1 + "*" + one_hop + "*" + relation2
                        if key not in possible_subgraph_set:
                            possible_subgraph_set.add(key)
                            relation_in_possible_set[one_hop] += 1
                    elif include_confidence > candidate_threshold and include_consistent_subsets > support_percent*support_threshold:
                        key = relation1 + "*" + one_hop + "*" + relation2
                        if key not in possible_subgraph_set:
                            possible_subgraph_set.add(key)
                            relation_in_possible_set[one_hop] += 1
                    elif inverse_include_confidence > candidate_threshold and inverse_include_consistent_subsets > support_percent*support_threshold:
                        key = relation1 + "*" + one_hop + "*" + relation2
                        if key not in possible_subgraph_set:
                            possible_subgraph_set.add(key)
                            relation_in_possible_set[one_hop] += 1
                    elif start_confidence > candidate_threshold and start_consistent_subsets > support_percent*support_threshold:
                        key = relation1 + "*" + one_hop + "*" + relation2
                        if key not in possible_subgraph_set:
                            possible_subgraph_set.add(key)
                            relation_in_possible_set[one_hop] += 1
                    elif finish_confidence > candidate_threshold and finish_consistent_subsets > support_percent*support_threshold:
                        key = relation1 + "*" + one_hop + "*" + relation2
                        if key not in possible_subgraph_set:
                            possible_subgraph_set.add(key)
                            relation_in_possible_set[one_hop] += 1

                # prune
                for r in relation_set:
                    relation_in_howmany_entities[r] += 1
                    if relation_in_howmany_entities[r] >= relation_prune_threshold:
                        if relation_in_possible_set[r] == 0:
                            pruned_relation.add(r)

    for f in OH_relations_statistics:
        relation1 = f[0]
        one_hop=f[1]
        relation2 = f[2]
        # 1
        # total_subsets = f[9]
        before_consistent_subsets = f[3]
        inverse_before_consistent_subsets=f[4]
        include_consistent_subsets = f[5]
        inverse_include_consistent_subsets=f[6]
        start_consistent_subsets = f[7]
        finish_consistent_subsets = f[8]
        before_total_subsets = f[9]
        inverse_before_total_subsets = f[10]
        include_total_subsets = f[11]
        inverse_include_total_subsets = f[12]
        start_total_subsets = f[13]
        finish_total_subsets = f[14]

        # 2
        if before_total_subsets == 0:
            before_confidence = 0
        else:
            before_confidence = before_consistent_subsets * 1.0 / before_total_subsets
        if inverse_before_total_subsets == 0:
            inverse_before_confidence = 0
        else:
            inverse_before_confidence = inverse_before_consistent_subsets * 1.0 / inverse_before_total_subsets
        if include_total_subsets == 0:
            include_confidence = 0
        else:
            include_confidence = include_consistent_subsets * 1.0 / include_total_subsets
        if inverse_include_total_subsets == 0:
            inverse_include_confidence = 0
        else:
            inverse_include_confidence = inverse_include_consistent_subsets * 1.0 / inverse_include_total_subsets
        if start_total_subsets == 0:
            start_confidence = 0
        else:
            start_confidence = start_consistent_subsets * 1.0 / start_total_subsets
        if finish_total_subsets == 0:
            finish_confidence = 0
        else:
            finish_confidence = finish_consistent_subsets * 1.0 / finish_total_subsets

        # 1
        # if total_subsets == 0:
        #     before_confidence = 0
        #     inverse_before_confidence = 0
        #     include_confidence = 0
        #     inverse_include_confidence = 0
        #     start_confidence = 0
        #     finish_confidence = 0
        # else:
        #     before_confidence = before_consistent_subsets * 1.0 / total_subsets
        #     inverse_before_confidence = inverse_before_consistent_subsets * 1.0 / total_subsets
        #     include_confidence = include_consistent_subsets * 1.0 / total_subsets
        #     inverse_include_confidence = inverse_include_consistent_subsets * 1.0 /total_subsets
        #     start_confidence = start_consistent_subsets * 1.0 / total_subsets
        #     finish_confidence = finish_consistent_subsets * 1.0 / total_subsets

        # if before_consistent_subsets != 0:
        #     print("before relation", relation1, one_hop, relation2, before_consistent_subsets, before_total_subsets, before_confidence)
        # if inverse_before_consistent_subsets != 0:
        #     print("inverse before relation", relation1, one_hop, relation2, inverse_before_consistent_subsets, inverse_before_total_subsets, inverse_before_confidence)
        # if include_consistent_subsets != 0:
        #     print("include relation", relation1, one_hop, relation2, include_consistent_subsets, include_total_subsets,include_confidence)
        # if inverse_include_consistent_subsets != 0:
        #     print("inverse include relation", relation1, one_hop, relation2, inverse_include_consistent_subsets, inverse_include_total_subsets, inverse_include_confidence)
        # if start_consistent_subsets != 0:
        #     print("start relation", relation1, one_hop, relation2, start_consistent_subsets, start_total_subsets, start_confidence)
        # if finish_consistent_subsets != 0:
        #     print("finish relation", relation1, one_hop, relation2, finish_consistent_subsets, finish_total_subsets,finish_confidence)

        if before_confidence > candidate_threshold and before_consistent_subsets>support_threshold:
            constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => before(t1,t2,t5,t6)|"+str(before_confidence)
            print(constraint)
            Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
        elif inverse_before_confidence > candidate_threshold and inverse_before_consistent_subsets>support_threshold:
            constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => before(t5,t6,t1,t2)|"+str(inverse_before_confidence)
            print(constraint)
            Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
        elif include_confidence > candidate_threshold and include_consistent_subsets>support_threshold:
            constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => include(t1,t2,t5,t6)|"+str(include_confidence)
            print(constraint)
            Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
        elif inverse_include_confidence > candidate_threshold and inverse_include_consistent_subsets>support_threshold:
            constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => include(t5,t6,t1,t2)|"+str(inverse_include_confidence)
            print(constraint)
            Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
        elif start_confidence > candidate_threshold and start_consistent_subsets>support_threshold:
            constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => start(t1,t2,t5,t6)|"+str(start_confidence)
            print(constraint)
            Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
        elif finish_confidence > candidate_threshold and finish_consistent_subsets>support_threshold:
            constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => finish(t1,t2,t5,t6)|"+str(finish_confidence)
            print(constraint)
            Mutiple_Entity_Temporal_Order_Constraint.append(constraint)

    print(relation_in_howmany_entities)
    ed=time.time()
    print("Mutiple Entity Temporal Order Mining time is",ed-st,"s")
    print("checked subgraph", possible_subgraph)
    return Mutiple_Entity_Temporal_Order_Constraint


def Compound(atoms):
    Compounded_atoms=[]
    for i in range(len(atoms)):
        noCompound=True
        atom1 = atoms[i]
        if atom1.__eq__("null"):
            continue
        for j in range(len(atoms)):
            atom2=atoms[j]
            if atom2.__eq__("null"):
                continue
            head1=atom1.replace(" ","").replace("(","").replace(")","").split(",")[0]
            relation1 = atom1.replace(" ","").replace("(", "").replace(")", "").split(",")[1]
            tail1=atom1.replace(" ","").replace("(","").replace(")","").split(",")[2]
            head2 = atom2.replace(" ","").replace("(", "").replace(")", "").split(",")[0]
            relation2 = atom2.replace(" ","").replace("(", "").replace(")", "").split(",")[1]
            tail2 = atom2.replace(" ","").replace("(", "").replace(")", "").split(",")[2]
            t3=atom2.replace(" ","").replace("(", "").replace(")", "").split(",")[3]
            t4 = atom2.replace(" ","").replace("(", "").replace(")", "").split(",")[4]
            if head2.__eq__(tail1):
                noCompound=False
                atom=head1+","+relation1+"*"+relation2+","+tail2+","+t3+","+t4
                Compounded_atoms.append(atom)
                atoms[i]="null"
                atoms[j]="null"
        if noCompound==True:
            atom1=atom1.replace(" ","").replace("(","").replace(")","")
            Compounded_atoms.append(atom1)

    return Compounded_atoms

def simplify_constraint(constraint):
    '''
    :param constraint:
    :return:
    '''
    '''
        (a,P569,b,t1,t2) & (a,P569,c,t3,t4) => disjoint(t1,t2,t3,t4)
        =>
        (a,P569,b) disjoint (a,P569,c)

        (a,P569,b,t1,t2) & (a,father,c,t3,t4) & (c,P569,d,t5,t6) => before(t5,t6,t1,t2)
        =>
        (a,P569,b,t1,t2) before (a,father*P569,d,t5,t6)
        '''
    # print(constraint)
    confidence=constraint.split("|")[1]
    constraint=constraint.split("|")[0]
    constraint = constraint.replace("=>", ":")

    body = constraint.split(":")[0]
    head = constraint.split(":")[1]
    #print(body, head)

    atoms = body.split("&")

    Compounded_atoms = Compound(atoms)
    # print(Compounded_atoms)
    relation=head.replace(" ","").split("(")[0]
    t=head.replace(" ","")
    if t=="MutualExclusion":
        simple_constraint = Compounded_atoms[0] + " " + relation + " " + Compounded_atoms[1]+"|"+confidence
        return simple_constraint
    t=t.split("(")[1].split(",")[0]

    if len(Compounded_atoms)!=2:
        print("Compound atoms error: len != 2 ")
        print(constraint)
        return ""

    if Compounded_atoms[0].split(",")[3].__eq__(t):
        simple_constraint=Compounded_atoms[0]+" "+relation+" "+Compounded_atoms[1]
    else:
        simple_constraint =Compounded_atoms[1]+" "+relation+" "+Compounded_atoms[0]
    simple_constraint=simple_constraint+"|"+confidence
    return simple_constraint

def Set_Include(constraint,Transitive_closure_set):
    confidence = constraint.split("|")[1]
    constraint = constraint.split("|")[0]
    fact1 = constraint.split(" ")[0]
    relation1 = fact1.split(",")[1]
    interval_relation1 = constraint.split(" ")[1]
    fact2 = constraint.split(" ")[2]
    relation2 = fact2.split(",")[1]
    include=False
    for constraint2 in Transitive_closure_set:
        confidence = constraint2.split("|")[1]
        constraint2 = constraint2.split("|")[0]
        fact3 = constraint2.split(" ")[0]
        relation3 = fact3.split(",")[1]
        interval_relation2 = constraint2.split(" ")[1]
        fact4 = constraint2.split(" ")[2]
        relation4 = fact4.split(",")[1]
        if interval_relation1.__eq__(interval_relation2) and relation1.__eq__(relation3) and relation2.__eq__(relation4):
            include=True

    return include

def formal(simple_constraint):
    # confidence = simple_constraint.split("|")[1]
    # simple_constraint = simple_constraint.split("|")[0]
    formal_constraint=""
    filtered_Constraint = []
    refined_Constraint = []

    # mutual exclusion constraints detection
    mutual_exclusion_constraints = []
    # functional constraints detection
    functional_constraints = []
    # inverse functional constraints detection
    inverse_functional_constraints = []
    # zero hop constraint detection
    zero_hop_constraints = []
    # first one hop constraint detection
    first_one_hop_constraints = []
    # second one hop constraint detection
    second_one_hop_constraints = []

    if simple_constraint.__contains__("class"):
        elem = simple_constraint.split(" ")
        if len(elem) == 5:
            atom1 = elem[0]
            class_type1 = elem[1]
            interval_relation = elem[2]
            atom2 = elem[3]
            class_type2 = elem[4]
            anchor = ""
            if atom1.split(",")[0].__eq__(atom2.split(",")[0]):
                anchor = "head"
            elif atom1.split(",")[2].__eq__(atom2.split(",")[2]):
                anchor = "tail"
            if anchor == "head":
                path1 = atom1.split(",")[1]
                edges1 = path1.split("*")
                path2 = atom2.split(",")[1]
                edges2 = path2.split("*")
                if edges1[0] == edges2[0] and len(edges1) == 1 and len(edges2) == 1:
                    # functional_constraints.append(c)
                    formal_constraint = "(" + atom1 + ") & ("+class_type1+") & (" + atom2 + ") & ("+class_type2+")  => " + "disjoint" + "(t1,t2,t3,t4)"
                elif edges1[0] != edges2[0] and len(edges1) == 1 and len(edges2) == 1:
                    # zero_hop_constraints.append(c)
                    formal_constraint = "(" + atom1 + ") & (" + class_type1 + ") & (" + atom2 + ") & (" + class_type2 + ")  => " + interval_relation + "(t1,t2,t3,t4)"

            elif anchor == "tail":
                formal_constraint = "(" + atom1 + ") & (" + class_type1 + ") & (" + atom2 + ") & (" + class_type2 + ")  => " + "disjoint" + "(t1,t2,t3,t4)"
                # inverse_functional_constraints.append(c)
        elif len(elem) == 6:
            if elem[2].__contains__("class"):
                atom2 = elem[0]
                type2 = elem[1]
                type3 = elem[2]
                interval_relation = elem[3]

                atom1 = elem[4]
                type1 = elem[5]

                path1 = atom1.split(",")[1]
                edges1 = path1.split("*")
                path2 = atom2.split(",")[1]
                edges2 = path2.split("*")
                formal_constraint = "(a," + edges1[0] + ",b,t1,t2) & (" + type1 + \
                                    ") & (a," + edges2[0] + ",c,t3,t4) & ("+type2+") & (c," + edges2[1] + ",d,t5,t6) & ("+type3+") => " \
                                    + interval_relation + "(t5,t6,t1,t2)"
            else:
                atom1 = elem[0]
                type1 = elem[1].split(",")[2]
                interval_relation = elem[2]
                atom2 = elem[3]
                type2 = elem[4].split(",")[2]
                type3 = elem[5].split(",")[2]

                path1 = atom1.split(",")[1]
                edges1 = path1.split("*")
                path2 = atom2.split(",")[1]
                edges2 = path2.split("*")

                formal_constraint = "(a," + edges1[0] + ",b,t1,t2) & (" + type1 + \
                                    ") & (a," + edges2[0] + ",c,t3,t4) & (" + type2 + ") & (c," + edges2[
                                        1] + ",d,t5,t6) & (" + type3 + ") => " \
                                    + interval_relation + "(t1,t2,t3,t4)"
            # one_hop_constraints.append(c)
    else:
        # print(simple_constraint)
        elem = simple_constraint.split(" ")
        atom1 = elem[0]
        interval_relation = elem[1]
        atom2 = elem[2]
        anchor = ""
        if interval_relation=="MutualExclusion":
            # mutual_exclusion_constraints.append(c)
            formal_constraint="("+atom1+") & ("+atom2+")  => MutualExclusion"
        else:
            if atom1.split(",")[0].__eq__(atom2.split(",")[0]):
                anchor = "head"
            elif atom1.split(",")[2].__eq__(atom2.split(",")[2]):
                anchor = "tail"
            if anchor == "head":
                path1 = atom1.split(",")[1]
                edges1 = path1.split("*")
                path2 = atom2.split(",")[1]
                edges2=path2.split("*")
                if edges1[0] == edges2[0] and len(edges1) == 1 and len(edges2) == 1:
                    formal_constraint = "(" + atom1 + ") & (" + atom2 + ")  => "+"disjoint"+"(t1,t2,t3,t4)"
                    # functional_constraints.append(c)
                elif edges1[0] != edges2[0] and len(edges1) == 1 and len(edges2) == 1:
                    formal_constraint = "(" + atom1 + ") & (" + atom2 + ")  => " + interval_relation + "(t1,t2,t3,t4)"
                    # zero_hop_constraints.append(c)
                elif len(edges1) == 2 and len(edges2) == 1:
                    # "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => before(t1,t2,t5,t6)
                    relation1 = edges2[0]
                    one_hop = edges1[0]
                    relation2 = edges1[1]
                    formal_constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => " + interval_relation + "(t5,t6,t1,t2)"
                    # first_one_hop_constraints.append(c)
                elif len(edges1) == 1 and len(edges2) == 2:
                    relation1 = edges1[0]
                    one_hop=edges2[0]
                    relation2= edges2[1]
                    formal_constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => " + interval_relation + "(t1,t2,t5,t6)"
                    # second_one_hop_constraints.append(c)
            elif anchor=="tail":
                # inverse_functional_constraints.append(c)
                formal_constraint = "(" + atom1 + ") & (" + atom2 + ")  => " + "disjoint" + "(t1,t2,t3,t4)"


    for sc in simple_constraint:
        sc=sc.split("|")[0]


    '''
    a,father*P569,d,t5,t6 before a,P26*P54,d,t5,t6
    =>
    (a,father,b,t1,t2) & (b,P569,c,t3,t4) & (a,P26,d,t5,t6) & (d,P54,e,t7,t8) => before(t3,t4,t7,t8)
    '''

    return formal_constraint

def apply_transfering_rules(constraint,Old_Transitive_closure_set):
    '''
    :param constraint:
    :param Old_Transitive_closure_set:
    :return:
    '''

    '''
    transfer rules
    a before b, b before c => a before c
    a include b , b include c => a include c
    a start b, b start c => a start c
    a finish b, b finish c => a finish c
    
    a before b, b start c => a before c
    a before b , b include c => a before c
    a include b, a before c => b before c
    a finish b, b before c => a before c
    '''

    confidence = constraint.split("|")[1]
    num_confidence=float(confidence)
    constraint = constraint.split("|")[0]
    transitive_constraint_set=[]
    fact1=constraint.split(" ")[0]
    relation1=fact1.split(",")[1]
    interval_relation1 = constraint.split(" ")[1]
    fact2=constraint.split(" ")[2]
    relation2=fact2.split(",")[1]

    for constraint2 in Old_Transitive_closure_set:
        confidence2 = constraint2.split("|")[1]
        num_confidence2=float(confidence2)
        constraint2 = constraint2.split("|")[0]
        fact3 = constraint2.split(" ")[0]
        relation3 = fact3.split(",")[1]
        interval_relation2 = constraint2.split(" ")[1]
        fact4 = constraint2.split(" ")[2]
        relation4 = fact4.split(",")[1]
        '''
        transfer rules
        a before b, b before c => a before c
        a include b , b include c => a include c
        a start b, b start c => a start c
        a start b, a start c => b start c
        a finish b, b finish c => a finish c
        a finish b, a finish c => b finish c
        a special situation
        a,father*P54,d,t5,t6 before a,P569,b,t1,t2 & a,P569,b,t1,t2 before a,P26*P108,d,t5,t6 => a,father*P54,d,t5,t6 before a,P26*P108,d,t5,t6|1.0
        '''
        interval_relations=["before","include","start","finish"]
        if relation2.__eq__(relation3):
            for interval_relation in interval_relations:
                if interval_relation1.__eq__(interval_relation) and interval_relation2.__eq__(interval_relation):
                    transfer_confidence=num_confidence*num_confidence2
                    transitive_constraint=fact1+" "+interval_relation+" "+fact4+"|"+str(transfer_confidence)
                    if transfer_confidence>truncate_threshold:
                        if Set_Include(transitive_constraint,Old_Transitive_closure_set)==False:
                            # print("add")
                            # print(constraint, "&", constraint2, "=>", transitive_constraint)
                            transitive_constraint_set.append(transitive_constraint)
            if interval_relation1.__eq__("before") and interval_relation2.__eq__("start"):
                transfer_confidence = num_confidence * num_confidence2
                transitive_constraint = fact1 + " " + "before" + " " + fact4+"|"+str(transfer_confidence)
                if transfer_confidence > truncate_threshold:
                    if Set_Include(transitive_constraint, Old_Transitive_closure_set) == False:
                        # print("add")
                        # print(constraint, "&", constraint2, "=>", transitive_constraint)
                        transitive_constraint_set.append(transitive_constraint)
            elif interval_relation1.__eq__("before") and interval_relation2.__eq__("include"):
                transfer_confidence = num_confidence * num_confidence2
                transitive_constraint = fact1 + " " + "before" + " " + fact4+"|"+str(transfer_confidence)
                if transfer_confidence > truncate_threshold:
                    if Set_Include(transitive_constraint, Old_Transitive_closure_set) == False:
                        # print("add")
                        # print(constraint, "&", constraint2, "=>", transitive_constraint)
                        transitive_constraint_set.append(transitive_constraint)
            elif interval_relation1.__eq__("finish") and interval_relation2.__eq__("before"):
                transfer_confidence = num_confidence * num_confidence2
                transitive_constraint = fact1 + " " + "before" + " " + fact4+"|"+str(transfer_confidence)
                if transfer_confidence > truncate_threshold:
                    if Set_Include(transitive_constraint, Old_Transitive_closure_set) == False:
                        # print("add")
                        # print(constraint, "&", constraint2, "=>", transitive_constraint)
                        transitive_constraint_set.append(transitive_constraint)
        '''
            transfer rules
            a before b, b start c => a before c
            a before b , b include c => a before c
            a include b, a before c => b before c
            a finish b, b before c => a before c
        '''
        small_interval_relations = ["start", "finish"]
        if relation1.__eq__(relation3):
            for interval_relation in small_interval_relations:
                if interval_relation1.__eq__(interval_relation) and interval_relation2.__eq__(interval_relation):
                    transfer_confidence = num_confidence * num_confidence2
                    transitive_constraint = fact1 + " " + interval_relation + " " + fact4+"|"+str(transfer_confidence)
                    if transfer_confidence > truncate_threshold:
                        if Set_Include(transitive_constraint, Old_Transitive_closure_set) == False:
                            # print("add")
                            # print(constraint, "&", constraint2, "=>", transitive_constraint)
                            transitive_constraint_set.append(transitive_constraint)

            if interval_relation1.__eq__("include") and interval_relation2.__eq__("before"):
                transfer_confidence = num_confidence * num_confidence2
                transitive_constraint = fact2 + " " + "before" + " " + fact4+"|"+str(transfer_confidence)
                if transfer_confidence > truncate_threshold:
                    if Set_Include(transitive_constraint, Old_Transitive_closure_set) == False:
                        # print("add")
                        # print(constraint, "&", constraint2, "=>", transitive_constraint)
                        transitive_constraint_set.append(transitive_constraint)

    return transitive_constraint_set

def transitive_closure(Constraint_Set):
    # warshall
    # how to transfer?

    print("before transfering: Constraint number is:",len(Constraint_Set))
    transitive_closure_set=[]
    for i in range(len(Constraint_Set)):
        constraint=Constraint_Set[i]
        constraint=simplify_constraint(constraint)
        transitive_closure_set.append(constraint)
    # print(transitive_closure_set)
    NoEnd = True
    while NoEnd:
        Old_Transitive_closure_set=transitive_closure_set
        for constraint in Old_Transitive_closure_set:
            transitive_closure_set += apply_transfering_rules(constraint,Old_Transitive_closure_set)
        if (len(transitive_closure_set)) == len(Old_Transitive_closure_set):
            NoEnd=False

    print("after transfering: Constraint number is:",len(transitive_closure_set))
    formal_transitive_closure_set=[]
    for i in range(len(transitive_closure_set)):
        constraint=transitive_closure_set[i]
        constraint=formal(constraint)
        formal_transitive_closure_set.append(constraint)
    return formal_transitive_closure_set

def Constraint_Mining(graph):
    '''

    :param utkg:
    :return:
    '''
    Constraint_list = []
    start = time.time()
    Constraint_list += Mutual_Exclusion_mining(graph)
    Constraint_list += functional_mining(graph)
    Constraint_list += inverse_functional_mining(graph)
    pruned_relation=set()
    Constraint_list += Single_Entity_Temporal_Order(graph,pruned_relation)
    Constraint_list += Mutiple_Entity_Temporal_Order(graph,pruned_relation)
    end=time.time()
    print("constraint mining running time is:",end-start,"s")
    print("Constraint_list:")
    for item in Constraint_list:
        print(item)
    # print(Constraint_list)
    return Constraint_list

def single_temporal_span(graph):
    '''
    :param graph:
    :return:
    '''
    '''
    dict={"max":max, "min": min, "0-20": , "20-40": , "40-60": , "60-80"}
    '''
    print("single temporal span mining")
    # we split duration into 10
    Probability_distributions=[]

    for relation in graph.relationList:
        span_list=[]
        for i in graph.eVertexList:

            for j in range(len(graph.eVertexList[i].hasStatement)):
                r = graph.eVertexList[i].hasStatement[j].getId()
                tail1 = graph.eVertexList[i].hasStatement[j].hasValue.getId()
                if relation.__eq__(r):

                    # if relation.__eq__("P286"):
                    #     print(graph.eVertexList[i].hasStatement[j].getEndTime(),graph.eVertexList[i].hasStatement[j].getStartTime())
                    span = graph.eVertexList[i].hasStatement[j].getEndTime() - graph.eVertexList[i].hasStatement[j].getStartTime()
                    span_list.append(span)

        # a naive statistic
        span_list.sort()
        total=len(span_list)
        max=span_list[len(span_list)-1]
        min=span_list[0]
        split=(max-min)/5

        # Divide the duration into five equal parts

        part1=0
        part2=0
        part3=0
        part4=0
        part5=0
        distribution_dict={}
        for i in range(total):
            if span_list[i]< min+0.2*split:
                part1 += 1
            elif span_list[i]<min+0.4*split:
                part2 += 1
            elif span_list[i] < min + 0.6 * split:
                part3 += 1
            elif span_list[i]<min+0.8*split:
                part4 += 1
            else:
                part5 += 1
        distribution_dict={"type":"single","relation":relation,"total":total, "max":max,"min":min,
        "0-20":part1*1.0/total,"20-40":part2*1.0/total,"40-60":part3*1.0/total,"60-80":part4*1.0/total,"80-100":part5*1.0/total}
        # print(distribution_dict)
        Probability_distributions.append(distribution_dict)

    return Probability_distributions


def binary_temporal_span(graph):
    # distance is computed by the start time
    print("binary temporal span mining")
    Probability_distributions = []

    for index in range(len(graph.relationList)-1):
        relation1 = graph.relationList[index]
        for index2 in range(index+1,len(graph.relationList)):
            relation2 = graph.relationList[index2]

            # above we select 2 relations
            span_list=[]
            hasRelation1 = False
            hasRelation2 = False
            for i in graph.eVertexList:
                for j in range(len(graph.eVertexList[i].hasStatement)):
                    r1 = graph.eVertexList[i].hasStatement[j].getId()
                    if relation1.__eq__(r1):
                        hasRelation1 = True
                        start1 = graph.eVertexList[i].hasStatement[j].getStartTime()
                        for k in range(len(graph.eVertexList[i].hasStatement)):
                            r2 = graph.eVertexList[i].hasStatement[k].getId()
                            if relation2.__eq__(r2):
                                hasRelation2 = True
                                start2 = graph.eVertexList[i].hasStatement[k].getStartTime()
                                span = start2 -start1
                                span_list.append(span)

            if hasRelation1 == True and hasRelation2 == True:
                # print("here")
                # a naive statistic
                span_list.sort()
                total = len(span_list)
                max = span_list[len(span_list) - 1]
                min = span_list[0]
                split = (max - min) / 5

                # Divide the duration into five equal parts

                part1 = 0
                part2 = 0
                part3 = 0
                part4 = 0
                part5 = 0
                distribution_dict = {}
                for i in range(total):
                    if span_list[i] < min + 0.2 * split:
                        part1 += 1
                    elif span_list[i] < min + 0.4 * split:
                        part2 += 1
                    elif span_list[i] < min + 0.6 * split:
                        part3 += 1
                    elif span_list[i] < min + 0.8 * split:
                        part4 += 1
                    else:
                        part5 += 1

                distribution_dict = {"type": "binary", "relation1": relation1, "relation2":relation2, "total": total, "max": max, "min": min,
                                 "0-20": part1 * 1.0 / total, "20-40": part2 * 1.0 / total, "40-60": part3 * 1.0 / total,
                                 "60-80": part4 * 1.0 / total, "80-100": part5 * 1.0 / total}
                # print(len(span_list))
                Probability_distributions.append(distribution_dict)

    # print(len(Probability_distributions))
    return Probability_distributions

def Soft_Constraint_Mining(graph):
    print("Soft temporal span mining")
    Soft_Constraint_list=[]
    # print(single_temporal_span(graph))
    print(binary_temporal_span(graph))

    return Soft_Constraint_list

def reformatFile():
    dir="anotation/quality of constraints"
    for root, ds, fs in os.walk(dir):
        for f in fs:
            fullname = os.path.join(root, f)
            file=open(fullname,"r")
            # print(fullname)
            lines= file.readlines()
            newlines=[]
            for line in lines:
                # line=line.replace("   ","\t")
                score=line.split("\t")[0]
                constraint=line.split("\t")[1].split("|")[0]
                fc=formal(constraint)
                line=score+"\t"+fc+"\n"
                newlines.append(line)
            file.close()
            file=open(fullname,"w")
            file.writelines("".join(newlines))
            file.close()

def statisticscount():
    # filename="raw_data/GDELT/train.txt"
    # filename = "raw_data/ICEWS14/train.txt"
    # filename = "raw_data/ICEWS18/train.txt"
    filename="data/GDELT/transed_train.txt"
    filename = "data/ICEWS14/transed_train.txt"
    filename="processed_data/GDELT/transed_train.txt"
    f = open(filename, "r", encoding="utf-8")
    utkg = []
    lines=f.readlines()
    f.close()
    relations=set()
    for line in lines:
        r = line.split("\t")[1]
        relations.add(r)
    print("len of relations is,",len(relations))

def test(filename,knowledgegraph):
    # utkg=read_datasets.read_file("footballdb_tsv/player_team_year_rockit_0.tsv")
    # functional_detection(utkg)
    g = Graph_Structure.Graph()
    # filename="footballdb_tsv/player_team_year_rockit_0.tsv"

    # filename = "WD50K_trans/new_rockit_wikidata_0_50k.tsv"
    # filename = "our_resource/all_relations_with_redundant_wikidata_alpha-1.3.tsv"
    # filename = "our_resource/all_relations_with_redundant_freebase_alpha-1.1.tsv"
    # filename = "processed_data/WIKI/time_merged_train.txt"
    # filename = "processed_data/ICEWS14/time_merged_train.txt"
    # filename = "processed_data/ICEWS18/time_merged_train.txt"
    # filename = "processed_data/GDELT/time_merged_train.txt"
    # filename = "processed_data/YAGO/time_merged_train.txt"
    # read_datasets.pre_process(filename)
    knowledgebase=knowledgegraph
    # filename.__contains__("WIKI") or
    g.ConstructThroughTsv(filename, knowledgebase, 100)

    print("number of entity vertex is ", g.num_eVertices)
    print("number of statement vertex is", g.num_sVertices)
    # print("len(g.relationList):",len(g.relationList))
    # print("g.relationList:",g.relationList)
    print("len(g.temporalRelationList):",len(g.temporalRelationList))
    print("g.temporalRelationList:",g.temporalRelationList)
    print("-------------------")
    # g.iterateOverGraph()

    Constraint_Set = Constraint_Mining(g)
    Simplified_constraint_set = []
    for c in Constraint_Set:
        sc=simplify_constraint(c)
        Simplified_constraint_set.append(sc)

    # Soft_Constraint_Mining(g)
    # transitive_constraint_set = transitive_closure(Constraint_Set)
    # for constraint in transitive_constraint_set:
    #     print(constraint)

    # write rule file
    write_filename = filename.replace("resource","output").replace(".tsv","") + ".rules"
    write_file = open(write_filename, "w", encoding="utf-8")
    write_file.writelines("\n".join(Simplified_constraint_set))
    # write_file.writelines("\n".join(transitive_constraint_set))

    # read rule file for detection
    # read_filename=filename+"_rules"
    # read_file = open(read_filename, "r", encoding="utf-8")
    # lines=read_file.readlines()
    # transitive_constraint_set=[]
    # for line in lines:
    #     constraint=line.strip()
    #     transitive_constraint_set.append(constraint)
    # print("\n".join(transitive_constraint_set))
    # Conflict_Detection.Conflict_Detection(g,transitive_constraint_set)
    return g

if __name__ == '__main__':
    # statisticscount()
    # test()
    # reformatFile()

    parser = argparse.ArgumentParser(description='Constraint Mining')
    parser.add_argument('--dataset', metavar='FILE', default='', help='KG to be mined')
    parser.add_argument('--knowledgegraph', metavar='KG', default='wikidata', help='which type of kg')
    parser.add_argument('--refinement', metavar='Boolean', default="False", help='whether to mine refined constraints')
    parser.add_argument('--typefile', metavar='FILE', default='',
                        help='entity type infomation file needed during refinement')
    parser.add_argument('--support', metavar='Number', type=int, default=100, help='constraint support')
    parser.add_argument('--candidate_confidence', metavar='Number', type=float, default=0.5,
                        help='constraint candidate confidence')
    parser.add_argument('--confidence', metavar='Number', type=float, default=0.9, help='constraint confidence')

    args = parser.parse_args()

    if not os.path.exists(args.dataset):
        print("Error: Invalid dataset %s" % args.dataset)
        exit(-1)

    if args.refinement == "True":
        if not os.path.exists(args.typefile):
            print("Error: Invalid typefile %s" % args.typefile)
            exit(-1)

    filename = args.dataset
    knowledgegraph = args.knowledgegraph
    candidate_threshold = args.candidate_confidence
    confidence_threshold = args.confidence
    support_threshold = args.support
    # pruned_threshold = 0.8 * candidate_threshold
    # pruned_instances = 0.5 * support_threshold
    # relation_prune_threshold = 5 * support_threshold

    tkg = test(filename, knowledgegraph)

    constraint_name = filename.replace("resource", "output").replace(".tsv", "") + ".rules"
    if args.refinement == "True":
        typefile = args.typefile
        Refinement_Mining.test(tkg, filename, constraint_name, typefile, knowledgegraph)

    MergeConstraint(filename)