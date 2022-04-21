import read_datasets
import Constraint_Mining
import Interval_Relations
import Graph_Structure

def translate_atom():
    print("hai")


def Constraint_Check(temporal_KG,constraint):
    '''
    translate and execute constraint
    :param Conflict_temporal_facts:
    :param constraint:
    :return:
    '''
    print(constraint)
    constraint=constraint.replace("=>",">")

    body=constraint.split(">")[0]
    head=constraint.split(">")[1]
    print(body,head)


def Conflict_Detection(temporal_KG,Constraints):
    # framework
    for constraint in Constraints:
        Constraint_Check(temporal_KG,constraint)
    fact=["<A.J.Bouye>","<playsFor>","<HoustonTexans>","<2013>","<2016>","<true>","<1.4604>"]
    certain_tkg=[]
    certain_tkg.append(fact)
    return certain_tkg


if __name__ == '__main__':
    temporal_KG = Constraint_Mining.Graph()
    filename = "wikidata_dataset_tsv/rockit_wikidata_0_50k.tsv"
    temporal_KG.ConstructThroughTsv(filename)
    print(temporal_KG.num_eVertices)

    Constraints=['(a,P108,b,t1,t2) & (a,P108,c,t3,t4) => disjoint(t1,t2,t3,t4)','(a,P570,b,t1,t2) & (a,P570,c,t3,t4) => disjoint(t1,t2,t3,t4)']
    Conflict_Detection(temporal_KG,Constraints)