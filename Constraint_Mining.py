import read_datasets
import Interval_Relations
import Graph_Structure
import time
import Conflict_Detection

confidence_threshold=0.95
truncate_threshold=0.95
support_threshold=0

def functional_mining(graph):
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets
    print("functional_mining")
    threshold = 0.8
    functional_constraint = []
    # to delete
    output_filename="functional_conflict.txt"

    for relation in graph.relationList:
        confidence = 0
        total_subsets = 0
        consistent_subsets = 0
        inconsistent_set=[]
        for i in graph.eVertexList:
            consistent = True
            hasRelation = False
            head=graph.eVertexList[i].getId()
            for j in range(len(graph.eVertexList[i].hasStatement)):
                r = graph.eVertexList[i].hasStatement[j].getId()
                tail1 = graph.eVertexList[i].hasStatement[j].hasValue.getId()
                if relation.__eq__(r):

                    i1 = graph.eVertexList[i].hasStatement[j].getStartTime()
                    i2 = graph.eVertexList[i].hasStatement[j].getEndTime()
                    # if not all null
                    if i1!=-1 or i2!=-1:
                        hasRelation =True
                        for k in range(j+1, len(graph.eVertexList[i].hasStatement)):
                            r1 = graph.eVertexList[i].hasStatement[k].getId()
                            tail2 = graph.eVertexList[i].hasStatement[k].hasValue.getId()
                            if relation.__eq__(r1):
                                i3 = graph.eVertexList[i].hasStatement[k].getStartTime()
                                i4 = graph.eVertexList[i].hasStatement[k].getEndTime()
                                # if not all null
                                if i3!=-1 or i4!=-1:
                                    if Interval_Relations.disjoint(i1, i2, i3, i4)==-1:
                                        consistent=False
                                        # to delete
                                        inconsistent_pair=head+","+relation+","+tail1+","+str(i1)+","+str(i2)+"\t"+head+","+relation+","+tail2+","+str(i3)+","+str(i4)
                                        inconsistent_set.append(inconsistent_pair)
                                        # print(head,tail1,i1,i2,tail2,i3,i4)
            if hasRelation:
                total_subsets += 1
                if consistent:
                    consistent_subsets += 1
        if total_subsets==0:
            confidence=0
        else:
            confidence = consistent_subsets * 1.0 / total_subsets
        print(relation, consistent_subsets,total_subsets,confidence)
        if confidence > confidence_threshold and consistent_subsets>support_threshold:
            constraint="(a," + relation + ",b,t1,t2) & (a,"+relation+",c,t3,t4) => disjoint(t1,t2,t3,t4)|"+str(confidence)
            print(constraint)
            functional_constraint.append(constraint)

            # to delete
            output_file=open(output_filename,"a",encoding="utf-8")
            output_file.write(constraint)
            output_file.write("\n")
            output_file.writelines("\n".join(inconsistent_set))
    # x relation1 y & x relation2 z t1(t1=开始结束时间取平均数) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1
    return functional_constraint

def inverse_functional_mining(graph):
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets
    print("inverse_functional_mining")
    threshold = 0.8
    inverse_functional_constraint = []

    for relation in graph.relationList:
        confidence = 0
        total_subsets = 0
        consistent_subsets = 0
        for i in graph.eVertexList:
            consistent = True
            hasRelation = False
            tail = graph.eVertexList[i].getId()
            conflict_vector=[]
            for j in range(len(graph.eVertexList[i].bePointedTo)):
                conflict_vector.append(1)
            for j in range(len(graph.eVertexList[i].bePointedTo)):
                r = graph.eVertexList[i].bePointedTo[j].getId()
                head1 = graph.eVertexList[i].bePointedTo[j].hasItem.getId()
                if relation.__eq__(r):
                    i1 = graph.eVertexList[i].bePointedTo[j].getStartTime()
                    i2 = graph.eVertexList[i].bePointedTo[j].getEndTime()
                    if i1!=-1 or i2!=-1:
                        hasRelation =True
                    for k in range(j+1, len(graph.eVertexList[i].bePointedTo)):
                        r1 = graph.eVertexList[i].bePointedTo[k].getId()
                        head2 = graph.eVertexList[i].bePointedTo[k].hasItem.getId()
                        if relation.__eq__(r1):
                            i3 = graph.eVertexList[i].bePointedTo[k].getStartTime()
                            i4 = graph.eVertexList[i].bePointedTo[k].getEndTime()
                            if i1 != -1 or i2 != -1:
                                hasRelation = True
                                if Interval_Relations.disjoint(i1, i2, i3, i4):
                                    continue
                                else:
                                    consistent = False
                                    conflict_vector[j]=0
                                    conflict_vector[k]=0
                                    # print(tail,head1, i1, i2, head2, i3, i4)
            if hasRelation:
                total_subsets += 1
                if consistent:
                    consistent_subsets += 1

                # TODO whether use this strategy
                # else:
                #     # we compute a fraction
                #     consistent_degree=0
                #     for j in range(len(conflict_vector)):
                #         consistent_degree+=conflict_vector[j]
                #     consistent_degree=consistent_degree*1.0/len(conflict_vector)
                #     consistent_subsets+=consistent_degree
        if total_subsets==0:
            confidence=0
        else:
            confidence = consistent_subsets * 1.0 / total_subsets
        print(relation, consistent_subsets,total_subsets,confidence)
        if confidence > confidence_threshold and consistent_subsets>support_threshold:
            constraint = "(a," + relation + ",b,t1,t2) & (c," + relation + ",b,t3,t4) => disjoint(t1,t2,t3,t4)|"+str(confidence)
            print(constraint)
            inverse_functional_constraint.append(constraint)

        # x relation1 y & x relation2 z t1(t1=开始结束时间取平均数) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1

    return inverse_functional_constraint


def Single_Entity_Temporal_Order(graph):
    # transitivity
    # before include start finish overlap disjoint
    Single_Entity_Temporal_Order_Constraint=[]

    print("Single Entity Temporal Order Mining")
    threshold = 0.95
    # to delete
    output_filename = "order_conflict.txt"
    for index in range(len(graph.relationList)):
        relation1 = graph.relationList[index]
        for index2 in range(len(graph.relationList)):
            relation2 = graph.relationList[index2]
            if relation2.__eq__(relation1):
                # print("yes")
                continue
            before_consistent_subsets = 0
            include_consistent_subsets = 0
            start_consistent_subsets=0
            finish_consistent_subsets=0
            total_subsets = 0
            # above we select 2 relations
            span_list = []
            inconsistent_set = []
            for i in graph.eVertexList:
                # this is a subset
                hasRelation1 = False
                hasRelation2 = False
                before_consistent = True
                include_consistent = True
                start_consistent = True
                finish_consistent = True
                head = graph.eVertexList[i].getId()
                for j in range(len(graph.eVertexList[i].hasStatement)):
                    r1 = graph.eVertexList[i].hasStatement[j].getId()
                    if relation1.__eq__(r1):

                        start1 = graph.eVertexList[i].hasStatement[j].getStartTime()
                        end1 = graph.eVertexList[i].hasStatement[j].getEndTime()
                        tail1 = graph.eVertexList[i].hasStatement[j].hasValue.getId()
                        if start1 != -1 or end1 != -1:
                            hasRelation1 = True
                            for k in range(len(graph.eVertexList[i].hasStatement)):
                                r2 = graph.eVertexList[i].hasStatement[k].getId()
                                if relation2.__eq__(r2):
                                    start2 = graph.eVertexList[i].hasStatement[k].getStartTime()
                                    end2 = graph.eVertexList[i].hasStatement[k].getEndTime()
                                    tail2 = graph.eVertexList[i].hasStatement[k].hasValue.getId()
                                    if start2 != -1 or end2 != -1:
                                        hasRelation2 = True
                                        # before relation
                                        if Interval_Relations.before(start1,end1,start2,end2)==-1:
                                            before_consistent=False
                                            # to delete
                                            inconsistent_pair =  head + "," + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                                end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                                start2) + "," + str(end2)
                                            inconsistent_set.append(inconsistent_pair)

                                        # include relation t1 include t2 i.e. t2 during t1
                                        if Interval_Relations.include(start1,end1,start2,end2)==-1:
                                            include_consistent=False

                                        # start relation
                                        if Interval_Relations.start(start1, end1, start2, end2) == -1:
                                            start_consistent = False

                                        # before relation
                                        if Interval_Relations.finish(start1, end1, start2, end2) == -1:
                                            finish_consistent = False

                if hasRelation1==True and hasRelation2==True:
                    total_subsets += 1

                    if before_consistent==True:
                        before_consistent_subsets +=1
                    elif include_consistent==True:
                        include_consistent_subsets +=1
                    elif start_consistent==True:
                        start_consistent_subsets +=1
                    elif finish_consistent==True:
                        finish_consistent_subsets +=1

            if total_subsets==0:
                before_confidence=0
                include_confidence=0
                start_confidence=0
                finish_confidence=0
            else:
                before_confidence = before_consistent_subsets * 1.0 / total_subsets
                include_confidence = include_consistent_subsets * 1.0 / total_subsets
                start_confidence = start_consistent_subsets * 1.0 / total_subsets
                finish_confidence = finish_consistent_subsets * 1.0 / total_subsets
            if before_consistent_subsets!=0:
                print("before relation",relation1, relation2, before_consistent_subsets, total_subsets, before_confidence)
            if include_consistent_subsets!=0:
                print("include relation",relation1, relation2, include_consistent_subsets, total_subsets, include_confidence)
            if start_consistent_subsets!=0:
                print("start relation", relation1, relation2, start_consistent_subsets, total_subsets,start_confidence)
            if finish_consistent_subsets!=0:
                print("finish relation", relation1, relation2, finish_consistent_subsets, total_subsets,finish_confidence)

            if before_confidence > confidence_threshold and before_consistent_subsets>support_threshold:
                constraint = "(a," + relation1 + ",b,t1,t2) & (a," + relation2 + ",c,t3,t4) => before(t1,t2,t3,t4)|"+str(before_confidence)
                print(constraint)
                Single_Entity_Temporal_Order_Constraint.append(constraint)

                # to delete
                output_file = open(output_filename, "a", encoding="utf-8")
                output_file.write(constraint)
                output_file.write("\n")
                output_file.writelines("\n".join(inconsistent_set))
            elif include_confidence > confidence_threshold and include_consistent_subsets>support_threshold:
                constraint = "(a," + relation1 + ",b,t1,t2) & (a," + relation2 + ",c,t3,t4) => include(t1,t2,t3,t4)|"+str(include_confidence)
                print(constraint)
                Single_Entity_Temporal_Order_Constraint.append(constraint)
            elif start_confidence > confidence_threshold and start_consistent_subsets>support_threshold:
                constraint = "(a," + relation1 + ",b,t1,t2) & (a," + relation2 + ",c,t3,t4) => start(t1,t2,t3,t4)|"+str(start_confidence)
                print(constraint)
                Single_Entity_Temporal_Order_Constraint.append(constraint)
            elif  finish_confidence > confidence_threshold and finish_consistent_subsets>support_threshold:
                constraint = "(a," + relation1 + ",b,t1,t2) & (a," + relation2 + ",c,t3,t4) => finish(t1,t2,t3,t4)|"+str(finish_confidence)
                print(constraint)
                Single_Entity_Temporal_Order_Constraint.append(constraint)
    return Single_Entity_Temporal_Order_Constraint

def Mutiple_Entity_Temporal_Order(graph):
    Mutiple_Entity_Temporal_Order_Constraint = []

    print("Mutiple Entity Temporal Order Mining")
    threshold = 0.95

    for index in range(len(graph.relationList)):
        relation1 = graph.relationList[index]
        for index1 in range(len(graph.relationList)):
            one_hop=graph.relationList[index1]

            if one_hop.__eq__(relation1):
                continue
            for index2 in range(len(graph.relationList)):
                relation2 = graph.relationList[index2]
                if relation2.__eq__(one_hop):
                    # print("yes")
                    continue
                before_consistent_subsets = 0
                inverse_before_consistent_subsets = 0
                include_consistent_subsets = 0
                inverse_include_consistent_subsets = 0
                start_consistent_subsets = 0
                finish_consistent_subsets = 0
                total_subsets = 0
                # above we select 2 relations
                span_list = []
                for i in graph.eVertexList:
                    # entity1
                    # this is a subset
                    hasRelation1 = False
                    hasOneHop= False
                    hasRelation2 = False
                    before_consistent = True
                    inverse_before_consistent = True
                    include_consistent = True
                    inverse_include_consistent = True
                    start_consistent = True
                    finish_consistent = True

                    for h in range(len(graph.eVertexList[i].hasStatement)):
                        rhop = graph.eVertexList[i].hasStatement[h].getId()
                        if one_hop.__eq__(rhop):
                            hasOneHop=True
                    if hasOneHop==False:
                        #prune
                        continue

                    for j in range(len(graph.eVertexList[i].hasStatement)):
                        r1 = graph.eVertexList[i].hasStatement[j].getId()
                        if relation1.__eq__(r1):
                            hasRelation1 = True
                            start1 = graph.eVertexList[i].hasStatement[j].getStartTime()
                            end1 = graph.eVertexList[i].hasStatement[j].getEndTime()

                            for h in range(len(graph.eVertexList[i].hasStatement)):
                                rhop = graph.eVertexList[i].hasStatement[h].getId()
                                if one_hop.__eq__(rhop):
                                    entity2=graph.eVertexList[i].hasStatement[h].hasValue

                                    for k in range(len(entity2.hasStatement)):
                                        r2 = entity2.hasStatement[k].getId()
                                        if relation2.__eq__(r2):

                                            hasRelation2 = True
                                            start2 = entity2.hasStatement[k].getStartTime()
                                            end2 = entity2.hasStatement[k].getEndTime()
                                            # if rhop.__eq__("father"):
                                            #     print("yes")
                                            #     print(start1,end1,start2,end2)

                                            # before relation
                                            if Interval_Relations.before(start1, end1, start2, end2) == -1:
                                                before_consistent = False

                                            # symmetric
                                            #inverse relation
                                            if Interval_Relations.before(start2,end2,start1,end1) == -1:
                                                inverse_before_consistent = False

                                            # include relation t1 include t2 i.e. t2 during t1
                                            if Interval_Relations.include(start1, end1, start2, end2) == -1:
                                                include_consistent = False

                                            # for symmetric
                                            if Interval_Relations.include(start2,end2,start1,end1) == -1:
                                                inverse_include_consistent = False

                                            # start relation
                                            if Interval_Relations.start(start1, end1, start2, end2) == -1:
                                                start_consistent = False

                                            # before relation
                                            if Interval_Relations.finish(start1, end1, start2, end2) == -1:
                                                finish_consistent = False

                    if hasRelation1 == True and hasRelation2 == True and hasOneHop==True:
                        total_subsets += 1
                        if before_consistent == True:
                            before_consistent_subsets += 1
                        elif inverse_before_consistent == True:
                            inverse_before_consistent_subsets +=1
                        elif include_consistent == True:
                            include_consistent_subsets += 1
                        elif inverse_include_consistent == True:
                            inverse_include_consistent_subsets += 1
                        elif start_consistent == True:
                            start_consistent_subsets += 1
                        elif finish_consistent == True:
                            finish_consistent_subsets += 1

                if total_subsets == 0:
                    before_confidence = 0
                    inverse_before_confidence = 0
                    include_confidence = 0
                    inverse_include_confidence = 0
                    start_confidence = 0
                    finish_confidence = 0
                else:
                    before_confidence = before_consistent_subsets * 1.0 / total_subsets
                    inverse_before_confidence = inverse_before_consistent_subsets * 1.0 / total_subsets
                    include_confidence = include_consistent_subsets * 1.0 / total_subsets
                    inverse_include_confidence = inverse_include_consistent_subsets * 1.0 /total_subsets
                    start_confidence = start_consistent_subsets * 1.0 / total_subsets
                    finish_confidence = finish_consistent_subsets * 1.0 / total_subsets
                if before_consistent_subsets != 0:
                    print("before relation", relation1, one_hop, relation2, before_consistent_subsets, total_subsets, before_confidence)
                if inverse_before_consistent_subsets != 0:
                    print("inverse before relation", relation1, one_hop, relation2, inverse_before_consistent_subsets, total_subsets, inverse_before_confidence)
                if include_consistent_subsets != 0:
                    print("include relation", relation1, one_hop, relation2, include_consistent_subsets, total_subsets,include_confidence)
                if inverse_include_consistent_subsets != 0:
                    print("inverse include relation", relation1, one_hop, relation2, inverse_include_consistent_subsets, total_subsets, inverse_include_confidence)
                if start_consistent_subsets != 0:
                    print("start relation", relation1, one_hop, relation2, start_consistent_subsets, total_subsets, start_confidence)
                if finish_consistent_subsets != 0:
                    print("finish relation", relation1, one_hop, relation2, finish_consistent_subsets, total_subsets,finish_confidence)

                if before_confidence > confidence_threshold and before_consistent_subsets>support_threshold:
                    constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => before(t1,t2,t5,t6)|"+str(before_confidence)
                    print(constraint)
                    Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
                elif inverse_before_confidence > confidence_threshold and inverse_before_consistent_subsets>support_threshold:
                    constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => before(t5,t6,t1,t2)|"+str(inverse_before_confidence)
                    print(constraint)
                    Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
                elif include_confidence > confidence_threshold and include_consistent_subsets>support_threshold:
                    constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => include(t1,t2,t5,t6)|"+str(include_confidence)
                    print(constraint)
                    Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
                elif inverse_include_confidence > confidence_threshold and inverse_include_consistent_subsets>support_threshold:
                    constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => include(t5,t6,t1,t2)|"+str(inverse_include_confidence)
                    print(constraint)
                    Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
                elif start_confidence >confidence_threshold and start_consistent_subsets>support_threshold:
                    constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => start(t1,t2,t5,t6)|"+str(start_confidence)
                    print(constraint)
                    Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
                elif finish_confidence > confidence_threshold and finish_consistent_subsets>support_threshold:
                    constraint = "(a," + relation1 + ",b,t1,t2) & (a," + one_hop + ",c,t3,t4) & (c," + relation2 + ",d,t5,t6) => finish(t1,t2,t5,t6)|"+str(finish_confidence)
                    print(constraint)
                    Mutiple_Entity_Temporal_Order_Constraint.append(constraint)
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
    t=head.replace(" ","").split("(")[1].split(",")[0]

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
                            print("add")
                            print(constraint, "&", constraint2, "=>", transitive_constraint)
                            transitive_constraint_set.append(transitive_constraint)
            if interval_relation1.__eq__("before") and interval_relation2.__eq__("start"):
                transfer_confidence = num_confidence * num_confidence2
                transitive_constraint = fact1 + " " + "before" + " " + fact4+"|"+str(transfer_confidence)
                if transfer_confidence > truncate_threshold:
                    if Set_Include(transitive_constraint, Old_Transitive_closure_set) == False:
                        print("add")
                        print(constraint, "&", constraint2, "=>", transitive_constraint)
                        transitive_constraint_set.append(transitive_constraint)
            elif interval_relation1.__eq__("before") and interval_relation2.__eq__("include"):
                transfer_confidence = num_confidence * num_confidence2
                transitive_constraint = fact1 + " " + "before" + " " + fact4+"|"+str(transfer_confidence)
                if transfer_confidence > truncate_threshold:
                    if Set_Include(transitive_constraint, Old_Transitive_closure_set) == False:
                        print("add")
                        print(constraint, "&", constraint2, "=>", transitive_constraint)
                        transitive_constraint_set.append(transitive_constraint)
            elif interval_relation1.__eq__("finish") and interval_relation2.__eq__("before"):
                transfer_confidence = num_confidence * num_confidence2
                transitive_constraint = fact1 + " " + "before" + " " + fact4+"|"+str(transfer_confidence)
                if transfer_confidence > truncate_threshold:
                    if Set_Include(transitive_constraint, Old_Transitive_closure_set) == False:
                        print("add")
                        print(constraint, "&", constraint2, "=>", transitive_constraint)
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
                            print("add")
                            print(constraint, "&", constraint2, "=>", transitive_constraint)
                            transitive_constraint_set.append(transitive_constraint)

            if interval_relation1.__eq__("include") and interval_relation2.__eq__("before"):
                transfer_confidence = num_confidence * num_confidence2
                transitive_constraint = fact2 + " " + "before" + " " + fact4+"|"+str(transfer_confidence)
                if transfer_confidence > truncate_threshold:
                    if Set_Include(transitive_constraint, Old_Transitive_closure_set) == False:
                        print("add")
                        print(constraint, "&", constraint2, "=>", transitive_constraint)
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
    Constraint_list += functional_mining(graph)
    Constraint_list += inverse_functional_mining(graph)
    Constraint_list += Single_Entity_Temporal_Order(graph)
    Constraint_list += Mutiple_Entity_Temporal_Order(graph)
    end=time.time()
    print("running time is:",end-start,"s")
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

    filename = "wikidata_dataset_tsv/rockit_wikidata_0_50k.tsv"
    # filename = "all_relations_with_redundant_wikidata_alpha-1.2.tsv"
    read_datasets.pre_process(filename)
    g.ConstructThroughTsv(filename, 100)

    print("number of entity vertex is ", g.num_eVertices)
    print("number of statement vertex is", g.num_sVertices)
    print(len(g.relationList))
    print(g.relationList)
    print("-------------------")
    # g.iterateOverGraph()

    Constraint_Set = Constraint_Mining(g)
    # Soft_Constraint_Mining(g)
    transitive_constraint_set = transitive_closure(Constraint_Set)
    for constraint in transitive_constraint_set:
        print(constraint)

    # write rule file
    write_filename = filename + "_rules"
    write_file = open(write_filename, "w", encoding="utf-8")
    write_file.writelines("\n".join(transitive_constraint_set))

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