import read_datasets
import Interval_Relations

# eVertex: entity Vertex
# sVertex: statement Vertex

class eVertex:
    def __init__(self, key, label="ToAdd"):
        self.id = key
        self.label = label
        self.bePointedTo=[]
        self.hasStatement = []

    def addEdge(self, nbr):
        self.hasStatement.append(nbr)
        nbr.hasItem = self

    def __str__(self):
        return str(self.id) + ' hasStatement: ' + str([x.id for x in self.hasStatement])

    def hasStatement(self):
        return self.hasStatement

    def getId(self):
        return self.id

    def getLabel(self):
        return self.label


class sVertex:
    def __init__(self, key, begin, end, weight=1, truth=True):
        self.id = key
        self.hasItem = None
        self.hasValue = None
        self.begin = begin
        self.end = end
        self.weight = weight
        self.truth = truth

    def addEdge(self, nbr):
        self.hasValue = nbr
        nbr.bePointedTo.append(self)

    def __str__(self):
        return str(self.id) + ' hasValue: ' + self.hasValue


    def hasItem(self):
        return self.hasItem

    def hasValue(self):
        return self.hasValue

    def getId(self):
        return self.id

    def getBeginTime(self):
        return self.begin

    def getEndTime(self):
        return self.end

    def getTruth(self):
        return self.truth

    def getWeight(self):
        return self.weight


class Graph:
    def __init__(self):
        self.eVertexList = {}
        self.relationList = []
        self.sVertexList = {}
        self.num_eVertices = 0
        self.num_sVertices = 0

    def add_eVertex(self, key):
        if key in self.eVertexList:
            return self.get_eVertex(key)
        self.num_eVertices = self.num_eVertices + 1
        newVertex = eVertex(key)
        self.eVertexList[key] = newVertex
        return newVertex

    def add_sVertex(self, key, begin, end, weight, truth=True):
        if key not in self.relationList:
            self.relationList.append(key)
        self.num_sVertices = self.num_sVertices + 1
        newVertex = sVertex(key, begin, end, weight, truth)
        # value of dic is a list
        self.sVertexList.setdefault(key, []).append(newVertex)
        return newVertex

    def get_eVertex(self, n):
        if n in self.eVertexList:
            return self.eVertexList[n]
        else:
            return None

    def get_sVertex(self, n):
        # return a list
        if n in self.sVertexList:
            return self.sVertexList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.eVertexList

    def add_e2s_Edge(self, e, s):
        e.addEdge(s)

    def add_s2e_Edge(self, s, e):
        s.addEdge(e)

    def __iter__(self):
        return iter(self.eVertexList.values())

    def iterateOverGraph(self):
        # there are 2 ways to iterate over the entire graph
        # the first way is iterating from entity
        for i in self.eVertexList:
            for j in self.eVertexList[i].hasStatement:
                head = self.eVertexList[i].getId()
                relation = j.getId()
                tail = j.hasValue.getId()
                begin = j.getBeginTime()
                end = j.getEndTime()
                weight = j.getWeight()
                truth = j.getTruth()
                print(head, relation, tail, begin, end, weight, truth)

        # the second way is iterating from relation
        for i in self.sVertexList.keys():
            statementList = self.sVertexList[i]
            for j in statementList:
                head = j.hasItem.getId()
                relation = j.getId()
                tail = j.hasValue.getId()
                begin = j.getBeginTime()
                end = j.getEndTime()
                weight = j.getWeight()
                truth = j.getTruth()
                print(head, relation, tail, begin, end, weight, truth)

    def ConstructThroughTsv(self, tsvFile):
        utkg = read_datasets.read_file(tsvFile)
        # we need to filter the duplicate

        NonDuplicate=[]
        for line in utkg:
            head = line[0]
            relation = line[1]
            tail = line[2]
            begin = int(line[3])
            end = int(line[4])
            duplicate=str(head)+str(relation)+str(tail)+str(begin)+str(end)
            if duplicate not in NonDuplicate:
                NonDuplicate.append(duplicate)
            else:
                continue

            if line[5].__eq__("true"):
                truth = True
            else:
                truth = False
            # weight = float(line[6])
            e1 = self.add_eVertex(head)
            s = self.add_sVertex(relation, begin, end, 1, truth)
            e2 = self.add_eVertex(tail)
            self.add_e2s_Edge(e1, s)
            self.add_s2e_Edge(s, e2)





def temporal_representation_constraint(graph):
    Conflicting_facts = []
    for i in graph.eVertexList:
        for j in graph.eVertexList[i].hasStatement:
            head = graph.eVertexList[i].getId()
            relation = j.getId()
            tail = j.hasValue.getId()
            begin = j.getBeginTime()
            end = j.getEndTime()
            weight = j.getWeight()
            truth = j.getTruth()
            fact = [head, relation, tail, begin, end, weight, truth]
            if begin > end:
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

                    i1 = graph.eVertexList[i].hasStatement[j].getBeginTime()
                    i2 = graph.eVertexList[i].hasStatement[j].getEndTime()
                    for k in range(j+1, len(graph.eVertexList[i].hasStatement)):
                        r1 = graph.eVertexList[i].hasStatement[k].getId()
                        tail2 = graph.eVertexList[i].hasStatement[k].hasValue.getId()
                        if relation.__eq__(r1):
                            i3 = graph.eVertexList[i].hasStatement[k].getBeginTime()
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
    # x relation1 y & x relation2 z t1(t1=开始结束时间取平均数) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1
    return functional_constraint

def reverse_functional_mining(graph):
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets
    print("reverse_functional_mining")
    threshold = 0.8
    functional_constraint = []
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
                    i1 = graph.eVertexList[i].bePointedTo[j].getBeginTime()
                    i2 = graph.eVertexList[i].bePointedTo[j].getEndTime()
                    for k in range(j+1, len(graph.eVertexList[i].bePointedTo)):
                        r1 = graph.eVertexList[i].bePointedTo[k].getId()
                        head2 = graph.eVertexList[i].bePointedTo[k].hasItem.getId()
                        if relation.__eq__(r1):
                            i3 = graph.eVertexList[i].bePointedTo[k].getBeginTime()
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
            print("TODO")
        # x relation1 y & x relation2 z t1(t1=开始结束时间取平均数) & y relation3 w t2 = > t2 before t1 / t1 before t2 / t1 during t2 / t2 during t1

    return functional_constraint


# def temporal
def Constraint_Mining(graph):
    '''

    :param utkg:
    :return:
    '''
    functional_mining(graph)
    Constraint_list = []
    return Constraint_list


def Conflict_Dectection(Constraints, dataset):
    '''
    :param dataset:
    :return: Conflicting_temporal_facts
    '''

    Conflicting_temporal_facts = []
    return Conflicting_temporal_facts


if __name__ == '__main__':
    # utkg=read_datasets.read_file("footballdb_tsv/player_team_year_rockit_0.tsv")
    # functional_detection(utkg)
    g = Graph()
    # filename="footballdb_tsv/player_team_year_rockit_0.tsv"
    filename = "wikidata_dataset_tsv/rockit_wikidata_0_50k.tsv"
    g.ConstructThroughTsv(filename)

    print(g.num_eVertices)
    print(g.num_sVertices)
    print(len(g.relationList))
    print(g.relationList)
    print("-------------------")
    # g.iterateOverGraph()
    conflicting_type1_facts = temporal_representation_constraint(g)
    print("temporal_representation_constraint",len(conflicting_type1_facts))
    functional_mining(g)

    reverse_functional_mining(g)
