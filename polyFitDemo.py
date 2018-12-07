import sys
from os.path import isfile

from polyFit import polyFit
from utility import getOpts
from fileIOUtils import loadDimentionalPoints

opts=getOpts(sys.argv)

if "-file" not in opts or len(opts["-file"])==0:
    print("You need to give me some data")
    exit()
if not isfile(opts["-file"][0]):
    print("Your file doesn't exist")

degree=int(opts["-d"][0] if "-d" in opts else 1)

data=loadDimentionalPoints(opts["-file"][0])
if len(data[0])!=2:
    print("Your data isn't 2d!")
    exit()

error,res=polyFit(data,degree)

if error is not None:
    print("Too few data points for that degree polynomial")
    exit()

print("The fit is f(x)="+str(res))
if "-x" in opts:
    print("f("+opts["-x"][0]+")="+str(round(res(float(opts["-x"][0])),3)))