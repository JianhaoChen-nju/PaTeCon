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
    def __init__(self, key, start=None, end=None,  weight=1, truth=True):
        self.id = key
        self.hasItem = None
        self.hasValue = None
        self.start = start
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

    def getStartTime(self):
        return self.start

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

    def add_sVertex(self, key, start, end, weight, truth=True):
        if key not in self.relationList:
            self.relationList.append(key)
        self.num_sVertices = self.num_sVertices + 1
        newVertex = sVertex(key, start, end, weight, truth)
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
                start = j.getStartTime()
                end = j.getEndTime()
                weight = j.getWeight()
                truth = j.getTruth()
                print(head, relation, tail, start, end,  weight, truth)

        # the second way is iterating from relation
        for i in self.sVertexList.keys():
            statementList = self.sVertexList[i]
            for j in statementList:
                head = j.hasItem.getId()
                relation = j.getId()
                tail = j.hasValue.getId()
                start = j.getStartTime()
                end = j.getEndTime()
                weight = j.getWeight()
                truth = j.getTruth()
                print(head, relation, tail, start, end,  weight, truth)

    def ConstructThroughTsv(self, tsvFile):
        utkg = read_datasets.read_file(tsvFile)
        # we need to filter the duplicate

        # NonDuplicate=[]
        for line in utkg:
            head = line[0]
            relation = line[1]
            tail = line[2]
            if line[3]=="null":
                start=-1
            else:
                start = int(line[3])
            if line[4]=="null":
                end=-1
            else:
                end = int(line[4])

            # deduplication has been abandoned
            # duplicate=str(head)+str(relation)+str(tail)+str(start)+str(end)
            # if duplicate not in NonDuplicate:
            #     NonDuplicate.append(duplicate)
            # else:
            #     continue

            if line[5].__eq__("true"):
                truth = True
            else:
                truth = False
            # weight = float(line[6])
            e1 = self.add_eVertex(head)
            s = self.add_sVertex(relation, start, end, 1, truth)
            e2 = self.add_eVertex(tail)
            self.add_e2s_Edge(e1, s)
            self.add_s2e_Edge(s, e2)