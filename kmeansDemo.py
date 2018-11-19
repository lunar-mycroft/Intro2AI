from pointGenerator import makePoints
from kmeans import cluster
from math import sqrt

centers=[
    (2,2),
    (4,4),
    (2,4),
    (3,3)
]
sizes=[
    (0.35,0.35),
    (0.35,0.35),
    (0.35,0.35),
    (3,3)
]

dif=lambda vec1,vec2: tuple(map(lambda x1,x2:x1-x2,vec1,vec2))
mag=lambda vec:sqrt(sum(map(lambda comp:comp**2,vec)))
dist=lambda vec1,vec2:mag(dif(vec1,vec2))

points=makePoints(centers,[.3,.3,.3,.1],sizes,100)