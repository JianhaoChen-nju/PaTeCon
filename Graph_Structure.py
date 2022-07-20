import time

import read_datasets
# eVertex: entity Vertex
# sVertex: statement Vertex

class eVertex:
    def __init__(self, key, label="ToAdd",isLiteral=False):
        self.id = key
        self.label = label
        self.isLiteral = isLiteral
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
        # self.eVertexSet=set()
        self.eVertexList = {}
        self.relationList = []
        self.temporalRelationList = []
        self.sVertexList = {}
        self.entityType={}
        self.num_eVertices = 0
        self.num_sVertices = 0

    def add_eVertex(self, key,label="Toadd",isLiteral=False):
        # if not self.eVertexSet.__contains__(key):
        #     self.eVertexSet.add(key)
            self.num_eVertices = self.num_eVertices + 1
            newVertex = eVertex(key,label=label,isLiteral=isLiteral)
            self.eVertexList[key] = newVertex
            return newVertex
        # else:
        #     return self.eVertexList[key]

    def add_sVertex(self, key, start, end, weight, truth=True):
        if key not in self.relationList:
            self.relationList.append(key)
        self.num_sVertices = self.num_sVertices + 1
        newVertex = sVertex(key, start, end, weight, truth)
        # value of dic is a list
        self.sVertexList.setdefault(key, []).append(newVertex)
        return newVertex


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

    def build_cache(self,utkg,tsvFile,knowledgebase):
        entity_list=set()
        for line in utkg:
            head=line[0]
            if knowledgebase=="wikidata":
                Begin_Word=head[0]
                if Begin_Word=="Q":
                    entity_list.add(head)
            elif knowledgebase=="freebase":
                Begin_Word=head[1]
                if Begin_Word==".":
                    entity_list.add(head)
            tail=line[2]
            if knowledgebase=="wikidata":
                Begin_Word=tail[0]
                if Begin_Word=="Q":
                    entity_list.add(tail)
            elif knowledgebase=="freebase":
                Begin_Word=tail[1]
                if Begin_Word==".":
                    entity_list.add(tail)
        file=open(tsvFile+"_cache","w",encoding="utf-8")
        file.writelines("\n".join(entity_list))
        file.close()




    def __iter__(self):
        return iter(self.eVertexList.values())

    def iterateOverGraph(self):
        # there are 2 ways to iterate over the entire graph
        # the first way is iterating from entity
        # for i in self.eVertexList:
        #     for j in self.eVertexList[i].hasStatement:
        #         head = self.eVertexList[i].getId()
        #         relation = j.getId()
        #         tail = j.hasValue.getId()
        #         start = j.getStartTime()
        #         end = j.getEndTime()
        #         weight = j.getWeight()
        #         truth = j.getTruth()
        #         print(head, relation, tail, start, end,  weight, truth)

        # the second way is iterating from relation
        # for i in self.sVertexList.keys():
        #     statementList = self.sVertexList[i]
        #     for j in statementList:
        #         head = j.hasItem.getId()
        #         relation = j.getId()
        #         tail = j.hasValue.getId()
        #         start = j.getStartTime()
        #         end = j.getEndTime()
        #         weight = j.getWeight()
        #         truth = j.getTruth()
        #         print(head, relation, tail, start, end,  weight, truth)
        max_count=0
        min_count=100
        for i in self.eVertexList:
            v=self.eVertexList[i]
            count=0
            for s in v.bePointedTo:
                count+=1
            if count==3282225:
                print(v.getId())
            if count>max_count:
                max_count=count
            if count<min_count:
                min_count=count
        print("max count is",max_count)
        print("min count is",min_count)


    def ConstructThroughTsv(self, tsvFile , knowledgebase, percent=100):
        # you can only define percent = 10,20,30...100
        temporalRelationList=set()
        starttime0=time.time()
        utkg = read_datasets.read_file(tsvFile)
        endtime0=time.time()
        readfiletime=endtime0-starttime0
        print("read file time:",readfiletime,"s")

        # we need to do a fundamental check
        starttime1=time.time()
        Conflict_free_utkg=read_datasets.temporal_representation_constraint(tsvFile,utkg)
        endtime1=time.time()
        runningtime1=endtime1-starttime1
        print("temporal representation running time is",runningtime1,"s")
        print("len of Conflict-free utkg is",len(Conflict_free_utkg))

        # we need to build a cache
        self.build_cache(utkg,tsvFile,knowledgebase)

        # random sample
        starttime2 = time.time()
        selected_Conflict_free_utkg=[]
        index=0
        for item in Conflict_free_utkg:
            index+=10
            if index<=percent:
                selected_Conflict_free_utkg.append(item)
            if index==100:
                index=0
        print("len of selected conflict free utkg is",len(selected_Conflict_free_utkg))
        endtime2 = time.time()
        runningtime2=endtime2-starttime2
        print("random sample running time is:",runningtime2,"s")

        # construct temporal kg
        starttime3=time.time()
        cache_file=open(tsvFile+"_cache","r",encoding="UTF-8")
        entities=cache_file.readlines()
        cache_file.close()
        for entity in entities:
            entity=entity.strip("\n")
            self.add_eVertex(entity)

        LiteralNum = 0
        LiteralKey = ""
        tailcount=0
        for line in selected_Conflict_free_utkg:
            head = line[0]
            head_isLiteral = False

            # wikidata
            if knowledgebase=="wikidata":
                head_Begin_Word=head[0]
                if head_Begin_Word!="Q":
                    head_isLiteral=True
                    LiteralKey="L"+str(LiteralNum)
                    LiteralNum+=1
            elif knowledgebase=="freebase":
                head_Begin_Word=head[1]
                if head_Begin_Word!=".":
                    head_isLiteral=True
                    LiteralKey="L"+str(LiteralNum)
                    LiteralNum+=1
            relation = line[1]
            tail = line[2]
            tail_isLiteral = False
            # wikidata
            if knowledgebase == "wikidata":
                tail_Begin_Word = tail[0]
                if tail_Begin_Word != "Q":
                    tail_isLiteral = True
                    LiteralKey = "L" + str(LiteralNum)
                    LiteralNum += 1
            elif knowledgebase == "freebase":
                tail_Begin_Word = tail[1]
                if tail_Begin_Word != ".":
                    tail_isLiteral = True
                    LiteralKey = "L" + str(LiteralNum)
                    LiteralNum += 1
            # if tail=="Q5958900":
            #     tailcount+=1

            if line[3]=="null":
                start=-1
            else:
                start = int(line[3])

            if line[4]=="null":
                end=-1
            else:
                end = int(line[4])
            if start!=-1 or end!=-1:
                temporalRelationList.add(relation)

            # we dont need truth and confidence
            # if line[5].__eq__("true"):
            #     truth = True
            # else:
            #     truth = False
            # weight = float(line[6])
            # e1=self.eVertexList[head]
            # e2 = self.eVertexList[tail]
            if head_isLiteral==True:
                e1=self.add_eVertex(LiteralKey,label=head,isLiteral=True)
            else:
                e1 = self.eVertexList[head]
            if tail_isLiteral == True:
                e2 = self.add_eVertex(LiteralKey, label=tail, isLiteral=True)
            else:
                e2=self.eVertexList[tail]
            s = self.add_sVertex(relation, start, end, 1, True)

            self.add_e2s_Edge(e1, s)
            self.add_s2e_Edge(s, e2)
        self.temporalRelationList=list(temporalRelationList)
        endtime3=time.time()
        runningtime3=endtime3-starttime3
        print("constructing graph running time is:",runningtime3,"s")