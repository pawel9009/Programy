import pandas as pd
import math
import numpy as np
import random
import operator
np.set_printoptions(precision=2)
from tkinter import *
from tkinter import ttk
import math
import numpy as np
import random
from tkinter import filedialog
from configparser import ConfigParser

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option("precision", 3)


def Metryka_euklidesowa(row1, row2, dl):
    suma = 0.0
    for i in range(dl):
        suma += (row1[i] - row2[i]) ** 2
    return math.sqrt(suma)

def Metryka_Manhatan(row1, row2, dl):
    suma = 0.0
    for i in range(dl):
        suma += math.fabs(row1[i] - row2[i])
    return suma

def Metryka_Log(row1, row2, dl):
    suma = 0.0
    for i in range(dl):
        suma += math.fabs(math.log(row1[i]) - math.log(row2[i]))
    return suma

def sasiedzi(test_set,train_set,dl,k, klasa):
    odp = []
    for test in range(len(test_set)):
        lista = []
        for train in range(len(train_set)):
            lista.append([Metryka_euklidesowa(test_set[test],
                                            train_set[train],
                                                15), train_set[train]])
        s = sorted(lista, key=operator.itemgetter(0))
        k_sasiadow = pokaz_k(s, k)
        odp.append([test_set[test], ocen(k_sasiadow, klasa)])

    return odp



def Get_name(nazwa):
    roz = str(nazwa)
    czlon = roz[::-1]
    pom = czlon.find('.')
    pom1 = czlon.find('/')
    wynik = czlon[pom + 1:pom1]
    wynik = wynik[::-1]
    return wynik

def pokaz_k(lista, k):
    somsiedzi = []
    for x in range(k):
        somsiedzi.append(lista[x+1])
    return somsiedzi

def fun(list):
    suma = 0
    for x,y in list:
        if int(x[15]) == y:
            suma+=1

    wynik = suma/len(list)

    wynik*=100
    wynik = wynik.__round__(2)
    return wynik

class Aplication(Frame):
    def __init__(self, master):
        super(Aplication, self).__init__(master)
        self.grid()
        self.create_widgets()
        self.zaladowany = False
        self.plik = None

    def create_widgets(self):
        Button(self,
               text='1. Wczytaj plik',
               command= self.onclick
               ).grid(row=0, column=0)
        Button(self,
               text='Oblicz',
               command=self.licz
               ).grid(row=6, column=1,sticky=W)

        self.result = Text(self,width=10,height=1)
        self.result.grid(row=7,column=1,sticky=W)

        self.probka = Text(self, width=120, height=5)
        self.probka.grid(row=0, column=1)

        self.info = Text(self, width=30, height=3)
        self.info.grid(row=8, column=1, sticky=W)

        Label(self,text="   Podaj k : ",width=5).grid(row=4,column=0)
        self.take_k = Entry(self, width=5)
        self.take_k.grid(row=4, column=1,sticky=W)

        Label(self, text="Klasa:", width=5).grid(row=5, column=0)
        self.take_class = Entry(self, width=5)
        self.take_class.grid(row=5, column=1,sticky=W)


    def onclick(self):
        self.message = ""
        self.result_mess = ""
        self.nazwa = filedialog.askopenfilename()

        self.message = pd.read_csv(self.nazwa, sep=',', header=None,index_col=0,)

        self.liczba_kolumn = self.message.columns[-1]

        self.probka.delete(0.0, END)
        self.probka.insert(0.0, self.message)

        self.set = np.array(self.message)
        print(self.liczba_kolumn)
        ile_czesci = 5
        self.dl = len(self.set)
        self.test_set, self.train_set = self.podziel_rowno(ile_czesci)
        self.test_set = pd.DataFrame(self.test_set)
        self.test = self.test_set.to_numpy()
        self.train_set = pd.DataFrame(self.train_set)
        self.train = self.test_set.to_numpy()


    def check_k(self):
        poprawne_k=True
        odp=''
        if self.k % 2 ==0:
            odp+="k nie moze być parzyste\n"
            poprawne_k=False
        elif self.k <1:
            odp+="k musi być dodatnie"
            poprawne_k = False

        self.result.delete(0.0, END)
        self.info.delete(0.0, END)
        self.info.insert(0.0, odp)

        return poprawne_k




    def licz(self):
        self.klasa = self.take_class.get()
        self.klasa = int(self.klasa)
        print(self.klasa)
        self.k = int(self.take_k.get())
        ok = self.check_k()
        if ok:
            self.wynik = sasiedzi(self.test, self.train, self.dl, self.k, self.klasa)
            self.acc = fun(self.wynik)
            print(self.acc)
            self.result.delete(0.0,END)
            self.result.insert(0.0, self.acc)

    def podziel_rowno(self, n):
        test = []
        dl = len(self.message)
        train = []
        for x in range(0, dl, n):
            test.append(self.message.iloc[x,:])
            for y in range(1, n):
                if (x + y) < dl:
                    train.append(self.message.iloc[x+y])
        return test, train

    # def sasiedzi(self):
    #     odp = []
    #     print(self.test_set)
    #     for test in range(len(self.test_set)):
    #         print("siema")
    #         lista = []
    #         for train in range(len(self.train_set)):
    #             print(self.test_set[test])
    #             lista.append([Metryka_euklidesowa(self.test_set[test],
    #                                               self.train_set[train],
    #                                               self.liczba_kolumn), self.train_set[train]])
    #         s = sorted(lista, key=operator.itemgetter(0))
    #         k_sasiadow = pokaz_k(s, self.k)
    #         odp.append([self.test_set[test], ocen(k_sasiadow, self.k)])
    #         print(odp)


    # def ocen(self, k):
    #     jedynki = 0
    #     zera = 0
    #     for x, y in list:
    #         if y[15] == 1:
    #             jedynki += 1
    #         elif y[15] == 0:
    #             zera += 1
    #     max = None
    #     if jedynki > zera:
    #         max = 1
    #     else:
    #         max = 0
    #     return max




# def podziel_losowo(listaa,n):
#     test = []
#     train = []
#     lista=list(listaa)
#
#     dl = len(lista)
#     pom = np.arange(dl)
#     pom=list(pom)
#     random.shuffle(pom)
#     for x in range(0,dl,n):
#         test.append(listaa[pom[x]])
#         for y in range(1, n):
#             if (x + y) < dl:
#                 train.append(listaa[pom[x+y]])
#
#     return test,train


def ocen(list, klasa):
    jedynki= 0
    zera =0
    for x,y in list:
        if y[klasa-1]==1:
            jedynki+=1
        elif y[klasa-1]==0:
            zera+=1
    max = None
    if jedynki>zera:
        max =1
    else:
        max=0
    return max



# test_set, train_set = podziel_losowo(set,ile_czesci)
#
# k=9
# odp = []
# for test in range(len(test_set)):
#
#     lista = []
#     for train in range(len(train_set)):
#         lista.append([Metryka_euklidesowa(test_set[test],
#                                           train_set[train],
#                                           liczba_kolumn-1),train_set[train]])
#     s = sorted(lista, key=operator.itemgetter(0))
#     k_sasiadow = pokaz_k(s, k)
#     odp.append([test_set[test],ocen(k_sasiadow,k)])
#
#
# suma = 0
# for x,y in odp:
#     #print(int(x[15]),y)
#     if int(x[15]) == y:
#         suma+=1
#
# wynik = suma/len(odp)
#
# wynik*=100
# wynik = wynik.__round__(2)
#
# print(f"Dokładnosc to {wynik}%")


root = Tk()
root.title("knn")
root.geometry("1000x300")
app = Aplication(root)
root.mainloop()
