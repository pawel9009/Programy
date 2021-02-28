class Player(object):
    """uczestnik gry """
    def __init__(self, name, score = 0):
        self.name = name
        self.score = score

    def __str__(self):
        rep = self.name + " " +str(self.score)
        return rep

def ask_yes_no(question):
    response = None
    while response not in ("t", "n"):
        response = input(question).lower()
    return response

def ask_number(qestion, low, high):
    response = None
    while response not in range(low,high):
        response = int(input(qestion))
    return response

if __name__ == "__main__":
    print("dziala bezposrednio")
    input("aby zakonczyc ")
