from numpy import array


def vectorString(vector):
    res = "\\left(\\begin{matrix}"
    for item in vector:
        res=res+str(round(item,3))+'\\\\'
    return res + '\\end{matrix}\\right)'

def matrixString(matrix):
    if len(matrix.shape)==1:
        return vectorString(matrix)

    res="\\left(\\begin{matrix}\n"

    for row in matrix:
        for i,item in enumerate(row):
            res=res+('    ' if i==0 else ' & ')+str(round(item,3))
        res=res+'\\\\\n'

    return res+'\\end{matrix}\\right)'
