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

def Constraint_Check(temporal_KG,constraint):

    '''
    translate and execute constraint
    :param Conflict_temporal_facts:
    :param constraint:
    :return:
    '''
    # TODO
    # simplify_constraint()
    simple_constraint=constraint
    print(constraint)

    Conflict_Fact_set=[]
    elem=constraint.split(" ")
    atom1=elem[0]
    interval_relation=elem[1]
    atom2=elem[2]
    anchor=""
    if atom1.split(",")[0].__eq__(atom2.split(",")[0]):
        anchor="head"
    elif atom1.split(",")[2].__eq__(atom2.split(",")[2]):
        anchor="tail"
    else:
        print("anchor error")
        return []
    if anchor=="head":
        path1=atom1.split(",")[1]
        edges1=path1.split("*")
        # print(edges1[0])
        path2=atom2.split(",")[1]
        edges2=path2.split("*")
        # print(edges2[0])
        for i in temporal_KG.eVertexList:
            v=temporal_KG.eVertexList[i]
            if len(v.hasStatement)<2:
                continue
            else:
                edge1_set = set()
                edge2_set = set()
                exist1 = False
                exist2 = False
                for s in v.hasStatement:
                    if edges1[0].__eq__(s.getId()):
                        if len(edges1)==2:
                            for t in s.hasStatement:
                                if edges1[1].__eq__(t.getId()):
                                    edge1_set.add(t)
                                    exist1=True
                        else:
                            edge1_set.add(s)
                            exist1=True
                    if edges2[0].__eq__(s.getId()):
                        if len(edges2)==2:
                            for t in s.hasStatement:
                                if edges2[1].__eq__(t.getId()):
                                    edge2_set.add(t)
                                    exist2=True
                        else:
                            edge2_set.add(s)
                            exist2=True
                if exist1==True and exist2==True:
                    for edge1 in edge1_set:
                        for edge2 in edge2_set:
                            start1 = edge1.getStartTime()
                            end1 = edge1.getEndTime()
                            start2 = edge2.getStartTime()
                            end2 = edge2.getEndTime()
                            head=v.getId()
                            relation1=edge1.getId()
                            tail1=edge1.hasValue.getId()
                            relation2 = edge2.getId()
                            tail2 = edge2.hasValue.getId()
                            if interval_relation.__eq__("before"):
                                if Interval_Relations.before(start1,end1,start2,end2)==-1:
                                    inconsistent_pair = constraint+"\t"+head + "," + relation1 + "," + tail1 + "," + str(start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif interval_relation.__eq__("disjoint"):
                                if Interval_Relations.disjoint(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = constraint+"\t"+head + "," + relation1 + "," + tail1 + "," + str(
                                        start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif interval_relation.__eq__("include"):
                                if Interval_Relations.include(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = constraint+"\t"+head + "," + relation1 + "," + tail1 + "," + str(
                                        start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif interval_relation.__eq__("start"):
                                if Interval_Relations.start(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = constraint+"\t"+head + "," + relation1 + "," + tail1 + "," + str(
                                        start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)
                            elif interval_relation.__eq__("finish"):
                                if Interval_Relations.finish(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = constraint+"\t"+head + "," + relation1 + "," + tail1 + "," + str(
                                        start1) + "," + str(
                                        end1) + "\t" + head + "," + relation2 + "," + tail2 + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)


    else:
        print("anchor == tail")
        #anchor==tail
        # actually only disjoint has this situation
        path1 = atom1.split(",")[1]
        edges1 = path1.split("*")
        # print(edges1[0])
        path2 = atom2.split(",")[1]
        edges2 = path2.split("*")
        # print(edges2[0])
        if len(edges1) == 2 or len(edges2) == 2:
            print("constraint form has something wrong")
            print(constraint)
            return []
        for i in temporal_KG.eVertexList:
            v = temporal_KG.eVertexList[i]
            if len(v.bePointedTo) < 2:
                continue
            else:
                edge1_set = set()
                edge2_set = set()
                exist1 = False
                exist2 = False
                for s in v.bePointedTo:
                    if edges1[0].__eq__(s.getId()):
                        edge1_set.add(s)
                        exist1 = True
                    if edges2[0].__eq__(s.getId()):
                        edge2_set.add(s)
                        exist2 = True
                if exist1 == True and exist2 == True:
                    for edge1 in edge1_set:
                        for edge2 in edge2_set:
                            start1 = edge1.getStartTime()
                            end1 = edge1.getEndTime()
                            start2 = edge2.getStartTime()
                            end2 = edge2.getEndTime()
                            tail = v.getId()
                            relation1 = edge1.getId()
                            head1 = edge1.hasItem.getId()
                            relation2 = edge2.getId()
                            head2 = edge2.hasItem.getId()

                            if interval_relation.__eq__("disjoint"):
                                if Interval_Relations.disjoint(start1, end1, start2, end2) == -1:
                                    inconsistent_pair = constraint + "\t" + head1 + "," + relation1 + "," + tail + "," + str(
                                        start1) + "," + str(
                                        end1) + "\t" + head2 + "," + relation2 + "," + tail + "," + str(
                                        start2) + "," + str(end2)
                                    Conflict_Fact_set.append(inconsistent_pair)

    return Conflict_Fact_set

def Conflict_Detection(temporal_KG,Constraint_Set):
    # framework
    # Constraint_Mining.simplify_constraint()
    # file=open()
    Conflict_Set=[]
    for constraint in Constraint_Set:
        Conflict_Set+=Constraint_Check(temporal_KG,constraint)

    return Conflict_Set


if __name__ == '__main__':
    temporal_KG = Graph_Structure.Graph()
    # filename = "wikidata_dataset_tsv/rockit_wikidata_0_50k.tsv"
    filename = "all_relations_with_redundant_wikidata_alpha-1.2.tsv"
    # read_datasets.pre_process(filename)

    starttime0 = time.time()
    temporal_KG.ConstructThroughTsv(filename,100)
    endtime0 = time.time()
    runningtime0 = endtime0-starttime0
    print("ConstructThroughTsv running time:",runningtime0,"s")
    #
    # print(temporal_KG.num_eVertices)
    #
    constraint="a,P569,b,t1,t2 before a,P54,c,t3,t4"
    constraint = "a,P286,b,t1,t2 disjoint c,P54,b,t3,t4"
    starttime=time.time()
    conflicts=Constraint_Check(temporal_KG,constraint)
    for conflict in conflicts:
        print(conflict)
    endtime=time.time()
    runningtime=endtime-starttime
    print("running time:",runningtime,"s")