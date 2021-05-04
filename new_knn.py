import pandas as pd
from tkinter import *
from tkinter import ttk
import numpy as np
import math
from tkinter import filedialog
from configparser import ConfigParser
import operator
from statistics import mode

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


def Metryka_Euklidesowa(row1, row2):
    suma = 0.0
    for i in range(len(row1)):
        suma += (row1[i] - row2[i]) ** 2
    return math.sqrt(suma)


def Metryka_Manhatan(row1, row2):
    suma = 0.0
    for i in range(len(row1)):
        suma += math.fabs(row1[i] - row2[i])
    return suma


def Metryka_Czebyszewa(row1, row2):
    max = 0
    for i in range(len(row1)):
        if math.fabs(row1[i] - row2[i]) > max:
            max = math.fabs(row1[i] - row2[i])
    return max


# def Metryka_Logarytmiczna(row1, row2):
#     suma = 0.0
#     for i in range(len(row1)):
#         x = math.log(row2[i])
#         y=math.log(row1[i])
#         suma += math.fabs(y-x)
#     return suma

def Metryka_Minkowskiego(row1, row2):
    p = 1
    suma = 0.0
    for i in range(len(row1)):
        suma += math.pow(math.fabs(row1[i] - row2[i]), p)
    return math.pow(suma, 1 / p)


def pokaz_k(lista, k):  # zwraca k najblizszych sasiadow
    somsiedzi = []
    for x in range(k):
        somsiedzi.append(lista[x + 1])
    return somsiedzi

def ocen(list):
    dl = []
    tab = []
    for e, t in list:
        dl.append(e)
        tab.append(t)
    klasy = []
    lenght = len(tab[0]) - 1

    for q in range(len(tab)):
        klasy.append(tab[q][lenght]) #WYCIAGANIE KLAS Z PROBEK

    odp = []
    for y in klasy:
        if y not in odp:
            odp.append(y)

    ilosc = len(odp)
    dict = {}
    for x in range(ilosc):
        dict[odp[x]] = 0   #dla klas dlugosci

    for x, y in list:
        if y[lenght] in dict.keys():
            dict[y[lenght]] += 1   #dodawanie w zaleznosci od klasy
    max = 0
    result = 0
    for key, value in dict.items():
        if value >= max:    #szukanie maxa
            max = value
            result = key

    powtorzenia = 0
    print(dict)

    for x in dict.values():     #czy max sie powtarza
        if x==max:
            powtorzenia+=1

    if powtorzenia>1:
        print("powtorzenaia ", powtorzenia)
        return "blad"
    return result




def funkcja_wariant_1(probka, train_set, k, metryka):
    # if k % 2==0 or k<0 or k>len(train_set):
    #     return "bledne k"
    odp = []
    fun = metryka
    print(metryka)
    lista = []
    for train in range(len(train_set)):
        lista.append([eval(fun)(probka, train_set[train]), train_set[train]])
    s = sorted(lista, key=operator.itemgetter(0))
    s = s[1:]
    k_sasiadow = pokaz_k(s, k)
    odp.append(ocen(k_sasiadow))
    return odp


def funkcja_wariant_2(probka, train_set, k, metryka):
    klasy = []
    print(metryka)
    lenght = len(train_set[0]) - 1
    for q in range(len(train_set)):
        klasy.append(train_set[q][lenght])
    uniq = []
    for y in klasy:
        if y not in uniq:
            uniq.append(y)
    klassy = []
    for x in range(len(uniq)):
        klassy.append([])

    index = 0
    for num in uniq:
        for row in train_set:
            if row[-1] == num:
                klassy[index].append(row)  # lista n klas podzielona na n list
        index += 1
    k_min = []
    for x in klassy:
        k_min.append(len(x))

    k_min.sort()
    k_m = k_min[0]  # najmniejsze k w zaleznosci od liczebnosci klasy
    if k > k_m:
        return "blad"
    else:
        fun = metryka
        decyzja = []
        for nr_decyzi in range(len(uniq)):
            lista =[]
            for train in range(len(klassy[nr_decyzi])):
                lista.append([eval(fun)(probka, klassy[nr_decyzi][train]), klassy[nr_decyzi][train]])
            s = sorted(lista, key=operator.itemgetter(0))
            s = s[1:]
            k_sasiadow = pokaz_k(s, k)
            for x,y in k_sasiadow:
                decyzja.append([x,uniq[nr_decyzi]])

        dict = {}
        for x in range(len(uniq)):
            dict[uniq[x]] = 0

        for x,y in decyzja:
            dict[y]+=x

        result = min(dict, key=dict.get)
        min_value = min(dict.values())
        powtorzenia = 0
        for x in dict.values():
            if x==min_value:
                powtorzenia+=1
        print("ilosc minim - ", powtorzenia)
        print(dict)
        if powtorzenia>1:
            print(dict)
            return "blad"
        return result


class Aplication(Frame):
    def __init__(self, master):
        super(Aplication, self).__init__(master)
        self.grid()
        self.create_widgets()
        self.zaladowany = False
        self.new =True
        self.czy_decydowac = False

    def proba(self):
        self.errors = ''

        col = len(self.message.columns)
        wiersz = len(self.message.index)
        if self.row != wiersz:
            self.errors += 'Nieprawidlowa ilosc wierszy\n'
        if self.col_num != col:
            self.errors += 'Nieprawidlowa ilosc kolumn\n'

    def create_widgets(self):
        self.choice = StringVar(value="Wariant 1")
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
               text="Probka",
               command=self.knn
               ).grid(row=8, column=0, sticky=W)
        Button(self,
               text="Statystyka",
               command=self.statystyka
               ).grid(row=11, column=0)
        Button(self,
               text="Dodaj klienta",
               command=self.n_klient
               ).grid(row=14, column=1)
        Button(self,
               text="Decyzja",
               command=self.decyzja
               ).grid(row=15, column=1)

        Radiobutton(self, text="Wariant 1", variable=self.choice, value="Wariant 1").grid(row=3, column=0, sticky=W)
        Radiobutton(self, text="Wariant 2", variable=self.choice, value="Wariant 2").grid(row=3, column=0, sticky=E)

        Label(self, text="Przedział oddzielony '-' ").grid(row=1, column=0, sticky=W, padx=1)

        Label(self, text="Kolumna :").grid(row=1, column=0, sticky=E)

        self.norm = Entry(self, width=27)
        self.norm.grid(row=1, column=0)

        self.normCol = Entry(self, width=6)
        self.normCol.grid(row=1, column=1)

        self.wynik = Text(self, width=138, height=15, wrap=CHAR)
        self.wynik.grid(row=2, column=0, columnspan=4, sticky=W)

        Label(self, text="      Wariant 1 ").grid(row=9, column=0, sticky=W)
        self.klasyfikacja1 = Text(self, width=20, height=1, wrap=CHAR)
        self.klasyfikacja1.grid(row=9, column=0)

        Label(self, text="      Wariant 2 ").grid(row=10, column=0, sticky=W)
        self.klasyfikacja2 = Text(self, width=20, height=1, wrap=CHAR)
        self.klasyfikacja2.grid(row=10, column=0)
        Label(self).grid(row=3)

        self.probka = Entry(self, width=6)
        self.probka.grid(row=6, column=0)
        Label(self, text="Podaj nr probki ").grid(row=6, column=0, sticky=W)

        Label(self, text="   Podaj k : ", width=5).grid(row=7, column=0, sticky=W)
        self.take_k = Entry(self, width=5)
        self.take_k.grid(row=7, column=0)

        self.metryka = ttk.Combobox(self, width=27, textvariable=3)
        self.metryka['values'] = ('Metryka_Euklidesowa', 'Metryka_Manhatan', 'Metryka_Czebyszewa',
                                  'Metryka_Minkowskiego')
        self.metryka.grid(row=4, column=0)

        Label(self, text="Pokrycie ").grid(row=12, column=0, sticky=W)
        self.pokrycie = Text(self, width=20, height=1, wrap=CHAR)
        self.pokrycie.grid(row=12, column=0)

        Label(self, text="Skuteczność ").grid(row=13, column=0, sticky=W)
        self.skutecznosc = Text(self, width=20, height=1, wrap=CHAR)
        self.skutecznosc.grid(row=13, column=0)
        #-----------------------------------------------------------------
        Label(self, text="Dane ").grid(row=14, column=0, sticky=W)
        self.klient = Entry(self, width=87)
        self.klient.grid(row=14, column=0)

        Label(self, text="Norm.").grid(row=15, column=0, sticky=W)
        self.klient_znormalizowane = Text(self, width=65, height=1)
        self.klient_znormalizowane.grid(row=15, column=0)

        Label(self, text="Decyzja").grid(row=16, column=0, sticky=W)
        self.klient_decyzja = Text(self, width=65, height=1)
        self.klient_decyzja.grid(row=16, column=0)

    def knn(self):
        wybor = self.choice.get()
        if wybor == 'Wariant 1':
            self.wariant_1()
        elif wybor == 'Wariant 2':
            self.wariant_2()

    def n_klient(self):
        if self.new == True:
            klient = self.klient.get()
            dlugosc = self.col_num
            # klient = '1 22.08 11.46 2 4 4 1.585 0 0 0 1 2 100 1213'

            # klient = 'a 12.63 2.64 y p aa v 0.32 t t 1 f g 0214 441'

            # klient = '1018561 2 1 2 1 2 1 3 1 1'


            klient= list(klient.split(' '))

            print(klient)
            if len(klient)==dlugosc-1:
                dec = self.message.iloc[0,-1]
                klient.append(dec)
                new = len(self.message.index)
                self.message.loc[new] = klient

                self.nor = list(self.message.iloc[new])

                self.klient_znormalizowane.delete(0.0,END)
                self.klient_znormalizowane.insert(0.0,self.nor)
                self.new = False
                self.czy_decydowac=True
            else:
                self.klient_znormalizowane.delete(0.0, END)
                self.klient_znormalizowane.insert(0.0, "błąd z danymi")


    def decyzja(self):
        if self.czy_decydowac and self.ready:
            k = 0
            metryka = self.metryka.get()
            try:
                k = int(self.take_k.get())
            except:
                pass
            wybor = self.choice.get()
            probka = self.message.iloc[-1]
            probka = probka.to_numpy()
            set = self.message.to_numpy()
            data_set=set[:-1,:]
            print(data_set)

            if wybor == 'Wariant 1':
                wyn = funkcja_wariant_1(probka,data_set,k,metryka)
                self.klient_decyzja.delete(0.0, END)
                self.klient_decyzja.insert(0.0, wyn)
            elif wybor == 'Wariant 2':
                wyn = funkcja_wariant_2(probka, data_set, k, metryka)
                self.klient_decyzja.delete(0.0, END)
                self.klient_decyzja.insert(0.0, wyn)


    def statystyka(self):
        wybor = self.choice.get()
        k = int(self.take_k.get())
        metryka = self.metryka.get()
        if wybor == 'Wariant 1':
            set = self.message.to_numpy()
            suma = 0
            poprawnosc =0
            for x in set:
                wynik = funkcja_wariant_1(x, set, k, metryka)
                print(wynik, "- wynik ")
                if wynik[0] == "blad":
                    # print("tu jest blad ")
                    suma+=1
                else:
                    print(wynik, " ---- ", x[-1])
                    if wynik[0] == x[-1]:
                        # print("Poprawnie ")
                        poprawnosc+=1
                    else:
                        print("tu sie nie zdaddza", wynik, x[-1])

            print(f'caly set {len(set)} bledy {suma} lacznie poprawnych {len(set)-suma} ')
            cower = (len(set)-suma)
            skutecznosc = (poprawnosc/cower)*100
            skutecznosc = skutecznosc.__round__(2)
            print(cower,"ilosc poprawnych")
            print(poprawnosc, "ilosc prawidlowych wynikow")
            pokrycie = (len(set)-suma)/len(set)*100
            pokrycie = pokrycie.__round__(2)
            self.pokrycie.delete(0.0, END)
            self.pokrycie.insert(0.0, pokrycie)
            self.skutecznosc.delete(0.0, END)
            self.skutecznosc.insert(0.0, skutecznosc)

        elif wybor == 'Wariant 2':
            set = self.message.to_numpy()
            suma = 0
            poprawnosc = 0
            for x in set:
                wynik = funkcja_wariant_2(x, set, k, metryka)
                print(wynik)
                if wynik == "blad":
                    print("tu jest blad ", wynik)
                    suma += 1
                else:
                    print(wynik, " ---- ", x[-1])
                    if wynik== x[-1]:
                        # print("Poprawnie ")
                        poprawnosc += 1
                    else:
                        print("tu sie nie zdaddza", wynik, x[-1])

            print(f'caly set {len(set)} bledy {suma} lacznie poprawnych {len(set) - suma} ')
            cower2 = (len(set) - suma)
            skutecznosc2 = (poprawnosc / cower2) * 100
            skutecznosc2 = skutecznosc2.__round__(2)
            print(cower2, "ilosc poprawnych")
            print(poprawnosc, "ilosc prawidlowych wynikow")
            pokrycie2 = (len(set) - suma) / len(set) * 100
            pokrycie2 = pokrycie2.__round__(2)
            self.pokrycie.delete(0.0, END)
            self.pokrycie.insert(0.0, pokrycie2)
            self.skutecznosc.delete(0.0, END)
            self.skutecznosc.insert(0.0, skutecznosc2)

    def wariant_1(self):
        probka, k = 0, 0
        metryka = self.metryka.get()
        try:
            probka = int(self.probka.get())
        except:
            pass
        try:
            k = int(self.take_k.get())
        except:
            pass
        pr = list(self.message.iloc[probka])

        set = self.message.to_numpy()
        result = funkcja_wariant_1(pr, set, k, metryka)

        self.klasyfikacja1.delete(0.0, END)
        self.klasyfikacja1.insert(0.0, result)

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
        metryka = self.metryka.get()
        set = self.message.to_numpy()
        pr = list(self.message.iloc[probka])

        wynik = funkcja_wariant_2(pr, set, k, metryka)

        self.klasyfikacja2.delete(0.0, END)
        self.klasyfikacja2.insert(0.0, wynik)

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

    # ----------------------------------------------------------------------------------------------------

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

        self.dict_NA = {}
        try:
            for a in range(1, self.col_num + 1):
                if self.name_file=="breast-cancer-wisconsin" and a==1:
                    continue
                self.dict_NA["NA{0}".format(a)] = config.get(self.name_file, f'NA{a}')
        except Exception:
            print("nie maa")
        print(self.dict_NA)
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
        top = self.message[col].mode()
        x=top[0]
        _ = self.message[col].replace('?', x, inplace=True)

        for x in self.message[col].values:
            lista.append(x)

        for y in lista:
            if y not in unique:
                unique.append(y)

        slownik = {}
        dl = len(unique)
        for x in range(dl):
            slownik[f"{unique[x]}"] = float(x)

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
                if self.new == False:
                    self.klient_znormalizowane.delete(0.0, END)
                    klient = list(self.message.iloc[-1])
                    klient= [round(elem, 2) for elem in klient]
                    self.klient_znormalizowane.insert(0.0, klient)

            else:
                pass

        else:
            pass


root = Tk()
root.title("Aplikacja")
root.geometry("1200x650")
app = Aplication(root)
root.mainloop()
