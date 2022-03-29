import read_datasets
import Constraint_Mining
import Conflict_Detection

def evaluate(ctkg,gold):
    total_predict=len(ctkg)
    correct=0
    for fact in ctkg:
        if fact[5]=="<true>":
            correct+=1
    total_correct=0
    for fact in gold:
        if fact[5]=="<true>":
            total_correct+=1

    P=correct*1.0/total_predict
    R=correct*1.0/total_correct
    print("Precision:",P)
    print("Recall:",R)

def threshold_statistics():
    # filename="footballdb_tsv/player_team_year_rockit_100.tsv"
    filename="wikidata_dataset_tsv/rockit_wikidata_100_50k.tsv"
    utkg=read_datasets.read_file(filename)
    true_maximal=0
    true_minimal=10
    false_minimal=10
    false_maximal=0
    true_count=0
    false_count=0
    for fact in utkg:
        weight=float(fact[6].replace("<","").replace(">",""))
        if weight==9223372036854776000.0000:
            #exception
            continue
        if fact[5]=="<true>":
            if weight<true_minimal:
                true_minimal=weight
            if weight>true_maximal:
                true_maximal=weight
            if weight<3:
                true_count+=1

        else:
            if weight<false_minimal:
                false_minimal=weight
            if weight>false_maximal:
                false_maximal=weight
            if weight<2:
                false_count+=1
    print("true threshold is",true_minimal,true_maximal)
    print("true count<3 is",true_count)
    print("false threshold is",false_minimal,false_maximal)
    print("false count<3 is",false_count)

def Eliminating_Conflicting_Framework():
    datasetname="footballdb_tsv"
    # datasetname="wikidata_dataset_tsv"
    dataset=read_datasets.read_dataset(datasetname)
    for utkg in dataset:
        Constraints=Conflict_Detection.Constraint_Mining(utkg)
        Conflict_temporal_facts=Conflict_Detection.Conflict_Dectection(Constraints,utkg)
        certain_TKG=Conflict_Resolution.Conflict_Resolution(Conflict_temporal_facts)
        evaluate(certain_TKG,utkg)


if __name__ == '__main__':
    '''
    test
    '''
    # threshold_statistics()
    # Eliminating_Conflicting_Framework()
    # utkg=read_datasets.read_file("footballdb_tsv/player_team_year_rockit_50.tsv")
    # print(len(utkg))
    # evaluate(utkg,utkg)