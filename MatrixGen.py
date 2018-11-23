from random import shuffle, uniform
from numpy import transpose

def randomHMMMatrix(size,digits=None):
    res=[]
    for i in range(0,size[0]):
        res.append(randRow(size[1],digits))
    return transpose(res)

def randRow(size,digits):
    res=[]
    s=0
    for i in range(0,size-1):
        val=uniform(0,1-s)
        if isinstance(digits,int):
            val=round(val,digits)
        s+=val
        res.append(val)
    val = 1-s
    if isinstance(digits, int):
        val = round(val, digits)
    res.append(val)
    shuffle(res)
    return res