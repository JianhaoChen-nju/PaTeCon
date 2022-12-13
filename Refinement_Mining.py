import Constraint_Mining
import Conflict_Detection
import time
import Graph_Structure
import Interval_Relations

candidate_threshold=0.5
confidence_threshold=0.9
truncate_threshold=0.9
support_threshold=100

entity_type_threshold=10
entity_type_threshold1=5
entity_type_threshold2=3

def refined_functional_mining(graph,constraint_set):
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets

    print("refined_functional_mining......")
    # output_filename = "functional_conflict.txt"
    # a quick index dict
    index_dict={}
    refined_functional_constraint = []

    # new_added
    functional_constraints = constraint_set
    print("len of functional constraint:", len(functional_constraints))
    F_relations = []
    for c in functional_constraints:
        F_relation = c.split(" ")[0].split(",")[1]
        if F_relation in graph.relationList:
            F_relations.append(F_relation)

    all_r_index_dict={}
    for i in range(len(graph.relationList)):
        all_r_index_dict[graph.relationList[i]]=i

    F_relations_statistics=[]
    cou=0
    for r in F_relations:
        index=all_r_index_dict[r]
        l=len(graph.sorted_Rotypes[index])
        if l==0:
            continue
        elif l<entity_type_threshold:
            # entity_type_threshold=10
            for i in range(l):
                type=graph.sorted_Rotypes[index][i][0]
                F_relations_statistics.append([r+"*"+type, 0, 0])
                index_dict[r+"*"+type]=cou
                cou+=1

        else:
            for i in range(entity_type_threshold):
                type=graph.sorted_Rotypes[index][i][0]
                F_relations_statistics.append([r+"*"+type, 0, 0])
                index_dict[r + "*" + type] = cou
                cou += 1
        #relation*type consistent_subset total_subset
        #[[P1*type,0,0]]

    # new_added
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
        all_relation_pairs = {}

        for s in v.hasStatement:
            i1 = s.getStartTime()
            i2 = s.getEndTime()
            # we only care temporal facts
            if i1 != -1 or i2 != -1:
                relation = s.getId()
                tail = s.hasValue.getId()
                if graph.entityType.__contains__(tail):
                    for t in graph.entityType[tail]:
                        combined=relation+"*"+t
                        if index_dict.__contains__(combined):
                            index=index_dict[combined]
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

                    # confidence = positive/positive+negative
                    result = Interval_Relations.disjoint(start1, end1, start2, end2)
                    if result == -1:
                        consistent = False
                        flag = False
                        negative = True
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
            elif negative == True:
                F_relations_statistics[j][2] += 1
        all_relation_pairs.clear()
    for f in F_relations_statistics:
        total_subsets=f[2]
        consistent_subsets=f[1]
        relation=f[0].split("*")[0]
        entity_type=f[0].split("*")[1]
        if total_subsets == 0:
            confidence = 0
        else:
            confidence = consistent_subsets * 1.0 / total_subsets
        # print(relation+"*"+entity_type, consistent_subsets, total_subsets, confidence)
        if confidence > confidence_threshold and consistent_subsets > support_threshold:
            constraint = "a," + relation + ",b,t1,t2 b,class,"+entity_type+" disjoint a," + relation + ",c,t3,t4 c,class,"+entity_type+"|" + str(
                confidence)
            # print(constraint)
            refined_functional_constraint.append(constraint)

        # x relation1 y & x relation2 z t1(t1=开始结束时间取平均数) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1
    return refined_functional_constraint

def refined_inverse_functional_mining(graph,constraint_set):
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets
    print("refined inverse_functional_mining......")

    refined_inverse_functional_constraint = []
    index_dict = {}

    # new_added
    inverse_functional_constraints = constraint_set
    print("len of inverse_functional constraint:", len(inverse_functional_constraints))
    IF_relations = []
    for c in inverse_functional_constraints:
        IF_relation = c.split(" ")[0].split(",")[1]
        if IF_relation in graph.relationList:
            IF_relations.append(IF_relation)

    all_r_index_dict={}
    for i in range(len(graph.relationList)):
        all_r_index_dict[graph.relationList[i]]=i

    IF_relations_statistics=[]
    cou=0
    for r in IF_relations:
        index=all_r_index_dict[r]
        l=len(graph.sorted_Rotypes[index])
        if l==0:
            continue
        elif l<entity_type_threshold:
            # entity_type_threshold=10
            for i in range(l):
                type=graph.sorted_Rotypes[index][i][0]
                IF_relations_statistics.append([r+"*"+type, 0, 0])
                index_dict[r+"*"+type]=cou
                cou+=1

        else:
            for i in range(entity_type_threshold):
                type=graph.sorted_Rotypes[index][i][0]
                IF_relations_statistics.append([r+"*"+type, 0, 0])
                index_dict[r + "*" + type] = cou
                cou += 1
        #relation*type consistent_subset total_subset
        #[[P1*type,0,0]]

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
                tail = v.getId()
                if graph.entityType.__contains__(tail):
                    for t in graph.entityType[tail]:
                        combined = relation + "*" + t
                        if index_dict.__contains__(combined):
                            index = index_dict[combined]
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

                    # confidence = positive/positive+negative
                    result = Interval_Relations.disjoint(start1, end1, start2, end2)
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
        relation = f[0].split("*")[0]
        entity_type = f[0].split("*")[1]
        if total_subsets == 0:
            confidence = 0
        else:
            confidence = consistent_subsets * 1.0 / total_subsets
        # print(relation+"*"+entity_type, consistent_subsets, total_subsets, confidence)
        if confidence > confidence_threshold and consistent_subsets > support_threshold:
        # if confidence > confidence_threshold and consistent_subsets > support_threshold:
            constraint = "a," + relation + ",b,t1,t2 b,class,"+entity_type+" disjoint c," + relation + ",b,t3,t4 b,class,"+entity_type+"|"+str(confidence)
            # print(constraint)
            refined_inverse_functional_constraint.append(constraint)

        # x relation1 y & x relation2 z t1(t1=开始结束时间取平均数) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1
    return refined_inverse_functional_constraint


def Refined_Single_Entity_Temporal_Order(graph,constraint_set):
    # transitivity
    # before include start finish overlap disjoint
    print("Refined Single Entity Temporal Order Mining......")
    index_dict = {}
    Refined_Single_Entity_Temporal_Order_Constraint = []
    ZH_relations_statistics=[]
    cou=0

    zero_hop_constraints = constraint_set
    print("len of Single Entity constraint:", len(zero_hop_constraints))
    ZHC_relations = []
    index_dict = {}
    count = 0

    for c in zero_hop_constraints:
        ZHC_relation1 = c.split(" ")[0].split(",")[1]
        ZHC_relation2 = c.split(" ")[2].split(",")[1]
        ZHC_interval_relation = c.split(" ")[1]
        if ZHC_relation1 in graph.relationList and ZHC_relation2 in graph.relationList:
            relation_pair = [ZHC_relation1, ZHC_relation2, ZHC_interval_relation]
            ZHC_relations.append(relation_pair)

    # r-o-type index
    all_r_index_dict = {}
    for i in range(len(graph.relationList)):
        all_r_index_dict[graph.relationList[i]] = i

    ZH_relations_statistics = []
    cou = 0
    for r in ZHC_relations:
        ZHC_relation1=r[0]
        ZHC_relation2=r[1]
        ZHC_interval_relation=r[2]
        index1= all_r_index_dict[ZHC_relation1]
        index2= all_r_index_dict[ZHC_relation2]
        l1 = len(graph.sorted_Rotypes[index1])
        l2 = len(graph.sorted_Rotypes[index2])

        if l1 == 0 and l2==0:
            continue
        else:
            type1=["null"]
            type2=["null"]
            len1=0
            len2=0
            if l1<entity_type_threshold1:
                len1=l1
            else:
                len1=entity_type_threshold1
            if l2<entity_type_threshold1:
                len2=l2
            else:
                len2=entity_type_threshold1
            for i in range(len1):
                type1.append(graph.sorted_Rotypes[index1][i][0])
            for i in range(len2):
                type2.append(graph.sorted_Rotypes[index2][i][0])

        for i in range(len(type1)):
            t1=type1[i]
            for j in range(len(type2)):
                t2=type2[j]
                ZH_relations_statistics.append([ZHC_relation1 + "*" + t1, ZHC_relation2+"*"+t2,ZHC_interval_relation, 0, 0])
                key=ZHC_relation1 + "*" + t1+"*"+ ZHC_relation2+"*"+t2
                index_dict[key]=cou
                cou+=1


    vertex_count = 0
    pre = time.time()
    # pool=ThreadPool(4)
    # def single_subgraph_traverse(i):
    all_relations = set()
    # print(ZHC_relations)
    for p in ZHC_relations:
        all_relations.add(p[0])
        all_relations.add(p[1])

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
            # a quick prune
            filter_count = 0
            for j in range(len(v.hasStatement)):
                s = v.hasStatement[j]
                if all_relations.__contains__(s.getId()):
                    filter_count += 1
            if filter_count < 2:
                continue

            for j in range(len(v.hasStatement)):
                s1 = v.hasStatement[j]
                start1 = s1.getStartTime()
                end1 = s1.getEndTime()
                if start1 != -1 or end1 != -1:
                    if not all_relations.__contains__(s1.getId()):
                        continue
                    for k in range(j+1,len(v.hasStatement)):
                            s2 = v.hasStatement[k]
                            if s1.getId().__eq__(s2.getId()):
                                continue
                            start2 = s2.getStartTime()
                            end2 = s2.getEndTime()
                            if start2 != -1 or end2 != -1:
                                if not all_relations.__contains__(s2.getId()):
                                    continue
                                tail1=s1.hasValue.getId()
                                tail2=s2.hasValue.getId()
                                r1 = s1.getId()
                                r2 = s2.getId()
                                if graph.entityType.__contains__(tail1):
                                    if graph.entityType.__contains__(tail2):
                                        for t in graph.entityType[tail1]:
                                            u="null"
                                            key=r1+"*"+t+"*"+r2+"*"+u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                            key = r2 + "*" + u + "*" + r1 + "*" + t
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                        for u in graph.entityType[tail2]:
                                            t="null"
                                            key=r1+"*"+t+"*"+r2+"*"+u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                            key = r2 + "*" + u + "*" + r1 + "*" + t
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                        for t in graph.entityType[tail1]:
                                            for u in graph.entityType[tail2]:
                                                key=r1+"*"+t+"*"+r2+"*"+u
                                                if index_dict.__contains__(key):
                                                    index=index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s1)
                                                    all_relation_pairs.setdefault(index, []).append(s2)
                                                key = r2 + "*" + u + "*" + r1 + "*" + t
                                                if index_dict.__contains__(key):
                                                    index = index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s2)
                                                    all_relation_pairs.setdefault(index, []).append(s1)

                                    else:
                                        for t in graph.entityType[tail1]:
                                            u="null"
                                            key=r1+"*"+t+"*"+r2+"*"+u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                            key = r2 + "*" + u + "*" + r1 + "*" + t
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                else:
                                    if graph.entityType.__contains__(tail2):
                                        for u in graph.entityType[tail2]:
                                            t="null"
                                            key=r1+"*"+t+"*"+r2+"*"+u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                            key = r2 + "*" + u + "*" + r1 + "*" + t
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                                all_relation_pairs.setdefault(index, []).append(s1)


            for j in all_relation_pairs.keys():
                consistent = True
                negative= False
                flag=True
                # total subsets+=1
                # ZH_relations_statistics[j][4]+=1
                # step=2
                ZHC_interval_relation=ZH_relations_statistics[j][2]
                for k in range(0,len(all_relation_pairs[j]), 2):
                    vertex1 = all_relation_pairs[j][k]
                    vertex2 = all_relation_pairs[j][k + 1]
                    start1 = vertex1.getStartTime()
                    end1 = vertex1.getEndTime()
                    start2 = vertex2.getStartTime()
                    end2 = vertex2.getEndTime()
                    # choose which interval relation is
                    if ZHC_interval_relation.__eq__("before"):
                        result = Interval_Relations.before(start1, end1, start2, end2)
                        if result == -1:
                            consistent = False
                            flag = False
                            negative = True
                            break
                        if result == 0:
                            consistent = False
                    elif ZHC_interval_relation.__eq__("include"):
                        result=Interval_Relations.include(start1, end1, start2, end2)
                        if result == -1:
                            consistent = False
                            flag = False
                            negative = True
                            break
                        if result == 0:
                            consistent = False
                    elif ZHC_interval_relation.__eq__("start"):
                        result = Interval_Relations.start(start1, end1, start2, end2)
                        if result == -1:
                            consistent = False
                            flag = False
                            negative = True
                            break
                        if result == 0:
                            consistent = False

                    elif ZHC_interval_relation.__eq__("finish"):
                        result = Interval_Relations.finish(start1, end1, start2, end2)
                        if result == -1:
                            consistent = False
                            flag = False
                            negative = True
                            break
                        if result == 0:
                            consistent = False

                    if flag==False:
                        break
                if consistent==True:
                    #before_consistent_subsets += 1
                    ZH_relations_statistics[j][3]+=1
                    # confidence = positive/positive+negative
                    ZH_relations_statistics[j][4] += 1
                elif negative == True:
                    ZH_relations_statistics[j][4] += 1
    for f in ZH_relations_statistics:
        relation1=f[0].split("*")[0]
        entity_type1=f[0].split("*")[1]
        relation2=f[1].split("*")[0]
        entity_type2=f[1].split("*")[1]
        total_subsets=f[4]
        consistent_subsets=f[3]
        ZHC_interval_relation=f[2]
        if total_subsets == 0:
            confidence = 0
        else:
            confidence = consistent_subsets * 1.0 / total_subsets
        # if consistent_subsets != 0:
        #     print(ZHC_interval_relation, relation1,entity_type1, relation2,entity_type2, consistent_subsets, total_subsets, confidence)

        # if before_confidence > confidence_threshold and before_consistent_subsets > support_threshold:
        if confidence > confidence_threshold and consistent_subsets > support_threshold:
            constraint = "a," + relation1 + ",b,t1,t2 b,class,"+entity_type1+" "+ZHC_interval_relation+" a," + relation2 + ",c,t3,t4 c,class,"+entity_type2+"|" + str(
                confidence)
            # print(constraint)
            Refined_Single_Entity_Temporal_Order_Constraint.append(constraint)

    return Refined_Single_Entity_Temporal_Order_Constraint

def Refined_Mutiple_Entity_Temporal_Order(graph,constraint_set):
    print("Refined Mutiple Entity Temporal Order Mining......")
    Refined_Mutiple_Entity_Temporal_Order_Constraint = []
    index_dict = {}
    OH_relations = []
    OH_relations_statistics = []
    cou = 0

    one_hop_constraints = constraint_set
    print("len of Mutiple Entity constraint:", len(one_hop_constraints))
    index_dict = {}
    for c in one_hop_constraints:
        elem = c.split(" ")
        atom1 = elem[0]
        interval_relation = elem[1]
        atom2 = elem[2]

        path1 = atom1.split(",")[1]
        edges1 = path1.split("*")
        path2 = atom2.split(",")[1]
        edges2 = path2.split("*")
        if len(edges1) == 2:
            interval_relation="inverse_"+interval_relation
            edges0=edges1
            edges1=edges2
            edges2=edges0

        FOH_relation0 = edges1[0]
        FOH_relation1 = edges2[0]
        FOH_relation2 = edges2[1]
        FOH_interval_relation = interval_relation
        relation_pair = [FOH_relation0, FOH_relation1, FOH_relation2, FOH_interval_relation]
        if FOH_relation1 in graph.relationList and FOH_relation2 in graph.relationList and FOH_relation0 in graph.relationList:
            OH_relations.append(relation_pair)

        # r-o-type index
    all_r_index_dict = {}
    for i in range(len(graph.relationList)):
        all_r_index_dict[graph.relationList[i]] = i

    cou = 0
    for r in OH_relations:
        OHC_relation0 = r[0]
        OHC_relation1 = r[1]
        OHC_relation2 = r[2]
        OHC_interval_relation = r[3]
        index0 = all_r_index_dict[OHC_relation0]
        index1 = all_r_index_dict[OHC_relation1]
        index2 = all_r_index_dict[OHC_relation2]
        l0 = len(graph.sorted_Rotypes[index0])
        l1 = len(graph.sorted_Rotypes[index1])
        l2 = len(graph.sorted_Rotypes[index2])

        if l1 == 0 and l2 == 0 and l0==0:
            continue
        else:
            type0 = ["null"]
            type1 = ["null"]
            type2 = ["null"]
            len0=0
            len1 = 0
            len2 = 0
            if l0 <entity_type_threshold2:
                len0=l0
            else:
                len0=entity_type_threshold2
            if l1 < entity_type_threshold2:
                len1 = l1
            else:
                len1 = entity_type_threshold2
            if l2 < entity_type_threshold2:
                len2 = l2
            else:
                len2 = entity_type_threshold2
            for i in range(len0):
                type0.append(graph.sorted_Rotypes[index0][i][0])
            for i in range(len1):
                type1.append(graph.sorted_Rotypes[index1][i][0])
            for i in range(len2):
                type2.append(graph.sorted_Rotypes[index2][i][0])
        for h in range(len(type0)):
            t0=type0[h]
            for i in range(len(type1)):
                t1 = type1[i]
                for j in range(len(type2)):
                    t2 = type2[j]

                    OH_relations_statistics.append(
                        [OHC_relation0+"*"+t0,OHC_relation1 + "*" + t1, OHC_relation2 + "*" + t2, OHC_interval_relation, 0, 0])
                    key = OHC_relation0+"*"+t0+"*"+OHC_relation1 + "*" + t1 + "*" + OHC_relation2 + "*" + t2
                    index_dict[key] = cou
                    cou += 1

    first_relations = set()
    second_relations = set()
    for p in OH_relations:
        first_relations.add(p[0])
        first_relations.add(p[1])

    for p in OH_relations:
        second_relations.add(p[2])

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
            # a quick prune
            filter_count = 0
            for j in range(len(v.hasStatement)):
                s = v.hasStatement[j]
                if first_relations.__contains__(s.getId()):
                    filter_count += 1
            if filter_count < 2:
                continue
            for j in range(len(v.hasStatement)):
                s1 = v.hasStatement[j]
                # a quick filtering
                i1 = s1.getStartTime()
                i2 = s1.getEndTime()
                if i1 != -1 or i2 != -1:
                    if not first_relations.__contains__(s1.getId()):
                        continue

                    # search for one hop
                    for k in range(len(v.hasStatement)):
                        s2 = v.hasStatement[k]
                        # two node cannot equal
                        if j == k:
                            continue

                        # a quick filtering
                        if not first_relations.__contains__(s2.getId()):
                            continue

                        hasOneHopRelation = False
                        for l in s2.hasValue.hasStatement:
                            if not second_relations.__contains__(l.getId()):
                                continue
                            hasOneHopRelation = True

                        if hasOneHopRelation == False:
                            continue

                        for l in s2.hasValue.hasStatement:
                            if not second_relations.__contains__(l.getId()):
                                continue

                            r0 = s1.getId()
                            tail0=s1.hasValue.getId()
                            r1 = s2.getId()
                            tail1=s2.hasValue.getId()
                            r2 = l.getId()
                            tail2=l.hasValue.getId()
                            if graph.entityType.__contains__(tail0):
                                if graph.entityType.__contains__(tail1):
                                    if graph.entityType.__contains__(tail2):
                                        # xoo
                                        for t in graph.entityType[tail1]:
                                            for u in graph.entityType[tail2]:
                                                s="null"
                                                key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                if index_dict.__contains__(key):
                                                    index = index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s1)
                                                    all_relation_pairs.setdefault(index, []).append(l)
                                        # oxo
                                        for s in graph.entityType[tail0]:
                                            for u in graph.entityType[tail2]:
                                                    t="null"
                                                    key=r0+"*"+s+"*"+r1+"*"+t+"*"+r2+"*"+u
                                                    if index_dict.__contains__(key):
                                                        index=index_dict[key]
                                                        all_relation_pairs.setdefault(index, []).append(s1)
                                                        all_relation_pairs.setdefault(index, []).append(l)
                                        # oox
                                        for s in graph.entityType[tail0]:
                                            for t in graph.entityType[tail1]:
                                                    u="null"
                                                    key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                    if index_dict.__contains__(key):
                                                        index = index_dict[key]
                                                        all_relation_pairs.setdefault(index, []).append(s1)
                                                        all_relation_pairs.setdefault(index, []).append(l)
                                        # oxx
                                        for s in graph.entityType[tail0]:
                                                    t="null"
                                                    u="null"
                                                    key=r0+"*"+s+"*"+r1+"*"+t+"*"+r2+"*"+u
                                                    if index_dict.__contains__(key):
                                                        index=index_dict[key]
                                                        all_relation_pairs.setdefault(index, []).append(s1)
                                                        all_relation_pairs.setdefault(index, []).append(l)

                                        # xox
                                        for t in graph.entityType[tail1]:
                                                    s = "null"
                                                    u = "null"
                                                    key=r0+"*"+s+"*"+r1+"*"+t+"*"+r2+"*"+u
                                                    if index_dict.__contains__(key):
                                                        index=index_dict[key]
                                                        all_relation_pairs.setdefault(index, []).append(s1)
                                                        all_relation_pairs.setdefault(index, []).append(l)

                                        # xxo
                                        for u in graph.entityType[tail2]:
                                                    s="null"
                                                    t="null"
                                                    key=r0+"*"+s+"*"+r1+"*"+t+"*"+r2+"*"+u
                                                    if index_dict.__contains__(key):
                                                        index=index_dict[key]
                                                        all_relation_pairs.setdefault(index, []).append(s1)
                                                        all_relation_pairs.setdefault(index, []).append(l)

                                        # ooo
                                        for s in graph.entityType[tail0]:
                                            for t in graph.entityType[tail1]:
                                                for u in graph.entityType[tail2]:
                                                    key=r0+"*"+s+"*"+r1+"*"+t+"*"+r2+"*"+u
                                                    if index_dict.__contains__(key):
                                                        index=index_dict[key]
                                                        all_relation_pairs.setdefault(index, []).append(s1)
                                                        all_relation_pairs.setdefault(index, []).append(l)
                                    else:
                                        # oox
                                        for s in graph.entityType[tail0]:
                                            for t in graph.entityType[tail1]:
                                                u = "null"
                                                key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                if index_dict.__contains__(key):
                                                    index = index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s1)
                                                    all_relation_pairs.setdefault(index, []).append(l)
                                        # oxx
                                        for s in graph.entityType[tail0]:
                                            t = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                        # xox
                                        for t in graph.entityType[tail1]:
                                            s = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                else:
                                    if graph.entityType.__contains__(tail2):
                                        # oxo
                                        for s in graph.entityType[tail0]:
                                            for u in graph.entityType[tail2]:
                                                t = "null"
                                                key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                if index_dict.__contains__(key):
                                                    index = index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s1)
                                                    all_relation_pairs.setdefault(index, []).append(l)
                                        # oxx
                                        for s in graph.entityType[tail0]:
                                            t = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                        # xxo
                                        for u in graph.entityType[tail2]:
                                                    s="null"
                                                    t="null"
                                                    key=r0+"*"+s+"*"+r1+"*"+t+"*"+r2+"*"+u
                                                    if index_dict.__contains__(key):
                                                        index=index_dict[key]
                                                        all_relation_pairs.setdefault(index, []).append(s1)
                                                        all_relation_pairs.setdefault(index, []).append(l)
                                    else:
                                        # oxx
                                        for s in graph.entityType[tail0]:
                                            t = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                            else:
                                if graph.entityType.__contains__(tail1):
                                    if graph.entityType.__contains__(tail2):
                                        # xoo
                                        for t in graph.entityType[tail1]:
                                            for u in graph.entityType[tail2]:
                                                s = "null"
                                                key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                if index_dict.__contains__(key):
                                                    index = index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s1)
                                                    all_relation_pairs.setdefault(index, []).append(l)
                                        # xox
                                        for t in graph.entityType[tail1]:
                                            s = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)

                                        # xxo
                                        for u in graph.entityType[tail2]:
                                            s = "null"
                                            t = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                    else:
                                        # xox
                                        for t in graph.entityType[tail1]:
                                            s = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                else:
                                    if graph.entityType.__contains__(tail2):
                                        # xxo
                                        for u in graph.entityType[tail2]:
                                            s = "null"
                                            t = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
            for j in all_relation_pairs.keys():
                consistent = True
                flag=True
                negative=False
                # total subsets+=1
                # OH_relations_statistics[j][5] += 1
                OHC_interval_relation=OH_relations_statistics[j][3]
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
                    if OHC_interval_relation.__eq__("before"):
                        result = Interval_Relations.before(start1, end1, start2, end2)
                        if result == -1:
                            consistent = False
                            flag = False
                            negative = True
                            break
                        if result == 0:
                            consistent = False
                        # if Interval_Relations.before(start1, end1, start2, end2) == -1:
                        #     consistent = False
                    elif OHC_interval_relation.__eq__("inverse_before"):
                        result = Interval_Relations.before(start2, end2, start1, end1)
                        if result == -1:
                            consistent = False
                            flag = False
                            negative = True
                            break

                        if result == 0:
                            consistent = False
                        # if Interval_Relations.before(start2, end2, start1, end1) == -1:
                        #     consistent = False
                    elif OHC_interval_relation.__eq__("include"):
                        result = Interval_Relations.include(start1, end1, start2, end2)
                        if result == -1:
                            consistent = False
                            flag = False
                            negative = True
                            break

                        if result == 0:
                            consistent = False
                        # if Interval_Relations.include(start1, end1, start2, end2) == -1:
                        #     consistent = False
                    elif OHC_interval_relation.__eq__("inverse_include"):
                        result = Interval_Relations.include(start2, end2, start1, end1)
                        if result == -1:
                            consistent = False
                            flag = False
                            negative = True
                            break

                        if result == 0:
                            consistent = False
                        # if Interval_Relations.include(start2, end2, start1, end1) == -1:
                        #     consistent = False
                    elif OHC_interval_relation.__eq__("start"):
                        result = Interval_Relations.start(start1, end1, start2, end2)
                        if result == -1:
                            consistent = False
                            flag = False
                            negative = True
                            break

                        if result == 0:
                            consistent = False
                        # if Interval_Relations.start(start1, end1, start2, end2) == -1:
                        #     consistent = False
                    elif OHC_interval_relation.__eq__("finish"):
                        result = Interval_Relations.finish(start1, end1, start2, end2)
                        if result == -1:
                            consistent = False
                            flag = False
                            negative = True
                            break

                        if result == 0:
                            consistent = False
                        # if Interval_Relations.finish(start1, end1, start2, end2) == -1:
                        #     consistent = False
                    if flag==False:
                        break
                if consistent == True:
                    # before_consistent_subsets += 1
                    OH_relations_statistics[j][4] += 1
                    # confidence = positive/positive+negative
                    OH_relations_statistics[j][5] += 1
                elif negative == True:
                    OH_relations_statistics[j][5] += 1

    for f in OH_relations_statistics:
        relation1 = f[0].split("*")[0]
        t0=f[0].split("*")[1]
        one_hop=f[1].split("*")[0]
        t1=f[1].split("*")[1]
        relation2 = f[2].split("*")[0]
        t2=f[2].split("*")[1]
        OHC_interval_relation=f[3]
        total_subsets = f[5]
        consistent_subsets=f[4]

        if total_subsets == 0:
            confidence = 0
        else:
            confidence = consistent_subsets * 1.0 / total_subsets
        # if consistent_subsets != 0:
        #     print(OHC_interval_relation, relation1,t0, one_hop,t1, relation2,t2, consistent_subsets, total_subsets, confidence)

        if confidence > confidence_threshold and consistent_subsets>support_threshold:
            if OHC_interval_relation.__contains__("inverse_"):
                OHC_interval_relation=OHC_interval_relation.replace("inverse_","")
                constraint = "a," + one_hop+"*"+relation2 + ",d,t3,t4 c,class,"+t1+" d,class,"+t2+" "+ OHC_interval_relation +" a," + relation1 + \
                             ",b,t1,t2 b,class,"+t0+"|" + str(confidence)
                # print(constraint)
                Refined_Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
            else:
                constraint = "a," + relation1 + ",b,t1,t2 b,class,"+t0+" "+OHC_interval_relation+" a," + one_hop+"*"+relation2 + ",d,t3,t4 c" \
                    ",class,"+t1+" d,class,"+t2+"|" + str(
                    confidence)
                # print(constraint)
                Refined_Mutiple_Entity_Temporal_Order_Constraint.append(constraint)

    return Refined_Mutiple_Entity_Temporal_Order_Constraint

def refined_mining(graph,typefile,Constraint_Set):

    # refined condition
    # unconditional refine or depending on confidence
    filtered_Constraint=[]
    for c in Constraint_Set:
        confidence=float(c.split("|")[1])
        if confidence>=candidate_threshold and confidence<confidence_threshold:
            filtered_Constraint.append(c)
    Constraint_Set=filtered_Constraint

    t0=time.time()
    type_file = open(typefile, "r", encoding="UTF-8")
    # if knowledgebase=="wikidata":
    #     type_file=open("our_resource/wikidata-entity-type-info.tsv","r",encoding="UTF-8")
    # elif knowledgebase=="freebase":
    #     type_file=open("our_resource/freebase-entity-type-info.tsv","r",encoding="UTF-8")

    types=type_file.readlines()
    type_file.close()
    for line in types:
        elems=line.strip().split("\t")
        key=elems[0]
        for i in range(1,len(elems)):
            graph.entityType.setdefault(key, []).append(elems[i])
    t1=time.time()
    print("read type cost time is:",t1-t0,"s")

    index_dict={}
    for i in range(len(graph.relationList)):
        index_dict[graph.relationList[i]]=i
    Rotypes=[]
    for i in range(len(graph.relationList)):
        Rotypes.append({})
    for i in graph.sVertexList.keys():
        statementList = graph.sVertexList[i]
        for s in statementList:
        # print(s)
            index=index_dict[s.getId()]
            tail=s.hasValue.getId()
            if graph.entityType.__contains__(tail):
                for t in graph.entityType[tail]:
                    if Rotypes[index].__contains__(t):
                        Rotypes[index][t]+=1
                    else:
                        Rotypes[index][t]=1

    for i in range(len(Rotypes)):
        # print(Rotypes[i].items())
        sorted_Rotype=sorted(Rotypes[i].items(),key=lambda x:x[1],reverse=True)
        graph.sorted_Rotypes.append(sorted_Rotype)
    # print(graph.sorted_Rotypes)

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
            edges2 = path2.split("*")
            if edges1[0] == edges2[0] and len(edges1) == 1 and len(edges2) == 1:
                functional_constraints.append(c)


    # inverse functional constraints detection
    inverse_functional_constraints = []
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
        if anchor == "tail":
            inverse_functional_constraints.append(c)


    # zero hop constraint detection
    zero_hop_constraints = []
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
            if edges1[0] != edges2[0] and len(edges1) == 1 and len(edges2) == 1:
                zero_hop_constraints.append(c)
    # print(zero_hop_constraints)

    # first one hop constraint detection
    one_hop_constraints = []
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
            if len(edges1) == 2 or len(edges2) == 2:
                one_hop_constraints.append(c)


    Fine_Grained_Constraint_Set=[]
    st = time.time()
    Fine_Grained_Constraint_Set += refined_functional_mining(graph, functional_constraints)
    ed0 = time.time()
    print("Fine Grained functional Constraint Set cost time:", ed0 - st, "s")
    Fine_Grained_Constraint_Set += refined_inverse_functional_mining(graph, inverse_functional_constraints)
    ed1 = time.time()
    print("Fine Grained inverse functional Constraint Set cost time:", ed1 - ed0, "s")
    Fine_Grained_Constraint_Set += Refined_Single_Entity_Temporal_Order(graph, zero_hop_constraints)
    ed2 = time.time()
    print("Fine Grained Single Entity Constraint Set cost time:", ed2 - ed1, "s")
    Fine_Grained_Constraint_Set += Refined_Mutiple_Entity_Temporal_Order(graph, one_hop_constraints)
    ed3 = time.time()
    print("Fine Grained Mutiple Entity Constraint Set cost time:", ed3 - ed2, "s")

    Post_Processed_Constraint_Set = set(inverse_functional_constraints).union(set(functional_constraints))
    Post_Processed_Constraint_Set = Post_Processed_Constraint_Set.union(zero_hop_constraints)
    Post_Processed_Constraint_Set = Post_Processed_Constraint_Set.union(one_hop_constraints)
    print("Total Constraint number is", len(Constraint_Set))
    print("Fine Grained Mining Constraint number is", len(Post_Processed_Constraint_Set))
    print("Constraints not fine grained mining yet:")
    UnPost_Processed_Constraint_Set = set()
    UnPost_Processed_Constraint_Set = set(Constraint_Set).difference(Post_Processed_Constraint_Set)
    # print(UnPost_Processed_Constraint_Set)

    return Fine_Grained_Constraint_Set

def test(tkg,filename,constraint_filename,typefile,knowledgegraph):

    # knowledgebase="wikidata"
    # knowledgebase = ""
    # if filename.__contains__("WIKI") or filename.__contains__("wikidata"):
    #     knowledgebase = "wikidata"
    # elif filename.__contains__("freebase"):
    #     knowledgebase = "freebase"
    # else:
    #     knowledgebase = "other"

    # read_datasets.pre_process

    knowledgebase = knowledgegraph

    temporal_KG=tkg

    # print("entity vertex number is:",temporal_KG.num_eVertices)

    constraint_set = Conflict_Detection.read_constraints(constraint_filename)
    starttime = time.time()
    constraints = refined_mining(temporal_KG, typefile,constraint_set)
    endtime = time.time()
    runningtime = endtime - starttime
    print("Refined mining running time:", runningtime, "s")

    write_filename = filename.replace("resource","output").replace(".tsv","") + ".refined_rules"
    write_file = open(write_filename, "w", encoding="utf-8")
    write_file.writelines("\n".join(constraints))
    return 0

if __name__ == '__main__':
    # filename = "wikidata_dataset_tsv/rockit_wikidata_0_50k.tsv"
    filename = "our_resource/all_relations_with_redundant_wikidata_alpha-1.3.tsv"
    # filename="our_resource/all_relations_with_redundant_freebase_alpha-1.1.tsv"

    constraint_filename = "our_resource/all_relations_with_redundant_wikidata_alpha-1.3.tsv_rules"
    # constraint_filename = "our_resource/all_relations_with_redundant_freebase_alpha-1.1.tsv_rules"
    # constraint_filename="WD50K_trans/new_rockit_wikidata_0_50k.tsv_rules"
    # constraint_filename="constraint_list_wikidata.txt"
    typefile="our_resource/wikidata-entity-type-info.tsv"
    knowledgegraph="wikidata"
    temporal_KG = Graph_Structure.Graph()
    starttime0 = time.time()
    temporal_KG.ConstructThroughTsv(filename, knowledgegraph, 100)
    endtime0 = time.time()
    runningtime0 = endtime0 - starttime0
    print("ConstructThroughTsv running time:", runningtime0, "s")
    test(temporal_KG,filename,constraint_filename,typefile,knowledgegraph)

    Constraint_Mining.MergeConstraint(filename)



