TAMANHO_MUNDO = 4


def funcaoMapear(tamanho: int) -> dict[tuple[int, int], str]:
    if tamanho < 2 or tamanho % 2 != 0:
        raise ValueError(f"Não existe ciclo que percorra uma sala {tamanho}x{tamanho}: o lado precisa ser par")

    mapa = {}
    for y in range(1, tamanho + 1):
        for x in range(1, tamanho + 1):
            if x == 1 and y > 1:
                mapa[(x, y)] = "acima"
            elif y == 1:
                mapa[(x, y)] = "direita" if x < tamanho else "abaixo"
            elif y % 2 == 0:
                if x > 2:
                    mapa[(x, y)] = "esquerda"
                else:
                    mapa[(x, y)] = "esquerda" if y == tamanho else "abaixo"
            else:
                mapa[(x, y)] = "direita" if x < tamanho else "abaixo"
    return mapa


MAPA = funcaoMapear(TAMANHO_MUNDO)


def agenteReativoSimples(percepcao: tuple[int, int, bool]) -> str:
    x, y, sujo = percepcao

    if sujo:
        return "aspirar"

    return MAPA[(x, y)]


def agenteObjetivo(percepcao: tuple[int, int, bool], objObtido: int) -> str:
    if objObtido == 0:
        return "NoOp"

    return agenteReativoSimples(percepcao)
