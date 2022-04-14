# (i1,i2)  (i3,i4)
# meets is a special case of before
def foundation(i1, i2):
    if i1 <= i2:
        return True
    else:
        return False


def before(i1, i2, i3, i4):
    # i2<=i3
    if i2 <= i3:
        return True
    else:
        return False


def meets(i1, i2, i3, i4):
    # i2=i3
    if i2 == i3:
        return True
    else:
        return False


# before is a special order of disjoint
def disjoint(i1, i2, i3, i4):
    # i2<i3 || i4<i1
    if i2 <= i3 or i4 <= i1:
        return True
    else:
        return False


# during, equal, starts, finish are special cases of overlap
def overlap(i1, i2, i3, i4):
    if i2 >= i3 and i1 <= i4:
        return True
    else:
        return False


def during(i1, i2, i3, i4):
    if i1 >= i3 and i2 <= i4:
        return True
    else:
        return False


def start(i1, i2, i3, i4):
    # i1=i3
    if i1 == i3:
        return True
    else:
        return False


def finish(i1, i2, i3, i4):
    # i2=i4
    if i2 == i4:
        return True
    else:
        return False


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