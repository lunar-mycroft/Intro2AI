from math import sqrt

def euclidianDistance(vec1,vec2):
    if len(vec1)!=len(vec2):
        return None
    return sqrt(sum((x1-x2)**2 for x1,x2 in zip(vec1,vec2)))

def manhattenDistance(vec1,vec2):
    if len(vec1)!=len(vec2):
        return None
    return sum(abs(x1-x2) for x1,x2 in zip(vec1,vec2))

def isValidPoint(point,length=None):
    if not isinstance(point,tuple):
        return False

    if length!=None and len(point)!=length:
        return False

    for axis in point:
        if not (isinstance(axis,float) or isinstance(axis,int)):
            return False
    return True

def isValidPointSet(points):
    if not isinstance(points,list):
        return False
    if not isValidPoint(points[0]):
        return False

    numAxes=len(points[0])

    for point in points:
        if not isValidPoint(point,numAxes):
            return False
    return True

def centroid(points):
    if not isValidPointSet(points):
        return None

    res=[0 for element in points[0]]
    n=len(points);

    for point in points:
        for i,axis in enumerate(point):
            res[i]+=axis/n

    return tuple(res)

def pointsInCluster(points,cent,distance,distanceFunction):
    if not isValidPointSet(points) or not isValidPoint(cent):
        return None
    if len(points[0])!=len(cent):
        return None

    return list(filter(lambda point: distanceFunction(point,cent)<=distance,points))

def optimizeCentroids(points,centroids,distance,distanceFunction):
    res=[]
    updated=False
    for cent in centroids:
        newCent=centroid(pointsInCluster(points,cent,distance,distanceFunction))
        if newCent!=cent:
            updated=True
        res.append(centroid(pointsInCluster(points,cent,distance,distanceFunction)))

    return updated,res

def cluster(points,seeds,distance,distanceFunction,n=None):
    if not isValidPointSet(points) or not isValidPointSet(seeds):
        return None
    if len(points[0])!=len(seeds[0]):
        return None

    res=[]
    i=0
    while n is None or i<n:
        i+=1
        updated,seeds=optimizeCentroids(points,seeds,distance,distanceFunction)
        if not updated:
            break
    return seeds

def pointInAnyCluster(point,centroids,distance,distanceFunction):
    for cent in centroids:
        if distanceFunction(cent,point)<=distance:
            return True
    return False

def outliers(points,centroids,distance,distanceFunction):
    return list(filter(lambda point: not pointInAnyCluster(point,centroids,distance,distanceFunction),points))