import read_datasets
import Constraint_Mining
def Conflict_Resolution(Conflict_temporal_facts):
    # framework
    fact=["<A.J.Bouye>","<playsFor>","<HoustonTexans>","<2013>","<2016>","<true>","<1.4604>"]
    certain_tkg=[]
    certain_tkg.append(fact)
    return certain_tkg

if __name__ == '__main__':
    Conflict_temporal_facts=[]
    Conflict_Resolution(Conflict_temporal_facts)