# PaTeCon+



This is also the code for our AAAI 2023 paper [**PaTeCon: A Pattern-Based Temporal Constraint Mining Method for Conflict Detection on Knowledge Graphs**](https://ojs.aaai.org/index.php/AAAI/article/view/25533).

Because we keep improving the code, the experimental results may be slightly different from the paper.

## Installation

To get source code, run:

```
git clone https://github.com/JianhaoChen-nju/PaTeCon.git
```

Install requirements

```shell
cd PaTeCon
conda create -n PaTeCon python=3.9
conda activate PaTeCon
pip install -r requirements.txt
```

## Dataset

Our datasets WD50K, WD27M and FB37M can be downloaded in url [Google Drive URL](https://drive.google.com/drive/folders/1tFmSPK7RzYM1qVDlCB7d8vuk_pHwqYGV?usp=sharing). You can also find the original WD50k in https://github.com/dwslab/TeCoRe/tree/master/conf/resources/rockit.

Our data is organized as follows:

| subject | property | **object** | start time | end time |
| ------- | -------- | ---------- | ---------- | -------- |
|         |          |            |            |          |

If start time or end time value == "null", it means that the time value is unknown or doesn't exist.

In this [Google Drive URL](https://drive.google.com/drive/folders/1tFmSPK7RzYM1qVDlCB7d8vuk_pHwqYGV?usp=sharing), you can also find the type files needed for refinements: wikidata-entity-type-info.tsv and freebase-entity-type-info.tsv.

The type file is organized as follows:

| entity | entity type 1 | entity type 2 | entity type ... |
| ------ | ------------- | ------------- | --------------- |
|        |               |               |                 |

Download all above files to PaTeCon/resource folder.

## Running the code

#### Constraint Mining:

run WD50K :

```shell
python Constraint_Mining.py --dataset=resource/WD50K.tsv --knowledgegraph=wikidata --support=10 --candidate_confidence=0.5 --confidence=0.9
```

run WD27M:

```shell
python Constraint_Mining.py --dataset=resource/WD27M.tsv --knowledgegraph=wikidata --refinement=True --typefile=resource/wikidata-entity-type-info.tsv --support=100 --candidate_confidence=0.5 --confidence=0.9
```

run FB37M:

```shell
python Constraint_Mining.py --dataset=resource/FB37M.tsv --knowledgegraph=freebase --refinement=True --typefile=resource/freebase-entity-type-info.tsv --support=100 --candidate_confidence=0.5 --confidence=0.9
```

Parameters to choose:

**dataset, knowledgegraph, refinement, typefile, support, candidate_confidence, confidence**

**dataset**: the dataset you want to mine constraints on.

**knowledgegraph**: Which type of knowledge graph the dataset is. We set three types: wikidata, freebase and other.

**refinement**: Whether to mine refined constraints. The default value of **refinement** is set to False. If you want to mine refined constraints, you should provide entity type files.

**typefile**: The entity type files needed during refinement stage. If you need to mine refined constraints on your own dataset, you need to provide typefile just like ours. 

**support**: The positive instances of constraints. The default value is 100. If the dataset is small, it is recommended to adjust the **support** smaller such as 20/50.

**candidate_confidence**: The candidate confidence of constraints. The default value is 0.5. We don't think it is usually necessary to modify the value of **candidate_confidence**.

**confidence**: The final confidence of constraints. Generally speaking, **confidence**=0.9 can get reliable constraints. Of course, you can also relax appropriately to get more constraints. Or increase **confidence** to more than 0.95 to get more correct constraints.

**Output**: 

We will output all candidate constraints in file "output/"+dataset+"\_rules". Refined rules are in file "output/"+dataset+"_refined_rules".

The final constraints are in file "output/"+dataset+"_all_constraints".

#### Conflict Detection:

run WD50K :

```shell
python Conflict_Detection.py --dataset=resource/WD50K.tsv --knowledgegraph=wikidata --constraint=output/WD50K.all_constraints
```

run WD27M

```
python Conflict_Detection.py --dataset=resource/WD27M.tsv --knowledgegraph=wikidata --constraint=output/WD27M.all_constraints --refinement=True --typefile=resource/wikidata-entity-type-info.tsv
```

run FB37M

```
python Conflict_Detection.py --dataset=resource/FB37M.tsv --knowledgegraph=freebase --constraint=output/FB37M.all_constraints --refinement=True --typefile=resource/freebase-entity-type-info.tsv
```

Parameters to choose:

**dataset, knowledgegraph, constraint, refinement, typefile**

**dataset**: the dataset you want to detect conflicts on.

**knowledgegraph**: Which type of knowledge graph the dataset is. We set three types: wikidata, freebase and other.

**constraints**: The constraint file used to detect conflicts.

**refinement**: Whether to mine refined constraints.

**typefile**: The entity type files needed during refinement stage.

**Output**: 

We will output conflicts which are detected by non-refined constraints in file "output/"+dataset+"\_conflict". Conflicts detected by refined constraints are in file "output/"+dataset+"_refined_conflict".

All conflicts are in file "output/"+dataset+"_all_conflicts".

## Constraint and conflict form

**Constraints:**

Our constraints are organized in the form of body => head.

For example:

```
(a,P39,b,t1,t2) & (a,P22,c,t3,t4) & (c,P569,d,t5,t6) => before(t5,t6,t1,t2)|0.9916566033593149								(1)
```

At output we output a simplified form of the constraint along with its confidence as follows.

```
a,P22*P569,d,t5,t6 before a,P39,b,t1,t2|0.9916566033593149																	(2)
```

(2) is the simple form of (1). The two can be transformed into each other. The "|" is followed by the confidence of the constraint "0.9916566033593149". 

"*" represents the compounding of relationships. The variable c is hidden after compounding in the simple form.

A more complex example:

```
(a,P54,b,t1,t2) & (b,class,Q6979593) & (a,P54,c,t3,t4) & (c,class,Q6979593) => disjoint(t1,t2,t3,t4)|0.9577199311039615		(3)
```

At output we output a simplified form of the constraint along with its confidence as follows.

```
a,P54,b,t1,t2 b,class,Q6979593 disjoint a,P54,c,t3,t4 c,class,Q6979593|0.9577199311039615									(4)
```

(4) is the simple form of (3). The two can be transformed into each other. The "|" is followed by the confidence of the constraint "0.9577199311039615". 

(b,class,Q6979593) means the variable b's class is Q6979593.

**Conflicts:**

Our conflicts are represented in the form of "constraint	fact1	fact2".

An example is as follows:

```
a,P569,b,t1,t2 MutualExclusion a,P569,c,t3,t4|0.9934953327578068    Q1611104,P569,1885-05-16 00:00:00Z,18850516,18850516   Q1611104,P569,1895-05-16 00:00:00Z,18950516,18950516
```

This example explains that Q1611104 has two birthdays, which violates the constraint a,P569,b,t1,t2 MutualExclusion a,P569,c,t3,t4|0.9934953327578068.

## How to cite

If you used our work or found it helpful, please use the following citation:

```bib
@inproceedings{chen2023patecon,
  title={PaTeCon: a pattern-based temporal constraint mining method for conflict detection on knowledge graphs},
  author={Chen, Jianhao and Ren, Junyang and Ding, Wentao and Qu, Yuzhong},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={37},
  number={4},
  pages={4166--4172},
  year={2023}
}
```

