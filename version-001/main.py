from ambiente import gerar_ambiente;

sala = gerar_ambiente(6, 6, 6)

def imprimir_sala(sala: list[list[str]]) -> None:
    for linha in sala:
        print(" ".join(str(celula) for celula in linha))

imprimir_sala(sala)