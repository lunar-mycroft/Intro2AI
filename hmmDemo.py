from hmm import HiddenMarkovModel
from numpy import array

T=array([
    [0.2,0.0,0.3,0.0],
    [0.7,0.0,0.3,0.5],
    [0.0,0.7,0.0,0.5],
    [0.1,0.3,0.0,0.0]
])
E=array([
    [0.6,0.2,0.0,0.2],
    [0.4,0.2,0.0,0.4],
    [0.0,0.6,0.2,0.2],
    [0.0,0.0,0.8,0.2]
])
I=array([0.3,0.4,0.3,0.0])

model=HiddenMarkovModel(T,E,I)

print(model.mostProbPath([0,1,2,3]))