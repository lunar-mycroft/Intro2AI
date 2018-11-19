from random import gauss,uniform
from kmeans import isValidPoint, isValidPointSet

def choices(items,weights):
    if len(items)!=len(weights):
        return None
    for item in weights:
        if not isinstance(item,float) or isinstance(item,int):
            return False
        if item<0:
            return None

    p=uniform(0,1)
    s=0
    for item,weight in zip(items,weights):
        s+=weight
        if s>=p:
            return item

    return item[-1]

def makePointInCluster(center,size):
    res=[]
    for mu,sigma in zip(center,size):
        res.append(gauss(mu,sigma))
    return tuple(res)

def makePointUniform(center,size):
    res=[]
    for mu,sigma in zip(center,size):
        res.append(uniform(mu-sigma,mu+sigma))
    return tuple(res)

def makePoint(centers,centerWeights,sizes):

    index=choices(range(0,len(sizes)),centerWeights)
    if index==len(sizes)-1:
        return makePointUniform(centers[-1],sizes[-1])
    return makePointInCluster(centers[index],sizes[index])



def makePoints(centers,centerWeights,sizes,n):
    if not isValidPointSet(centers) or not isValidPointSet(sizes):
        return None
    if len(centers)!=len(sizes) or len(centers)!=len(centerWeights):
        return None
    if len(centers)==0:
        return None
    for term in centerWeights:
        if not (isinstance(term,float) or isinstance(term,int)):
            return None
        if term>1 or term<0:
            return None
    if sum(centerWeights)>1.001 or sum(centerWeights)<0.999:

        return None

    res=[]
    for i in range(0,n):
        res.append(makePoint(centers,centerWeights,sizes))
    return res