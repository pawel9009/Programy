class Critter(object):
    """Wirtualny pupil"""


    def __init__(self, name, hunger = 0, boredom =0):
        self.name = name
        self.hunger=hunger
        self.boredom = boredom

    @property
    def name(self):
        return self.__name

    @property
    def mood(self):
        unhapiness = self.hunger+self.boredom
        if unhapiness<5:
            m = "szczesliwy"
        elif 5 <= unhapiness <= 10:
            m = "zadowolony"
        elif 11 <= unhapiness <=15:
            m = "poddenerwowany"
        else:
            m = "wsciekły"
        return m

    @name.setter
    def name(self, new_name):
        if new_name == "":
            print("nie moze być pusty ciaz znaków gamoniu")
        else:
            self.__name = new_name
            print("zmiana imienia sie powiedła")

    def __str__(self):
        rep = "Objekt klasy Critter\n"
        rep += "name: " + self.name + "\n"
        rep += "glod: " + str(self.hunger) + "\n"
        rep += "znudzenie : " + str(self.boredom) + "\n"
        return rep

    def __pass_time(self):
        self.hunger+=1
        self.boredom+=1

    def talk(self):
        print("Cześć! Jestem ", self.name, " i jestem teraz ", self.mood , "\n")
        self.__pass_time()

    def eat(self, food):
        print("mniam mniam. Dziekuję ")


        if food == "1":
            self.hunger -= 1
        elif food == "2":
            self.hunger -= 2
        elif food == "3":
            self.hunger -= 3
        elif food == "4":
            self.hunger -= 4
        else:
            print("zla ilosc nic nie dostanie")
            self.hunger-= 0

        if self.hunger<0:
            self.hunger=0
        self.__pass_time()

    def play(self, fun = 4):
        print("hurraa!")
        self.boredom-= fun
        if self.boredom<0:
            self.boredom=0
        self.__pass_time()

def main():
    crit_name = input("jak chcesz nazwac zwierzaka?")
    crit = Critter(crit_name)

    choice =None
    while choice!="0":
        print \
            ("""
            Opiekun zwierzaka
            0 - zakończ
            1 - słuchaj swojego zwierzaka
            2 - nakarm zwierzaka
            3 - pobaw sie 
            """)
        choice = input("Wybierasz?")

        if choice == "0":
            print("Do widzenia.")
        elif choice == "1":
            crit.talk()
        elif choice == "2":
            food = input("ile jedzenia dac? 1-4")
            crit.eat(food)
        elif choice == "3":
            crit.play()
        else:
            print("zły wybór")


main()
