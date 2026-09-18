import random

import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

LIMPO = 0
SUJO = 2
PAREDE = 1


def criar_ambiente(linhas=4, colunas=4, prob_sujeira=0.5, semente=None):
    if semente is not None:
        random.seed(semente)

    matriz = np.full((linhas, colunas), PAREDE, dtype=int)
    for i in range(1, linhas - 1):
        for j in range(1, colunas - 1):
            matriz[i][j] = SUJO if random.random() < prob_sujeira else LIMPO
    return matriz


def parede(matriz, linha, coluna):
    linhas, colunas = matriz.shape
    if not (0 <= linha < linhas and 0 <= coluna < colunas):
        return True
    return matriz[linha][coluna] == PAREDE


def exibir(matriz, posicao=None):
    if plt is None:
        raise RuntimeError("matplotlib nao esta instalado neste ambiente.")

    plt.imshow(matriz, cmap="gray", vmin=LIMPO, vmax=PAREDE)

    if posicao is not None:
        linha, coluna = posicao
        plt.plot([coluna], [linha], marker="o", color="r", ls="")

    plt.show(block=False)
    plt.pause(0.5)
    plt.clf()


if __name__ == "__main__":
    ambiente = criar_ambiente(6, 6)
    print(ambiente)
