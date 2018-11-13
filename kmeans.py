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

    res=[]
    for axis in points[0]:
        res.append(0)

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
    if not isValidPointSet(points) or not isValidPointSet(centroids):
        return None
    if len(points[0])!=len(centroids[0]):
        return None

    res=[]
    for cent in centroids:
        res.append(centroid(pointsInCluster(points,cent,distance,distanceFunction)))

    return res

