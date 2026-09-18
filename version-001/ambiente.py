import random;

def gerar_ambiente(largura_sala: int, comprimento_sala: int, quantidade_sujeira: int) -> list[list[str]]:
    sala = []

    for x in range(largura_sala):
        larg = []
        for y in range(comprimento_sala):
            if x == 0 or x == largura_sala - 1 or y == 0 or y == comprimento_sala - 1:
                larg.append(1)  # Adiciona parede
            else:
                larg.append(0)  # Adiciona espaço vazio
        sala.append(larg)


    for _ in range(quantidade_sujeira):
        x = random.randint(1, largura_sala - 2)
        y = random.randint(1, comprimento_sala - 2)
        sala[y][x] = "2"  # Adiciona sujeira

    posicoes_livres = [
        (x, y)
        for y in range(1, comprimento_sala - 1)
        for x in range(1, largura_sala - 1)
        if sala[y][x] == 0
    ]
    x, y = random.choice(posicoes_livres)
    sala[y][x] = "R"  # Adiciona o robô

    return sala