from numpy import array
import sys

from hmm import HiddenMarkovModel
from MatrixGen import randomHMMMatrix,randRow
from fileIOUtils import loadHMM,saveHMM
from utility import getOpts


def getESequence(maxEmission):
    while True:
        try:
            res=tuple(map(lambda n:int(n),input("What emission sequence did you observe? ").split(',')))
            for num in res:
                if num<0 or num>maxEmission:
                    continue
            return res
        except:
            print("You entered an invalid sequence")
            continue

opts=getOpts(sys.argv)

if not ('-file' in opts or ('-n_e' in opts and '-n_s' in opts)):
    print("You must enter either a file or a size")
    exit()

noFile = '-file' in opts
if noFile:
    noFile=len(opts['-file'])<=0
if '-n_e' in opts: # and '-n_s' in opts (second check unneeded
    if len(opts['-n_e'])<=0 or len(opts['-n_s'])<=0:
        print("You must enter either a file or a size")
        exit()

model=None
if '-n_e' in opts:
    print("gen")
    n_e=0
    n_s=0
    try:
        n_e=int(opts['-n_e'][0])
        n_s=int(opts['-n_s'][0])
    except:
        print("Invalid size")
        exit()
    T=randomHMMMatrix((n_s,n_s),2)
    E=randomHMMMatrix((n_e,n_s),2)
    I=randRow(n_e,3)
    model=HiddenMarkovModel(T,E,I)

    if not noFile:
        saveHMM(opts['-file'][0],model)
else:
    model=loadHMM(opts['-file'][0])

seqence=getESequence(len(model._T_))

mostProb=model.mostProbPath(seqence)
print("The most probable sequence is "+str(mostProb[0]))
print("The probability of that sequence explaining your observation is "+str(round(mostProb[1],5)))






