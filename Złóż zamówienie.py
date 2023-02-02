from tkinter import *


class Aplication(Frame):
    def __init__(self, master):
        super(Aplication, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        Label(self,
              text="Witam w mojej kuchni, na co masz ochote?"
              ).grid(row=0, column=0, columnspan=4, sticky=W)

        self.pierogi = BooleanVar()
        Checkbutton(self,
                    text="pierogi - 12.70",
                    variable=self.pierogi
                    ).grid(row=1, column=0, sticky=W)

        self.barszcz = BooleanVar()
        Checkbutton(self,
                    text="barszcz - 8.50",
                    variable=self.barszcz
                    ).grid(row=2, column=0, sticky=W)

        self.nalesniki = BooleanVar()
        Checkbutton(self,
                    text="nalesniki -11.00",
                    variable=self.nalesniki
                    ).grid(row=3, column=0, sticky=W)

        self.kebab = BooleanVar()
        Checkbutton(self,
                    text="kebab - 15.50",
                    variable=self.kebab
                    ).grid(row=4, column=0, sticky=W)

        Button(self,
               text="Złóż zamówienie ",
               command=self.podlicz
               ).grid(row=5, column=0, sticky=W)

        Label(self,
              text="Twoje zamówienie zawiera :"
              ).grid(row=6, column=0, sticky=W)

        self.wynik = Text(self, height=40, width=60, wrap=WORD)
        self.wynik.grid(row=7, column=0, columnspan=3, sticky=W)

    def podlicz(self):
        cena = 0
        result = "Twoje zamówienie zawiera - "
        if self.pierogi.get():
            cena += 12.70
            result += "pierogi "
        if self.barszcz.get():
            cena += 8.50
            result += "barszcz "
        if self.nalesniki.get():
            cena += 11.00
            result += " nalesniki"
        if self.kebab.get():
            cena += 15.50
            result += " kebab"

        result += " i kosztuje - "
        result += str(cena) + "zł. "

        self.wynik.delete(0.0, END)
        self.wynik.insert(0.0, result)


root = Tk()
root.title("Złóż zamówienie")
root.geometry("500x300")
app = Aplication(root)
root.mainloop()
