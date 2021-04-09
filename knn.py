import pandas as pd
import math
import numpy as np
import operator

data = pd.read_csv('kkn.csv', index_col=0, header=None)

liczba_kolumn = data.columns[-1]
def pokaz_k(list,k):
    somsiedzi=[]
    for x in range(k):
        somsiedzi.append(list[x+1])
    return somsiedzi

def podziel(list,n):
    test = []
    dl = len(list)
    train = []
    for x in range(0, dl, n):
        train.append(list[x])
        for y in range(1, n):
            if (x + y) < dl:
                test.append(list[x + y])
    return train, test

def ocen(list,k):
    jedynki= 0
    zera =0
    for x,y in list:
        if y[15]==1:
            jedynki+=1
        elif y[15]==0:
            zera+=1
    max = None
    if jedynki>zera:
        max =1
    else:
        max=0

    return max



def Metryka_euklidesowa(row1, row2,dl):
    suma =0.0
    for i in range(dl):
        suma+=(row1[i] - row2[i]) ** 2
    return math.sqrt(suma)

set = np.array(data)
ile_czesci = 5

dl = len(set)

probka =set[0]
test_set, train_set = podziel(set,ile_czesci)

print(len(test_set))
k=7
odp = []
for test in range(len(test_set)):

    lista = []
    for train in range(len(train_set)):
        lista.append([Metryka_euklidesowa(test_set[test],
                                          train_set[train],
                                          liczba_kolumn-1),train_set[train]])
    s = sorted(lista, key=operator.itemgetter(0))
    k_sasiadow = pokaz_k(s, k)
    odp.append([test_set[test],ocen(k_sasiadow,k)])


suma = 0
for x,y in odp:
    #print(int(x[15]),y)
    if int(x[15]) == y:
        suma+=1

wynik = suma/len(odp)
wynik = wynik.__round__(4)
wynik*=100

print(f"Dokładnosc to {wynik}%")


#for x,y in k_sasiadow:
#    print(x, y[15])

#Metryka_euklidesowa(set1,set[x-1,x],14))