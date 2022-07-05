### 冲突定义

有规则和一致性才能推出冲突

### 一致性类型：



**传统functional** ：一个人不能有两个birthdate/deathdate。这种传统的functional属性其实与时间无关。

**关注点**：加上时间维度后对一致性带来的变化

#### **单实体内一致性（短距离）**：

**Temporal Disjointness** ：对于单实体来说，不同的四元组共享一个时间functional关系，在时间域上不能有相交。例子：一个人不能同时和两个人结婚。本质：时间维的加入使得一些关系具有时间functional性质。

**Temporal Ordering** ：对于单实体来说，关系是有序的，例子：一个人要在出生之后才能学习、工作。本质：关系本身具有时间顺序，因此加入时间维度后对时间有约束。

**Time Span(软约束)**：多关系上的时间跨度具有一个统计上的均值，例子：一个人的出生和死亡时间间隔通常小于100年。（软约束其实还可以有很多其他的）

#### **多实体间一致性（长距离）**：

**Temporal Disjointness** : 多实体在同一个关系和值上不能时间相交。例子：不能两个人同时担任美国总统。本质：时间维的加入使得对于一个关系在同时间段内不能有多个头实体，也就是对subject是functional的。

**Temporal Ordering** ：对于有关系的多实体，同关系的时间是有序的。例子：a是b的父亲，所以a的出生日期应该早于b的出生日期。本质：实体间的关系暗含了时间关系，因此各自实体的同一个关系上继续保持了这种先后关系，从而对时间起约束作用。

**Time Span（软约束）** :  对于有周期性的事件，发生时间的跨度也有一个统计上的均值。例子：每届奥运会举办时间通常间隔4年。

### 现有工作：

**慕尼黑大学AAAI-17**：考虑了**Temporal Disjointness**，**Temporal Ordering**和**Time Span**。约束用amie自动挖掘+人工提出。

**苏大WISE-18**：专门针对**Temporal Ordering**约束提出了一种自动发掘约束的方法。

### **Motivation**：

1.现在没有工作针对单实体内的Time Disjointness做一个自动化的发掘，即什么样的关系是具有时间functional性质的。

2.对于多实体间一致性的两种约束类型都没有人探究，挖掘什么样的关系应该具有对object的时间functional性质，并且探究多实体间的关系的temporal order

3.对于两种Time Span可以做一个统计上的分析

### 技术路线：

流程上分为两部分：约束挖掘和冲突消解。

#### 约束挖掘

**前提假设**：从一个高质量知识库获取的是一张完全正确的时态知识图谱。然后从完全正确的时态知识图谱中去挖掘约束。

首先需要将时态知识图谱构建成图：

图的构建参照wikidata的数据模型，实体与实体之间采用statement连接，一个statement里会包含关系和关系的起始与结束时间。

**图1 时态知识图谱：**

![graph construction.drawio](E:\一致性检测\画图\graph construction.drawio.png)



**time interval relations**

foundation: i1<i2

before: i2<=i3

meets: i2=i3

disjoint: i2<=i3 or i4<=i1

overlap: i2>=i3 and i1<=i4

during: i1 >= i3 and i2 <= i4

equal: i1=i3 and i2=i4

starts: i1=i3

finish: i2=i4

before包含meets

overlap包含equal，during，starts，finishes

需要用到的时间段之间的关系：其中equal，during，starts，finishes均是overlap的特殊情况，meets是before的特殊情况。disjoint即x before y 或者 y before x。

**图2 时间段的关系**



![interval relations.drawio(1)](E:\一致性检测\画图\interval relations.drawio(1).png)





基于我们的motivation从完全正确的图中发现约束：

**约束0**：时间本身表示begin<=end。（这是一个基础的对时间表示的约束，实际在wikidata50k的数据中发现1248个不符合的）

**约束1**：temporal functional关系挖掘

**定义一**：具有temporal functional性质的关系是指对于一个头实体的某一个关系，拥有多个尾实体当且仅当他们的关系各自的成立时间不相交。

**挖掘算法的的流程**：

对于图中所有实体节点，分别去遍历他们的statement，将所有包含该关系的statement以及头尾实体抽出形成子图。检查每个子图中的关系成立时间是否不想交，若满足，则有效子图数+1。最终我们统计一个confidence=有效子图数/总子图数，当confidence>threshold时我们判定该关系具有temporal functional性质。

**图3 单实体内的同关系子图划分**：

![temporal functional.drawio](E:\一致性检测\画图\temporal functional.drawio.png)

**约束2**：关系的temporal order挖掘

temporal order关系在AAAI-17的设定下指一个实体的某些关系存在发生的先后顺序，那么这些关系就是存在temporal order的。在WISE-18中已对单实体的temporal order做过研究，这里我们直接继承过来。

**挖掘算法的的流程**：

对于一个知识库中的所有关系，我们两两去探究他们之间有无前序或是包含关系。从一个实体出发，若该实体同时存在这两种关系的statement，则把所有包含这两个关系的statement以及他们的头尾实体抽取出来形成一张子图，并探究子图中的statement是否满足before或者during性质，满足则各自的consistent subset数+1,最后他们的confidence=consistent subset/total subset数，confidence>threshold则存在偏序或包含关系。

**图4 单实体内两个关系构成的子图：**

![temporal order.drawio](E:\一致性检测\画图\temporal order.drawio.png)

**约束3**：对于object的temporal functional关系挖掘

**定义二**：一个关系对object是temporal functional的是指对于一个尾实体的某一个关系，拥有多个头实体当且仅当他们的关系各自的成立时间不相交。

**挖掘算法的的流程**：

对于图中所有实体节点，分别去遍历指向他们的statement，将所有包含该关系的statement以及头尾实体抽出形成子图。检查每个子图中的关系成立时间是否不想交，若满足，则有效子图数+1。最终我们统计一个confidence=有效子图数/总子图数，当confidence>threshold时我们判定该关系具有temporal functional性质。

**图4 指向单实体的同关系子图划分**：

![object functional.drawio](E:\一致性检测\画图\object functional.drawio.png)

**约束4**：对于多实体间的temporal order关系挖掘

多实体间的temporal order较为复杂，最简单的情况可以做一些限定，例如这里约定实体与实体只存在一跳关系，即查询实体和一跳范围内邻居的所有statement形成的子图中是否存在temporal order。

**挖掘算法的的流程**：

对于一个知识库中的所有关系，我们两两去探究他们之间有无长距离的前序或是包含关系。从一个实体出发，扫描他的所有经一跳关系到达的邻居实体，若出发的实体和抵达的实体分别存在这两种关系的statement，则把所有包含这两个关系的statement和他们的头尾实体以及出发抵达实体间的关系抽取出来形成一张子图，并探究子图中的statement是否满足before或者during性质，满足则各自的consistent subset数+1,最后他们的confidence=consistent subset/total subset数，confidence>threshold则存在偏序或包含关系。

**图5 多实体间的temporal order子图：**

![multi-head temporal order.drawio](E:\一致性检测\画图\multi-head temporal order.drawio.png)

在最后形式化表示约束时可以表示为: 

x relation1 y & x relation2 z t1(t1=开始结束时间取平均数) & y  relation3 w t2 => t2 before t1 / t1 before t2

/ t1 during t2 / t2 during t1

**约束5**：对于单个关系的成立时间TimeSpan统计

单个关系的成立时间一般存在一个阈值，如美国总统一般4-8年，利用统计可以发现这类关系的规律。

**挖掘算法的的流程**：

对于所有待挖掘的关系，遍历其所有成立时间的起始时间差，就能统计出一个概率分布。

**约束6**：对于关系之间成立时间的跨度统计

关系之间的时间跨度可能存在合理的阈值范围，例如从出生到上学的时间跨度通常在一个合理的时间范围内。

**挖掘算法的的流程**：

如图4所示，在同一个实体内，对于两两关系统计他们成立时间的差值，就能统计出一个概率分布。



**数据集构建（从服务器提取合适子集）**

当前数据集主要有两个问题：1关系很少，wikidata50k数据集有6个关系，这就导致自动挖掘算法挖不到大量约束，并且实际上AAAI-17是人工观察数据集提出的约束，这倒是我们在别人的数据集上不能超过人工。

2.是纯粹的时间事实（四元组）构成的知识库，没有三元组的话导致我们的约束4实际无法发挥作用，因为我们依赖于三元组的路径（奥巴马的继任者当总统的时间晚于奥巴马）

因此需要数据集构建并且也是目前急需做的。



#### 冲突消解

这部分本来是想沿用AAAI-17的概率软逻辑或者是马尔科夫逻辑网络直接作为我们的求解器，但是目前复现有困难，考虑用最大团算法快速替换。



