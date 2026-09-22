import itertools

from ambiente import gerar_ambiente, checkObj, percepcao, executar_acao, ACOES, SUJO
from agente import TAMANHO_MUNDO, agenteReativoSimples, agenteObjetivo
from main import POSICAO_INICIAL_OBJETIVO, simular_objetivo

LADO = TAMANHO_MUNDO + 2
CELULAS = TAMANHO_MUNDO * TAMANHO_MUNDO
CASAS = list(itertools.product(range(1, TAMANHO_MUNDO + 1), repeat=2))


def sala_com_sujeira(casas):
    sala = gerar_ambiente(LADO, LADO, 0)
    for x, y in casas:
        sala[y][x] = SUJO
    return sala


def rodar_reativo_por(sala, quantidade):
    posicao = POSICAO_INICIAL_OBJETIVO
    for _ in range(quantidade):
        posicao = executar_acao(sala, posicao, agenteReativoSimples(percepcao(sala, posicao)))


def testar_checkobj():
    assert checkObj(gerar_ambiente(LADO, LADO, 0)) == 0
    assert checkObj(sala_com_sujeira([(3, 2)])) == 1
    assert checkObj(sala_com_sujeira(CASAS)) == 1
    print("ok: checkObj devolve 1 se há sujeira e 0 se a sala está limpa")


def testar_noop():
    assert "NoOp" in ACOES and len(ACOES) == 6
    sala = sala_com_sujeira([(2, 2)])
    antes = [linha[:] for linha in sala]
    assert executar_acao(sala, (2, 2), "NoOp") == (2, 2)
    assert sala == antes
    print("ok: NoOp é a sexta ação e não muda nada")


def testar_agente_objetivo():
    for x, y in CASAS:
        for sujo in (True, False):
            assert agenteObjetivo((x, y, sujo), 0) == "NoOp"
            assert agenteObjetivo((x, y, sujo), 1) == agenteReativoSimples((x, y, sujo))
    assert agenteObjetivo((2, 2, True), 1) == "aspirar"
    assert agenteObjetivo((1, 1, False), 1) == "direita"
    print("ok: sem sujeira o agente devolve NoOp; com sujeira age como o reativo simples")


def testar_sala_ja_limpa():
    assert simular_objetivo(gerar_ambiente(LADO, LADO, 0), mostrar=False) == 0
    print("ok: sala já limpa termina com 0 pontos")


def testar_casos_conhecidos():
    assert simular_objetivo(sala_com_sujeira([(1, 1)]), mostrar=False) == 1
    assert simular_objetivo(sala_com_sujeira([(2, 1)]), mostrar=False) == 2
    assert simular_objetivo(sala_com_sujeira([(1, TAMANHO_MUNDO)]), mostrar=False) == 13 + 1
    assert simular_objetivo(sala_com_sujeira([(1, 2)]), mostrar=False) == (CELULAS - 1) + 1
    assert simular_objetivo(sala_com_sujeira(CASAS), mostrar=False) == (CELULAS - 1) + CELULAS
    print("ok: pontos esperados em casos conhecidos, com o pior caso em 31")


def testar_todas_as_distribuicoes():
    for mascara in range(1 << CELULAS):
        casas = [CASAS[i] for i in range(CELULAS) if mascara >> i & 1]

        sala = sala_com_sujeira(casas)
        pontos = simular_objetivo(sala, mostrar=False)
        assert checkObj(sala) == 0, mascara
        assert pontos <= (CELULAS - 1) + CELULAS, (mascara, pontos)

        if pontos > 0:
            sala = sala_com_sujeira(casas)
            rodar_reativo_por(sala, pontos - 1)
            assert checkObj(sala) == 1, f"parou tarde demais (máscara {mascara})"
        sala = sala_com_sujeira(casas)
        rodar_reativo_por(sala, pontos)
        assert checkObj(sala) == 0, f"parou cedo demais (máscara {mascara})"
    print(f"ok: nas {1 << CELULAS} distribuições de sujeira a sala termina limpa e o agente para no primeiro instante possível")


if __name__ == "__main__":
    testar_checkobj()
    testar_noop()
    testar_agente_objetivo()
    testar_sala_ja_limpa()
    testar_casos_conhecidos()
    testar_todas_as_distribuicoes()
