import random;

try:
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
except ImportError:
    plt = None

LIMPO = 0
PAREDE = 1
SUJO = 2

ACOES = ("acima", "abaixo", "esquerda", "direita", "aspirar")
MOVIMENTOS = {
    "acima": (0, -1),
    "abaixo": (0, 1),
    "esquerda": (-1, 0),
    "direita": (1, 0),
}


def gerar_ambiente(largura_sala: int, comprimento_sala: int, quantidade_sujeira: int) -> list[list[int]]:
    sala = []

    for y in range(comprimento_sala):
        linha = []
        for x in range(largura_sala):
            if x == 0 or x == largura_sala - 1 or y == 0 or y == comprimento_sala - 1:
                linha.append(PAREDE)
            else:
                linha.append(LIMPO)
        sala.append(linha)

    posicoes_sujeira = [
        (x, y)
        for y in range(1, comprimento_sala - 1)
        for x in range(1, largura_sala - 1)
    ]
    for x, y in random.sample(posicoes_sujeira, quantidade_sujeira):
        sala[y][x] = SUJO

    return sala


def posicao_inicial(sala: list[list[int]]) -> tuple[int, int]:
    return random.randint(1, len(sala[0]) - 2), random.randint(1, len(sala) - 2)


def percepcao(sala: list[list[int]], posicao: tuple[int, int]) -> tuple[int, int, bool]:
    x, y = posicao
    return x, y, sala[y][x] == SUJO


def checkObj(sala: list[list[int]]) -> int:
    return int(any(celula == SUJO for linha in sala for celula in linha))


def executar_acao(sala: list[list[int]], posicao: tuple[int, int], acao: str) -> tuple[int, int]:
    x, y = posicao

    if acao == "aspirar":
        sala[y][x] = LIMPO
        return posicao

    if acao not in MOVIMENTOS:
        raise ValueError(f"Ação inválida: {acao}")

    dx, dy = MOVIMENTOS[acao]
    if sala[y + dy][x + dx] == PAREDE:
        return posicao

    return x + dx, y + dy


def imprimir_sala(sala: list[list[int]], posicao: tuple[int, int]) -> None:
    x_robo, y_robo = posicao
    for y, linha in enumerate(sala):
        print(" ".join("R" if (x, y) == (x_robo, y_robo) else str(celula) for x, celula in enumerate(linha)))


def exibir(sala: list[list[int]], posicao: tuple[int, int]) -> None:
    if plt is None:
        raise RuntimeError("matplotlib nao esta instalado neste ambiente.")

    x, y = posicao

    cores = ListedColormap(["white", "dimgray", "saddlebrown"])
    plt.imshow(sala, cmap=cores, vmin=LIMPO, vmax=SUJO)

    plt.text(x, y, "R", color="red", fontsize=20, fontweight="bold", ha="center", va="center")

    plt.show(block=False)

    plt.pause(0.5)
    plt.clf()
