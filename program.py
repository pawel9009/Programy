import pandas as pd
from tkinter import *
import numpy as np
import random
from tkinter import filedialog
from configparser import ConfigParser

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
               text='5 .Zapisz plik',
               command=self.zapisz
               ).grid(row=1, column=2)

        Label(self, text="Przedział oddzielony '-' ").grid(row=1, column=0, sticky=W, padx=1)

        Label(self, text="Kolumna :").grid(row=1, column=0, sticky=E)

        self.norm = Entry(self, width=27)
        self.norm.grid(row=1, column=0)

        self.normCol = Entry(self, width=6)
        self.normCol.grid(row=1, column=1)

        self.to_save = Entry(self)
        self.to_save.grid(row=1, column=2, sticky=E)

        self.wynik = Text(self, width=138, height=20, wrap=CHAR)
        self.wynik.grid(row=2, column=0, columnspan=4, sticky=W)
        Label(self).grid(row=3)
        self.info_file = Text(self, width=55, height=14, wrap=WORD)
        self.info_file.grid(row=4, column=0, sticky=W)

        self.result = Text(self, width=65, height=10, wrap=CHAR)
        self.result.grid(row=4, column=2, sticky=W)

        # czesc 2 --------------------------------------------------------------------------

        Label(self,
              text="Część druga zadania pierwszego( brak wejscia = odczyt z pliku )"
              ).grid(row=5, column=0, sticky=W)
        Label(self,
              text="Struktura oddzielona ( - )"
              ).grid(row=6, column=0, sticky=W)

        Button(self,
               text="Akceptuj",
               command=self.czesc_druga
               ).grid(row=6, column=2, sticky=W)

        self.struktura = Entry(self)
        self.struktura.grid(row=6, column=1, sticky=W)

        self.wynik_czesc2 = Text(self, width=70, height=4, wrap=CHAR)
        self.wynik_czesc2.grid(row=7, column=0, columnspan=5, sticky=W)

    def czesc_druga(self):
        try:
            str = self.struktura.get()
            if str == '':
                plik = open("czesc2.txt", 'r')
                zawartosc = plik.read()
                plik.close()
                self.wynik_czesc2.delete(0.0, END)
                self.wynik_czesc2.insert(0.0, zawartosc)
            else:
                print(str)
                wezly = []
                liczby = list(str.split('-'))
                for znak in liczby:
                    wezly.append(int(znak))
                print(wezly)
                liczba_kr = len(wezly) - 1
                krawedzie = []
                wynik = 0
                for i in range(liczba_kr):
                    kr = wezly[i] * wezly[i + 1] + wezly[i + 1]
                    krawedzie.append(kr)
                    wynik += kr
                print(wynik)
                zapis = []
                for a in range(wynik):
                    zapis.append(random.random())
                sd = [round(elem, 2) for elem in zapis]
                self.wynik_czesc2.delete(0.0, END)
                self.wynik_czesc2.insert(0.0, sd)
                plik = open("czesc2.txt", 'w+')
                plik.writelines(str)
                plik.write(f"\n{sd}")
                plik.close()
        except Exception:
            blad = "Nieprawidłowe wejscie"
            self.wynik_czesc2.delete(0.0, END)
            self.wynik_czesc2.insert(0.0, blad)

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

        opis = ""
        opis += (f"Liczba wierszy : {self.row}\n")
        opis += (f"Liczba kolumn : {self.col_num}\n")
        opis += (f"Separator : '{self.separator}'\n")
        opis += (f"Klasa decyzyjna : '{self.klasa}'\n")
        opis += (f"Pola Liczbowe : '{self.liczbowe}'\n")

        self.info_file.delete(0.0, END)
        self.info_file.insert(0.0, opis)

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
        for a in range(len(listaSymb)):
            x = 0
            for wiersz in self.message[self.symbol[a]]:
                if wiersz not in listaSymb[a]:
                    ilos_bledow += 1
                    self.errors += f"{self.symbol[a]} ma nieprawidlowa wartosc w wierszu {x} - {wiersz} \n"
                x += 1

        for licz in range(len(listaLiczb)):
            x = 0
            for wiersz in self.message[self.liczbowe[licz]]:
                if wiersz:
                    try:
                        float(wiersz) + 1

                        if float(wiersz) > 1000:
                            self.errors += f"{self.liczbowe[licz]} ma nieprawidlowa wartosc w wierszu {x} - {wiersz} \n"
                            ilos_bledow += 1
                    except:
                        ilos_bledow += 1
                        self.errors += f"{self.liczbowe[licz]} ma nieprawidlowa wartosc w wierszu {x} - {wiersz} \n"
                x += 1

        if self.errors == '':
            self.errors = "Jest ok"
        else:
            self.errors += f"ilosc bledow : {ilos_bledow}"
        self.result.delete(0.0, END)
        self.result.insert(0.0, self.errors)

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
        ilos_bledow = 0

        _ = self.message.fillna('?', inplace=True)

        for a in range(len(listaSymb)):
            x = 0
            for wiersz in self.message[self.symbol[a]]:

                if str(wiersz) not in listaSymb[a]:
                    ilos_bledow += 1
                    self.errors += f"{self.symbol[a]} ma nieprawidlowa wartosc w wierszu {x} - {wiersz} \n"
                x += 1

        for licz in range(len(listaLiczb)):
            x = 0
            for wiersz in self.message[self.liczbowe[licz]]:
                if wiersz:
                    try:

                        float(wiersz) + 1

                        if float(wiersz) > 100111110:
                            self.errors += f"{self.liczbowe[licz]} ma nieprawidlowa wartosc w wierszu {x} - {wiersz} \n"
                            ilos_bledow += 1
                    except:
                        ilos_bledow += 1
                        self.errors += f"{self.liczbowe[licz]} ma nieprawidlowa wartosc w wierszu {x} - {wiersz} \n"
                x += 1

        if self.errors == '':
            self.errors = "Jest ok"
        else:
            self.errors += f"ilosc bledow : {ilos_bledow}"
        self.result.delete(0.0, END)
        self.result.insert(0.0, self.errors)

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

        print(self.skip)
        listasymboli = [a2, a3, a4, a5, a6, a7, a8, a9, a10]
        ilos_bledow = 0

        _ = self.message.fillna('?', inplace=True)

        for licz in range(len(listasymboli)):
            x = 0
            for wiersz in self.message[self.symbol[licz]]:
                if wiersz:
                    try:

                        float(wiersz) + 1

                        if float(wiersz) > 1000:
                            self.errors += f"{self.symbol[licz]} ma nieprawidlowa wartosc w wierszu {x} - {wiersz} \n"
                            ilos_bledow += 1
                    except:
                        ilos_bledow += 1
                        self.errors += f"{self.symbol[licz]} ma nieprawidlowa wartosc w wierszu {x} - {wiersz} \n"
                x += 1

        if self.errors == '':
            self.errors = "Jest ok"
        else:
            self.errors += f"ilosc bledow : {ilos_bledow}"
        self.result.delete(0.0, END)
        self.result.insert(0.0, self.errors)

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

    def zapisz(self):

        nazwa = self.to_save.get()
        if self.zaladowany:
            col = self.res
            self.message = self.message.iloc[:, 0:]
            self.message.to_csv(f"{nazwa}.csv", header=False)

        else:
            self.result_mess = "Taka nazwa pliku juz istnieje. Wybierz inna"

        self.result.delete(0.0, END)
        self.result.insert(0.0, self.result_mess)

    def onclick(self):
        self.message = ""
        self.result_mess = ""
        self.nazwa = filedialog.askopenfilename()

        try:
            self.read_config()
            self.result_mess = "Powodzenie"
            if self.nazwa:
                self.message = pd.read_csv(self.nazwa, sep=self.separator, header=None)
                self.zaladowany = True

                self.message.columns = self.res

        except:
            self.result_mess = "Cos poszło nie tak "
            self.zaladowany = False

        self.wynik.delete(0.0, END)
        self.wynik.insert(0.0, self.message)

        self.result.delete(0.0, END)
        self.result.insert(0.0, self.result_mess)

    def normalizuj(self):
        if self.zaladowany:
            if self.ready:
                selected = self.normCol.get()
                print(len(selected))
                if len(selected) < 2:
                    self.message = self.message.astype(float)
                    for kolumna in self.res:
                        if kolumna == self.klasa:
                            continue
                        else:
                            try:
                                self.message[kolumna] = np.float32(self.message[kolumna])
                                self.norm_numbers(kolumna)
                                self.result_mess = "Pomyślne znormalizowano "
                            except:
                                self.result_mess = "bład normalizacji"

                    self.wynik.delete(0.0, END)
                    self.wynik.insert(0.0, self.message)
                else:
                    try:
                        self.message[f'{selected}'] = np.float32(self.message[f'{selected}'])

                        self.norm_numbers(f'{selected}')
                        self.result_mess = "Pomyślne znormalizowano "
                    except:
                        self.result_mess = "bład normalizacji"
                self.wynik.delete(0.0, END)
                self.wynik.insert(0.0, self.message)
            else:
                self.result_mess = "Dane nie sa gotowe do normalizacji"
                self.result.delete(0.0, END)
                self.result.insert(0.0, self.result_mess)
        else:
            self.result_mess = "Wczytaj plik"
            self.result.delete(0.0, END)
            self.result.insert(0.0, self.result_mess)


root = Tk()
root.title("Aplikacja")
root.geometry("1200x900")
app = Aplication(root)
root.mainloop()
