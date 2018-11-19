from polyFit import polyFit,polynomial

data= [(1, 3),(2, 7), (3, 5), (4, 9), (5, 11), (6, 12), (7, 15)]
error,fit=polyFit(data,1)
print(fit)
print(fit(7))