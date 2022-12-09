import Graph_Structure
import time
import Interval_Relations

def Refined_Subgraph_Detection0(temporal_KG,Constraint_Set):
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
    print("len of constraint0:",len(functional_constraints))
    FC_relations = []
    for c in functional_constraints:
        FC_relation = c.split(" ")[0].split(",")[1]
        # new_added
        type=c.split(" ")[1].split(",")[2]
        FC_relations.append(FC_relation+"*"+type)
    index_dict={}
    for i in range(len(FC_relations)):
        index_dict[FC_relations[i]]=i
    # actions=0
    vertex_count = 0
    pre = time.time()
    for i in temporal_KG.eVertexList:
        v = temporal_KG.eVertexList[i]
        vertex_count += 1
        if vertex_count % 1000000 == 0:
            ed = time.time()
            print("have traversed nodes:", vertex_count)
            print("time cost:", ed - pre, "s")
        if v.isLiteral==True:
            continue
        if len(v.hasStatement) < 2:
            continue
        else:
            all_relation_pairs = {}
            for s in v.hasStatement:
                r=s.getId()
                i1=s.getStartTime()
                i2=s.getEndTime()
                tail=s.hasValue.getId()
                if i1!=-1 or i2!=-1:
                    # new added
                    if temporal_KG.entityType.__contains__(tail):
                        #add null and itself
                        for t in temporal_KG.entityType[tail]:
                            key=r+"*"+t
                            if index_dict.__contains__(key):
                                index=index_dict[key]
                                all_relation_pairs.setdefault(index, []).append(s)

            # print("detect cost time:", ed - st, "s")
            for j in all_relation_pairs.keys():
                for k in range(len(all_relation_pairs[j])):
                    vertex1=all_relation_pairs[j][k]

                    for l in range(k+1,len(all_relation_pairs[j])):
                        vertex2 = all_relation_pairs[j][l]
                        start1 = vertex1.getStartTime()
                        end1 = vertex1.getEndTime()
                        start2 = vertex2.getStartTime()
                        end2 = vertex2.getEndTime()
                        head = v.getId()
                        relation1 = vertex1.getId()
                        if vertex1.hasValue.isLiteral == True:
                            tail1 = vertex1.hasValue.getLabel()
                        else:
                            tail1 = vertex1.hasValue.getId()
                        relation2 = vertex2.getId()
                        if vertex2.hasValue.isLiteral == True:
                            tail2 = vertex2.hasValue.getLabel()
                        else:
                            tail2 = vertex2.hasValue.getId()
                        if Interval_Relations.disjoint(start1, end1, start2, end2) == -1:
                            # actions+=1
                            inconsistent_pair = functional_constraints[j] + "\t" + head + "," + relation1 + "," + tail1 + "," + str(
                                start1) + "," + str(
                                end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                start2) + "," + str(end2)
                            Conflict_Fact_set.append(inconsistent_pair)
    # print(actions)
    return Conflict_Fact_set

def Refined_Subgraph_Detection1(temporal_KG,Constraint_Set):

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
    print("len of constraint1:", len(inverse_functional_constraints))
    IFC_relations = []
    for c in inverse_functional_constraints:
        IFC_relation = c.split(" ")[0].split(",")[1]
        type=c.split(" ")[1].split(",")[2]
        IFC_relations.append(IFC_relation+"*"+type)
    index_dict={}
    for i in range(len(IFC_relations)):
        index_dict[IFC_relations[i]]=i
    # actions=0
    vertex_count = 0
    pre = time.time()
    for i in temporal_KG.eVertexList:
        v = temporal_KG.eVertexList[i]
        vertex_count += 1
        if vertex_count % 1000000 == 0:
            ed = time.time()
            print("have traversed nodes:", vertex_count)
            print("time cost:", ed - pre, "s")
        if v.isLiteral==True:
            continue
        if len(v.bePointedTo) < 2:
            continue
        else:
            all_relation_pairs={}
            action=0
            for s in v.bePointedTo:
                r = s.getId()
                i1 = s.getStartTime()
                i2 = s.getEndTime()
                tail=v.getId()
                if i1 != -1 or i2 != -1:
                    # new added
                    if temporal_KG.entityType.__contains__(tail):
                        for t in temporal_KG.entityType[tail]:
                            key = r + "*" + t
                            if index_dict.__contains__(key):
                                index = index_dict[key]
                                all_relation_pairs.setdefault(index, []).append(s)

            # print(action)
            if action>1000:
                continue
            for j in all_relation_pairs.keys():
                for k in range(len(all_relation_pairs[j])):
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
                            # actions+=1
                            inconsistent_pair = inverse_functional_constraints[j] + "\t" + head1 + "," + relation1 + "," + tail + "," + str(
                                start1) + "," + str(
                                end1) + "\t" + head2 + "," + relation2 + "," + tail + "," + str(
                                start2) + "," + str(end2)
                            Conflict_Fact_set.append(inconsistent_pair)
    # print(actions)
    return Conflict_Fact_set

def Refined_Subgraph_Detection2(temporal_KG,Constraint_Set):

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
    print("len of constraint2:", len(zero_hop_constraints))
    ZHC_relations = []
    index_dict = {}
    count=0
    for c in zero_hop_constraints:
        c=c.split("|")[0]
        ZHC_relation1 = c.split(" ")[0].split(",")[1]
        type1 = c.split(" ")[1].split(",")[2]
        ZHC_relation2 = c.split(" ")[3].split(",")[1]
        type2 = c.split(" ")[4].split(",")[2]
        ZHC_interval_relation=c.split(" ")[2]
        relation_pair=[ZHC_relation1+"*"+type1,ZHC_relation2+"*"+type2,ZHC_interval_relation]
        key=ZHC_relation1+"*"+type1+"*"+ZHC_relation2+"*"+type2
        index_dict[key]=count
        count+=1
        ZHC_relations.append(relation_pair)
        #[[P54,P569,before],[P54,P570,before]]
    all_relations=set()
    # print(ZHC_relations)
    for p in ZHC_relations:
        all_relations.add(p[0].split("*")[0])
        all_relations.add(p[1].split("*")[0])
    # print(all_relations)
    # cou=0

    vertex_count = 0
    pre = time.time()
    for i in temporal_KG.eVertexList:
        v = temporal_KG.eVertexList[i]
        vertex_count += 1
        if vertex_count % 1000000 == 0:
            ed = time.time()
            print("have traversed nodes:", vertex_count)
            print("time cost:", ed - pre, "s")
        # cou+=1
        # print(cou)
        if v.isLiteral==True:
            continue
        if len(v.hasStatement) < 2:
            continue
        else:
            all_relation_pairs={}
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
                i1=s1.getStartTime()
                i2=s1.getEndTime()
                if i1!=-1 or i2!=-1:
                    r1=s1.getId()
                    if not all_relations.__contains__(s1.getId()):
                        continue
                    for k in range(j+1,len(v.hasStatement)):
                        s2=v.hasStatement[k]
                        i3=s2.getStartTime()
                        i4=s2.getEndTime()
                        # a quick filtering
                        if i3!=-1 or i4!=-1:
                            r2 = s2.getId()
                            if not all_relations.__contains__(s2.getId()):
                                continue
                            tail1=s1.hasValue.getId()
                            tail2=s2.hasValue.getId()
                            # print("yes")
                            if temporal_KG.entityType.__contains__(tail1):
                                if temporal_KG.entityType.__contains__(tail2):
                                    # print("yes")
                                    for t in temporal_KG.entityType[tail1]:
                                        u = "null"
                                        key = r1 + "*" + t + "*" + r2 + "*" + u
                                        if index_dict.__contains__(key):
                                            index = index_dict[key]
                                            all_relation_pairs.setdefault(index, []).append(s1)
                                            all_relation_pairs.setdefault(index, []).append(s2)
                                        key = r2 + "*" + u + "*" + r1 + "*" + t
                                        if index_dict.__contains__(key):
                                            index = index_dict[key]
                                            all_relation_pairs.setdefault(index, []).append(s2)
                                            all_relation_pairs.setdefault(index, []).append(s1)
                                    for u in temporal_KG.entityType[tail2]:
                                        t = "null"
                                        key = r1 + "*" + t + "*" + r2 + "*" + u
                                        if index_dict.__contains__(key):
                                            index = index_dict[key]
                                            all_relation_pairs.setdefault(index, []).append(s1)
                                            all_relation_pairs.setdefault(index, []).append(s2)
                                        key = r2 + "*" + u + "*" + r1 + "*" + t
                                        if index_dict.__contains__(key):
                                            index = index_dict[key]
                                            all_relation_pairs.setdefault(index, []).append(s2)
                                            all_relation_pairs.setdefault(index, []).append(s1)
                                    for t in temporal_KG.entityType[tail1]:
                                        for u in temporal_KG.entityType[tail2]:
                                            key = r1 + "*" + t + "*" + r2 + "*" + u
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
                                    for t in temporal_KG.entityType[tail1]:
                                        u = "null"
                                        key = r1 + "*" + t + "*" + r2 + "*" + u
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
                                if temporal_KG.entityType.__contains__(tail2):
                                    for u in temporal_KG.entityType[tail2]:
                                        t = "null"
                                        key = r1 + "*" + t + "*" + r2 + "*" + u
                                        if index_dict.__contains__(key):
                                            index = index_dict[key]
                                            all_relation_pairs.setdefault(index, []).append(s1)
                                            all_relation_pairs.setdefault(index, []).append(s2)
                                        key = r2 + "*" + u + "*" + r1 + "*" + t
                                        if index_dict.__contains__(key):
                                            index = index_dict[key]
                                            all_relation_pairs.setdefault(index, []).append(s2)
                                            all_relation_pairs.setdefault(index, []).append(s1)
                            # key1=r1+"*"+r2
                            # if index_dict.__contains__(key1):
                            #     index1=index_dict[key1]
                            #     all_relation_pairs.setdefault(index1, []).append(s1)
                            #     all_relation_pairs.setdefault(index1, []).append(s2)
                            # key2=r2+"*"+r1
                            # if index_dict.__contains__(key2):
                            #     # print("yes")
                            #     index2=index_dict[key2]
                            #     all_relation_pairs.setdefault(index2, []).append(s2)
                            #     all_relation_pairs.setdefault(index2, []).append(s1)

            # print(all_relation_pairs)
            # print(len(all_relation_pairs))
            for j in all_relation_pairs.keys():
                    # step=2
                    for k in range(0,len(all_relation_pairs[j]),2):
                        # print(len(all_relation_pairs[j]))
                        vertex1 = all_relation_pairs[j][k]
                        vertex2 = all_relation_pairs[j][k+1]
                        start1 = vertex1.getStartTime()
                        end1 = vertex1.getEndTime()
                        start2 = vertex2.getStartTime()
                        end2 = vertex2.getEndTime()
                        head = v.getId()
                        relation1 = vertex1.getId()
                        if vertex1.hasValue.isLiteral == True:
                            tail1 = vertex1.hasValue.getLabel()
                        else:
                            tail1 = vertex1.hasValue.getId()
                        relation2 = vertex2.getId()
                        if vertex2.hasValue.isLiteral == True:
                            tail2 = vertex2.hasValue.getLabel()
                        else:
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


def Refined_Subgraph_Detection3(temporal_KG,Constraint_Set):

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
    one_hop_constraints = Constraint_Set
    print("len of constraint4:", len(one_hop_constraints))
    SOH_relations = []
    index_dict = {}
    count = 0

    for c in one_hop_constraints:
        c = c.split("|")[0]
        elem = c.split(" ")
        if elem[2].__contains__("class"):
            atom2 = elem[0]
            type2 = elem[1].split(",")[2]
            type3 = elem[2].split(",")[2]
            SOH_interval_relation = elem[3]
            SOH_interval_relation = "inverse_" + SOH_interval_relation
            atom1 = elem[4]
            type1 = elem[5].split(",")[2]

            path1 = atom1.split(",")[1]
            edges1 = path1.split("*")
            path2 = atom2.split(",")[1]
            edges2 = path2.split("*")

        else:
            atom1 = elem[0]
            type1=elem[1].split(",")[2]
            SOH_interval_relation = elem[2]
            atom2 = elem[3]
            type2 = elem[4].split(",")[2]
            type3 = elem[5].split(",")[2]

            path1 = atom1.split(",")[1]
            edges1 = path1.split("*")
            path2 = atom2.split(",")[1]
            edges2 = path2.split("*")

        SOH_relation0 = atom1.split(",")[1]
        SOH_relation1 = path2.split("*")[0]
        SOH_relation2 = path2.split("*")[1]

        relation_pair = [SOH_relation0+"*"+type1, SOH_relation1+"*"+type2, SOH_relation2+"*"+type3, SOH_interval_relation]
        key = SOH_relation0 + "*" +type1+"*"+ SOH_relation1 +"*"+type2 + "*" + SOH_relation2 +"*"+type3
        index_dict[key] = count
        count += 1
        SOH_relations.append(relation_pair)
        # [[P54,P569,before],[P54,P570,before]]


    first_relations=set()
    second_relations=set()
    for p in SOH_relations:
        first_relations.add(p[0].split("*")[0])
        first_relations.add(p[1].split("*")[0])

    for p in SOH_relations:
        second_relations.add(p[2].split("*")[0])

    vertex_count = 0
    pre = time.time()
    for i in temporal_KG.eVertexList:
        v = temporal_KG.eVertexList[i]
        vertex_count += 1
        if vertex_count % 1000000 == 0:
            ed = time.time()
            print("have traversed nodes:", vertex_count)
            print("time cost:", ed - pre, "s")
        if v.isLiteral==True:
            continue
        if len(v.hasStatement) < 2:
            continue
        else:
            all_relation_pairs = {}
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
                i1=s1.getStartTime()
                i2=s1.getEndTime()
                if i1!=-1 or i2!=-1:
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

                        hasOneHopRelation=False
                        for l in s2.hasValue.hasStatement:
                            if not second_relations.__contains__(l.getId()):
                                continue
                            hasOneHopRelation=True

                        if hasOneHopRelation==False:
                            continue

                        for l in s2.hasValue.hasStatement:
                            if not second_relations.__contains__(l.getId()):
                                continue
                            r0 = s1.getId()
                            tail0 = s1.hasValue.getId()
                            r1 = s2.getId()
                            tail1 = s2.hasValue.getId()
                            r2 = l.getId()
                            tail2 = l.hasValue.getId()
                            if temporal_KG.entityType.__contains__(tail0):
                                if temporal_KG.entityType.__contains__(tail1):
                                    if temporal_KG.entityType.__contains__(tail2):
                                        # xoo
                                        for t in temporal_KG.entityType[tail1]:
                                            for u in temporal_KG.entityType[tail2]:
                                                s = "null"
                                                key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                if index_dict.__contains__(key):
                                                    index = index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s1)
                                                    all_relation_pairs.setdefault(index, []).append(l)
                                                    all_relation_pairs.setdefault(index, []).append(s2)
                                        # oxo
                                        for s in temporal_KG.entityType[tail0]:
                                            for u in temporal_KG.entityType[tail2]:
                                                t = "null"
                                                key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                if index_dict.__contains__(key):
                                                    index = index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s1)
                                                    all_relation_pairs.setdefault(index, []).append(l)
                                                    all_relation_pairs.setdefault(index, []).append(s2)
                                        # oox
                                        for s in temporal_KG.entityType[tail0]:
                                            for t in temporal_KG.entityType[tail1]:
                                                u = "null"
                                                key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                if index_dict.__contains__(key):
                                                    index = index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s1)
                                                    all_relation_pairs.setdefault(index, []).append(l)
                                                    all_relation_pairs.setdefault(index, []).append(s2)
                                        # oxx
                                        for s in temporal_KG.entityType[tail0]:
                                            t = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)

                                        # xox
                                        for t in temporal_KG.entityType[tail1]:
                                            s = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)

                                        # xxo
                                        for u in temporal_KG.entityType[tail2]:
                                            s = "null"
                                            t = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)

                                        # ooo
                                        for s in temporal_KG.entityType[tail0]:
                                            for t in temporal_KG.entityType[tail1]:
                                                for u in temporal_KG.entityType[tail2]:
                                                    key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                    if index_dict.__contains__(key):
                                                        index = index_dict[key]
                                                        all_relation_pairs.setdefault(index, []).append(s1)
                                                        all_relation_pairs.setdefault(index, []).append(l)
                                                        all_relation_pairs.setdefault(index, []).append(s2)
                                    else:
                                        # oox
                                        for s in temporal_KG.entityType[tail0]:
                                            for t in temporal_KG.entityType[tail1]:
                                                u = "null"
                                                key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                if index_dict.__contains__(key):
                                                    index = index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s1)
                                                    all_relation_pairs.setdefault(index, []).append(l)
                                                    all_relation_pairs.setdefault(index, []).append(s2)
                                        # oxx
                                        for s in temporal_KG.entityType[tail0]:
                                            t = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                        # xox
                                        for t in temporal_KG.entityType[tail1]:
                                            s = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                else:
                                    if temporal_KG.entityType.__contains__(tail2):
                                        # oxo
                                        for s in temporal_KG.entityType[tail0]:
                                            for u in temporal_KG.entityType[tail2]:
                                                t = "null"
                                                key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                if index_dict.__contains__(key):
                                                    index = index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s1)
                                                    all_relation_pairs.setdefault(index, []).append(l)
                                                    all_relation_pairs.setdefault(index, []).append(s2)
                                        # oxx
                                        for s in temporal_KG.entityType[tail0]:
                                            t = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                        # xxo
                                        for u in temporal_KG.entityType[tail2]:
                                            s = "null"
                                            t = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                    else:
                                        # oxx
                                        for s in temporal_KG.entityType[tail0]:
                                            t = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)
                            else:
                                if temporal_KG.entityType.__contains__(tail1):
                                    if temporal_KG.entityType.__contains__(tail2):
                                        # xoo
                                        for t in temporal_KG.entityType[tail1]:
                                            for u in temporal_KG.entityType[tail2]:
                                                s = "null"
                                                key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                                if index_dict.__contains__(key):
                                                    index = index_dict[key]
                                                    all_relation_pairs.setdefault(index, []).append(s1)
                                                    all_relation_pairs.setdefault(index, []).append(l)
                                                    all_relation_pairs.setdefault(index, []).append(s2)
                                        # xox
                                        for t in temporal_KG.entityType[tail1]:
                                            s = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)

                                        # xxo
                                        for u in temporal_KG.entityType[tail2]:
                                            s = "null"
                                            t = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                    else:
                                        # xox
                                        for t in temporal_KG.entityType[tail1]:
                                            s = "null"
                                            u = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)
                                else:
                                    if temporal_KG.entityType.__contains__(tail2):
                                        # xxo
                                        for u in temporal_KG.entityType[tail2]:
                                            s = "null"
                                            t = "null"
                                            key = r0 + "*" + s + "*" + r1 + "*" + t + "*" + r2 + "*" + u
                                            if index_dict.__contains__(key):
                                                index = index_dict[key]
                                                all_relation_pairs.setdefault(index, []).append(s1)
                                                all_relation_pairs.setdefault(index, []).append(l)
                                                all_relation_pairs.setdefault(index, []).append(s2)

            for j in all_relation_pairs.keys():
                    # step=2
                    for k in range(0,len(all_relation_pairs[j]),3):
                        vertex1 = all_relation_pairs[j][k]
                        vertex2 = all_relation_pairs[j][k+1]
                        one_hop_vertex = all_relation_pairs[j][k + 2]
                        one_hop_entity = one_hop_vertex.hasValue.getId()
                        start1 = vertex1.getStartTime()
                        end1 = vertex1.getEndTime()
                        start2 = vertex2.getStartTime()
                        end2 = vertex2.getEndTime()
                        head = v.getId()
                        relation=SOH_relations[j][1]
                        relation1 = vertex1.getId()

                        if vertex1.hasValue.isLiteral == True:
                            tail1 = vertex1.hasValue.getLabel()
                        else:
                            tail1 = vertex1.hasValue.getId()
                        relation2 = vertex2.getId()
                        if vertex2.hasValue.isLiteral == True:
                            tail2 = vertex2.hasValue.getLabel()
                        else:
                            tail2 = vertex2.hasValue.getId()

                        # choose which interval relation is
                        if SOH_relations[j][3].__eq__("before"):
                            if Interval_Relations.before(start1,end1,start2,end2)==-1:
                                inconsistent_pair = one_hop_constraints[j]+"\t"+head+"," \
                                                    + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                    end1) + "\t" + head  + ","+ relation+","+one_hop_entity+","+ relation2 + "," + tail2 + "," + str(start2) + "," + str(end2)
                                Conflict_Fact_set.append(inconsistent_pair)
                        if SOH_relations[j][3].__eq__("inverse_before"):
                            if Interval_Relations.before(start2, end2, start1, end1) == -1:
                                inconsistent_pair = one_hop_constraints[j] + "\t" + head + "," \
                                                    + relation2 + "," + tail2 + "," + str(start2) + "," + str(
                                    end2) + "\t" + head + "," + relation + ","+one_hop_entity+"," + relation1 + "," + tail1 + "," + str(
                                    start1) + "," + str(end1)
                                Conflict_Fact_set.append(inconsistent_pair)
                        elif SOH_relations[j][3].__eq__("include"):
                            if Interval_Relations.include(start1, end1, start2, end2) == -1:
                                inconsistent_pair = one_hop_constraints[j] + "\t" + head+"," \
                                                    + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                    end1) + "\t" + head + "," + relation + ","+one_hop_entity+","+ relation2 + "," + tail2 + "," + str(
                                    start2) + "," + str(end2)
                                Conflict_Fact_set.append(inconsistent_pair)
                        elif SOH_relations[j][3].__eq__("inverse_include"):
                            if Interval_Relations.include(start2, end2, start1, end1) == -1:
                                inconsistent_pair = one_hop_constraints[j] + "\t" + head+"," \
                                                    + relation2 + "," + tail2 + "," + str(start2) + "," + str(
                                    end2) + "\t" + head + "," + relation + ","+one_hop_entity+","+ relation1 + "," + tail1 + "," + str(
                                    start1) + "," + str(end1)
                                Conflict_Fact_set.append(inconsistent_pair)
                        elif SOH_relations[j][3].__eq__("start"):
                            if Interval_Relations.start(start1, end1, start2, end2) == -1:
                                inconsistent_pair = one_hop_constraints[j] + "\t" + head+"," \
                                                    + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                    end1) + "\t" + head + "," + relation + ","+one_hop_entity+","+ relation2 + "," + tail2 + "," + str(
                                    start2) + "," + str(end2)
                                Conflict_Fact_set.append(inconsistent_pair)
                        elif SOH_relations[j][3].__eq__("finish"):
                            if Interval_Relations.finish(start1, end1, start2, end2) == -1:
                                inconsistent_pair = one_hop_constraints[j] + "\t" + head+"," \
                                                    + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                    end1) + "\t" + head + "," + relation + ","+one_hop_entity+","+ relation2 + "," + tail2 + "," + str(
                                    start2) + "," + str(end2)
                                Conflict_Fact_set.append(inconsistent_pair)

    return Conflict_Fact_set

def Refined_Conflict_Detection(temporal_KG, Constraint_Set,filename,typefile):
    t0 = time.time()
    # if knowledgebase == "wikidata":
    #     type_file = open("our_resource/wikidata-entity-type-info.tsv", "r", encoding="UTF-8")
    # elif knowledgebase == "freebase":
    #     type_file = open("our_resource/freebase-entity-type-info.tsv", "r", encoding="UTF-8")
    type_file = open(typefile, "r", encoding="UTF-8")
    types = type_file.readlines()
    type_file.close()
    for line in types:
        elems = line.strip().split("\t")
        key = elems[0]
        for i in range(1, len(elems)):
            temporal_KG.entityType.setdefault(key, []).append(elems[i])
    t1 = time.time()
    print("read type cost time is:", t1 - t0, "s")
    Conflict_Set = []

    # functional constraints detection
    functional_constraints = []
    # inverse functional constraints detection
    inverse_functional_constraints = []
    # zero hop constraint detection
    zero_hop_constraints = []
    # one hop constraint detection
    one_hop_constraints = []


    for c in Constraint_Set:
        c1=c.split("|")[0]
        elem = c1.split(" ")
        if len(elem)==5:
            atom1 = elem[0]
            class_type1=elem[1]
            interval_relation = elem[2]
            atom2 = elem[3]
            class_type1=elem[4]
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
                elif edges1[0] != edges2[0] and len(edges1) == 1 and len(edges2) == 1:
                    zero_hop_constraints.append(c)

            elif anchor == "tail":
                inverse_functional_constraints.append(c)
        elif len(elem)==6:
                one_hop_constraints.append(c)
    st = time.time()
    Conflict_Set += Refined_Subgraph_Detection0(temporal_KG, functional_constraints)
    ed0 = time.time()
    print("Refined Detection0 cost time:", ed0 - st, "s")

    Conflict_Set += Refined_Subgraph_Detection1(temporal_KG, inverse_functional_constraints)
    ed1 = time.time()
    print("Refined Detection1 cost time:", ed1 - ed0, "s")

    Conflict_Set += Refined_Subgraph_Detection2(temporal_KG, zero_hop_constraints)
    ed2 = time.time()
    print("Refined Detection2 cost time:", ed2 - ed1, "s")

    Conflict_Set += Refined_Subgraph_Detection3(temporal_KG, one_hop_constraints)
    ed3 = time.time()
    print("Refined Detection4 cost time:", ed3 - ed2, "s")

    Detected_Constraint_Set = set(inverse_functional_constraints).union(set(functional_constraints))
    Detected_Constraint_Set = Detected_Constraint_Set.union(zero_hop_constraints)
    Detected_Constraint_Set = Detected_Constraint_Set.union(one_hop_constraints)
    print("Total Constraint number is", len(Constraint_Set))
    print("Detected Constraint number is", len(Detected_Constraint_Set))
    print("Constraints not detected yet:")
    Undetected_Constraint_Set = set()
    Undetected_Constraint_Set = set(Constraint_Set).difference(Detected_Constraint_Set)
    print(Undetected_Constraint_Set)

    conflict_file = open(filename + "_refined_conflict", "w", encoding="UTF-8")
    conflict_file.writelines("\n".join(Conflict_Set))
    return Conflict_Set

def test():
    Refined_Conflict_Detection()
    return

if __name__ == '__main__':
    test()