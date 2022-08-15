# (i1,i2)  (i3,i4)
# meets is a special case of before
# a naive strategy
# if i1==-1 or i2==-1 or i3==-1 or i4==-1:

class FuzzyTime:
    def __init__(self,timeInt):
        if timeInt==-1:
            self.Year="####"
            self.Month="##"
            self.Day="##"
        else:
            timeString=str(timeInt)
            bc=""
            if timeString[0]=="-":
                bc="-"
                timeString=timeString[1:]
            while len(timeString)<5:
                timeString='0'+timeString
            timeString=bc+timeString

            self.Day=int(timeString[-2:])
            self.Month=int(timeString[-4:-2])
            self.Year=int(timeString[:-4])
            if self.Day==1:
                self.Day="##"
                if self.Month==1:
                    self.Month="##"
        # print(self)
    def __repr__(self):
        return f'FuzzyTime({self.Year}-{self.Month}-{self.Day})'
    def get_precision(self):
        if self.Day!="##":
            return "Day"
        elif self.Month!="##":
            return "Month"
        elif self.Year!="####":
            return "Year"
        return "null"
    def isnotnull(self):
        return self.get_precision()!="null"
    def isnull(self):
        return self.get_precision()=="null"

def comp_time(t1,t2):
    if t1.get_precision()=="null" or t2.get_precision()=="null":
        return "unk"
    if t1.Year<t2.Year:
        return "lt"
    if t1.Year>t2.Year:
        return "gt"

    if t1.Month=="##" and t2.Month=="##":
        return "eq"
    if t1.Month=="##" or t2.Month=="##":
        return "unk"
    if t1.Month<t2.Month:
        return "lt"
    if t1.Month>t2.Month:
        return "gt"
    
    if t1.Day=="##" and t2.Day=="##":
        return "eq"
    if t1.Day=="##" or t2.Day=="##":
        return "unk"
    if t1.Day<t2.Day:
        return "lt"
    if t1.Day>t2.Day:
        return "gt"  
    
    return "eq"


def foundation(i1, i2):
    if i1 <= i2:
        return True
    else:
        return False


def before(i1, i2, i3, i4):
    t1=FuzzyTime(i1)
    t2=FuzzyTime(i2)
    t3=FuzzyTime(i3)
    t4=FuzzyTime(i4)
    # i2<=i3
    if t1.isnotnull() and t2.isnotnull() and t3.isnotnull() and t4.isnotnull():
        if comp_time(t1, t3) == "eq" and comp_time(t2, t4) == "eq":
            return -1
        comp_res=comp_time(t2,t3)
        if comp_res == "lt" or comp_res=="eq":
            return 1
        elif comp_res=="unk":
            return 0
        else:
            return -1
    else:
        if t1.isnull():
            #i2!=-1
            if t3.isnull():
                #i4!=-1
                # (-,i2) (-,i4)
                if comp_time(t2,t4)=="gt":
                    return -1
                else:
                    return 0
            elif t4.isnull():
                #i3!=-1
                # (-,i2) (i3,-)
                comp_res=comp_time(t2,t3)
                if comp_res == "lt" or comp_res=="eq":
                    return 1
                elif comp_res=="unk":
                    return 0
                else:
                    return -1
            else:
                #i3&i4!=-1
                # (-,i2) (i3,i4)
                comp_res=comp_time(t2,t3)
                if comp_res == "lt" or comp_res=="eq":
                    return 1
                elif comp_res=="unk":
                    return 0
                else:
                    return -1
        elif t2.isnull():
            #i1!=-1
            if t3.isnull():
                #i4!=-1
                # (i1,-) (-,i4)
                if comp_time(t1,t4)=="gt":
                    return -1
                else:
                    return 0
            elif t4.isnull():
                #i3!=-1
                # (i1,-) (i3,-)
                if comp_time(t1,t3)=="gt":
                    return -1
                else:
                    return 0
            else:
                #i3&i4!=-1
                # (i1,-) (i3,i4)
                if comp_time(t1,t3)=="gt":
                    return -1
                else:
                    return 0
        else:
            #i1&i2!=-1
            if t3.isnull():
                # i4!=-1
                # (i1,i2) (-,i4)
                if comp_time(t4,t2)=="lt":
                    return -1
                else:
                    return 0
            else:
                # i3!=-1
                # (i1,i2) (i3,-)
                comp_res=comp_time(t2,t3)
                if comp_res == "lt" or comp_res=="eq":
                    return 1
                elif comp_res=="unk":
                    return 0
                else:
                    return -1


def meets(i1, i2, i3, i4):
    # i2=i3
    if i2 == i3:
        return True
    else:
        return False



# before is a special order of disjoint
def disjoint(i1, i2, i3, i4):
    t1=FuzzyTime(i1)
    t2=FuzzyTime(i2)
    t3=FuzzyTime(i3)
    t4=FuzzyTime(i4)
    # i2<i3 || i4<i1
    if t1.isnotnull() and t2.isnotnull() and t3.isnotnull() and t4.isnotnull():
        if comp_time(t1, t3) == "eq" and comp_time(t2, t4) == "eq":
            return -1
        comp_res_t2t3=comp_time(t2,t3)
        comp_res_t4t1=comp_time(t4,t1)
        if comp_res_t2t3=="lt" or comp_res_t2t3=="eq" or comp_res_t4t1=="lt" or comp_res_t4t1=="eq":
            return 1
        elif comp_res_t2t3=="unk" or comp_res_t4t1=="unk":
            return 0
        else:
            return -1
    else:
        if t1.isnull():
            #i2!=-1
            if t3.isnull():
                #i4!=-1
                # (-,i2) (-,i4)
                return 0
            elif t4.isnull():
                #i3!=-1
                # (-,i2) (i3,-)
                comp_res_t2t3=comp_time(t2,t3)
                if comp_res_t2t3=="lt" or comp_res_t2t3=="eq":
                    return 1
                else:
                    return 0
            else:
                #i3&i4!=-1
                # (-,i2) (i3,i4)
                comp_res_t2t3=comp_time(t2,t3)
                comp_res_t2t4=comp_time(t2,t4)
                if comp_res_t2t3=="lt" or comp_res_t2t3=="eq":
                    return 1
                elif comp_res_t2t3=="gt" and comp_res_t2t4=="lt":
                    return -1
                else:
                    return 0
        elif t2.isnull():
            #i1!=-1
            if t3.isnull():
                #i4!=-1
                # (i1,-) (-,i4)
                comp_res_t1t4=comp_time(t1,t4)
                if comp_res_t1t4=="gt" or comp_res_t1t4=="eq":
                    return 1
                else:
                    return 0
            elif t4.isnull():
                #i3!=-1
                # (i1,-) (i3,-)

                return 0
            else:
                #i3&i4!=-1
                # (i1,-) (i3,i4)
                comp_res_t1t4=comp_time(t1,t4)
                comp_res_t1t3=comp_time(t1,t3)
                if comp_res_t1t4=="gt" or comp_res_t1t4=="eq":
                    return 1
                elif comp_res_t1t3=="gt" and comp_res_t1t4=="lt":
                    return -1
                else:
                    return 0
        else:
            #i1&i2!=-1
            if t3.isnull():
                # i4!=-1
                # (i1,i2) (-,i4)
                comp_res_t4t1=comp_time(t4,t1)
                comp_res_t4t2=comp_time(t4,t2)
                if comp_res_t4t1=="lt" or comp_res_t4t1=="eq":
                    return 1
                elif comp_res_t4t1=="gt" and comp_res_t4t2=="lt":
                    return -1
                else:
                    return 0
            else:
                # i3!=-1
                # (i1,i2) (i3,-)
                comp_res_t2t3=comp_time(t2,t3)
                comp_res_t3t1=comp_time(t3,t1)

                if comp_res_t2t3=="lt" or comp_res_t2t3=="eq":
                    return 1
                elif comp_res_t2t3=="gt" and comp_res_t3t1=="gt":
                    return -1
                else:
                    return 0



# during, equal, starts, finish are special cases of overlap
def overlap(i1, i2, i3, i4):
    if i2 >= i3 and i1 <= i4:
        return True
    else:
        return False

def include(i1, i2, i3, i4):
    t1=FuzzyTime(i1)
    t2=FuzzyTime(i2)
    t3=FuzzyTime(i3)
    t4=FuzzyTime(i4)
    if t1.isnotnull() and t2.isnotnull() and t3.isnotnull() and t4.isnotnull():
        comp_res_t1t3=comp_time(t1,t3)
        comp_res_t1t4=comp_time(t1,t4)
        comp_res_t2t3=comp_time(t2,t3)
        comp_res_t2t4=comp_time(t2,t4)
        if (comp_res_t1t3=="lt" or comp_res_t1t3=="eq") and (comp_res_t2t4=="gt" or comp_res_t2t4=="eq"):
            return 1
        elif (comp_res_t2t3=="gt" and comp_res_t2t4=="lt") or (comp_res_t1t3=="gt" and comp_res_t1t4=="lt") or (comp_res_t2t3=="lt") or (comp_res_t1t4=="gt"):
            return -1
        else:
            return 0
    else:
        if t1.isnull():
            #i2!=-1
            if t3.isnull():
                #i4!=-1
                # (-,i2) (-,i4)
                if comp_time(t2,t4)=="lt":
                    return -1
                else:
                    return 0
            elif t4.isnull():
                #i3!=-1
                # (-,i2) (i3,-)
                if comp_time(t2,t3)=="lt":
                    return -1
                else:
                    return 0
            else:
                #i3&i4!=-1
                # (-,i2) (i3,i4)
                if comp_time(t2,t4)=="lt":
                    return -1
                else:
                    return 0
        elif t2.isnull():
            #i1!=-1
            if t3.isnull():
                #i4!=-1
                # (i1,-) (-,i4)
                if comp_time(t1,t4)=="gt":
                    return -1
                else:
                    return 0
            elif t4.isnull():
                #i3!=-1
                # (i1,-) (i3,-)
                if comp_time(t1,t3)=="gt":
                    return -1
                else:
                    return 0
            else:
                #i3&i4!=-1
                # (i1,-) (i3,i4)
                if comp_time(t1,t3)=="gt":
                    return -1
                else:
                    return 0
        else:
            #i1&i2!=-1
            if t3.isnull():
                # i4!=-1
                # (i1,i2) (-,i4)
                comp_res_t4t1=comp_time(t4,t1)
                comp_res_t4t2=comp_time(t4,t2)
                if comp_res_t4t1=="lt" or comp_res_t4t2=="gt":
                    return -1
                else:
                    return 0
            else:
                # i3!=-1
                # (i1,i2) (i3,-)
                comp_res_t3t1=comp_time(t3,t1)
                comp_res_t3t2=comp_time(t3,t2)
                if comp_res_t3t1=="lt" or comp_res_t3t2=="gt":
                    return -1
                else:
                    return 0

def during(i1, i2, i3, i4):
    if i1 >= i3 and i2 <= i4:
        return True
    else:
        return False


def start(i1, i2, i3, i4):
    # i1=i3
    t1=FuzzyTime(i1)
    t2=FuzzyTime(i2)
    t3=FuzzyTime(i3)
    t4=FuzzyTime(i4)
    if t1.isnotnull() and t2.isnotnull() and t3.isnotnull() and t4.isnotnull():
        if comp_time(t1,t3)=="eq":
            return 1
        elif comp_time(t1,t3)=="unk":
            return 0
        else:
            return -1
    else:
        if t1.isnull():
            #i2!=-1
            if t3.isnull():
                #i4!=-1
                # (-,i2) (-,i4)
                return 0
            elif t4.isnull():
                #i3!=-1
                # (-,i2) (i3,-)
                if comp_time(t2,t3)=="lt":
                    return -1
                else:
                    return 0
            else:
                #i3&i4!=-1
                # (-,i2) (i3,i4)
                if comp_time(t2,t3)=="lt":
                    return -1
                else:
                    return 0
        elif t2.isnull():
            #i1!=-1
            if t3.isnull():
                #i4!=-1
                # (i1,-) (-,i4)
                if comp_time(t1,t4)=="gt":
                    return -1
                else:
                    return 0
            elif t4.isnull():
                #i3!=-1
                # (i1,-) (i3,-)
                if comp_time(t1,t3)=="eq":
                    return 1
                elif comp_time(t1,t3)=="unk":
                    return 0
                else:
                    return -1
            else:
                #i3&i4!=-1
                # (i1,-) (i3,i4)
                if comp_time(t1,t3)=="eq":
                    return 1
                elif comp_time(t1,t3)=="unk":
                    return 0
                else:
                    return -1
        else:
            #i1&i2!=-1
            if t3.isnull():
                # i4!=-1
                # (i1,i2) (-,i4)
                if comp_time(t4,t1)=="lt":
                    return -1
                else:
                    return 0
            else:
                # i3!=-1
                # (i1,i2) (i3,-)
                if comp_time(t1,t3)=="eq":
                    return 1
                elif comp_time(t1,t3)=="unk":
                    return 0
                else:
                    return -1


def finish(i1, i2, i3, i4):
    # i2=i4
    t1=FuzzyTime(i1)
    t2=FuzzyTime(i2)
    t3=FuzzyTime(i3)
    t4=FuzzyTime(i4)
    if t1.isnotnull() and t2.isnotnull() and t3.isnotnull() and t4.isnotnull():
        if comp_time(t2,t4)=="eq":
            return 1
        elif comp_time(t2,t4)=="unk":
            return 0
        else:
            return -1
    else:
        if t1.isnull():
            # i2!=-1
            if t3.isnull():
                # i4!=-1
                # (-,i2) (-,i4)
                if comp_time(t2,t4)=="eq":
                    return 1
                elif comp_time(t2,t4)=="unk":
                    return 0
                else:
                    return -1
            elif t4.isnull():
                # i3!=-1
                # (-,i2) (i3,-)
                if comp_time(t2,t3)=="lt":
                    return -1
                else:
                    return 0
            else:
                # i3&i4!=-1
                # (-,i2) (i3,i4)
                if comp_time(t2,t4)=="eq":
                    return 1
                elif comp_time(t2,t4)=="unk":
                    return 0
                else:
                    return -1
        elif t2.isnull():
            # i1!=-1
            if t3.isnull():
                # i4!=-1
                # (i1,-) (-,i4)
                if comp_time(t1,t4)=="gt":
                    return -1
                else:
                    return 0
            elif t4.isnull():
                # i3!=-1
                # (i1,-) (i3,-)

                return 0
            else:
                # i3&i4!=-1
                # (i1,-) (i3,i4)
                if comp_time(t1,t4)=="gt":
                    return -1
                else:
                    return 0
        else:
            # i1&i2!=-1
            if t3.isnull():
                # i4!=-1
                # (i1,i2) (-,i4)
                if comp_time(t2,t4)=="eq":
                    return 1
                elif comp_time(t2,t4)=="unk":
                    return 0
                else:
                    return -1
            else:
                # i3!=-1
                # (i1,i2) (i3,-)
                if comp_time(t2,t3)=="lt":
                    return -1
                else:
                    return 0


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