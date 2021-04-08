import pandas as pd
from tkinter import *
import numpy as np
import random
import ast
import json
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

    def create_widgets(self):
        Button(self,
               text='Wczytaj plik',
               command=self.onclick
               ).grid(row=0, column=0, sticky=W)
        Button(self,
               text="Znormalizuj",
               command=self.normalizuj
               ).grid(row=1, column=1, sticky=W)

        Button(self,
               text='Zapisz plik',
               command=self.zapisz
               ).grid(row=1, column=3, sticky=W)

        self.to_norm = Entry(self)
        self.to_norm.grid(row=1, column=0, sticky=W)

        self.to_save = Entry(self)
        self.to_save.grid(row=1, column=4, sticky=W)

        self.wynik = Text(self, width=125, height=20, wrap=CHAR)
        self.wynik.grid(row=2, column=0, columnspan=5,sticky=W)
        Label(self).grid(row =3)
        self.info_file = Text(self, width=60, height=14, wrap=CHAR)
        self.info_file.grid(row=4, column=0, columnspan=2, sticky=W)

        self.result = Text(self, width=55, height=10, wrap=CHAR)
        self.result.grid(row=4, column=4, columnspan=2,sticky=W)



    def wczytaj(self):
        name_file=Get_name(self.nazwa)
        config =ConfigParser()
        if name_file == "australian":
            config.read('config-australian.ini')
        elif name_file == "crx":
            config.read('config-crx.ini')
        elif name_file == "breast-cancer-wisconsin":
            config.read('config-bcw.ini')
        self.do_zapisu_nazwa = self.to_save.get()
        self.row = config.getint(name_file, 'num_rows')
        self.col_num = config.getint(name_file, 'col_num')
        self.col = config.get(name_file, 'columns')
        self.klasa = config.get(name_file,'class')
        self.znormalizowane = config.get(name_file, 'normalizowane')
        self.znormalizowane = list(self.znormalizowane.split(' '))
        self.przedial = config.get(name_file, 'przedzial')
        self.przedzial = list(self.przedial.split('-'))
        self.separator = config.get(name_file, 'sep')
        self.liczbowe = config.get(name_file, 'liczbowe')
        self.liczbowelist = list(self.liczbowe.split(' '))
        self.separator = self.separator[1]
        self.d = {}
        for x in self.przedzial:
            print(x)
        try:
            for a in range(1, self.col_num + 1):
                self.d["A{0}".format(a)] = config.get(name_file, f'A{a}')
        except Exception:
            print("nie maa")

        self.res = list(self.col.split(' '))
        opis = ""
        opis += (f"Liczba wierszy : {self.row}\n")
        opis += (f"Liczba kolumn : {self.col_num}\n")
        opis += (f"Separator : '{self.separator}'\n")
        opis += (f"Pola Liczbowe : '{self.liczbowe}'\n")
        opis += (f"Przedział normalizowania : '{self.przedial}'\n")
        opis += (f"Klasa decyzyjna : '{self.klasa}'\n")

        self.info_file.delete(0.0, END)
        self.info_file.insert(0.0, opis)

    def norm_numbers(self,col):

            od = float(self.przedzial[0])
            do = float(self.przedzial[1])

            min = float(self.message[col].min())
            max = float(self.message[col].max())
            norm= (self.message[col].values - min) / (max - min)

            self.message[col] = (norm * (do - od)) + od

    def zapisz(self):

        nazwa = self.to_save.get()
        if self.zaladowany:
            col = self.res
            self.message=self.message.iloc[:,1:]
            self.message.to_csv(f"{nazwa}.csv", header=False )

        else:
            self.result_mess = "Taka nazwa pliku juz istnieje. Wybierz inna"

        self.result.delete(0.0, END)
        self.result.insert(0.0, self.result_mess)

    def sprawdz(self, col):


            if self.zaladowany:
                try:

                    _ = pd.DataFrame(self.message)
                    self.message[col].replace('?', '0', inplace=True)
                    self.message[col].replace(np.nan, '0', inplace=True)

                    self.praw = ast.literal_eval(self.d[col])

                    _ = _[col].replace(self.praw, inplace=True)

                    self.result_mess = "halo :)"
                except:
                    self.result_mess = "Tduadsda"
            else:
                self.result_mess = "Najpierw załaduj plik"

    def check_wczytaj(self):
        ilosc_wierszy=self.message.index.shape[0]
        ilosc_kolumn=self.message.columns.shape[0]
        self.result_mess=""
        if ilosc_wierszy!=self.row:
            self.zaladowany=False
            self.result_mess="błędna ilosc wierszy\n"
        if ilosc_kolumn!=self.col_num:
            self.zaladowany=False
            self.result_mess+="błędna ilosc kolumn "


        self.result.delete(0.0, END)
        self.result.insert(0.0, self.result_mess)



    def onclick(self):
        self.message = ""
        self.result_mess = ""
        self.nazwa = filedialog.askopenfilename()


        try:
            self.wczytaj()
            self.result_mess="Powodzenie"
            if self.nazwa:
                self.message = pd.read_csv(self.nazwa, sep=self.separator, header=None)
                self.zaladowany = True

                self.data = pd.DataFrame(self.message)
                self.message.columns = self.res

        except:
            self.result_mess = "Cos poszło nie tak "
            self.zaladowany = False


        self.wynik.delete(0.0, END)
        self.wynik.insert(0.0, self.message)
        self.check_wczytaj()

        self.result.delete(0.0, END)
        self.result.insert(0.0, self.result_mess)

    def normalizuj(self):
            if self.to_norm.get() == '':

                    for kolumna in self.znormalizowane:

                        col = kolumna
                        self.sprawdz(col)
                        if self.zaladowany:
                            self._ = pd.DataFrame(self.message)

                            try:

                                self.message[col] = np.float32(self.message[col])
                                self.norm_numbers(col)
                                self.result_mess = "Pomyślne znormalizowano "
                                self.result_mess += self.col
                                self.result_mess += " do zakresu "
                                self.result_mess += self.d[self.col]
                            except:
                                self.result_mess = ""
                        else:
                            self.result_mess = "Wczytaj plik"

                        if self.zaladowany:
                            self.wynik.delete(0.0, END)
                            self.wynik.insert(0.0, self._)

                        self.result.delete(0.0, END)
                        self.result.insert(0.0, self.result_mess)
            else:
                col = self.col
                self.sprawdz(col)
                if self.zaladowany:
                    self._ = pd.DataFrame(self.message)

                    try:
                        self.col = self.to_norm.get()
                        self.message[col] = np.float32(self.message[col])
                        self.norm_numbers(col)
                        self.result_mess = "Pomyślne znormalizowano "
                        self.result_mess+= self.col
                        self.result_mess+=" do zakresu "
                        self.result_mess+=self.d[self.col]
                    except:
                        self.result_mess="Nie da sie znormalizować"
                else:
                    self.result_mess = "Wczytaj plik"

                if self.zaladowany:
                    self.wynik.delete(0.0, END)
                    self.wynik.insert(0.0, self._)

                self.result.delete(0.0, END)
                self.result.insert(0.0, self.result_mess)


root = Tk()
root.geometry("1100x600")
app = Aplication(root)
root.mainloop()

