from time import time
from numpy import  matmul
from numpy.linalg import inv as invert

class polynomial:
    def __init__(self,coeffs):
        self.A=coeffs
    def __str__(self):
        res=""
        for i,a in enumerate(reversed(self.A)):
            p=len(self.A)-(i+1)
            res+=str(round(a,3))+("x"+("^"+str(p) if p>1 else "") if p>0 else "")+"+"
        return res[:-1]

    def __call__(self, x):
        res=0
        for p,a in enumerate(self.A):
            res+=a*(x**p)
        return res

def sum2Power(data,power):
    if power==0:
        return len(data)
    if power==1:
        return sum(data)
    return sum(map(lambda x:x**power,data))

def regressVectorTerm(data,power):
    if power==0:
        return sum(map(lambda x: x[1],data))

    return sum(map(lambda x: x[1]*(x[0]**power),data))

def regressVector(data,degree):
    result=[]
    for i in range(0,degree+1):
        result.append(regressVectorTerm(data,i))
    return result

def regressMatrix(data,degree):
    result=[]
    for i in range(0,degree+1):
        row=[]
        for j in range(0,degree+1):
            row.append(sum2Power(data,i+j))
        result.append(row)
    return result

def polyFit(data,degree):
    if len(data)<degree:
        return 1, None
    if len(data)<2*degree:
        return 2, None
    xOnly=list(map(lambda x:x[0],data))

    return None, (polynomial(matmul(regressVector(data,degree),invert(regressMatrix(xOnly,degree)))))