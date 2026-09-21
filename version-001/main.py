from ambiente import gerar_ambiente, posicao_inicial, percepcao, executar_acao, checkObj, imprimir_sala, exibir
from agente import TAMANHO_MUNDO, agenteReativoSimples

MAX_MOVIMENTOS = 30
QUANTIDADE_SUJEIRA = 6


def simular(sala: list[list[int]], posicao: tuple[int, int], mostrar: bool = True) -> int:
    movimentos = 0
    acoes = 0
    if mostrar:
        exibir(sala, posicao)

    while movimentos < MAX_MOVIMENTOS or percepcao(sala, posicao)[2]:
        acao = agenteReativoSimples(percepcao(sala, posicao))
        posicao = executar_acao(sala, posicao, acao)
        acoes += 1
        if acao != "aspirar":
            movimentos += 1
        if mostrar:
            exibir(sala, posicao)

    return acoes


if __name__ == "__main__":
    lado = TAMANHO_MUNDO + 2
    sala = gerar_ambiente(lado, lado, QUANTIDADE_SUJEIRA)
    posicao = posicao_inicial(sala)

    imprimir_sala(sala, posicao)
    acoes = simular(sala, posicao)
    print(f"{MAX_MOVIMENTOS} movimentos concluídos, {acoes} ações no total")
    print("Verificação: sala limpa" if checkObj(sala) == 0 else "Verificação: ainda há sujeira")
