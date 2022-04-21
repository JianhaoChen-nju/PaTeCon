import read_datasets
import Interval_Relations
import Graph_Structure






def temporal_representation_constraint(graph):
    Conflicting_facts = []
    for i in graph.eVertexList:
        for j in graph.eVertexList[i].hasStatement:
            head = graph.eVertexList[i].getId()
            relation = j.getId()
            tail = j.hasValue.getId()
            start = j.getStartTime()
            end = j.getEndTime()
            weight = j.getWeight()
            truth = j.getTruth()
            fact = [head, relation, tail, start, end, weight, truth]
            if start > end:
                Conflicting_facts.append(fact)

    return Conflicting_facts


def functional_mining(graph):
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets
    print("functional_mining")
    threshold = 0.8
    functional_constraint = []
    consistent_subsets = 0
    total_subsets = 0
    for relation in graph.relationList:
        confidence = 0
        for i in graph.eVertexList:
            consistent = True
            hasRelation = False
            head=graph.eVertexList[i].getId()
            for j in range(len(graph.eVertexList[i].hasStatement)):
                r = graph.eVertexList[i].hasStatement[j].getId()
                tail1 = graph.eVertexList[i].hasStatement[j].hasValue.getId()
                if relation.__eq__(r):
                    hasRelation = True

                    i1 = graph.eVertexList[i].hasStatement[j].getStartTime()
                    i2 = graph.eVertexList[i].hasStatement[j].getEndTime()
                    for k in range(j+1, len(graph.eVertexList[i].hasStatement)):
                        r1 = graph.eVertexList[i].hasStatement[k].getId()
                        tail2 = graph.eVertexList[i].hasStatement[k].hasValue.getId()
                        if relation.__eq__(r1):
                            i3 = graph.eVertexList[i].hasStatement[k].getStartTime()
                            i4 = graph.eVertexList[i].hasStatement[k].getEndTime()
                            if Interval_Relations.disjoint(i1, i2, i3, i4):
                                continue
                            else:
                                consistent=False
                                # print(head,tail1,i1,i2,tail2,i3,i4)
            if hasRelation:
                total_subsets += 1
                if consistent:
                    consistent_subsets += 1
        confidence = consistent_subsets * 1.0 / total_subsets
        print(relation, consistent_subsets,total_subsets,confidence)
        if confidence > 0.95:
            constraint="(a," + relation + ",b,t1,t2) & (a,"+relation+",c,t3,t4) => disjoint(t1,t2,t3,t4)"
            print(constraint)
            functional_constraint.append(constraint)
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
    consistent_subsets = 0
    total_subsets = 0
    for relation in graph.relationList:
        confidence = 0
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
                    hasRelation = True
                    i1 = graph.eVertexList[i].bePointedTo[j].getStartTime()
                    i2 = graph.eVertexList[i].bePointedTo[j].getEndTime()
                    for k in range(j+1, len(graph.eVertexList[i].bePointedTo)):
                        r1 = graph.eVertexList[i].bePointedTo[k].getId()
                        head2 = graph.eVertexList[i].bePointedTo[k].hasItem.getId()
                        if relation.__eq__(r1):
                            i3 = graph.eVertexList[i].bePointedTo[k].getStartTime()
                            i4 = graph.eVertexList[i].bePointedTo[k].getEndTime()
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
        confidence = consistent_subsets * 1.0 / total_subsets
        print(relation, consistent_subsets,total_subsets,confidence)
        if confidence > 0.95:
            constraint = "(a," + relation + ",b,t1,t2) & (c," + relation + ",b,t3,t4) => disjoint(t1,t2,t3,t4)"
            print(constraint)
            inverse_functional_constraint.append(constraint)

        # x relation1 y & x relation2 z t1(t1=开始结束时间取平均数) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1

    return inverse_functional_constraint



def Constraint_Mining(graph):
    '''

    :param utkg:
    :return:
    '''
    Constraint_list = []
    Constraint_list += functional_mining(graph)
    Constraint_list += inverse_functional_mining(graph)

    print(Constraint_list)
    return Constraint_list

def single_temporal_span(graph):
    print("single temporal span mining")
    Probability_distributions={}



    return Probability_distributions


def binary_temporal_span(graph):
    print("single temporal span mining")
    Probability_distributions = {}

    return Probability_distributions

def Soft_Constraint_Mining(graph):
    print("Soft temporal span mining")
    Soft_Constraint_list=[]
    single_temporal_span(graph)

    return Soft_Constraint_list


if __name__ == '__main__':
    # utkg=read_datasets.read_file("footballdb_tsv/player_team_year_rockit_0.tsv")
    # functional_detection(utkg)
    g = Graph_Structure.Graph()
    # filename="footballdb_tsv/player_team_year_rockit_0.tsv"
    # filename = "wikidata_dataset_tsv/rockit_wikidata_0_50k.tsv"
    filename = "required_relations_alpha-1.tsv"
    g.ConstructThroughTsv(filename)

    print(g.num_eVertices)
    print(g.num_sVertices)
    print(len(g.relationList))
    print(g.relationList)
    print("-------------------")
    # g.iterateOverGraph()
    # conflicting_type1_facts = temporal_representation_constraint(g)
    # print("temporal_representation_constraint",len(conflicting_type1_facts))
    # Constraint_Mining(g)
    # Soft_Constraint_Mining(g)
    # functional_mining(g)
    # inverse_functional_mining(g)
