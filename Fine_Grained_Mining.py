import Constraint_Mining
import Conflict_Detection
import time
import Graph_Structure
import Interval_Relations

def Fine_Grained_Mining0(temporal_KG,Constraint_Set):

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
        FC_relations.append(FC_relation)
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
                if i1!=-1 or i2!=-1:
                    if index_dict.__contains__(r):
                        index=index_dict[r]
                        all_relation_pairs.setdefault(index, []).append(s)
                        #[[P54,e,e,e],[P286,e,e,e]]
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
                        tail1 = vertex1.hasValue.getId()
                        relation2 = vertex2.getId()
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

def Fine_Grained_Mining1(temporal_KG,Constraint_Set):

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
        IFC_relations.append(IFC_relation)
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
                if i1 != -1 or i2 != -1:
                    if index_dict.__contains__(r):
                        action+=1
                        index = index_dict[r]
                        all_relation_pairs.setdefault(index, []).append(s)
                        #[[P54,e,e,e],[P286,e,e,e]]
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

def Fine_Grained_Mining2(temporal_KG,Constraint_Set):

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
        ZHC_relation1 = c.split(" ")[0].split(",")[1]
        ZHC_relation2 = c.split(" ")[2].split(",")[1]
        ZHC_interval_relation=c.split(" ")[1]
        relation_pair=[ZHC_relation1,ZHC_relation2,ZHC_interval_relation]
        key=ZHC_relation1+"*"+ZHC_relation2
        index_dict[key]=count
        count+=1
        ZHC_relations.append(relation_pair)
        #[[P54,P569,before],[P54,P570,before]]
    all_relations=set()
    # print(ZHC_relations)
    for p in ZHC_relations:
        all_relations.add(p[0])
        all_relations.add(p[1])
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
                            key1=r1+"*"+r2
                            if index_dict.__contains__(key1):
                                index1=index_dict[key1]
                                all_relation_pairs.setdefault(index1, []).append(s1)
                                all_relation_pairs.setdefault(index1, []).append(s2)
                            key2=r2+"*"+r1
                            if index_dict.__contains__(key2):
                                # print("yes")
                                index2=index_dict[key2]
                                all_relation_pairs.setdefault(index2, []).append(s2)
                                all_relation_pairs.setdefault(index2, []).append(s1)

            # print(all_relation_pairs)
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

def Fine_Grained_Mining3(temporal_KG,Constraint_Set):

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
    print("len of constraint3:", len(first_one_hop_constraints))
    FOH_relations = []
    index_dict = {}
    count = 0
    for c in first_one_hop_constraints:
        FOH_relation0 = c.split(" ")[0].split(",")[1].split("*")[0]
        FOH_relation1 = c.split(" ")[0].split(",")[1].split("*")[1]
        FOH_relation2 = c.split(" ")[2].split(",")[1]
        FOH_interval_relation=c.split(" ")[1]
        relation_pair=[FOH_relation0,FOH_relation1,FOH_relation2,FOH_interval_relation]
        key = FOH_relation0 + "*" + FOH_relation1+"*"+FOH_relation2
        index_dict[key] = count
        count += 1
        FOH_relations.append(relation_pair)
        #[[P54,P26,P569,before],[P54,P570,before]]
    first_relations=set()
    second_relations=set()
    for p in FOH_relations:
        first_relations.add(p[0])
        first_relations.add(p[2])

    for p in FOH_relations:
        second_relations.add(p[1])

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
                    i1=l.getStartTime()
                    i2=l.getEndTime()
                    if i1!=-1 or i2!=-1:
                        if not second_relations.__contains__(l.getId()):
                            continue

                        for k in range(len(v.hasStatement)):
                            # two node cannot equal
                            if j == k:
                                continue
                            s2=v.hasStatement[k]
                            i3=s2.getStartTime()
                            i4=s2.getEndTime()

                            if i3!=-1 or i4!=-1:
                                # a quick filtering
                                if not first_relations.__contains__(s2.getId()):
                                    continue
                                r1 = s1.getId()
                                r2= l.getId()
                                r3= s2.getId()
                                key = r1+"*"+r2+"*"+r3
                                if index_dict.__contains__(key):
                                    index=index_dict[key]
                                    all_relation_pairs.setdefault(index, []).append(l)
                                    all_relation_pairs.setdefault(index, []).append(s2)

            for j in all_relation_pairs.keys():
                    # step=2
                    for k in range(0,len(all_relation_pairs[j]),2):
                        vertex1 = all_relation_pairs[j][k]
                        vertex2 = all_relation_pairs[j][k+1]
                        start1 = vertex1.getStartTime()
                        end1 = vertex1.getEndTime()
                        start2 = vertex2.getStartTime()
                        end2 = vertex2.getEndTime()
                        head = v.getId()
                        relation=FOH_relations[j][0]
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

def Fine_Grained_Mining4(temporal_KG,Constraint_Set):

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
    print("len of constraint4:", len(second_one_hop_constraints))
    SOH_relations = []
    index_dict = {}
    count = 0
    for c in second_one_hop_constraints:
        SOH_relation0 = c.split(" ")[0].split(",")[1]
        SOH_relation1 = c.split(" ")[2].split(",")[1].split("*")[0]
        SOH_relation2 = c.split(" ")[2].split(",")[1].split("*")[1]
        SOH_interval_relation=c.split(" ")[1]
        relation_pair=[SOH_relation0,SOH_relation1,SOH_relation2,SOH_interval_relation]
        key = SOH_relation0 + "*" + SOH_relation1 + "*" + SOH_relation2
        index_dict[key] = count
        count += 1
        SOH_relations.append(relation_pair)
        #[[P54,P569,before],[P54,P570,before]]
    first_relations=set()
    second_relations=set()
    for p in SOH_relations:
        first_relations.add(p[0])
        first_relations.add(p[1])

    for p in SOH_relations:
        second_relations.add(p[2])

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
                            r1 = s1.getId()
                            r2 = s2.getId()
                            r3 = l.getId()
                            key = r1 + "*" + r2 + "*" + r3
                            if index_dict.__contains__(key):
                                index = index_dict[key]
                                all_relation_pairs.setdefault(index, []).append(s1)
                                all_relation_pairs.setdefault(index, []).append(l)

            for j in all_relation_pairs.keys():
                    # step=2
                    for k in range(0,len(all_relation_pairs[j]),2):
                        vertex1 = all_relation_pairs[j][k]
                        vertex2 = all_relation_pairs[j][k+1]
                        start1 = vertex1.getStartTime()
                        end1 = vertex1.getEndTime()
                        start2 = vertex2.getStartTime()
                        end2 = vertex2.getEndTime()
                        head = v.getId()
                        relation=SOH_relations[j][1]
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

def Fine_Grained_Mining5(temporal_KG,Constraint_Set):

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
    print("len of constraint5:", len(both_one_hop_constraints))
    BOH_relations = []
    index_dict = {}
    count = 0
    for c in both_one_hop_constraints:
        BOH_relation = c.split(" ")[0].split(",")[1].split("*")[0]
        BOH_relation0 = c.split(" ")[0].split(",")[1].split("*")[1]
        BOH_relation1 = c.split(" ")[2].split(",")[1].split("*")[0]
        BOH_relation2 = c.split(" ")[2].split(",")[1].split("*")[1]
        BOH_interval_relation=c.split(" ")[1]
        relation_pair=[BOH_relation,BOH_relation0,BOH_relation1,BOH_relation2,BOH_interval_relation]
        key = BOH_relation+"*"+BOH_relation0 + "*" + BOH_relation1 + "*" + BOH_relation2
        index_dict[key] = count
        count += 1
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
                    i1=l.getStartTime()
                    i2=l.getEndTime()
                    if i1!=-1 or i2!=-1:
                        if not second_relations.__contains__(l.getId()):
                            continue

                        for k in range(j+1,len(v.hasStatement)):
                            s2=v.hasStatement[k]
                            # a quick filtering
                            if not first_relations.__contains__(s2.getId()):
                                continue
                            for m in s2.hasValue.hasStatement:
                                i3=m.getStartTime()
                                i4=m.getEndTime()
                                if i3!=-1 or i4!=-1:
                                    if not second_relations.__contains__(m.getId()):
                                        continue
                                    r1 = s1.getId()
                                    r2 = l.getId()
                                    r3 = s2.getId()
                                    r4 = m.getId()
                                    key1 = r1 + "*" + r2 + "*" + r3 +"*" + r4
                                    if index_dict.__contains__(key1):
                                        index1 = index_dict[key1]
                                        all_relation_pairs.setdefault(index1, []).append(l)
                                        all_relation_pairs.setdefault(index1, []).append(m)
                                    key2 = r3 +"*"+ r4 +"*"+ r1+"*"+r2
                                    if index_dict.__contains__(key2):
                                        index2 = index_dict[key2]
                                        all_relation_pairs.setdefault(index2, []).append(m)
                                        all_relation_pairs.setdefault(index2, []).append(l)

            for j in all_relation_pairs.keys():
                    # step=2
                    for k in range(0,len(all_relation_pairs[j]),2):
                        vertex1 = all_relation_pairs[j][k]
                        vertex2 = all_relation_pairs[j][k+1]
                        start1 = vertex1.getStartTime()
                        end1 = vertex1.getEndTime()
                        start2 = vertex2.getStartTime()
                        end2 = vertex2.getEndTime()
                        head = v.getId()
                        relation=BOH_relations[j][0]
                        relation1 = vertex1.getId()
                        tail1 = vertex1.hasValue.getId()
                        relation3=BOH_relations[j][2]
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

def fine_grained_mining(graph,knowledgebase,Constraint_Set):
    t0=time.time()
    if knowledgebase=="wikidata":
        type_file=open("wikidata-entity-type-info.tsv","r",encoding="UTF-8")
    elif knowledgebase=="freebase":
        type_file=open("freebase-entity-type-info.tsv","r",encoding="UTF-8")

    types=type_file.readlines()
    type_file.close()
    for line in types:
        elems=line.strip().split("\t")
        key=elems[0]
        for i in range(1,len(elems)):
            graph.entityType.setdefault(key, []).append(elems[i])
    t1=time.time()
    print("read type cost time is:",t1-t0,"s")

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

    Fine_Grained_Constraint_Set=[]
    st = time.time()
    Fine_Grained_Constraint_Set += Fine_Grained_Mining0(graph, functional_constraints)
    ed0 = time.time()
    print("Fine Grained Constraint Set0 cost time:", ed0 - st, "s")
    Fine_Grained_Constraint_Set += Fine_Grained_Mining1(graph, inverse_functional_constraints)
    ed1 = time.time()
    print("Fine Grained Constraint Set1 cost time:", ed1 - ed0, "s")
    Fine_Grained_Constraint_Set += Fine_Grained_Mining2(graph, zero_hop_constraints)
    ed2 = time.time()
    print("Fine Grained Constraint Set2 cost time:", ed2 - ed1, "s")
    Fine_Grained_Constraint_Set += Fine_Grained_Mining3(graph, first_one_hop_constraints)
    ed3 = time.time()
    print("Fine Grained Constraint Set3 cost time:", ed3 - ed2, "s")
    Fine_Grained_Constraint_Set += Fine_Grained_Mining4(graph, second_one_hop_constraints)
    ed4 = time.time()
    print("Fine Grained Constraint Set4 cost time:", ed4 - ed3, "s")
    Fine_Grained_Constraint_Set += Fine_Grained_Mining5(graph, both_one_hop_constraints)
    ed5 = time.time()
    print("Fine Grained Constraint Set5 cost time:", ed5 - ed4, "s")

    Post_Processed_Constraint_Set = set(inverse_functional_constraints).union(set(functional_constraints))
    Post_Processed_Constraint_Set = Post_Processed_Constraint_Set.union(zero_hop_constraints)
    Post_Processed_Constraint_Set = Post_Processed_Constraint_Set.union(first_one_hop_constraints)
    Post_Processed_Constraint_Set = Post_Processed_Constraint_Set.union(second_one_hop_constraints)
    Post_Processed_Constraint_Set = Post_Processed_Constraint_Set.union(both_one_hop_constraints)
    print("Total Constraint number is", len(Constraint_Set))
    print("Fine Grained Mining Constraint number is", len(Post_Processed_Constraint_Set))
    print("Constraints not fine grained mining yet:")
    UnPost_Processed_Constraint_Set = set()
    UnPost_Processed_Constraint_Set = set(Constraint_Set).difference(Post_Processed_Constraint_Set)
    print(UnPost_Processed_Constraint_Set)

    return Fine_Grained_Constraint_Set

def test():
    temporal_KG = Graph_Structure.Graph()
    knowledgebase="wikidata"
    # knowledgebase = "freebase"
    filename = "wikidata_dataset_tsv/rockit_wikidata_0_50k.tsv"
    # filename = "all_relations_with_redundant_wikidata_alpha-1.2.tsv"
    # filename="all_relations_with_redundant_freebase_alpha-1.1.tsv"
    # read_datasets.pre_process(filename)

    starttime0 = time.time()
    temporal_KG.ConstructThroughTsv(filename, knowledgebase, 100)
    endtime0 = time.time()
    runningtime0 = endtime0 - starttime0
    print("ConstructThroughTsv running time:", runningtime0, "s")


    # print("entity vertex number is:",temporal_KG.num_eVertices)
    constraint_filename = "all_relations_with_redundant_wikidata_alpha-1.2.tsv_rules"
    # constraint_filename = "all_relations_with_redundant_freebase_alpha-1.1.tsv_rules"
    # constraint_filename="constraint_list_wikidata.txt"
    constraint_set = Conflict_Detection.read_constraints(constraint_filename)
    starttime = time.time()
    conflicts = fine_grained_mining(temporal_KG, "wikidata",constraint_set)
    endtime = time.time()
    runningtime = endtime - starttime
    print("Conflict detection running time:", runningtime, "s")
    return 0

if __name__ == '__main__':
    test()