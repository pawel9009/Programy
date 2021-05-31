from tkinter import *

lista = []
score1= []

def post_order(node):
    if not node.children:
        return node.value

    if node.player1:
        maxEva = -44444
        score1 = []
        for child in node.children:
            eva = post_order(child)
            maxEva = max(maxEva,eva)
            score1.append(eva)
            # print(maxEva, "max - glebokosc", child.depth, child.player1)
        print(max(score1)," maxy")
        return max(score1)

    else:
        minEva = 999999
        score2 = []
        for child in node.children:
            eva = post_order(child)
            minEva = min(minEva, eva)
            score2.append(eva)
            # print(minEva, "min -  glebokosc", child.depth, child.player1)
        print(min(score2)," minima")
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
        wynik = post_order(root)
        print(wynik, "wunik")


class TreeNode:
    def __init__(self, value):
        self.children = []
        self.value = value
        self.data = value
        self.parent = None
        self.depth = 0
        self.player1 = True
        self.end=False

    def add_child(self, child):
        child.parent = self
        child.data = child.value
        child.value += self.value

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
            print("Przegrana", "Protagonista" if self.get_level() % 2 == 0 else "Antagonista")
        elif (self.value == Aplication.WIN):
            self.end=0
            print("Remis")

        print("   " * self.depth, f"głębokość - {self.depth}, value {self.value} - gracz ||{self.player1}")
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
app.geometry("300x80")
app = Aplication(app)
app.mainloop()

# def minmax(self):
#     if not self:
#         return []
#     stack = [self]
#     last = None
#     while stack:
#         self = stack[-1]
#         if not self.children or last and (last in self.children):
#             print(self.value)
#             stack.pop()
#             last = self
#         else:
#             for child in self.children[::-1]:
#                 stack.append(child)
