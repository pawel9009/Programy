from tkinter import *
import random


class Aplication(Frame):
    def __init__(self, master):
        super(Aplication, self).__init__(master)
        self.grid()
        self.create_widgets()


    def create_widgets(self):
        self.var = random.randrange(1,100)
        self.proby=0
        Label(self,
              text = " Wpisz liczbę :"
              ).grid(row = 0, column = 0,sticky = W)

        self.podpowiedz = Text(self, height =1 , width =50)
        self.podpowiedz.grid(row=1, column=0, sticky=W)

        self.ansver = Entry(self)
        self.ansver.grid(row = 0, column =1, sticky =W)


        Button(self,
               text = "Sprawdz",
               command = self.check
               ).grid(row = 0, column = 2, sticky = W)




        self.wynik = Text(self, height=1 ,width =50, wrap=WORD)
        self.wynik.grid(row=2, column=0, columnspan=3, sticky=W)

    def check(self):
        response = ""
        podpowiedz = ""
        self.proby+=1
        if self.ansver.get() == str(self.var):
            response = "Zgadza sie wynik to "+ str(self.var) + " udalo ci sie w " + str(self.proby)+ " próbach"
        elif self.ansver.get() < str(self.var):
            podpowiedz = "Za mało "
            response = "Niepoprawna liczba"
        elif self.ansver.get() > str(self.var):
            podpowiedz = "Za dużo "
            response = "Niepoprawna liczba"
        else:
            response = "Błędne dane"


        self.wynik.delete(0.0,END)
        self.podpowiedz.delete(0.0,END)
        self.wynik.insert(0.0, response)
        self.podpowiedz.insert(0.0, podpowiedz)

root = Tk()
root.title("Zgadnij jaka to liczba :")
app = Aplication(root)
root.mainloop()