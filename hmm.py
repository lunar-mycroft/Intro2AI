from matrix import Matrix

def matrixOf1s(n,m):
    res=[]
    for i in range(0,n):
        row=[]
        for j in range(0,m):
            row.append(1)
        res.append(row)

class HiddenMarkovModel:
    def __init__(self,Transition,Emission):
        if not (isinstance(Transition,Matrix) and isinstance(Emission,Matrix)):
            self._T_=None
            self._E_=None
        if Transition.dimentions()[0]==Emission.dimentions()[1]:
            self._T_=None
            self._E_=None

        self._T_=Transition
        self._E_=Emission

    def valid(self):
        return not (self._E_==None or self._T_==None)