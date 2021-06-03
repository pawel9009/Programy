from tkinter import *
import os
from graphviz import Digraph
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

dot = Digraph(comment='graf')
disp = []
lista = []
score1= []
trasa=[]
id =1
def minmax(node):
    if not node.children:
        return node.end

    if node.player1:
        score1 = []
        for child in node.children:

            result = minmax(child)
            one = f'"prot;\\n {node.id} \\n value {node.value}"'

            if result not in score1:
                score1.append(result)
            two = f'"ant;\\n {child.id} \\n value {child.value}" [label = "{child.data}"]'
            disp.append(f" {one} -> {two}")
        node.end=max(score1)
            # print(maxEva, "max - glebokosc", child.depth, child.player1)
        print(max(score1)," maxy ", f"glebokosc = {node.depth} , gracz1?{node.player1}", )
        return max(score1)

    else:
        score2 = []
        for child in node.children:

            result = minmax(child)
            one = f'"ant;\\n {node.id} \\n value {node.value}"'
            two = f'"prot;\\n {child.id} \\n value {child.value}" [label = "{child.data}"  color="red"]'
            disp.append(f" {one} -> {two}")
            if result not in score2:
                score2.append(result)
        node.end = min(score2)
        print(min(score2), " minima ", f"glebokosc = {node.depth} , gracz1?{node.player1}", )
        return min(score2)


class Aplication(Frame):
    WIN = 4
    ZMIENNE = None

    def __init__(self, master):
        super(Aplication, self).__init__(master)
        self.grid()
        self.create_widgets()
        self.WIN = 0

    def create_widgets(self):
        Label(self,
              text="Liczba n "
              ).grid(row=0, column=0, sticky=W)
        Label(self,
              text="Dane po spacji "
              ).grid(row=1, column=0, sticky=W)
        self.win = Entry(self)
        self.win.grid(row=0, column=1, sticky=W)

        self.liczby = Entry(self)
        self.liczby.grid(row=1, column=1, sticky=W)

        self.wynik = Text(self)
        self.wynik.grid(row=4, columnspan=15, sticky=W)

        Label(self,
              ).grid(row=3, column=0, sticky=W)

        Button(self,
               text="Licz",
               command=self.apka
               ).grid(row=2, column=0, sticky=W)

    def apka(self):
        Aplication.WIN = int(self.win.get())
        dane = self.liczby.get()
        liczby = []
        dane = list(dane.split(' '))
        for x in dane:
            liczby.append(int(x))
        Aplication.ZMIENNE = liczby

        root = build_product_tree()
        root.print_tree()
        wynik = minmax(root)
        print(len(lista))
        print(wynik, "wynik")

        self.wynik.insert(0.0, disp)


class TreeNode:
    def __init__(self, value):
        self.children = []
        self.value = value
        self.data = value
        self.parent = None
        self.depth = 0
        self.zmiany=""
        self.player1 = True
        self.end=False
        self.id=0

    def add_child(self, child):
        global id
        child.parent = self
        child.data = child.value
        child.value += self.value

        child.id = id
        id+=1
        self.children.append(child)

        child.depth = self.depth + 1
        if self.player1:
            child.player1 = False
        elif self.player1 == False:
            child.player1 = True
        lista.append(child)

    def take_child(self):
        return self.children

    def tak(self, dep):
        if self.depth == dep:
            add(self)

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    # def post_order(self):
    #
    #     if self is not None:
    #         for child in self.children:
    #             self.droga += f" -> {child.value}"
    #             child.post_order()
    #
    #         print(self.value, self.player1)

    def print_tree(self):
        if (self.value > Aplication.WIN):
            if self.player1:
                self.end=1
            else:
                self.end=-1
            # print("Przegrana", "Protagonista" if self.get_level() % 2 == 0 else "Antagonista")
        elif (self.value == Aplication.WIN):
            self.end=0
            print("Remis")

        print(self.id, "   " * self.depth, f"głębokość - {self.depth}, value {self.value} - gracz ||{self.player1}")
        if self.children:
            for child in self.children:
                child.print_tree()


def add(root):
    for x in range(len(Aplication.ZMIENNE)):
        root.add_child(TreeNode(Aplication.ZMIENNE[x]))
    return root


def build_product_tree():
    root = TreeNode(0)
    root.tak(0)
    tak = 0
    flaga = True
    while flaga:
        for x in lista:
            if x.depth == tak:
                if x.value < Aplication.WIN:
                    add(x)

        tak += 1
        if tak > 18:
            flaga = False
    return root


app = Tk()
app.title("Aplikacja")
app.geometry("600x220")
app = Aplication(app)
app.mainloop()
