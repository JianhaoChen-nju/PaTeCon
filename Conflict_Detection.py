import copy
import time

import read_datasets
import Constraint_Mining
import Interval_Relations
import Graph_Structure

'''
functional
(a," + relation + ",b,t1,t2) & (a,"+relation+",c,t3,t4) => disjoint(t1,t2,t3,t4)
inverse_functional
(a," + relation + ",b,t1,t2) & (c," + relation + ",b,t3,t4) => disjoint(t1,t2,t3,t4)
single_before
(a," + relation1 + ",b,t1,t2) & (a," + relation2 + ",c,t3,t4) => before(t1,t2,t3,t4)
single_include
(a," + relation1 + ",b,t1,t2) & (a," + relation2 + ",c,t3,t4) => include(t1,t2,t3,t4)
single_temporal_span


binary_temporal_span
distribution_dict = {"type": "binary", "relation1": relation1, "relation2":relation2, "total": total, "max": max, "min": min,
                                 "0-20": part1 * 1.0 / total, "20-40": part2 * 1.0 / total, "40-60": part3 * 1.0 / total,
                                 "60-80": part4 * 1.0 / total, "80-100": part5 * 1.0 / total}
'''

Constraint_Set=["(a,P569,b,t1,t2) & (a,P569,c,t3,t4) => disjoint(t1,t2,t3,t4)",\
                "(a,P26,b,t1,t2) & (a,P26,c,t3,t4) => disjoint(t1,t2,t3,t4)",\
                "(a,P570,b,t1,t2) & (a,P570,c,t3,t4) => disjoint(t1,t2,t3,t4)",\
"(a,P108,b,t1,t2) & (a,P108,c,t3,t4) => disjoint(t1,t2,t3,t4)",\
"(a,P286,b,t1,t2) & (a,P286,c,t3,t4) => disjoint(t1,t2,t3,t4)",\
"(a,P570,b,t1,t2) & (c,P570,b,t3,t4) => disjoint(t1,t2,t3,t4)",\
"(a,P108,b,t1,t2) & (c,P108,b,t3,t4) => disjoint(t1,t2,t3,t4)",\
"(a,P286,b,t1,t2) & (c,P286,b,t3,t4) => disjoint(t1,t2,t3,t4)",\
"(a,P54,b,t1,t2) & (a,P570,c,t3,t4) => before(t1,t2,t3,t4)",\
"(a,P569,b,t1,t2) & (a,P54,c,t3,t4) => before(t1,t2,t3,t4)",\
"(a,P569,b,t1,t2) & (a,P26,c,t3,t4) => before(t1,t2,t3,t4)",\
"(a,P569,b,t1,t2) & (a,P570,c,t3,t4) => before(t1,t2,t3,t4)",\
"(a,P569,b,t1,t2) & (a,P108,c,t3,t4) => before(t1,t2,t3,t4)",\
"(a,P26,b,t1,t2) & (a,P570,c,t3,t4) => before(t1,t2,t3,t4)",\
"(a,P108,b,t1,t2) & (a,P570,c,t3,t4) => before(t1,t2,t3,t4)",\
"(a,P54,b,t1,t2) & (a,P26,c,t3,t4) & (c,P569,d,t5,t6) => before(t5,t6,t1,t2)",\
"(a,P569,b,t1,t2) & (a,P26,c,t3,t4) & (c,P54,d,t5,t6) => before(t1,t2,t5,t6)",\
"(a,P569,b,t1,t2) & (a,P26,c,t3,t4) & (c,P570,d,t5,t6) => before(t1,t2,t5,t6)",\
"(a,P569,b,t1,t2) & (a,P26,c,t3,t4) & (c,P108,d,t5,t6) => before(t1,t2,t5,t6)",\
"(a,P569,b,t1,t2) & (a,father,c,t3,t4) & (c,P569,d,t5,t6) => before(t5,t6,t1,t2)",\
"(a,P26,b,t1,t2) & (a,father,c,t3,t4) & (c,P569,d,t5,t6) => before(t5,t6,t1,t2)",\
"(a,P570,b,t1,t2) & (a,P26,c,t3,t4) & (c,P569,d,t5,t6) => before(t5,t6,t1,t2)",\
"(a,P570,b,t1,t2) & (a,father,c,t3,t4) & (c,P569,d,t5,t6) => before(t5,t6,t1,t2)",\
"(a,P108,b,t1,t2) & (a,P26,c,t3,t4) & (c,P569,d,t5,t6) => before(t5,t6,t1,t2)"]

def Compound(atom):
    return



def Subgraph_Detection0(temporal_KG,Constraint_Set):

    '''
    translate and execute constraint
    :param Conflict_temporal_facts:
    :param constraint:
    :return:
    '''
    # TODO
    # simplify_constraint()
    Conflict_Fact_set=[]
    # functional constraints detection
    functional_constraints = Constraint_Set
    FC_relations = []
    for c in functional_constraints:
        FC_relation = c.split(" ")[0].split(",")[1]
        FC_relations.append(FC_relation)
    for i in temporal_KG.eVertexList:
        v = temporal_KG.eVertexList[i]
        if len(v.hasStatement) < 2:
            continue
        else:
            exist = False
            all_relation_pairs=[]
            for r in FC_relations:
                pairs=[r]
                all_relation_pairs.append(pairs)
            # print(len(all_relation_pairs[0]))
            for s in v.hasStatement:
                for index in range(len(FC_relations)):
                    if s.getId().__eq__(FC_relations[index]):
                        exist=True
                        all_relation_pairs[index].append(s)
                        #[[P54,e,e,e],[P286,e,e,e]]

            if exist==True:
                for j in range(len(all_relation_pairs)):
                    if len(all_relation_pairs[j])>2:
                        for k in range(1,len(all_relation_pairs[j])):
                            vertex1=all_relation_pairs[j][k]
                            for l in range(k+1,len(all_relation_pairs[j])):
                                vertex2 = all_relation_pairs[j][l]
                                start1 = vertex1.getStartTime()
                                end1 = vertex1.getEndTime()
                                start2 = vertex2.getStartTime()
                                end2 = vertex2.getEndTime()
                                head = v.getId()
                                relation1 = vertex1.getId()
                                tail1 = vertex1.hasValue.getId()
                                relation2 = vertex2.getId()
                                tail2 = vertex2.hasValue.getId()


                                if Interval_Relations.disjoint(start1, end1, start2, end2) == -1:
                                        inconsistent_pair = functional_constraints[j] + "\t" + head + "," + relation1 + "," + tail1 + "," + str(
                                            start1) + "," + str(
                                            end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                            start2) + "," + str(end2)
                                        Conflict_Fact_set.append(inconsistent_pair)

    return Conflict_Fact_set

def Subgraph_Detection1(temporal_KG,Constraint_Set):

    '''
    translate and execute constraint
    :param Conflict_temporal_facts:
    :param constraint:
    :return:
    '''
    # TODO
    # simplify_constraint()
    Conflict_Fact_set=[]
    # inverse functional constraints detection
    inverse_functional_constraints = Constraint_Set
    IFC_relations = []
    for c in inverse_functional_constraints:
        IFC_relation = c.split(" ")[0].split(",")[1]
        IFC_relations.append(IFC_relation)
    for i in temporal_KG.eVertexList:
        v = temporal_KG.eVertexList[i]
        if len(v.bePointedTo) < 2:
            continue
        else:
            exist = False
            all_relation_pairs=[]
            for r in IFC_relations:
                pairs=[r]
                all_relation_pairs.append(pairs)
            # print(IFC_relations[1])
            for s in v.bePointedTo:
                for index in range(len(IFC_relations)):
                    if s.getId().__eq__(IFC_relations[index]):
                        exist=True
                        all_relation_pairs[index].append(s)
                        #[[P54,e,e,e],[P286,e,e,e]]

            if exist==True:
                for j in range(len(all_relation_pairs)):
                    if len(all_relation_pairs[j])>2:
                        for k in range(1,len(all_relation_pairs[j])):
                            vertex1=all_relation_pairs[j][k]
                            for l in range(k+1,len(all_relation_pairs[j])):
                                vertex2 = all_relation_pairs[j][l]
                                start1 = vertex1.getStartTime()
                                end1 = vertex1.getEndTime()
                                start2 = vertex2.getStartTime()
                                end2 = vertex2.getEndTime()
                                tail = v.getId()
                                relation1 = vertex1.getId()
                                head1 = vertex1.hasItem.getId()
                                relation2 = vertex2.getId()
                                head2 = vertex2.hasItem.getId()


                                if Interval_Relations.disjoint(start1, end1, start2, end2) == -1:
                                        inconsistent_pair = inverse_functional_constraints[j] + "\t" + head1 + "," + relation1 + "," + tail + "," + str(
                                            start1) + "," + str(
                                            end1) + "\t" + head2 + "," + relation2 + "," + tail + "," + str(
                                            start2) + "," + str(end2)
                                        Conflict_Fact_set.append(inconsistent_pair)

    return Conflict_Fact_set

def Subgraph_Detection2(temporal_KG,Constraint_Set):

    '''
    translate and execute constraint
    :param Conflict_temporal_facts:
    :param constraint:
    :return:
    '''
    # TODO
    # simplify_constraint()
    Conflict_Fact_set=[]
    # functional constraints detection
    zero_hop_constraints = Constraint_Set
    ZHC_relations = []
    for c in zero_hop_constraints:
        ZHC_relation1 = c.split(" ")[0].split(",")[1]
        ZHC_relation2 = c.split(" ")[2].split(",")[1]
        ZHC_interval_relation=c.split(" ")[1]
        relation_pair=[ZHC_relation1,ZHC_relation2,ZHC_interval_relation]
        ZHC_relations.append(relation_pair)
        #[[P54,P569,before],[P54,P570,before]]
    all_relations=set()
    # print(ZHC_relations)
    for p in ZHC_relations:
        all_relations.add(p[0])
        all_relations.add(p[1])
    print(all_relations)
    # cou=0
    for i in temporal_KG.eVertexList:
        # cou+=1
        # print(cou)
        v = temporal_KG.eVertexList[i]
        if len(v.hasStatement) < 2:
            continue
        else:
            exist = False
            all_relation_pairs=[]
            for p in ZHC_relations:
                pair=[p[0],p[1],p[2]]
                all_relation_pairs.append(pair)

            # a quick prune
            filter_count=0
            for j in range(len(v.hasStatement)):
                s=v.hasStatement[j]
                if all_relations.__contains__(s.getId()):
                    filter_count+=1
            if filter_count<2:
                continue

            for j in range(len(v.hasStatement)):
                s1=v.hasStatement[j]
                # a quick filtering
                if not all_relations.__contains__(s1.getId()):
                    continue
                for k in range(j+1,len(v.hasStatement)):
                    s2=v.hasStatement[k]
                    # a quick filtering
                    if not all_relations.__contains__(s2.getId()):
                        continue
                    for index in range(len(ZHC_relations)):
                        r1=ZHC_relations[index][0]
                        r2=ZHC_relations[index][1]
                        if s1.getId().__eq__(r1) and s2.getId().__eq__(r2):
                            all_relation_pairs[index].append(s1)
                            all_relation_pairs[index].append(s2)
                            #[[P54,P569,before,e,e]]
                            exist=True
                        elif s1.getId().__eq__(r2) and s2.getId().__eq__(r1):
                            all_relation_pairs[index].append(s2)
                            all_relation_pairs[index].append(s1)
                            # [[P54,P569,before,e,e]]
                            exist = True
            # print(all_relation_pairs)
            if exist==True:
                for j in range(len(all_relation_pairs)):
                    if len(all_relation_pairs[j])>3:
                        # step=2
                        for k in range(3,len(all_relation_pairs[j]),2):
                            # print(len(all_relation_pairs[j]))
                            vertex1 = all_relation_pairs[j][k]
                            vertex2 = all_relation_pairs[j][k+1]
                            start1 = vertex1.getStartTime()
                            end1 = vertex1.getEndTime()
                            start2 = vertex2.getStartTime()
                            end2 = vertex2.getEndTime()
                            head = v.getId()
                            relation1 = vertex1.getId()
                            tail1 = vertex1.hasValue.getId()
                            relation2 = vertex2.getId()
                            tail2 = vertex2.hasValue.getId()

                            # choose which interval relation is
                            if ZHC_relations[j][2].__eq__("before"):
                                if Interval_Relations.before(start1,end1,start2,end2)==-1:
                                    inconsistent_pair = zero_hop_constraints[j]+"\t"+head + "," + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif ZHC_relations[j][2].__eq__("include"):
                                if Interval_Relations.include(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = zero_hop_constraints[j]+"\t"+head + "," + relation1 + "," + tail1 + "," + str(
                                        start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif ZHC_relations[j][2].__eq__("start"):
                                if Interval_Relations.start(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = zero_hop_constraints[j]+"\t"+head + "," + relation1 + "," + tail1 + "," + str(
                                        start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif ZHC_relations[j][2].__eq__("finish"):
                                if Interval_Relations.finish(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = zero_hop_constraints[j]+"\t"+head + "," + relation1 + "," + tail1 + "," + str(
                                        start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)

    return Conflict_Fact_set

def Subgraph_Detection3(temporal_KG,Constraint_Set):

    '''
    translate and execute constraint
    :param Conflict_temporal_facts:
    :param constraint:
    :return:
    '''
    # TODO
    # simplify_constraint()
    Conflict_Fact_set=[]
    # functional constraints detection
    first_one_hop_constraints = Constraint_Set
    FOH_relations = []
    for c in first_one_hop_constraints:
        FOH_relation0 = c.split(" ")[0].split(",")[1].split("*")[0]
        FOH_relation1 = c.split(" ")[0].split(",")[1].split("*")[1]
        FOH_relation2 = c.split(" ")[2].split(",")[1]
        FOH_interval_relation=c.split(" ")[1]
        relation_pair=[FOH_relation0,FOH_relation1,FOH_relation2,FOH_interval_relation]
        FOH_relations.append(relation_pair)
        #[[P54,P26,P569,before],[P54,P570,before]]
    first_relations=set()
    second_relations=set()
    for p in FOH_relations:
        first_relations.add(p[0])
        first_relations.add(p[2])

    for p in FOH_relations:
        second_relations.add(p[1])

    for i in temporal_KG.eVertexList:
        v = temporal_KG.eVertexList[i]
        if len(v.hasStatement) < 2:
            continue
        else:
            exist = False
            all_relation_pairs=[]
            for p in FOH_relations:
                pair = [p[0], p[1], p[2],p[3]]
                all_relation_pairs.append(pair)

            # a quick prune
            filter_count = 0
            for j in range(len(v.hasStatement)):
                s = v.hasStatement[j]
                if first_relations.__contains__(s.getId()):
                    filter_count += 1
            if filter_count < 2:
                continue

            for j in range(len(v.hasStatement)):
                s1=v.hasStatement[j]
                # a quick filtering
                if not first_relations.__contains__(s1.getId()):
                    continue

                # prune again
                hasOneHopRelation=False
                # search for one hop
                for l in s1.hasValue.hasStatement:
                    if not second_relations.__contains__(l.getId()):
                        continue
                    hasOneHopRelation=True

                if hasOneHopRelation==False:
                    continue

                for l in s1.hasValue.hasStatement:
                    if not second_relations.__contains__(l.getId()):
                        continue

                    for k in range(len(v.hasStatement)):
                        s2=v.hasStatement[k]
                        #two node cannot equal
                        if j==k:
                            continue

                        # a quick filtering
                        if not first_relations.__contains__(s2.getId()):
                            continue
                        for index in range(len(FOH_relations)):
                            r0=FOH_relations[index][0]
                            r1=FOH_relations[index][1]
                            r2=FOH_relations[index][2]
                            if s1.getId().__eq__(r0) and l.getId().__eq__(r1) and s2.getId().__eq__(r2):
                                all_relation_pairs[index].append(l)
                                all_relation_pairs[index].append(s2)
                                #[[P26,P569,P54,before,e,e]]
                                exist=True

            if exist==True:
                print("yes")
                for j in range(len(all_relation_pairs)):
                    if len(all_relation_pairs[j])>4:
                        # step=2
                        for k in range(4,len(all_relation_pairs[j]),2):
                            vertex1 = all_relation_pairs[j][k]
                            vertex2 = all_relation_pairs[j][k+1]
                            start1 = vertex1.getStartTime()
                            end1 = vertex1.getEndTime()
                            start2 = vertex2.getStartTime()
                            end2 = vertex2.getEndTime()
                            head = v.getId()
                            relation=all_relation_pairs[j][0]
                            relation1 = vertex1.getId()
                            tail1 = vertex1.hasValue.getId()
                            relation2 = vertex2.getId()
                            tail2 = vertex2.hasValue.getId()

                            # choose which interval relation is
                            if FOH_relations[j][3].__eq__("before"):
                                if Interval_Relations.before(start1,end1,start2,end2)==-1:
                                    inconsistent_pair = first_one_hop_constraints[j]+"\t"+head + ","+ relation+",entity,"\
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif FOH_relations[j][3].__eq__("include"):
                                if Interval_Relations.include(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = first_one_hop_constraints[
                                                            j] + "\t" + head + "," + relation + ",entity," \
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif FOH_relations[j][3].__eq__("start"):
                                if Interval_Relations.start(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = first_one_hop_constraints[
                                                            j] + "\t" + head + "," + relation + ",entity," \
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif FOH_relations[j][3].__eq__("finish"):
                                if Interval_Relations.finish(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = first_one_hop_constraints[
                                                            j] + "\t" + head + "," + relation + ",entity," \
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)

    return Conflict_Fact_set

def Subgraph_Detection4(temporal_KG,Constraint_Set):

    '''
    translate and execute constraint
    :param Conflict_temporal_facts:
    :param constraint:
    :return:
    '''
    # TODO
    # simplify_constraint()
    Conflict_Fact_set=[]
    # functional constraints detection
    second_one_hop_constraints = Constraint_Set
    SOH_relations = []
    for c in second_one_hop_constraints:
        SOH_relation0 = c.split(" ")[0].split(",")[1]
        SOH_relation1 = c.split(" ")[2].split(",")[1].split("*")[0]
        SOH_relation2 = c.split(" ")[2].split(",")[1].split("*")[1]
        SOH_interval_relation=c.split(" ")[1]
        relation_pair=[SOH_relation0,SOH_relation1,SOH_relation2,SOH_interval_relation]
        SOH_relations.append(relation_pair)
        #[[P54,P569,before],[P54,P570,before]]
    first_relations=set()
    second_relations=set()
    for p in SOH_relations:
        first_relations.add(p[0])
        first_relations.add(p[1])

    for p in SOH_relations:
        second_relations.add(p[2])

    for i in temporal_KG.eVertexList:
        v = temporal_KG.eVertexList[i]
        if len(v.hasStatement) < 2:
            continue
        else:
            exist = False
            all_relation_pairs=[]
            for p in SOH_relations:
                pair = [p[0], p[1], p[2],p[3]]
                all_relation_pairs.append(pair)

            # a quick prune
            filter_count = 0
            for j in range(len(v.hasStatement)):
                s = v.hasStatement[j]
                if first_relations.__contains__(s.getId()):
                    filter_count += 1
            if filter_count < 2:
                continue

            for j in range(len(v.hasStatement)):
                s1=v.hasStatement[j]
                # a quick filtering
                if not first_relations.__contains__(s1.getId()):
                    continue

                # prune again
                hasOneHopRelation=False
                # search for one hop
                for l in s1.hasValue.hasStatement:
                    if not second_relations.__contains__(l.getId()):
                        continue
                    hasOneHopRelation=True

                if hasOneHopRelation==False:
                    continue

                for l in s1.hasValue.hasStatement:
                    if not second_relations.__contains__(l.getId()):
                        continue

                    for k in range(len(v.hasStatement)):
                        s2=v.hasStatement[k]
                        #two node cannot equal
                        if j==k:
                            continue

                        # a quick filtering
                        if not first_relations.__contains__(s2.getId()):
                            continue
                        for index in range(len(SOH_relations)):
                            r0=SOH_relations[index][0]
                            r1=SOH_relations[index][1]
                            r2=SOH_relations[index][2]
                            if s1.getId().__eq__(r1) and l.getId().__eq__(r2) and s2.getId().__eq__(r0):
                                all_relation_pairs[index].append(s2)
                                all_relation_pairs[index].append(l)
                                #[[P26,P569,P54,before,e,e]]
                                exist=True

            if exist==True:
                print("yes")
                for j in range(len(all_relation_pairs)):
                    if len(all_relation_pairs[j])>4:
                        # step=2
                        for k in range(4,len(all_relation_pairs[j]),2):
                            vertex1 = all_relation_pairs[j][k]
                            vertex2 = all_relation_pairs[j][k+1]
                            start1 = vertex1.getStartTime()
                            end1 = vertex1.getEndTime()
                            start2 = vertex2.getStartTime()
                            end2 = vertex2.getEndTime()
                            head = v.getId()
                            relation=all_relation_pairs[j][1]
                            relation1 = vertex1.getId()
                            tail1 = vertex1.hasValue.getId()
                            relation2 = vertex2.getId()
                            tail2 = vertex2.hasValue.getId()

                            # choose which interval relation is
                            if SOH_relations[j][3].__eq__("before"):
                                if Interval_Relations.before(start1,end1,start2,end2)==-1:
                                    inconsistent_pair = second_one_hop_constraints[j]+"\t"+head+"," \
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head  + ","+ relation+",entity,"+ relation2 + "," + tail2 + "," + str(start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif SOH_relations[j][3].__eq__("include"):
                                if Interval_Relations.include(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = second_one_hop_constraints[j] + "\t" + head+"," \
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + "," + relation + ",entity,"+ relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif SOH_relations[j][3].__eq__("start"):
                                if Interval_Relations.start(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = second_one_hop_constraints[j] + "\t" + head+"," \
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + "," + relation + ",entity,"+ relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif SOH_relations[j][3].__eq__("finish"):
                                if Interval_Relations.finish(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = second_one_hop_constraints[j] + "\t" + head+"," \
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + "," + relation + ",entity,"+ relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)

    return Conflict_Fact_set

def Subgraph_Detection5(temporal_KG,Constraint_Set):

    '''
    translate and execute constraint
    :param Conflict_temporal_facts:
    :param constraint:
    :return:
    '''
    # TODO
    # simplify_constraint()
    Conflict_Fact_set=[]
    # functional constraints detection
    both_one_hop_constraints = Constraint_Set
    BOH_relations = []
    for c in both_one_hop_constraints:
        SOH_relation = c.split(" ")[0].split(",")[1].split("*")[0]
        SOH_relation0 = c.split(" ")[0].split(",")[1].split("*")[1]
        SOH_relation1 = c.split(" ")[2].split(",")[1].split("*")[0]
        SOH_relation2 = c.split(" ")[2].split(",")[1].split("*")[1]
        SOH_interval_relation=c.split(" ")[1]
        relation_pair=[SOH_relation,SOH_relation0,SOH_relation1,SOH_relation2,SOH_interval_relation]
        BOH_relations.append(relation_pair)
        #[[P54,P569,before],[P54,P570,before]]
    first_relations=set()
    second_relations=set()
    for p in BOH_relations:
        first_relations.add(p[0])
        first_relations.add(p[2])

    for p in BOH_relations:
        second_relations.add(p[1])
        second_relations.add(p[3])

    for i in temporal_KG.eVertexList:
        v = temporal_KG.eVertexList[i]
        if len(v.hasStatement) < 2:
            continue
        else:
            exist = False
            all_relation_pairs=[]
            for p in BOH_relations:
                pair = [p[0], p[1], p[2],p[3],p[4]]
                all_relation_pairs.append(pair)

            # a quick prune
            filter_count = 0
            for j in range(len(v.hasStatement)):
                s = v.hasStatement[j]
                if first_relations.__contains__(s.getId()):
                    filter_count += 1
            if filter_count < 2:
                continue

            for j in range(len(v.hasStatement)):
                s1=v.hasStatement[j]
                # a quick filtering
                if not first_relations.__contains__(s1.getId()):
                    continue

                # prune again
                hasOneHopRelation=False
                # search for one hop
                for l in s1.hasValue.hasStatement:
                    if not second_relations.__contains__(l.getId()):
                        continue
                    hasOneHopRelation=True

                if hasOneHopRelation==False:
                    continue

                for l in s1.hasValue.hasStatement:
                    if not second_relations.__contains__(l.getId()):
                        continue

                    for k in range(j+1,len(v.hasStatement)):
                        s2=v.hasStatement[k]
                        # a quick filtering
                        if not first_relations.__contains__(s2.getId()):
                            continue
                        for m in s2.hasValue.hasStatement:
                            if not second_relations.__contains__(m.getId()):
                                continue

                            for index in range(len(BOH_relations)):
                                r0=BOH_relations[index][0]
                                r1=BOH_relations[index][1]
                                r2=BOH_relations[index][2]
                                r3=BOH_relations[index][3]
                                if s1.getId().__eq__(r0) and l.getId().__eq__(r1) and s2.getId().__eq__(r2) and m.getId().__eq__(r3):
                                    all_relation_pairs[index].append(l)
                                    all_relation_pairs[index].append(m)
                                    #[[P26,P569,P54,before,e,e]]
                                    exist=True

                                elif s1.getId().__eq__(r2) and l.getId().__eq__(r3) and s2.getId().__eq__(r0) and m.getId().__eq__(r1):
                                    all_relation_pairs[index].append(m)
                                    all_relation_pairs[index].append(l)
                                    #[[P26,P569,P54,before,e,e]]
                                    exist=True

            if exist==True:
                print("yes")
                for j in range(len(all_relation_pairs)):
                    if len(all_relation_pairs[j])>5:
                        # step=2
                        for k in range(5,len(all_relation_pairs[j]),2):
                            vertex1 = all_relation_pairs[j][k]
                            vertex2 = all_relation_pairs[j][k+1]
                            start1 = vertex1.getStartTime()
                            end1 = vertex1.getEndTime()
                            start2 = vertex2.getStartTime()
                            end2 = vertex2.getEndTime()
                            head = v.getId()
                            relation=all_relation_pairs[j][0]
                            relation1 = vertex1.getId()
                            tail1 = vertex1.hasValue.getId()
                            relation3=all_relation_pairs[j][2]
                            relation2 = vertex2.getId()
                            tail2 = vertex2.hasValue.getId()

                            # choose which interval relation is
                            if BOH_relations[j][4].__eq__("before"):
                                if Interval_Relations.before(start1,end1,start2,end2)==-1:
                                    inconsistent_pair = both_one_hop_constraints[j]+"\t"+head + ","+ relation+",entity,"\
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + ","+ relation3+",entity," + relation2 + "," + tail2 + "," + str(start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif BOH_relations[j][4].__eq__("include"):
                                if Interval_Relations.include(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = both_one_hop_constraints[
                                                            j] + "\t" + head + "," + relation + ",entity," \
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + "," + relation3+",entity,"+ relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif BOH_relations[j][4].__eq__("start"):
                                if Interval_Relations.start(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = both_one_hop_constraints[
                                                            j] + "\t" + head + "," + relation + ",entity," \
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + "," + relation3+",entity,"+ relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif BOH_relations[j][4].__eq__("finish"):
                                if Interval_Relations.finish(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = both_one_hop_constraints[
                                                            j] + "\t" + head + "," + relation + ",entity," \
                                                        + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + ","+ relation3+",entity," + relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)

    return Conflict_Fact_set

def Conflict_Detection(temporal_KG,Constraint_Set):
    # framework
    # Constraint_Mining.simplify_constraint()
    # file=open()
    # Conflict_Set=[]
    # for constraint in Constraint_Set:
    Conflict_Set=[]

    # functional constraints detection
    functional_constraints = []
    for c in Constraint_Set:
        elem = c.split(" ")
        atom1 = elem[0]
        interval_relation = elem[1]
        atom2 = elem[2]
        anchor = ""
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
                functional_constraints.append(c)
    Conflict_Set += Subgraph_Detection0(temporal_KG, functional_constraints)

    # inverse functional constraints detection
    inverse_functional_constraints = []
    for c in Constraint_Set:
        elem = c.split(" ")
        atom1=elem[0]
        interval_relation=elem[1]
        atom2=elem[2]
        anchor=""
        if atom1.split(",")[0].__eq__(atom2.split(",")[0]):
            anchor="head"
        elif atom1.split(",")[2].__eq__(atom2.split(",")[2]):
            anchor="tail"
        if anchor=="tail":
            inverse_functional_constraints.append(c)
    Conflict_Set+=Subgraph_Detection1(temporal_KG,inverse_functional_constraints)

    # zero hop constraint detection
    zero_hop_constraints=[]
    for c in Constraint_Set:
        elem = c.split(" ")
        atom1=elem[0]
        interval_relation=elem[1]
        atom2=elem[2]
        anchor=""
        if atom1.split(",")[0].__eq__(atom2.split(",")[0]):
            anchor="head"
        elif atom1.split(",")[2].__eq__(atom2.split(",")[2]):
            anchor="tail"
        if anchor=="head":
            path1 = atom1.split(",")[1]
            edges1 = path1.split("*")
            path2 = atom2.split(",")[1]
            edges2 = path2.split("*")
            if edges1[0] != edges2[0] and len(edges1) == 1 and len(edges2) == 1:
                zero_hop_constraints.append(c)
    # print(zero_hop_constraints)
    Conflict_Set+=Subgraph_Detection2(temporal_KG,zero_hop_constraints)

    # first one hop constraint detection
    first_one_hop_constraints = []
    for c in Constraint_Set:
        elem = c.split(" ")
        atom1 = elem[0]
        interval_relation = elem[1]
        atom2 = elem[2]
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
            if len(edges1) == 2 and len(edges2) == 1:
                first_one_hop_constraints.append(c)
    Conflict_Set += Subgraph_Detection3(temporal_KG, first_one_hop_constraints)

    # second one hop constraint detection
    second_one_hop_constraints = []
    for c in Constraint_Set:
        elem = c.split(" ")
        atom1 = elem[0]
        interval_relation = elem[1]
        atom2 = elem[2]
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
            if len(edges1) == 1 and len(edges2) == 2:
                second_one_hop_constraints.append(c)
    Conflict_Set += Subgraph_Detection4(temporal_KG, second_one_hop_constraints)

    # both one hop constraint detection
    both_one_hop_constraints = []
    for c in Constraint_Set:
        elem = c.split(" ")
        atom1 = elem[0]
        interval_relation = elem[1]
        atom2 = elem[2]
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
            if len(edges1) == 2 and len(edges2) == 2:
                both_one_hop_constraints.append(c)
    Conflict_Set += Subgraph_Detection5(temporal_KG, both_one_hop_constraints)


    Detected_Constraint_Set=set(inverse_functional_constraints).union(set(functional_constraints))
    Detected_Constraint_Set=Detected_Constraint_Set.union(zero_hop_constraints)
    Detected_Constraint_Set = Detected_Constraint_Set.union(first_one_hop_constraints)
    Detected_Constraint_Set = Detected_Constraint_Set.union(second_one_hop_constraints)
    Detected_Constraint_Set = Detected_Constraint_Set.union(both_one_hop_constraints)
    print("Total Constraint number is",len(Constraint_Set))
    print("Detected Constraint number is",len(Detected_Constraint_Set))
    print("Constraints not detected yet:")
    Undetected_Constraint_Set=set()
    Undetected_Constraint_Set=set(Constraint_Set).difference(Detected_Constraint_Set)
    print(Undetected_Constraint_Set)
    return Conflict_Set

def test():
    temporal_KG = Graph_Structure.Graph()
    # filename = "wikidata_dataset_tsv/rockit_wikidata_0_50k.tsv"
    filename = "all_relations_with_redundant_wikidata_alpha-1.2.tsv"
    # filename="all_relations_with_redundant_freebase_alpha-1.1.tsv"
    # read_datasets.pre_process(filename)

    starttime0 = time.time()
    temporal_KG.ConstructThroughTsv(filename, 100)
    endtime0 = time.time()
    runningtime0 = endtime0 - starttime0
    print("ConstructThroughTsv running time:", runningtime0, "s")

    # print("entity vertex number is:",temporal_KG.num_eVertices)
    #
    constraint_set = []
    constraint = "a,P569,b,t1,t2 before a,P54,c,t3,t4|1"
    constraint_set.append(constraint)
    constraint = "a,P54,b,t1,t2 before a,P570,c,t3,t4|1"
    constraint_set.append(constraint)
    constraint = "a,P286,b,t1,t2 disjoint c,P286,b,t3,t4|1"
    constraint_set.append(constraint)
    constraint = "a,P26,b,t1,t2 disjoint a,P26,c,t3,t4|1"
    constraint_set.append(constraint)
    constraint = "a,P26,b,t1,t2 disjoint c,P26,b,t3,t4|1"
    constraint_set.append(constraint)
    constraint = "a,P26*P569,d,t5,t6 before a,P54,b,t1,t2|1.0"
    constraint_set.append(constraint)
    constraint = "a,P569,b,t1,t2 before a,P26*P108,d,t5,t6|1.0"
    constraint_set.append(constraint)
    constraint = "a,P22*P569,b,t1,t2 before a,P26*P569,d,t5,t6|1.0"
    constraint_set.append(constraint)
    #
    starttime = time.time()
    conflicts = Conflict_Detection(temporal_KG, constraint_set)
    for conflict in conflicts:
        print(conflict)
    endtime = time.time()
    runningtime = endtime - starttime
    print("Conflict detection running time:", runningtime, "s")

if __name__ == '__main__':
    test()