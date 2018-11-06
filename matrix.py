from numpy import matmul,add,subtract,array
from numpy.linalg import inv as invert

class Matrix:
    def __init__(self,m,n):
        l=[]
        for i in range(0,m):
            row=[]
            for j in range(0,n):
                row.append(0)
            l.append(row)
        self._m_=array(l)

    @staticmethod
    def identity(n):
        res=Matrix(n,n)
        for i in range(0,n):
            res[i][i]=1
        return res

    def dimentions(self):
        return len(self._m_),len(self._m_[0])

    def inverted(self):
        if self.dimentions()[0]!=self.dimentions()[1]:
            return None
        res=Matrix(1,1)
        res._m_=invert(self._m_)
        return res

    def __getitem__(self, item):
        if not isinstance(item,int):
            return None
        return self._m_[item % len(self._m_)]
    def __setitem__(self, key, value):
        if not isinstance(key,int):
            return
        if not isinstance(value,list):
            return
        if not len(value)==len(self._m_[key % len(self._m_)]):
            return

        self._m_[key % len(self._m_)]=value

    def __add__(self, other):
        if not isinstance(other,Matrix):
            return None
        if not self.dimentions()[0]==other.dimentions()[0] and self.dimentions()[1]==other.dimentions()[1]:
            return None
        res=Matrix(1,1)
        res._m_=add(self._m_,other._m_)
        return res

    def __sub__(self, other):
        if not isinstance(other,Matrix):
            return None
        if not self.dimentions()[0]==other.dimentions()[0] and self.dimentions()[1]==other.dimentions()[1]:
            return None
        res=Matrix(1,1)
        res._m_=subtract(self._m_,other._m_)
        return res

    def __mul__(self, other):
        if isinstance(other,float) or isinstance(other,int):
            res = Matrix(self.dimentions()[0], self.dimentions()[1])
            res._m_=self._m_*other
        if not isinstance(other,Matrix):
            return None
        if not other.dimentions()[1]==other.dimentions()[0]:
            return None

        res=Matrix(1,1)
        res._m_=matmul(self._m_,other._m_)
        return res

    def __truediv__(self,other):
        if isinstance(other,float) or isinstance(other,int):
            return self*(1/other)
        if not isinstance(other,Matrix):
            return None
        return self*other.inverted()

    def __pow__(self, power, modulo=None):
        if not (isinstance(power,int) or (isinstance(power,float) and int(power)==power)):
            return None
        if self.dimentions()[0]!=self.dimentions()[1]:
            return None

        if power==0:
            return Matrix.identity(self.dimentions()[0])
        if power<0:
            return (self**abs(power)).inverted()

        res=Matrix(1,1)
        res._m_=self._m_
        for i in range(0,self.dimentions()[0]):
            res=res*self
        return res


