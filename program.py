import pandas as pd
import sys
import os
import yaml
from tkinter import *
import json
import random
from tkinter import filedialog
import pandas_datareader.data as web
import numpy as np

from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
row = config.getint('australian', 'num_rows')
col_num = config.getint('australian', 'col_num')
col = config.get('australian', 'columns')
A1= config.get('australian', 'A1')
A4= config.get('australian', 'A4')
A5= config.get('australian', 'A5')
a1 = json.loads(A1)
a4 = json.loads(A4)
a5 = json.loads(A5)

for i in a5:
    print(i, a5[i])



def rozszerzenie(nazwa):
    roz = str(nazwa)
    czlon = roz[::-1]
    pom = czlon.find('.')
    wynik = czlon[0:pom]
    wynik = wynik[::-1]
    return wynik

class Aplication(Frame):
    def __init__(self,master ):
        super(Aplication, self).__init__(master)
        self.grid()
        self.create_widgets()
        self.zaladowany = False
        self.plik = None


    def create_widgets(self):

        Button(self,
               text="Znormalizuj",
               command=self.normalizuj
               ).grid(row=1, column=1, sticky=W)
        Button(self,
               text='Wczytaj plik',
               command=self.onclick
               ).grid(row=0, column=0, sticky=W)

        self.entry = Entry(self)
        self.entry.grid(row=0, column=1, sticky=W)
        Button(self,
               text = "Dodaj separator",
               command = self.AddSep
               ).grid(row=0,column =2, sticky=W)
        self.wynik = Text(self,width = 170 , height = 20, wrap =CHAR)
        self.wynik.grid(row=2,column=0, columnspan=10)


    def onclick(self):
        self.sep = self.entry.get()
        self.message = ""
        print(self.sep)
        self.nazwa = filedialog.askopenfilename()
        rozsz = rozszerzenie(self.nazwa)
        print(rozsz)
        if  rozsz == "csv":
            try:
                if self.nazwa:
                    self.message = pd.read_csv(self.nazwa, sep=",")
                    self.zaladowany = True
            except:
                self.message = "cos poszło nie tak "
                self.zaladowany = False
        elif rozsz == "xls" or rozsz == "xlsx":
            try:
                if self.nazwa:
                    self.message = pd.read_excel(self.nazwa)
                    _=pd.DataFrame(self.message, columns=['Product','Product','Product','Product','Product','Product', ])

                    self.plik = pd.read_excel(self.nazwa)
                    self.zaladowany = True
            except:
                self.message = "cos poszło nie tak "
                self.zaladowany = False
        else:
            try:
                if self.nazwa:
                    self.message = pd.read_table(self.nazwa, sep=',')
                    self.plik = pd.read_table(self.nazwa)
                    self.zaladowany = True
            except:
                self.message = "cos poszło nie tak "
                self.zaladowany = False

        self.wynik.delete(0.0, END)

        with pd.option_context('display.max_rows', None, 'display.max_colwidth', None,'display.max_columns', None):
            self.wynik.insert(0.0, (self.message.to_string()).split(" - "))

    def normalizuj(self,):
        self.data = self.plik

        print(type(self.data))



        self.wynik.delete(0.0, END)
        self.wynik.insert(0.0, self.data)


    def AddSep(self):
        self.message = pd.read_csv(self.nazwa, sep=self.sep)


        self.wynik.delete(0.0, END)
        self.wynik.insert(0.0, self.message)

root = Tk()
root.geometry("1700x300")
app= Aplication(root)
root.mainloop()
