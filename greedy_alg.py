import numpy as np
import matplotlib.pyplot as plt

wzor1 = [[0, 0, 0, 1],
         [0, 0, 1, 1],
         [0, 1, 0, 1],
         [0, 0, 0, 1],
         [0, 0, 0, 1]]

wzor2 = [[0, 1, 1, 1],
         [1, 0, 0, 1],
         [0, 0, 1, 0],
         [0, 1, 0, 0],
         [1, 1, 1, 1]]

wzor3 = [[1, 1, 1, 0],
         [0, 0, 0, 1],
         [1, 1, 1, 1],
         [0, 0, 0, 1],
         [1, 1, 1, 0]]

test1 = [[0, 0, 0, 0],
         [0, 0, 1, 1],
         [0, 1, 1, 1],
         [0, 0, 0, 1],
         [0, 0, 0, 1]]

test2 = [[1, 1, 1, 1],
         [0, 0, 0, 1],
         [1, 1, 1, 1],
         [0, 0, 1, 1],
         [1, 1, 1, 1]]

test3 = [[1, 1, 1, 1],
         [0, 0, 0, 1],
         [0, 0, 1, 0],
         [1, 1, 0, 0],
         [1, 1, 1, 1]]
wzorce = [wzor1, wzor2, wzor3]
testowe = [test1, test2, test3]


def rysuj(wzor, test):
    size = len(test)
    test_plot = np.array(test).reshape((size, size - 1))
    wzor_plot = np.array(wzor).reshape((size, size - 1))

    fig, ax = plt.subplots(1, 2)

    ax[0].matshow(wzor_plot)

    cax = ax[1].matshow(test_plot)
    fig.colorbar(cax)
    ax[0].set_title('Wzor')
    ax[1].set_title('Dopasowany obraz')
    plt.legend()
    plt.show()


def metryka_euk(a, b):
    return np.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))


def manhattan(a, b):
    return sum(abs(val1 - val2) for val1, val2 in zip(a, b))


def miara_niepodobienstwa(mapa, wzorzec):
    miara = 0
    for x in range(len(mapa)):
        for y in range(len(mapa[0])):
            if mapa[x][y] == 1:
                odl_min = 9999999
                for wzor_x in range(len(wzorzec)):
                    for wzor_y in range(len(wzorzec[0])):
                        if wzorzec[wzor_x][wzor_y] == 1:
                            odl_akt = metryka_euk([x, y], [wzor_x, wzor_y])
                            odl_min = min(odl_min, odl_akt)
                miara += odl_min
    return miara


for i, test in enumerate(testowe):
    miara_obustronna = []
    for j, wzor in enumerate(wzorce):
        miara_obustronna.append(-(miara_niepodobienstwa(test, wzor) + miara_niepodobienstwa(wzor, test)))
    index = miara_obustronna.index(max(miara_obustronna))
    print(f' Dla testu{i + 1} najbardziej odpowiada wzorzec {index + 1}')
    rysuj(wzorce[index], test)
