import numpy as np
import matplotlib.pyplot as plt
import copy

wzorzec1 = [1, 1, 0, 0, 0,
            0, 1, 0, 0, 0,
            0, 1, 0, 0, 0,
            0, 1, 0, 0, 0,
            0, 1, 0, 0, 0]

wzorzec2 = [1, 0, 0, 0, 1,
            0, 1, 0, 1, 0,
            0, 0, 1, 0, 0,
            0, 1, 0, 1, 0,
            1, 0, 0, 0, 1]

wzorzec3 = [0, 0, 1, 0, 0,
            0, 0, 1, 0, 0,
            1, 1, 1, 1, 1,
            0, 0, 1, 0, 0,
            0, 0, 1, 0, 0]

test1 = [0, 1, 0, 0, 0,
         0, 1, 0, 0, 0,
         0, 1, 0, 0, 0,
         0, 1, 0, 0, 0,
         0, 1, 0, 0, 0]

test2 = [1, 1, 0, 0, 1,
         0, 1, 0, 1, 0,
         0, 1, 1, 1, 0,
         0, 1, 0, 1, 0,
         1, 1, 0, 0, 1]

test3 = [0, 0, 0, 0, 0,
         0, 0, 1, 0, 0,
         1, 1, 1, 1, 1,
         0, 0, 0, 0, 0,
         0, 0, 1, 0, 0]

test4 = [0, 1, 1, 1, 1,
         1, 0, 1, 1, 1,
         1, 0, 1, 1, 1,
         1, 0, 1, 1, 1,
         1, 0, 1, 1, 1]


def rysuj(wzor, wejscie, wynik):
    size = len(wynik) // 5
    wynik_plot = np.array(wynik).reshape((size, size))
    wejscie_plot = np.array(wejscie).reshape((size, size))
    wzor_plot = np.array(wzor).reshape((size, size))
    fig = plt.figure(figsize=(8,7),dpi=150)
    ax = fig.subplots(2, 2)
    ax[0][0].matshow(wzor_plot)
    ax[0][1].matshow(wejscie_plot)
    cax = ax[1][0].matshow(wynik_plot, interpolation='nearest')
    ax[1, 1].axis('off')

    fig.colorbar(cax)

    ax[0][0].set_title('Wzor')
    ax[0][1].set_title('Do rozpoznania')
    ax[1][0].set_title('Wynik')
    plt.legend(bbox_to_anchor=(2.5, 1.0))
    plt.show()


def zamien(wagi):
    for x in range(len(wagi)):
        if wagi[x] > 0:
            wagi[x] = 1.0
        else:
            wagi[x] = -1.0
    return wagi


class Hopfield:
    def __init__(self, h, w):

        self.n = h * w
        self.weights = np.zeros((self.n, self.n))

    def naucz_obraz(self, wejscie):
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    waga = self.weights[i][j]
                    suma = (wejscie[i] * wejscie[j]) / self.n
                    self.weights[i][j] = waga + suma

    def rozpoznaj_obraz(self, img):
        wejscie = copy.copy(img)

        while True:
            ilosc_zmian = 0
            for i in range(self.n):
                suma = 0
                for j in range(self.n):
                    if i != j:
                        suma += (wejscie[j] * self.weights[i, j])
                if suma >= 0:
                    if wejscie[i] == -1:
                        ilosc_zmian += 1
                    wejscie[i] = 1
                else:
                    if wejscie[i] == 1:
                        ilosc_zmian += 1
                    wejscie[i] = -1
            print('ilosc_zmian - ', ilosc_zmian)
            if ilosc_zmian == 0:
                break
        return wejscie


przypadek = 2

if przypadek == 1:
    wzorzec_bipolar = zamien(wzorzec1)
    test_bipolar = zamien(test1)
elif przypadek == 2:
    wzorzec_bipolar = zamien(wzorzec2)
    test_bipolar = zamien(test2)
elif przypadek == 3:
    wzorzec_bipolar = zamien(wzorzec3)
    test_bipolar = zamien(test3)
elif przypadek == 4:
    wzorzec_bipolar = zamien(wzorzec3)
    test_bipolar = zamien(test4)

h = Hopfield(5, 5)

h.naucz_obraz(wzorzec_bipolar)

wynik = h.rozpoznaj_obraz(test_bipolar)

rysuj(wzorzec_bipolar, test_bipolar, wynik)
