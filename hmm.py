from numpy import array, matmul
from numpy.linalg import matrix_power
from itertools import product as cartProd

class HiddenMarkovModel:
    def __init__(self,Transition,Emission,initialProb):
        if not (isinstance(Transition,array) and isinstance(Emission,array) and isinstance(initialProb,array)):
            self._T_=None
            self._E_=None
            self._I_=None
        if Transition.dimentions()[0]!=Emission.dimentions()[1]:
            self._T_=None
            self._E_=None
            self._I_=None

        self._T_=Transition
        self._E_=Emission
        self._I_ = initialProb

    def valid(self):
        return not (self._E_ is None or self._T_ is None)

    def probAfter(self,initialProbs,numTransitions):
        if numTransitions==0:
            return initialProbs

        return matmul(matrix_power(self._T_,numTransitions),initialProbs)

    def probOfTransSequence(self,sequence,initialProb=None):
        if initialProb is None:
            initialProb=self._I_
        res=1
        for i,state in sequence:
            if i==0:
                res*=initialProb
            else:
                res*=self._T_[state][sequence[i-1]]
        return res

    def probOfEmissionAndTransitions(self,tSequence,eSequece,initialProbability=None):
        if initialProbability is None:
            initialProbability=self._I_
        if len(tSequence)!=len(eSequece) or len(initialProbability!=len(self._T_)):
            return None

        res=1
        for i in range(0,len(tSequence)):
            if i==0:
                res*=initialProbability[tSequence[i]]*self._E_[eSequece[i]][tSequence[i]]
            else:
                res*=self._T_[tSequence[i]][tSequence[i-1]]*self._E_[eSequece[i]][tSequence[i]]
        return res

    def probOfEmission(self,eSequence,initialProbability=None):
        if initialProbability is None:
            initialProbability=self._I_
        res=1
        for i,emission in enumerate(eSequence):
            res*=matmul(emission,self.probAfter(initialProbability,i))[emission]
        return res

    def mostProbPath(self,eSequence,initialProbability=None):
        maxProd=0
        res=None
        for tSequence in cartProd(list(range(0,len(self._I_))),len(eSequence)):
            p=self.probOfEmissionAndTransitions(tSequence,eSequence,initialProbability)
            if p>maxProd:
                maxProd=p
                res=tSequence

        return res,self.probOfSequenceGivenEmission(res,eSequence,initialProbability)

    def probOfSequenceGivenEmission(self,tSequence,eSequence,initialProbability):
        pEandT=self.probOfEmissionAndTransitions(tSequence,eSequence,initialProbability)
        pE=self.probOfEmission(eSequence,initialProbability)
        if pEandT is None or pE is None:
            return None
        return pEandT/pE