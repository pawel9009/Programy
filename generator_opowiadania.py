from tkinter import *

class Aplication(Frame):
    def __init__(self, master):
        super(Aplication, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        Label(self,
              text = "Wprowadz informacje do nowego opowiadania."
              ).grid(row = 0, column = 0, columnspan = 2, sticky=W)

        Label(self,
              text = "Osoba: "
              ).grid(row = 1, column = 0 , sticky = W)

        self.person_ent = Entry(self)
        self.person_ent.grid(row = 1 , column =1, sticky =W)


        Label(self,
              text="Rzeczownik w liczbie mnogiej: "
              ).grid(row=2, column=0, sticky=W)

        self.noun_ent = Entry(self)
        self.noun_ent.grid(row=2, column=1, sticky=W)

        Label(self,
              text="Czasownik : "
              ).grid(row=3, column=0, sticky=W)

        self.verb_ent = Entry(self)
        self.verb_ent.grid(row=3, column=1, sticky=W)


        Label(self,
              text="Przymiotnik(i): "
              ).grid(row=4, column=0, sticky=W)

        self.is_itchy = BooleanVar()
        Checkbutton(self,
                    text = "naglace",
                    variable = self.is_itchy
                    ).grid(row = 4, column =1, sticky = W)

        self.is_joyous = BooleanVar()
        Checkbutton(self,
                    text="radosne",
                    variable=self.is_joyous
                    ).grid(row=4, column=2, sticky=W)

        self.is_electric = BooleanVar()
        Checkbutton(self,
                    text="elektryzjace",
                    variable=self.is_electric
                    ).grid(row=4, column=3, sticky=W)

        self.is_joyous = BooleanVar()
        Checkbutton(self,
                    text="radosne",
                    variable=self.is_joyous
                    ).grid(row=4, column=2, sticky=W)

        Label(self,
              text = "Cześć ciała :"
              ).grid(row = 5 , column = 0, sticky =W)

        self.body_part = StringVar()
        self.body_part.set(None)

        body_parts = ["pępek", "duzy palec u nogi", "rdzeń przedłuzony"]
        column =1
        for part in body_parts:
            Radiobutton(self,
                        text = part,
                        variable = self.body_part,
                        value = part
                        ).grid(row = 5 , column = column, sticky = W)
            column+=1

        Button(self,
               text = "Akceptuj",
               command = self.tell_story
               ).grid(row = 6, column = 0 , sticky = W)


        self.story_txt = Text(self, width = 75, height = 10 , wrap = WORD)
        self.story_txt.grid(row = 7, column = 0, columnspan = 4)


    def tell_story(self):
        person = self.person_ent.get()
        noun = self.noun_ent.get()
        verb = self.verb_ent.get()
        adjectives=""
        if self.is_itchy.get():
            adjectives+=" naglące "
        if self.is_joyous.get():
            adjectives+=" radosne "
        if self.is_electric.get():
            adjectives+=" elektryzujące "

        body_part = self.body_part.get()


        story = "Sławny badacz i odkrywca"
        story+=person
        story+=" o mało co nie zrezygnowal z zyciowej misji poszukiwania"
        story+=" zaginionego miasta, ktore zamieszkiwały  "
        story+=noun
        story+=", gdy pewnego dnia"
        story+=noun
        story+=" znalazły "
        story+= person
        story+= "a. "
        story+="Silne, "
        story+=adjectives
        story+="osobliwe uczucie owładnęło badaczem. "
        story+="Po tak długim czasie poszukiwanie wreszcie sie zakończyło. W oku "
        story+=person
        story+="a pojawiła sie łza, która spadła na jego "
        story+=body_part
        story+=". A wtedy "
        story+= noun
        story+=" szybko pożarły "
        story+=person
        story+="a. Jaki morał z tego opowiadania? Pomyśl, zanim zaczniesz coś "
        story+=verb
        story+="."




        self.story_txt.delete(0.0, END)
        self.story_txt.insert(0.0 , story)


root = Tk()
root.title("filmy")
app = Aplication(root)
root.mainloop()