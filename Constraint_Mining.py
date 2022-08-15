import gc

import read_datasets
import Interval_Relations
import Graph_Structure
import time
import Conflict_Detection
from multiprocessing.dummy import Pool as ThreadPool
import Refinement_Mining

candidate_threshold=0.6
confidence_threshold=0.9
mutual_exclusion_threshold= 0.98
truncate_threshold=0.9
support_threshold=100

def Mutual_Exclusion_mining(graph):
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets

    print("Mutual_Exclusion_mining......")
    st = time.time()
    # output_filename = "functional_conflict.txt"
    # a quick index dict
    index_dict={}
    Mutual_Exclusion_constraint = []

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
                #用一个set把index填进去
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

        # x relation1 y & x relation2 z t1(t1=开始结束时间取平均数) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1
    ed = time.time()
    print("Mutual_Exclusion_Mining time is", ed - st, "s")
    return Mutual_Exclusion_constraint


def functional_mining(graph):
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets

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
                #用一个set把index填进去
        for j in all_relation_pairs.keys():
            # hasRelation=true
            # total subsets+=1
            # if len(all_relation_pairs[j])==1:
            #     continue

            # F_relations_statistics[j][2] += 1
            consistent = True
            negative = False
            for k in range(len(all_relation_pairs[j])):
                vertex1 = all_relation_pairs[j][k]
                flag = True
                for l in range(k + 1, len(all_relation_pairs[j])):
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
                        break

                    if result == 0:
                        consistent = False

                if flag == False:
                    break

            if consistent == True:
                # consistent subsets+=1
                F_relations_statistics[j][1] += 1
            # confidence = positive/positive+negative
                F_relations_statistics[j][2] += 1
            elif negative==True:
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

        # x relation1 y & x relation2 z t1(t1=开始结束时间取平均数) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1
    ed = time.time()
    print("functional_mining time is", ed - st, "s")
    return functional_constraint


def inverse_functional_mining(graph):
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
        # if len(v.bePointedTo)<2:
        #     continue
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
            for k in range(len(all_relation_pairs[j])):
                vertex1 = all_relation_pairs[j][k]
                flag=True
                for l in range(k + 1, len(all_relation_pairs[j])):
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
                        break

                    if result == 0:
                        consistent = False
                if flag==False:
                    break
            if consistent == True:
                # consistent subsets+=1
                IF_relations_statistics[j][1] += 1
                # confidence = positive/positive+negative
                IF_relations_statistics[j][2] += 1
            elif negative == True:
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

        # x relation1 y & x relation2 z t1(t1=开始结束时间取平均数) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1
    ed=time.time()
    print("inverse_functional_mining time is",ed-st,"s")
    return inverse_functional_constraint

def Single_Entity_Temporal_Order(graph):
    # transitivity
    # before include start finish overlap disjoint
    print("Single Entity Temporal Order Mining......")
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
    for i in graph.eVertexList:
        cou+=1
        # print(cou)
        vertex_count += 1
        if vertex_count % 1000000 == 0:
            ed = time.time()
            print("have traversed nodes:", vertex_count)
            print("time cost:", ed - pre, "s")

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
            for j in range(len(v.hasStatement)):
                s1 = v.hasStatement[j]
                start1 = s1.getStartTime()
                end1 = s1.getEndTime()
                if start1 != -1 or end1 != -1:
                    for k in range(j+1,len(v.hasStatement)):
                            s2 = v.hasStatement[k]
                            if s1.getId().__eq__(s2.getId()):
                                continue
                            start2 = s2.getStartTime()
                            end2 = s2.getEndTime()
                            if start2 != -1 or end2 != -1:
                                key1=s1.getId()+"*"+s2.getId()
                                key2=s2.getId()+"*"+s1.getId()
                                index1=index_dict[key1]
                                index2=index_dict[key2]
                                all_relation_pairs.setdefault(index1, []).append(s1)
                                all_relation_pairs.setdefault(index1, []).append(s2)
                                all_relation_pairs.setdefault(index2, []).append(s2)
                                all_relation_pairs.setdefault(index2, []).append(s1)
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
                    result1=Interval_Relations.before(start1, end1, start2, end2)
                    result2=Interval_Relations.include(start1, end1, start2, end2)
                    result3=Interval_Relations.start(start1, end1, start2, end2)
                    result4=Interval_Relations.finish(start1, end1, start2, end2)
                    if result1== -1:
                        before_consistent=False
                        before_negative=True
                        flag1=False
                    elif result1==0:
                        before_consistent=False

                    if result2 == -1:
                        include_consistent = False
                        include_negative = True
                        flag2 = False
                    elif result2 == 0:
                        include_consistent = False

                    if result3 == -1:
                        start_consistent = False
                        start_negative = True
                        flag3 = False
                    elif result3 == 0:
                        start_consistent = False

                    if result4 == -1:
                        finish_consistent = False
                        finish_negative = True
                        flag4 = False
                    elif result4 == 0:
                        finish_consistent = False

                    # 1
                    # if before_consistent==False and include_consistent==False and start_consistent==False and finish_consistent==False:
                    #     break
                    if flag1==False and flag2==False and flag3==False and flag4==False:
                        break
                if before_consistent==True:
                    #before_consistent_subsets += 1
                    ZH_relations_statistics[j][2]+=1
                    # confidence = positive/positive+negative
                    ZH_relations_statistics[j][6] += 1
                elif before_negative == True:
                    ZH_relations_statistics[j][6] += 1

                if include_consistent==True:
                    #include_consistent_subsets +=1
                    ZH_relations_statistics[j][3] += 1
                    # confidence = positive/positive+negative
                    ZH_relations_statistics[j][7] += 1
                elif include_negative == True:
                    ZH_relations_statistics[j][7] += 1

                if start_consistent==True:
                    #start_consistent_subsets +=1
                    ZH_relations_statistics[j][4] += 1
                    # confidence = positive/positive+negative
                    ZH_relations_statistics[j][8] += 1
                elif start_negative == True:
                    ZH_relations_statistics[j][8] += 1

                if finish_consistent==True:
                    #finish_consistent_subsets +=1
                    ZH_relations_statistics[j][5] += 1
                    # confidence = positive/positive+negative
                    ZH_relations_statistics[j][9] += 1
                elif finish_negative == True:
                    ZH_relations_statistics[j][9] += 1
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

        # 1
        # if total_subsets == 0:
        #     before_confidence = 0
        #     include_confidence = 0
        #     start_confidence = 0
        #     finish_confidence = 0
        # else:
        #     before_confidence = before_consistent_subsets * 1.0 / total_subsets
        #     include_confidence = include_consistent_subsets * 1.0 / total_subsets
        #     start_confidence = start_consistent_subsets * 1.0 / total_subsets
        #     finish_confidence = finish_consistent_subsets * 1.0 / total_subsets

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
            start_confidence = before_consistent_subsets * 1.0 / start_total_subsets
        if finish_total_subsets == 0:
            finish_confidence = 0
        else:
            finish_confidence = before_consistent_subsets * 1.0 / finish_total_subsets

        if before_consistent_subsets != 0:
            print("before relation", relation1, relation2, before_consistent_subsets, before_total_subsets, before_confidence)
        if include_consistent_subsets != 0:
            print("include relation", relation1, relation2, include_consistent_subsets, include_total_subsets, include_confidence)
        if start_consistent_subsets != 0:
            print("start relation", relation1, relation2, start_consistent_subsets, start_total_subsets, start_confidence)
        if finish_consistent_subsets != 0:
            print("finish relation", relation1, relation2, finish_consistent_subsets, finish_total_subsets, finish_confidence)

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
    ed=time.time()
    print("Single Entity Temporal Order Mining time is",ed-st,"s")
    return Single_Entity_Temporal_Order_Constraint

def Mutiple_Entity_Temporal_Order(graph):
    print("Mutiple Entity Temporal Order Mining......")
    st = time.time()
    Mutiple_Entity_Temporal_Order_Constraint = []
    index_dict = {}
    OH_relations = []
    OH_relations_statistics = []
    cou = 0
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
            for j in range(len(v.hasStatement)):
                s1 = v.hasStatement[j]
                start1 = s1.getStartTime()
                end1 = s1.getEndTime()
                if start1 != -1 or end1 != -1:
                    for k in range(len(v.hasStatement)):
                        if j==k:
                            continue
                        s2 = v.hasStatement[k]
                        if s1.getId().__eq__(s2.getId()):
                            continue
                        for l in range(len(s2.hasValue.hasStatement)):
                            s3=s2.hasValue.hasStatement[l]
                            if s2.getId().__eq__(s3.getId()):
                                continue
                            start2 = s3.getStartTime()
                            end2 = s3.getEndTime()
                            if start2 != -1 or end2 != -1:
                                key1 = s1.getId() + "*" + s2.getId()+"*"+s3.getId()
                                index1 = index_dict[key1]
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
                    elif result1==0:
                        before_consistent=False

                    if  result2== -1:
                        inverse_before_consistent = False
                        inverse_before_negative = True
                        flag2 = False
                    elif result2 == 0:
                        inverse_before_consistent = False

                    if  result3== -1:
                        include_consistent = False
                        include_negative = True
                        flag3 = False
                    elif result3 == 0:
                        include_consistent = False

                    if  result4== -1:
                        inverse_include_consistent = False
                        inverse_include_negative = True
                        flag4 = False
                    elif result4 == 0:
                        inverse_include_consistent = False

                    if  result5== -1:
                        start_consistent = False
                        start_negative = True
                        flag5 = False
                    elif result5 == 0:
                        start_consistent = False

                    if  result6== -1:
                        finish_consistent = False
                        finish_negative = True
                        flag6 = False
                    elif result6 == 0:
                        finish_consistent = False

                    # if before_consistent==False and inverse_before_consistent==False and include_consistent==False \
                    #         and inverse_include_consistent==False and start_consistent==False and finish_consistent==False:
                    #     break
                    if flag1==False and flag2==False and flag3==False and flag4==False and flag5==False and flag6==False:
                        break
                if before_consistent == True:
                    # before_consistent_subsets += 1
                    OH_relations_statistics[j][3] += 1
                    # confidence = positive/positive+negative
                    OH_relations_statistics[j][9] += 1
                elif before_negative == True:
                    OH_relations_statistics[j][9] += 1

                if inverse_before_consistent == True:
                    # inverse_before_consistent_subsets +=1
                    OH_relations_statistics[j][4] += 1
                    # confidence = positive/positive+negative
                    OH_relations_statistics[j][10] += 1
                elif inverse_before_negative == True:
                    OH_relations_statistics[j][10] += 1

                if include_consistent == True:
                    # include_consistent_subsets +=1
                    OH_relations_statistics[j][5] += 1
                    # confidence = positive/positive+negative
                    OH_relations_statistics[j][11] += 1
                elif include_negative == True:
                    OH_relations_statistics[j][11] += 1

                if inverse_include_consistent == True:
                    # inverse_include_consistent_subsets +=1
                    OH_relations_statistics[j][6] += 1
                    # confidence = positive/positive+negative
                    OH_relations_statistics[j][12] += 1
                elif inverse_include_negative == True:
                    OH_relations_statistics[j][12] += 1

                if start_consistent == True:
                    # start_consistent_subsets +=1
                    OH_relations_statistics[j][7] += 1
                    # confidence = positive/positive+negative
                    OH_relations_statistics[j][13] += 1
                elif start_negative == True:
                    OH_relations_statistics[j][13] += 1

                if finish_consistent == True:
                    # finish_consistent_subsets +=1
                    OH_relations_statistics[j][8] += 1
                    # confidence = positive/positive+negative
                    OH_relations_statistics[j][14] += 1
                elif finish_negative == True:
                    OH_relations_statistics[j][14] += 1
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
            start_confidence = before_consistent_subsets * 1.0 / start_total_subsets
        if finish_total_subsets == 0:
            finish_confidence = 0
        else:
            finish_confidence = before_consistent_subsets * 1.0 / finish_total_subsets

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
        if before_consistent_subsets != 0:
            print("before relation", relation1, one_hop, relation2, before_consistent_subsets, before_total_subsets, before_confidence)
        if inverse_before_consistent_subsets != 0:
            print("inverse before relation", relation1, one_hop, relation2, inverse_before_consistent_subsets, inverse_before_total_subsets, inverse_before_confidence)
        if include_consistent_subsets != 0:
            print("include relation", relation1, one_hop, relation2, include_consistent_subsets, include_total_subsets,include_confidence)
        if inverse_include_consistent_subsets != 0:
            print("inverse include relation", relation1, one_hop, relation2, inverse_include_consistent_subsets, inverse_include_total_subsets, inverse_include_confidence)
        if start_consistent_subsets != 0:
            print("start relation", relation1, one_hop, relation2, start_consistent_subsets, start_total_subsets, start_confidence)
        if finish_consistent_subsets != 0:
            print("finish relation", relation1, one_hop, relation2, finish_consistent_subsets, finish_total_subsets,finish_confidence)

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

    ed=time.time()
    print("Mutiple Entity Temporal Order Mining time is",ed-st,"s")
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
    constraint = constraint.replace("=>", ">")

    body = constraint.split(">")[0]
    head = constraint.split(">")[1]
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

    variable_list=[]

    fact1 = simple_constraint.split(" ")[0]
    relation1 = fact1.split(",")[1]
    interval_relation1 = simple_constraint.split(" ")[1]
    fact2 = simple_constraint.split(" ")[2]
    relation2 = fact2.split(",")[1]
    '''
    a,father*P569,d,t5,t6 before a,P26*P54,d,t5,t6
    =>
    (a,father,b,t1,t2) & (b,P569,c,t3,t4) & (a,P26,d,t5,t6) & (d,P54,e,t7,t8) => before(t3,t4,t7,t8)
    '''

    return simple_constraint

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
    Constraint_list += Single_Entity_Temporal_Order(graph)
    Constraint_list += Mutiple_Entity_Temporal_Order(graph)
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



def test():
    # utkg=read_datasets.read_file("footballdb_tsv/player_team_year_rockit_0.tsv")
    # functional_detection(utkg)
    g = Graph_Structure.Graph()
    # filename="footballdb_tsv/player_team_year_rockit_0.tsv"

    # filename = "wikidata_dataset_tsv/rockit_wikidata_0_50k.tsv"
    filename = "all_relations_with_redundant_wikidata_alpha-1.3.tsv"
    # filename = "all_relations_with_redundant_freebase_alpha-1.1.tsv"
    # read_datasets.pre_process(filename)
    g.ConstructThroughTsv(filename, "wikidata",100)
    # g.ConstructThroughTsv(filename, "freebase", 100)

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
    write_filename = filename + "_rules"
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

if __name__ == '__main__':
    test()