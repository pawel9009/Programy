import pandas as pd
from tkinter import *
from tkinter import ttk
import numpy as np
import random
from collections import OrderedDict
import math
from tkinter import filedialog
from configparser import ConfigParser
import operator
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option("precision", 3)


def Get_name(nazwa):
    roz = str(nazwa)
    czlon = roz[::-1]
    pom = czlon.find('.')
    pom1 = czlon.find('/')
    wynik = czlon[pom + 1:pom1]
    wynik = wynik[::-1]
    return wynik


def Metryka_euklidesowa(row1, row2):
    suma = 0.0
    for i in range(len(row1)):
        suma += (row1[i] - row2[i]) ** 2
    return math.sqrt(suma)

def Metryka_Manhatan(row1, row2):
    suma = 0.0
    for i in range(len(row1)):
        suma += math.fabs(row1[i] - row2[i])
    return suma

def pokaz_k(lista, k): # zwraca k najblizszych sasiadow
    somsiedzi = []
    for x in range(k):
        somsiedzi.append(lista[x+1])
    return somsiedzi

def fun(list, klasa): #liczenie wyniku dokladnosci
    suma = 0
    for x,y in list:
        if int(x[klasa-1]) == y:
            suma+=1

    wynik = suma/len(list)

    wynik*=100
    wynik = wynik.__round__(2)
    return wynik

def ocen(list):

    dl = []
    tab = []
    for e,t in list:
        dl.append(e)
        tab.append(t)
    klasy = []
    lenght = len(tab[0])-1

    for q in range(len(tab)):
        klasy.append(tab[q][lenght])

    odp = []
    for y in klasy:
        if y not in odp:
            odp.append(y)

    ilosc= len(odp)
    dict = {}
    for x in range(ilosc):
        dict[odp[x]] = 0

    for x,y in list:
        if y[lenght] in dict.keys():
            dict[y[lenght]]+=1

    max = 0
    tak =0
    print(dict)
    for key,value in dict.items():
        if value >= max:
            max = value
            tak=key

    return tak

def sasiedzi(probka,train_set,k,metryka):
    odp = []
    lista =[]
    for train in range(len(train_set)):
        lista.append([Metryka_euklidesowa(probka,
                                        train_set[train]
                                            ), train_set[train]])
    s = sorted(lista, key=operator.itemgetter(0))
    s = s[1:]
    k_sasiadow = pokaz_k(s, k)
    odp.append(ocen(k_sasiadow))
    return odp



class Aplication(Frame):
    def __init__(self, master):
        super(Aplication, self).__init__(master)
        self.grid()
        self.create_widgets()
        self.zaladowany = False
        self.plik = None

    def proba(self):
        self.errors = ''

        col = len(self.message.columns)
        wiersz = len(self.message.index)
        if self.row != wiersz:
            self.errors += 'Nieprawidlowa ilosc wierszy\n'
        if self.col_num != col:
            self.errors += 'Nieprawidlowa ilosc kolumn\n'

    def create_widgets(self):
        Button(self,
               text='1. Wczytaj plik',
               command=self.onclick
               ).grid(row=0, column=0)

        Button(self,
               text="2. Walidacja",
               command=self.validuj
               ).grid(row=0, column=1)
        Button(self,
               text='3. Napraw',
               command=self.repair
               ).grid(row=0, column=2)
        Button(self,
               text="4. Znormalizuj",
               command=self.normalizuj
               ).grid(row=1, column=2, sticky=W)
        Button(self,
               text="Zrob cos",
               command=self.knn
               ).grid(row=7, column=0, sticky=W)

        Label(self, text="Przedział oddzielony '-' ").grid(row=1, column=0, sticky=W, padx=1)

        Label(self, text="Kolumna :").grid(row=1, column=0, sticky=E)

        self.norm = Entry(self, width=27)
        self.norm.grid(row=1, column=0)

        self.normCol = Entry(self, width=6)
        self.normCol.grid(row=1, column=1)

        self.wynik = Text(self, width=138, height=20, wrap=CHAR)
        self.wynik.grid(row=2, column=0, columnspan=4, sticky=W)

        self.klasyfikacja = Text(self, width=20, height=1, wrap=CHAR)
        self.klasyfikacja.grid(row=8, column=0, sticky=W)
        Label(self).grid(row=3)

        self.probka = Entry(self, width=6)
        self.probka.grid(row=5, column=0)
        Label(self, text = " Podaj nr probki "). grid(row=5,column=0, sticky=W)

        Label(self, text="   Podaj k : ", width=5).grid(row=6, column=0,sticky=W)
        self.take_k = Entry(self, width=5)
        self.take_k.grid(row=6, column=0)

        self.wariant = ttk.Combobox(self, width=27, textvariable=3)
        self.wariant['values'] = ('wariant 1', 'wariant 2')
        self.wariant.grid(row=4, column=0, sticky=W)
        # czesc 2 --------------------------------------------------------------------------

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

    def knn(self):
        wybor = self.wariant.get()
        if wybor == 'wariant 1':
            self.wariant_1()
        elif wybor == 'wariant 2':
            self.wariant_2()

    def wariant_1(self):
        probka, k = 0,0
        try:
            probka = int(self.probka.get())
        except:
            pass
        try:
            k = int(self.take_k.get())
        except:
            pass
        pr = list(self.message.iloc[probka])
        metryka = ""

        set = self.message.to_numpy()
        result = sasiedzi(pr, set, k, metryka)

        self.klasyfikacja.delete(0.0,END)
        self.klasyfikacja.insert(0.0,result)

    def wariant_2(self):
        probka, k = 0, 0
        try:
            probka = int(self.probka.get())
        except:
            pass
        try:
            k = int(self.take_k.get())
        except:
            pass
        pr = list(self.message.iloc[probka])
        print(pr, k)
        # probka, k = 0, 0
        # try:
        #     probka = int(self.probka.get())
        # except:
        #     pass
        # try:
        #     k = int(self.take_k.get())
        # except:
        #     pass
        # print(list(self.message.iloc[probka]))
        # pr = list(self.message.iloc[probka])
        # metryka = ""
        #
        # set = self.message.to_numpy()
        # result = sasiedzi(pr, set, k, metryka)
        #
        # self.klasyfikacja.delete(0.0, END)
        # self.klasyfikacja.insert(0.0, result)


    # def licz(self):
    #     self.klasa = self.take_class.get()
    #     self.klasa = int(self.klasa)
    #     print(self.klasa)
    #     self.k = int(self.take_k.get())
    #     ok = self.check_k()
    #     if ok:
    #         self.wynik = sasiedzi(self.test, self.train, self.dl, self.k, self.klasa)
    #         self.acc = fun(self.wynik, self.klasa)
    #         print(self.acc)
    #         self.result.delete(0.0, END)
    #         self.result.insert(0.0, self.acc)

    def podziel_rowno(self, n):
        test = []
        dl = len(self.message)
        train = []
        for x in range(0, dl, n):
            test.append(self.message.iloc[x, :])
            for y in range(1, n):
                if (x + y) < dl:
                    train.append(self.message.iloc[x + y])
        return test, train
    #----------------------------------------------------------------------------------------------------

    def read_config(self):
        self.name_file = Get_name(self.nazwa)
        config = ConfigParser()
        if self.name_file == "australian":
            config.read('config-australianval.ini')
        elif self.name_file == "crx":
            config.read('config-crxval.ini')
        elif self.name_file == "breast-cancer-wisconsin":
            config.read('config-bcw.ini')

        self.separator = config.get(self.name_file, 'sep')
        self.separator = self.separator[1]
        self.row = config.getint(self.name_file, 'num_rows')
        self.maxval = config.getint(self.name_file, 'maxval')
        try:
            self.skip = config.get(self.name_file, 'dropcol')
            self.skip = list(self.skip.split(' '))
        except:
            pass
        self.col_num = config.getint(self.name_file, 'col_num')
        self.col = config.get(self.name_file, 'columns')
        self.klasa = config.get(self.name_file, 'class')
        self.symbol = config.get(self.name_file, 'symboliczne')
        self.symbol = list(self.symbol.split(' '))
        self.liczbowe = config.get(self.name_file, 'liczbowe')
        self.liczbowe = list(self.liczbowe.split(' '))
        self.res = list(self.col.split(' '))
        self.d = {}
        try:
            for a in range(1, self.col_num + 1):
                self.d["A{0}".format(a)] = config.get(self.name_file, f'A{a}')
        except Exception:
            print("nie maa")

        self.ready = False

    def validuj(self):
        name_file = Get_name(self.nazwa)
        if name_file == "crx":
            self.validate_crx()
        elif name_file == "australian":
            self.validate_australian()
        elif name_file == "breast-cancer-wisconsin":
            self.validate_bcw()

    def repair(self):
        name_file = Get_name(self.nazwa)
        if name_file == "crx":
            self.repair_crx()
        elif name_file == "australian":
            self.repair_australian()
        elif name_file == "breast-cancer-wisconsin":
            self.repair_bcv()

    def validate_crx(self):
        self.proba()
        a1 = list(self.d['A1'].split(','))
        a2 = list(self.d['A2'].split(','))
        a3 = list(self.d['A3'].split(','))
        a4 = list(self.d['A4'].split(','))
        a5 = list(self.d['A5'].split(','))
        a6 = list(self.d['A6'].split(','))
        a7 = list(self.d['A7'].split(','))
        a8 = list(self.d['A8'].split(','))
        a9 = list(self.d['A9'].split(','))
        a10 = list(self.d['A10'].split(','))
        a11 = list(self.d['A11'].split(','))
        a12 = list(self.d['A12'].split(','))
        a13 = list(self.d['A13'].split(','))
        a14 = list(self.d['A14'].split(','))
        a15 = list(self.d['A15'].split(','))

        listaSymb = [a1, a4, a5, a6, a7, a9, a10, a12, a13]
        listaLiczb = [a2, a3, a8, a11, a14, a15]
        ilos_bledow = 0
        for licz in range(len(listaLiczb)):
            for wiersz in self.message[self.liczbowe[licz]]:
                if wiersz:
                    try:
                        float(wiersz) + 1

                    except:
                        pass

    def validate_australian(self):
        self.proba()

        a1 = list(self.d['A1'].split(','))
        a2 = list(self.d['A2'].split(','))
        a3 = list(self.d['A3'].split(','))
        a4 = list(self.d['A4'].split(','))
        a5 = list(self.d['A5'].split(','))
        a6 = list(self.d['A6'].split(','))
        a7 = list(self.d['A7'].split(','))
        a8 = list(self.d['A8'].split(','))
        a9 = list(self.d['A9'].split(','))
        a10 = list(self.d['A10'].split(','))
        a11 = list(self.d['A11'].split(','))
        a12 = list(self.d['A12'].split(','))
        a13 = list(self.d['A13'].split(','))
        a14 = list(self.d['A14'].split(','))

        listaSymb = [a1, a4, a5, a6, a8, a9, a11, a12]
        listaLiczb = [a2, a3, a7, a10, a13, a14]


        _ = self.message.fillna('?', inplace=True)


        for licz in range(len(listaLiczb)):

            for wiersz in self.message[self.liczbowe[licz]]:
                if wiersz:
                    try:

                        float(wiersz) + 1

                    except:
                        pass

    def validate_bcw(self):
        self.proba()

        a2 = list(self.d['A2'].split(','))
        a3 = list(self.d['A3'].split(','))
        a4 = list(self.d['A4'].split(','))
        a5 = list(self.d['A5'].split(','))
        a6 = list(self.d['A6'].split(','))
        a7 = list(self.d['A7'].split(','))
        a8 = list(self.d['A8'].split(','))
        a9 = list(self.d['A9'].split(','))
        a10 = list(self.d['A10'].split(','))

        listasymboli = [a2, a3, a4, a5, a6, a7, a8, a9, a10]

        _ = self.message.fillna('?', inplace=True)

        for licz in range(len(listasymboli)):
            x = 0
            for wiersz in self.message[self.symbol[licz]]:
                if wiersz:
                    try:

                        float(wiersz) + 1

                        if float(wiersz) > 1000:
                            self.errors += f"{self.symbol[licz]} ma nieprawidlowa wartosc w wierszu {x} - {wiersz} \n"

                    except:
                       pass

                x += 1


    def symbols(self, col):
        unique = []
        lista = []
        top = self.message[col].max()
        _ = self.message[col].replace('?', top, inplace=True)

        for x in self.message[col].values:
            lista.append(x)

        for y in lista:
            if y not in unique:
                unique.append(y)

        slownik = {}
        dl = len(unique)
        for x in range(dl):
            slownik[f"{unique[x]}"] = x

        for key, value in slownik.items():
            _ = self.message[col].replace(key, value, inplace=True)

    def repair_crx(self):
        for column in self.symbol:
            self.symbols(column)

        prog = self.maxval

        for columna in self.liczbowe:
            self.message[columna] = pd.to_numeric(self.message[columna], errors='coerce')

            top = (self.message[columna].mean()).round(2)
            _ = self.message[columna].replace(np.nan, top, inplace=True)

            for x in self.message[columna]:
                if x > prog:
                    _ = self.message[columna].replace(x, prog, inplace=True)

        self.ready = True
        self.wynik.delete(0.0, END)
        self.wynik.insert(0.0, self.message)

    def repair_australian(self):
        prog = self.maxval

        for columna in self.liczbowe:
            self.message[columna] = pd.to_numeric(self.message[columna], errors='coerce')

            top = (self.message[columna].mean()).round(2)
            _ = self.message[columna].replace(np.nan, top, inplace=True)

            for x in self.message[columna]:
                if x > prog:
                    _ = self.message[columna].replace(x, prog, inplace=True)

        self.ready = True
        self.wynik.delete(0.0, END)
        self.wynik.insert(0.0, self.message)

    def repair_bcv(self):

        for column in self.symbol:
            self.symbols(column)

        for x in self.skip:
            self.message.drop(x, inplace=True, axis=1)

        self.ready = True
        self.wynik.delete(0.0, END)
        self.wynik.insert(0.0, self.message)

    def norm_numbers(self, col):
        przedzial = self.norm.get()
        if przedzial == '':
            od = 0
            do = 1
        else:
            przedzial = list(przedzial.split('-'))
            od = float(przedzial[0])
            do = float(przedzial[1])
        min = float(self.message[col].min())
        max = float(self.message[col].max())
        norm = (self.message[col].values - min) / (max - min)
        self.message[col] = (norm * (do - od)) + od


    def onclick(self):
        self.message = ""
        self.nazwa = filedialog.askopenfilename()

        try:
            self.read_config()
            if self.nazwa:
                self.message = pd.read_csv(self.nazwa, sep=self.separator, header=None)
                self.zaladowany = True

                self.message.columns = self.res

        except:
            try:
                self.message = pd.read_csv(self.nazwa, sep=',', header=None)
            except:
                self.zaladowany = False

        self.wynik.delete(0.0, END)
        self.wynik.insert(0.0, self.message)


    def normalizuj(self):
        if self.zaladowany:
            if self.ready:
                selected = self.normCol.get()

                if len(selected) < 2:
                    self.message = self.message.astype(float)
                    for kolumna in self.res:
                        if kolumna == self.klasa:
                            continue
                        else:
                            try:
                                self.message[kolumna] = np.float32(self.message[kolumna])
                                self.norm_numbers(kolumna)
                            except:
                                pass

                    self.wynik.delete(0.0, END)
                    self.wynik.insert(0.0, self.message)
                else:
                    try:
                        self.message[f'{selected}'] = np.float32(self.message[f'{selected}'])
                        self.norm_numbers(f'{selected}')
                    except:
                        self.result_mess = "bład normalizacji"
                self.wynik.delete(0.0, END)
                self.wynik.insert(0.0, self.message)
            else:
                pass

        else:
            pass



root = Tk()
root.title("Aplikacja")
root.geometry("1200x550")
app = Aplication(root)
root.mainloop()

