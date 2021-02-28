import gry,karty
class BJ_Card(karty.Cards):
    """ karta do black jacka"""
    ACE_VALUE = 1

    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10 :
                v = 10
        else:
            v = None
        return v

class BJ_Deck(karty.Deck):
    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank,suit))




class BJ_Hand(karty.Hand):

    def __init__(self,name):
        super(BJ_Hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t"+ super(BJ_Hand, self).__str__()
        if self.total:
            rep +="("+ str(self.total) + ")"
        return rep

    @property
    def total(self):
        for card in self.cards:
            if not card.value:
                return None

        t = 0
        for card in self.cards:
            t+=card.value

        contains_ace = False

        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True

        if contains_ace and t<= 11:
            t+=10

        return t

    def isbusted(self):
        return self.total>21

class BJ_Player(BJ_Hand):

    def is_hitting(self):
        response = gry.ask_yes_no("\n" + self.name+ " Chcesz dobrac kartę (t/n) ? ")
        return response == "t"

    def bust(self):
        print(self.name+" ma fure ")
        self.lose()

    def lose(self):
        print(self.name+ " przegrywa ")

    def win(self):
        print(self.name+ " wygrywa")

    def push(self):
        print(self.name + " remisuje ")


class BJ_Dealer(BJ_Hand):
    def is_hitting(self):
        return self.total<17

    def bust(self):
        print(self.name+ " ma fure")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()


class BJ_Game(object):

    def __init__(self, names):
        self.players = []
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)

        self.dealer = BJ_Dealer("Rozdajacy")

        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shufle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.isbusted():
                sp.append(player)
            return sp

    def __aditional_cards(self,player):
        while not player.isbusted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.isbusted():
                player.bust()

    def play(self):
        #rozdaj kazdemu karty 2
        self.deck.deal(self.players + [self.dealer], per_hand= 2)
        self.dealer.flip_first_card()
        for player in self.players:
            print(player)
        print(self.dealer)

        #rozdaj graczom pozostale
        for player in self.players:
            self.__aditional_cards(player)

        self.dealer.flip_first_card()

        if not self.still_playing:
            print(self.dealer)
        else:
            print(self.dealer)
            self.__aditional_cards(self.dealer)

            if self.dealer.isbusted():
                #kazdy wygrywa
                for player in self.still_playing:
                    player.win()
            else:
                #porównaj punkty kazdego gracza pozostajacego w grze z punktami rozdajacego
                for player in self.still_playing:
                    if player.total> self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

        for player in self.players:
            player.clear()

        self.dealer.clear()


def main():
    print("\t Witaj w grze Black Jack! \n")

    names = []
    numbers = gry.ask_number("podaj liczbe graczy od 1 do 7 :", low=1, high=8)
    for i in range(numbers):
        name = input("Podaj imie gracza: ")
        names.append(name)
    print()

    game = BJ_Game(names)
    again = None

    while again !="n":
        game.play()
        again = gry.ask_yes_no("\n Czy chcesz zagrac ponownie?")


main()
print("nasisnij aby zakonczyc")




