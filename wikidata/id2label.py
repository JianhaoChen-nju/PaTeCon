def read_file(file_name):
    f=open(file_name,"r")
    lines=f.readlines()
    for line in lines:
        line=line.strip()
        l=line.split("\t")
        name=l[0]
        id=l[1]
        num=l[2]
        class_pairs_s=l[3]
        class_pairs_list=class_pairs_s.split("],")
        class_pairs=[]
        for item in class_pairs_list:
            a_pair=[]
            a_pair=item.replace("[","").replace("]","").replace(" ","").replace("'","").split(",")
            class_pairs.append(a_pair)
        print(class_pairs)
        time_predicate_s=l[4]
        time_predicate=time_predicate_s.replace("[","").replace("]","").replace(" ","").replace("'","").split(",")
        # print(time_predicate)
    # print(len(lines))



if __name__ == '__main__':
    read_file("class_pairs_res.txt")