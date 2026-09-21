import itertools
import random

from ambiente import gerar_ambiente, checkObj, percepcao, executar_acao, LIMPO, SUJO
from agente import TAMANHO_MUNDO, agenteReativoSimples, funcaoMapear
from main import MAX_MOVIMENTOS, simular

LADO = TAMANHO_MUNDO + 2
CELULAS = TAMANHO_MUNDO * TAMANHO_MUNDO
INICIOS = list(itertools.product(range(1, TAMANHO_MUNDO + 1), repeat=2))


def testar_mapa_e_um_ciclo_unico():
    for tamanho in (2, 4, 6, 8):
        mapa = funcaoMapear(tamanho)
        sala = gerar_ambiente(tamanho + 2, tamanho + 2, 0)
        posicao, visitados = (1, 1), set()
        for _ in range(tamanho * tamanho):
            visitados.add(posicao)
            nova = executar_acao(sala, posicao, mapa[posicao])
            assert nova != posicao, f"bateu na parede em {posicao}"
            posicao = nova
        assert posicao == (1, 1) and len(visitados) == tamanho * tamanho, tamanho
    print("ok: o mapa é um ciclo único que passa por todos os quadrados, para lados 2, 4, 6 e 8")


def testar_lado_impar():
    for tamanho in (1, 3, 5):
        try:
            funcaoMapear(tamanho)
        except ValueError:
            continue
        raise AssertionError(f"lado {tamanho} deveria levantar ValueError")
    print("ok: lado ímpar levanta ValueError")


def testar_instrucoes_do_4x4():
    esperado = {
        (1, 1): "direita", (2, 1): "direita", (3, 1): "direita", (4, 1): "abaixo",
        (1, 2): "acima", (2, 2): "abaixo", (3, 2): "esquerda", (4, 2): "esquerda",
        (1, 3): "acima", (2, 3): "direita", (3, 3): "direita", (4, 3): "abaixo",
        (1, 4): "acima", (2, 4): "esquerda", (3, 4): "esquerda", (4, 4): "esquerda",
    }
    assert funcaoMapear(4) == esperado
    for (x, y), acao in esperado.items():
        assert agenteReativoSimples((x, y, False)) == acao
        assert agenteReativoSimples((x, y, True)) == "aspirar"
    print("ok: o agente aspira quando sujo e, quando limpo, segue a instrução da casa em que está")


def testar_agente_sem_estado():
    percepcoes = [(1, 1, False), (3, 2, True), (1, 1, False), (4, 4, False), (3, 2, True)]
    primeira = [agenteReativoSimples(p) for p in percepcoes]
    segunda = [agenteReativoSimples(p) for p in reversed(percepcoes)][::-1]
    assert primeira == segunda == ["direita", "aspirar", "direita", "esquerda", "aspirar"]

    sala = gerar_ambiente(LADO, LADO, 0)
    sala[2][2] = SUJO
    assert percepcao(sala, (2, 2)) == (2, 2, True)
    assert percepcao(sala, (3, 3)) == (3, 3, False)
    executar_acao(sala, (2, 2), "aspirar")
    assert sala[2][2] == LIMPO
    print("ok: o agente só usa a percepção (posição e sujo) e não guarda estado")


def testar_todas_as_posicoes_iniciais():
    random.seed(0)
    simulacoes = 0
    for inicio in INICIOS:
        for quantidade in list(range(CELULAS + 1)) * 30:
            sala = gerar_ambiente(LADO, LADO, quantidade)
            acoes = simular(sala, inicio, mostrar=False)
            assert checkObj(sala) == 0, f"sala não ficou limpa (início {inicio}, sujeira {quantidade})"
            assert acoes == MAX_MOVIMENTOS + quantidade, (inicio, quantidade, acoes)
            simulacoes += 1
    print(f"ok: {simulacoes} simulações rodaram {MAX_MOVIMENTOS} movimentos e terminaram com a sala limpa")


def testar_exaustivo_de_dois_inicios():
    for inicio in [(1, 1), (3, 2)]:
        for mascara in range(1 << CELULAS):
            sala = gerar_ambiente(LADO, LADO, 0)
            for i in range(CELULAS):
                if mascara >> i & 1:
                    sala[1 + i // TAMANHO_MUNDO][1 + i % TAMANHO_MUNDO] = SUJO
            simular(sala, inicio, mostrar=False)
            assert checkObj(sala) == 0, (inicio, mascara)
    print(f"ok: as {1 << CELULAS} distribuições de sujeira, partindo de (1, 1) e de (3, 2), ficaram limpas")


def testar_continua_ate_o_limite():
    for inicio in INICIOS:
        sala = gerar_ambiente(LADO, LADO, 0)
        assert simular(sala, inicio, mostrar=False) == MAX_MOVIMENTOS, inicio

        sala = gerar_ambiente(LADO, LADO, 0)
        sala[1][2] = SUJO
        assert simular(sala, inicio, mostrar=False) == MAX_MOVIMENTOS + 1, inicio
        assert checkObj(sala) == 0, inicio
    print(f"ok: sala limpa ou quase limpa continua até os {MAX_MOVIMENTOS} movimentos")


def testar_limite_cobre_a_sala():
    assert MAX_MOVIMENTOS >= CELULAS - 1
    print(f"ok: {MAX_MOVIMENTOS} movimentos bastam para percorrer os {CELULAS} quadrados ({CELULAS - 1} necessários)")


if __name__ == "__main__":
    testar_mapa_e_um_ciclo_unico()
    testar_lado_impar()
    testar_instrucoes_do_4x4()
    testar_agente_sem_estado()
    testar_todas_as_posicoes_iniciais()
    testar_exaustivo_de_dois_inicios()
    testar_continua_ate_o_limite()
    testar_limite_cobre_a_sala()
