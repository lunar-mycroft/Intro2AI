from requests import get as webget
from json import loads as loadJJSON
from random import shuffle
from math import atan,pi

from neuralNet import NeuralNet, errorFunc



#Functions to help retrieve and process training data
def importStats(url):
    opgg=webget(url)

    start=opgg.text.find("matchupData.stats")
    end=opgg.text.find('\n',start)-1
    string=opgg.text[start+20:end]
    stats=loadJJSON(string)
    res=dict()
    for champ in stats:
        res[(champ["key"],champ["role"])]=champ["general"]
    return res

def inputData(champData,sums):
    return [champData[key]/sums[key] for key in sums]

def kda(champData):
    res=[champData["kills"],champData["assists"],champData["deaths"]]
    s=sum(res)
    return [n/s for n in res]

def sums(stats,keys):
    res={key:0 for key in keys}
    for champRole in stats:
        champData=stats[champRole]
        for key in keys:
            res[key]+=champData[key]
    return res

statsToInclude = ["totalDamageTaken", "totalDamageDealtToChampions", "playPercent", "banRate"]
stats=importStats("https://champion.gg/statistics/")

champsAndRoles = [(champ,role) for champ,role in stats]
shuffle(champsAndRoles)

trainingChamps = champsAndRoles[:100]
nonTrainingChamps = champsAndRoles[100:]

s=sums(stats,statsToInclude)
for key in s:
    s[key]/=len(stats)

trainingData = [(inputData(stats[champ],s),kda(stats[champ])) for champ in trainingChamps]
testData= [(inputData(stats[champ],s),kda(stats[champ])) for champ in nonTrainingChamps]

activationFunc=lambda x:atan(x)*(2/pi)
dSigma=lambda x:(2/pi)/(x**2+1)

#setting up the neural net

net=NeuralNet(4)
net.addLayer(6,activationFunc,dSigma)
net.addLayer(3,activationFunc,dSigma)

orgEr=net.totalError(testData,errorFunc)
net.train(trainingData,0.1,1000)

finalError=net.totalError(testData,errorFunc)
print("Initial error:", orgEr)
print("Error after training:", finalError)


for champRole in nonTrainingChamps:
    print(str(champRole)[1:-1])
    champData=stats[champRole]
    actual = tuple([round(num,3) for num in kda(champData)])
    predicted=tuple([round(num,3) for num in net(inputData(champData,s))])
    print("predicted K/D/A:", predicted)
    print("actual K/D/A:", actual)