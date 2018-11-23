from csv import reader, writer
from numpy import array
from hmm import HiddenMarkovModel

def loadHMM(path):
    dump=CSVLoad(path)
    numStates=int(dump[0][0])
    numEmissions=int(dump[0][1])
    T=matrixFromDump(dump,(1,0),(1+numStates,numStates))
    E=matrixFromDump(dump,(1+numStates,0),(1+numStates+numEmissions,numStates))
    I=matrixFromDump(dump,(1+numStates+numEmissions,0),(2+numStates+numEmissions,numStates))

    return HiddenMarkovModel(T,E,I[0])

def saveHMM(path,model):
    numStates=len(model._T_)
    numEmissions=len(model._E_)

    toSave=[[numStates,numEmissions]]
    toSave.extend(model._T_)
    toSave.extend(model._E_)
    toSave.extend(model._I_)
    CSVSave(toSave,path)

def matrixFromDump(dump,topLeft,botRight):
    if not topLeft[0]<botRight[0] or not topLeft[1]<botRight[1]:
        return None
    try:
        trimed=[list(map(lambda x:float(x),row[topLeft[1]:botRight[1]])) for row in dump[topLeft[0]:botRight[0]]]
        return array(trimed)
    except:
        return None

def CSVLoad(path):
    res=[]
    with open(path,mode='r') as file:
        csv=reader(file)
        for row in csv:
            r=[]
            for cell in row:
                try:
                    r.append(float(cell))
                except:
                    r.append(cell)
            res.append(r)
    return res

def CSVSave(data,path):
    with open(path,mode='w') as file:
        csv=writer(file,lineterminator='\n')
        for row in data:
            csv.writerow(row)