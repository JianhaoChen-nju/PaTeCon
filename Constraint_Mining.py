import read_datasets


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
    def __init__(self, key, begin, end, weight, truth=True):
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
        for line in utkg:
            head = line[0]
            relation = line[1]
            tail = line[2]
            begin = int(line[3])
            end = int(line[4])
            if line[5].__eq__("true"):
                truth = True
            else:
                truth = False
            weight = float(line[6])
            e1 = g.add_eVertex(head)
            s = g.add_sVertex(relation, begin, end, weight, truth)
            e2 = g.add_eVertex(tail)
            g.add_e2s_Edge(e1, s)
            g.add_s2e_Edge(s, e2)


# (i1,i2)  (i3,i4)
# meets is a special case of before
def foundation(i1, i2):
    if i1 <= i2:
        return True
    else:
        return False


def before(i1, i2, i3, i4):
    # i2<=i3
    if i2 <= i3:
        return True
    else:
        return False


def meets(i1, i2, i3, i4):
    # i2=i3
    if i2 == i3:
        return True
    else:
        return False


# before is a special order of disjoint
def disjoint(i1, i2, i3, i4):
    # i2<i3 || i4<i1
    if i2 <= i3 or i4 <= i1:
        return True
    else:
        return False


# during, equal, starts, finish are special cases of overlap
def overlap(i1, i2, i3, i4):
    if i2 >= i3 and i1 <= i4:
        return True
    else:
        return False


def during(i1, i2, i3, i4):
    if i1 >= i3 and i2 <= i4:
        return True
    else:
        return False


def start(i1, i2, i3, i4):
    # i1=i3
    if i1 == i3:
        return True
    else:
        return False


def finish(i1, i2, i3, i4):
    # i2=i4
    if i2 == i4:
        return True
    else:
        return False


def equal(i1, i2, i3, i4):
    # i1=i3 && i2=i4
    if i1 == i3 and i2 == i4:
        return True
    else:
        return False


def validSpanBelow(i1, i2, span):
    # i2-i1<=span
    if i2 - i1 <= span:
        return True
    else:
        return False


def validSpanAbove(i1, i2, span):
    # i2-i1>span
    if i2 - i1 > span:
        return True
    else:
        return False


def relationsSpanBelow(i1, i2, i3, i4, span):
    # i3-i1<=span
    if i3 - i1 <= span:
        return True
    else:
        return False


def relationsSpanAbove(i1, i2, i3, i4, span):
    if i3 - i1 > span:
        return True
    else:
        return False


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
    threshold = 0.8
    functional_constraint = []
    consistent_subsets = 0
    total_subsets = 0
    for relation in graph.relationList:
        confidence = 0
        for i in graph.eVertexList:
            consistent = True
            hasRelation = False
            for j in range(len(graph.eVertexList[i].hasStatement)):
                r = graph.eVertexList[i].hasStatement[j].getId()
                if relation.__eq__(r):
                    hasRelation = True
                    i1 = graph.eVertexList[i].hasStatement[j].getBeginTime()
                    i2 = graph.eVertexList[i].hasStatement[j].getEndTime()
                    for k in range(j, len(graph.eVertexList[i].hasStatement)):
                        r1 = graph.eVertexList[i].hasStatement[k].getId()
                        if relation.__eq__(r1):
                            i3 = graph.eVertexList[i].hasStatement[k].getBeginTime()
                            i4 = graph.eVertexList[i].hasStatement[k].getEndTime()
                            if disjoint(i1, i2, i3, i4):
                                consistent = True
                            else:
                                consistent=False
                                # print(i1,i2,i3,i4)
            if hasRelation:
                total_subsets += 1
                if consistent:
                    consistent_subsets += 1
            confidence = consistent_subsets * 1.0 / total_subsets
        print(relation, confidence)

    return functional_constraint

def reverse_functional_mining(graph):
    # a relation is temporally functional if its value's valid time has no overlaps
    # find which relation is functional
    # what a functional constraint is like?
    # how to compute confidence? present strategy is consistent subsets/total subsets
    threshold = 0.8
    functional_constraint = []
    consistent_subsets = 0
    total_subsets = 0
    for relation in graph.relationList:
        confidence = 0
        for i in graph.eVertexList:
            consistent = True
            hasRelation = False
            for j in range(len(graph.eVertexList[i].bePointedTo)):
                r = graph.eVertexList[i].bePointedTo[j].getId()

                if relation.__eq__(r):
                    hasRelation = True
                    i1 = graph.eVertexList[i].bePointedTo[j].getBeginTime()
                    i2 = graph.eVertexList[i].bePointedTo[j].getEndTime()
                    for k in range(j, len(graph.eVertexList[i].bePointedTo)):
                        r1 = graph.eVertexList[i].bePointedTo[k].getId()
                        if relation.__eq__(r1):
                            i3 = graph.eVertexList[i].bePointedTo[k].getBeginTime()
                            i4 = graph.eVertexList[i].bePointedTo[k].getEndTime()
                            if overlap(i1, i2, i3, i4):
                                consistent = False
            if hasRelation:
                total_subsets += 1
                if consistent:
                    consistent_subsets += 1
            confidence = consistent_subsets * 1.0 / total_subsets
        print(relation, confidence)

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
    print(len(conflicting_type1_facts))
    functional_mining(g)
    reverse_functional_mining(g)
