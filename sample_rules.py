import random
sample_goal=50

filename="all_relations_with_redundant_wikidata_alpha-1.3.tsv_rules"
raw_rule_file=open(filename,"r")
sampled_file=open("sampled_%d_rules.txt" %sample_goal,"w")
all_rules=raw_rule_file.readlines()
raw_rule_file.close()

rules_cnt=len(all_rules)

selected_set=set()
while len(selected_set)<sample_goal:
    selected_set.add(random.randrange(0,rules_cnt))

for i in selected_set:
    sampled_file.write(all_rules[i])
sampled_file.close()