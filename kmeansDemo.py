
from sys import argv

from kmeans import cluster, manhattenDistance, euclidianDistance, pointsInCluster,outliers
from utility import getOpts
from fileIOUtils import CSVLoad

def tupFromString(s):
    return tuple([float(substr) for substr in s.split(',')])

opts=getOpts(argv)

sufficientParameters=True

if "-file" not in opts:
    sufficientParameters=False
    print("You need to provide points to cluster")
if "-distFunc" not in opts:
    sufficientParameters=False
    print("You need to provide a distance function")
if "-dist" not in opts:
    sufficientParameters=False
    print("You need to provide cluster size")
if "-centers" not in opts:
    sufficientParameters=False
    print("you need to provide initial points for the clusterer")
if not sufficientParameters:
    exit()

if opts["-distFunc"][0] not in ["e","m"]:
    print("You must use either euclidian ('e') or manhatten ('m') distance")
    exit()

centIt=iter(opts["-centers"])
centers = [(float(x),float(next(centIt))) for x in centIt]
points = [tuple(row) for row in CSVLoad(opts["-file"][0])]
distFunc = euclidianDistance if opts["-distFunc"][0]=='e' else manhattenDistance
maxDist = float(opts["-dist"][0])

centers = cluster(points,centers,maxDist,distFunc)
clusters = [(cent,pointsInCluster(points,cent,maxDist,distFunc)) for cent in centers]
unclustered=outliers(points,centers,maxDist,distFunc)

for clust in clusters:
    print("\nCluster of "+str(len(clust[1]))+" points, centroid: "+str(clust[0]))
    print("points:")
    for point in clust[1]:
        print(point)

print("\nThere were "+str(len(unclustered))+" outliers:")
for point in unclustered:
    print(point)

