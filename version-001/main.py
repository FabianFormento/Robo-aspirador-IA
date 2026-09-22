import sys

from ambiente import gerar_ambiente, posicao_inicial, percepcao, executar_acao, checkObj, imprimir_sala, exibir
from agente import TAMANHO_MUNDO, agenteReativoSimples, agenteObjetivo

MAX_MOVIMENTOS = 30
QUANTIDADE_SUJEIRA = 6
POSICAO_INICIAL_OBJETIVO = (1, 1)


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


def simular_objetivo(sala: list[list[int]], mostrar: bool = True) -> int:
    posicao = POSICAO_INICIAL_OBJETIVO
    pontos = 0
    if mostrar:
        exibir(sala, posicao)

    while True:
        acao = agenteObjetivo(percepcao(sala, posicao), checkObj(sala))
        if acao == "NoOp":
            return pontos

        posicao = executar_acao(sala, posicao, acao)
        pontos += 1
        if mostrar:
            exibir(sala, posicao)


if __name__ == "__main__":
    tipo = sys.argv[1] if len(sys.argv) > 1 else "reativo"
    if tipo not in ("reativo", "objetivo"):
        sys.exit("Uso: python3 main.py [reativo|objetivo]")

    lado = TAMANHO_MUNDO + 2
    sala = gerar_ambiente(lado, lado, QUANTIDADE_SUJEIRA)

    if tipo == "reativo":
        posicao = posicao_inicial(sala)
        imprimir_sala(sala, posicao)
        acoes = simular(sala, posicao)
        print(f"{MAX_MOVIMENTOS} movimentos concluídos, {acoes} ações no total")
    else:
        imprimir_sala(sala, POSICAO_INICIAL_OBJETIVO)
        pontos = simular_objetivo(sala)
        print(f"Objetivo atingido em {pontos} pontos")

    print("Verificação: sala limpa" if checkObj(sala) == 0 else "Verificação: ainda há sujeira")
