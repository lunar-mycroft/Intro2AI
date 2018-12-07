from math import exp, sqrt
from numpy import array, matmul, subtract

from neuralNet import NeuralNet

round1000=lambda x: float(int(x*1000+0.5)/1000)

HWNet=NeuralNet(3)

HWNet.addLayer(4,lambda x:1.5/(1+exp(-x)),lambda x :1.5*exp(-x)/((1+exp(-x))**2))
HWNet.layers[-1].weights=array([
    [-0.1,0,0],
    [0.7,0.4,0],
    [0,0.5,-0.3],
    [0,0.9,-0.2]
])
HWNet.addLayer(3,lambda x:1.5/(1+exp(-x)),lambda x :1.5*exp(-x)/((1+exp(-x))**2))
HWNet.layers[-1].weights=array([
    [0.2,0.5,0,0],
    [0.3,0.6,0,0],
    [0,0.4,0.2,0.8]
])

trainintData=[
    ([1,1,0],[1,0,1]),
    ([1,0,1],[1,1,0]),
    ([0,0,0],[0,0,0]),
    ([0,1,0],[0,0,1])
]

def makeCostTable(tData):
    s = 0
    for i,scenario in enumerate(tData):
        res=[]
        for n in HWNet(scenario[0]):
            res.append(round1000(n))
        error=subtract(res,scenario[1])
        errorScale=sqrt(matmul(error,error))
        print('$'+str(i+1)+'$ &$'+str(tuple(scenario[0]))+'$ & $'+str(tuple(scenario[1]))+'$ & $'+str(tuple(res))+'$ & $'+str(round(errorScale,3))+'$\\\\')
        print('\\hline')
        s+=errorScale

    print(round(s,4))

HWNet.train(trainintData,0.1,25)
makeCostTable(trainintData)