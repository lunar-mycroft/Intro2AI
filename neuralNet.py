from numpy import array, ones,zeros, matmul
from random import uniform

from printingUtils import matrixString

from math import sqrt

def errorFunc(goal,actual):
    return sqrt(sum(map(lambda g,a:(g-a)**2,goal,actual)))

class NNLayer:
    def __init__(self,nNodesPrev,nNodes,activation,dSigmadZ):
        self.activation=activation
        self.dSigmadZ=dSigmadZ
        self.weights=ones((nNodes,nNodesPrev))
        self.biases=zeros(nNodes)

    def __call__(self, prev):
        return array(list(map(self.activation,self.Z(prev))))

    def __str__(self):
        return "Weights:\n"+matrixString(self.weights)+"\nBiases:\n"+matrixString(self.biases)

    def randomize(self,minVal=-1,maxVal=1):
        n=self.nNext()
        m=self.nPrev()

        self.weights=array([[uniform(minVal,maxVal) for j in range(0,m)] for i in range(0,n)])
        self.biases=array([uniform(minVal,maxVal) for i in range(0,n)])


    def Z(self,prev):
        try:
            return matmul(self.weights,prev)+self.biases
        except:
            print(self.weights)
            print(prev)
            print(self.biases)
            exit()

    def CommonDerivatives(self,nextCDs,prevActivations):
        Z=self.Z(prevActivations)
        res=[]

        for k in range(0, len(self.weights[0])):
            s=0
            for j in range(0,len(self.weights)):
                s+=nextCDs[j]*self.dSigmadZ(Z[j])
            res.append(s)
        return array(res)

    def weightGrad(self,NextCDs,prevActivations):
        res=[]
        Z=self.Z(prevActivations)
        for j in range(0,len(self.weights)):
            row=[]
            dSigmaDz=self.dSigmadZ(Z[j])
            for k in range(0, len(self.weights[0])):
                row.append(dSigmaDz*prevActivations[k]*NextCDs[j])
            res.append(row)
        return array(res)

    def biasGrad(self,NextCDs,prevActivations):
        res=[]
        Z = self.Z(prevActivations);
        for j in range(0, len(self.weights)):
            res.append(Z[j]*NextCDs[j])
        return array(res)

    def addGrad(self,grad,alpha):
        self.weights+=grad[0]*alpha
        self.biases+=grad[1]*alpha

    def nPrev(self):
        return len(self.weights[0])
    def nNext(self):
        return len(self.biases)


class NeuralNet:
    def __init__(self,nInputs):
        self.layers=[]
        self.nInputs=nInputs

    def addLayer(self,n,activation,dSigmadZ):
        if not (isinstance(n,int)):
            return
        if n<=0:
            return

        nPrev=self.nInputs if len(self.layers)==0 else self.layers[-1].nNext()
        self.layers.append(NNLayer(nPrev,n,activation,dSigmadZ))

    def grad(self,I,T):
        #Takes the input (I) and the target(T) and returns a list of tupples o numpyArrays for the gradients with respect to each layer's weights and bias

        if not (isinstance(I,list) or isinstance(I,array)):
            return
        if not (isinstance(T,list) or isinstance(T,array)):
            return

        activations=[array(I)]
        Zs=[array(I)]
        for layer in self.layers:
            activations.append(array(layer(activations[-1])))
            Zs.append(array(layer.Z(activations[-2])))

        vec=[]
        for i,t in enumerate(T):
            o=activations[-1][i]
            vec.append(2*(t-o))
        commonDerivatives=[(array(vec))]
        res=[]
        for L,layer in enumerate(reversed(self.layers)):
            weights=layer.weightGrad(commonDerivatives[-1],activations[-(L+2)])
            biases=layer.biasGrad(commonDerivatives[-1],activations[-(L+2)])
            commonDerivatives.append(layer.CommonDerivatives(commonDerivatives[-1],activations[-(L+2)]))
            res.append((weights,biases))
        return list(reversed(res))

    def addGrad(self,grad,alpha):
        for layerGrad,layer in zip(grad,self.layers):
            layer.addGrad(layerGrad,alpha)

    def trainingIteration(self,trainingData,trainingRate):
        alpha=trainingRate/len(trainingData)
        grad=None;
        for example in trainingData:
            newGrad =self.grad(example[0],example[1])
            if grad is None:
                grad=newGrad
            else:
                res=[]
                for old,new in zip(grad,newGrad):
                    res.append((old[0]+new[0],old[1]+new[1]))
                grad=res
        self.addGrad(grad,alpha)

    def train(self,trainingData,trainingRate,n):
        for i in range(0,n):
            self.trainingIteration(trainingData,trainingRate)

    def totalError(self,trainingData,costFunc):
        return sum(map(lambda example: costFunc(self(example[0]),example[1]),trainingData))

    def __str__(self):
        res=''
        for L,layer in enumerate(self.layers):
            res=res+"\nLayer "+str(L)+'\n'+str(layer)
        return res
    def __call__(self, input):
        if not (isinstance(input,list) or isinstance(input,array)):
            return
        if not len(input)==self.nInputs:
            return

        output=input
        for layer in self.layers:
            output=layer(output)

        return output