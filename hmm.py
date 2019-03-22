from numpy import array, matmul,ndarray
from numpy.linalg import matrix_power
from itertools import product as cartProd

class HiddenMarkovModel:
    def __init__(self,Transition,Emission,initialProb):
        if not (isinstance(Transition,ndarray) and isinstance(Emission,ndarray) and isinstance(initialProb,ndarray)):
            self._T_=None
            self._E_=None
            self._I_=None
        if len(Transition[0])!=len(Transition[1]) or len(Transition[0])!=len(Emission[0]):
            self._T_=None
            self._E_=None
            self._I_=None

        self._T_=Transition
        self._E_=Emission
        self._I_ = initialProb

    def valid(self):
        return not (self._E_ is None or self._T_ is None)

    def probAfter(self,numTransitions,initialProbs=None):
        if initialProbs is None:
            initialProbs=self._I_
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
        if len(tSequence)!=len(eSequece) or len(initialProbability)!=len(self._T_):
            print(initialProbability)
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
        res=0
        for possibility in cartProd(list(range(0,len(self._I_))),repeat=len(eSequence)):
            res+=self.probOfEmissionAndTransitions(possibility,eSequence)
        return res

    def mostProbPath(self,eSequence,initialProbability=None):
        maxProd=0
        res=None
        for tSequence in cartProd(list(range(0,len(self._I_))),repeat=len(eSequence)):
            p=self.probOfEmissionAndTransitions(tSequence,eSequence,initialProbability)
            print("Trying ",tSequence)
            print("P =",self.probOfSequenceGivenEmission(tSequence,eSequence,initialProbability))
            try:
                if p>maxProd:
                    maxProd=p
                    res=tSequence
            except:
                print(p,maxProd)
                exit()

        return res , self.probOfSequenceGivenEmission(res,eSequence,initialProbability)

    def probOfSequenceGivenEmission(self,tSequence,eSequence,initialProbability):
        pEandT=self.probOfEmissionAndTransitions(tSequence,eSequence,initialProbability)
        pE=self.probOfEmission(eSequence,initialProbability)
        if pEandT is None or pE is None:
            return None
        return pEandT/pE