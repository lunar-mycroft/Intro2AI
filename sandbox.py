from numpy import array
from math import sqrt

def vecMag(vec):
    return sqrt(sum(x**2 for x in vec))

def vectorDistanceMatrix(A):
    result=[]
    for vec1 in A:
        row=[]
        for vec2 in A:
            row.append(vecMag(array(vec1)-array(vec2)))
        result.append(row)
    return result

