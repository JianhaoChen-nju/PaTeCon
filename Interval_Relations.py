# (i1,i2)  (i3,i4)
# meets is a special case of before
# a naive strategy
# if i1==-1 or i2==-1 or i3==-1 or i4==-1:

def foundation(i1, i2):
    if i1 <= i2:
        return True
    else:
        return False


def before(i1, i2, i3, i4):
    # i2<=i3
    if i1 != -1 and i2 != -1 and i3 != -1 and i4 != -1:
        if i2 <= i3:
            return 1
        else:
            return -1
    else:
        if i1==-1:
            #i2!=-1
            if i3==-1:
                #i4!=-1
                # (-,i2) (-,i4)
                if i2 > i4:
                    return -1
                else:
                    return 0
            elif i4==-1:
                #i3!=-1
                # (-,i2) (i3,-)
                if i2<=i3:
                    return 1
                else:
                    return -1
            else:
                #i3&i4!=-1
                # (-,i2) (i3,i4)
                if i2<=i3:
                    return 1
                else:
                    return -1
        elif i2==-1:
            #i1!=-1
            if i3==-1:
                #i4!=-1
                # (i1,-) (-,i4)
                if i1 > i4:
                    return -1
                else:
                    return 0
            elif i4==-1:
                #i3!=-1
                # (i1,-) (i3,-)
                if i1 > i3:
                    return -1
                else:
                    return 0
            else:
                #i3&i4!=-1
                # (i1,-) (i3,i4)
                if i1 > i3:
                    return -1
                else:
                    return 0
        else:
            #i1&i2!=-1
            if i3 == -1:
                # i4!=-1
                # (i1,i2) (-,i4)
                if i4 < i2:
                    return -1
                else:
                    return 0
            else:
                # i3!=-1
                # (i1,i2) (i3,-)
                if i2 <= i3:
                    return 1
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
    # i2<i3 || i4<i1
    if i1!=-1 and i2!=-1 and i3!=-1 and i4!=-1:
        if i2 <= i3 or i4 <= i1:
            return 1
        else:
            return -1
    else:
        if i1==-1:
            #i2!=-1
            if i3==-1:
                #i4!=-1
                # (-,i2) (-,i4)
                return 0
            elif i4==-1:
                #i3!=-1
                # (-,i2) (i3,-)
                if i2<=i3:
                    return 1
                else:
                    return 0
            else:
                #i3&i4!=-1
                # (-,i2) (i3,i4)
                if i2<=i3:
                    return 1
                elif i2>=i4:
                    return 0
                else:
                    return -1
        elif i2==-1:
            #i1!=-1
            if i3==-1:
                #i4!=-1
                # (i1,-) (-,i4)
                if i1>=i4:
                    return 1
                else:
                    return 0
            elif i4==-1:
                #i3!=-1
                # (i1,-) (i3,-)

                return 0
            else:
                #i3&i4!=-1
                # (i1,-) (i3,i4)
                if i1>=i4:
                    return 1
                elif i1<=i3:
                    return 0
                else:
                    return -1
        else:
            #i1&i2!=-1
            if i3 == -1:
                # i4!=-1
                # (i1,i2) (-,i4)
                if i4<=i1:
                    return 1
                elif i4>=i2:
                    return 0
                else:
                    return -1
            else:
                # i3!=-1
                # (i1,i2) (i3,-)
                if i2 <= i3:
                    return 1
                elif i3<=i1:
                    return 0
                else:
                    return -1



# during, equal, starts, finish are special cases of overlap
def overlap(i1, i2, i3, i4):
    if i2 >= i3 and i1 <= i4:
        return True
    else:
        return False

def include(i1, i2, i3, i4):
    if i1 != -1 and i2 != -1 and i3 != -1 and i4 != -1:
        if i1 <= i3 and i2 >= i4:
            return 1
        else:
            return -1
    else:
        if i1==-1:
            #i2!=-1
            if i3==-1:
                #i4!=-1
                # (-,i2) (-,i4)
                if i2<i4:
                    return -1
                else:
                    return 0
            elif i4==-1:
                #i3!=-1
                # (-,i2) (i3,-)
                if i2 < i3:
                    return -1
                else:
                    return 0
            else:
                #i3&i4!=-1
                # (-,i2) (i3,i4)
                if i2 < i4:
                    return -1
                else:
                    return 0
        elif i2==-1:
            #i1!=-1
            if i3==-1:
                #i4!=-1
                # (i1,-) (-,i4)
                if i1 > i4:
                    return -1
                else:
                    return 0
            elif i4==-1:
                #i3!=-1
                # (i1,-) (i3,-)
                if i1>i3:
                    return -1
                else:
                    return 0
            else:
                #i3&i4!=-1
                # (i1,-) (i3,i4)
                if i1>i3:
                    return -1
                else:
                    return 0
        else:
            #i1&i2!=-1
            if i3 == -1:
                # i4!=-1
                # (i1,i2) (-,i4)
                if i4>=i1 and i4<=i2:
                    return 0
                else:
                    return -1
            else:
                # i3!=-1
                # (i1,i2) (i3,-)
                if i3>=i1 and i3 <= i2:
                    return 0
                else:
                    return -1

def during(i1, i2, i3, i4):
    if i1 >= i3 and i2 <= i4:
        return True
    else:
        return False


def start(i1, i2, i3, i4):
    # i1=i3

    if i1 != -1 and i2 != -1 and i3 != -1 and i4 != -1:
        if i1 == i3:
            return 1
        else:
            return -1
    else:
        if i1==-1:
            #i2!=-1
            if i3==-1:
                #i4!=-1
                # (-,i2) (-,i4)
                return 0
            elif i4==-1:
                #i3!=-1
                # (-,i2) (i3,-)
                if i2 < i3:
                    return -1
                else:
                    return 0
            else:
                #i3&i4!=-1
                # (-,i2) (i3,i4)
                if i2 < i3:
                    return -1
                else:
                    return 0
        elif i2==-1:
            #i1!=-1
            if i3==-1:
                #i4!=-1
                # (i1,-) (-,i4)
                if i1 > i4:
                    return -1
                else:
                    return 0
            elif i4==-1:
                #i3!=-1
                # (i1,-) (i3,-)
                if i1==i3:
                    return 1
                else:
                    return -1
            else:
                #i3&i4!=-1
                # (i1,-) (i3,i4)
                if i1==i3:
                    return 1
                else:
                    return -1
        else:
            #i1&i2!=-1
            if i3 == -1:
                # i4!=-1
                # (i1,i2) (-,i4)
                if i4 < i1:
                    return -1
                else:
                    return 0
            else:
                # i3!=-1
                # (i1,i2) (i3,-)
                if i1==i3:
                    return 1
                else:
                    return -1


def finish(i1, i2, i3, i4):
    # i2=i4
    if i1 != -1 and i2 != -1 and i3 != -1 and i4 != -1:
        if i2 == i4:
            return 1
        else:
            return -1
    else:
        if i1 == -1:
            # i2!=-1
            if i3 == -1:
                # i4!=-1
                # (-,i2) (-,i4)
                if i2==i4:
                    return 1
                else:
                    return -1
            elif i4 == -1:
                # i3!=-1
                # (-,i2) (i3,-)
                if i2 < i3:
                    return -1
                else:
                    return 0
            else:
                # i3&i4!=-1
                # (-,i2) (i3,i4)
                if i2 == i4:
                    return 1
                else:
                    return -1
        elif i2 == -1:
            # i1!=-1
            if i3 == -1:
                # i4!=-1
                # (i1,-) (-,i4)
                if i1 > i4:
                    return -1
                else:
                    return 0
            elif i4 == -1:
                # i3!=-1
                # (i1,-) (i3,-)

                return 0
            else:
                # i3&i4!=-1
                # (i1,-) (i3,i4)
                if i1 > i4:
                    return -1
                else:
                    return 0
        else:
            # i1&i2!=-1
            if i3 == -1:
                # i4!=-1
                # (i1,i2) (-,i4)
                if i2==i4:
                    return 1
                else:
                    return -1
            else:
                # i3!=-1
                # (i1,i2) (i3,-)
                if i2 < i3:
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