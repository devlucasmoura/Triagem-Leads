"""Testes da regra de negocio.

Nenhum deles precisa de banco ou de rede: a classificacao e funcao pura.
E exatamente esse o motivo de a regra viver em Python e nao dentro do n8n.
"""

from core.classificacao import (
    calcular_score,
    classificar,
    definir_categoria,
    definir_urgencia,
)


def test_mensagem_com_erro_vira_suporte():
    assert definir_categoria("O sistema nao funciona desde ontem") == "suporte"


def test_mensagem_com_orcamento_vira_comercial():
    assert definir_categoria("Gostaria de um orcamento") == "comercial"


def test_mensagem_sem_palavra_chave_vira_geral():
    assert definir_categoria("Bom dia, tudo bem?") == "geral"


def test_suporte_tem_prioridade_sobre_comercial():
    # Mensagem com as duas palavras: problema pesa mais que preco.
    assert definir_categoria("Tive um erro ao pagar, qual o valor?") == "suporte"


def test_palavra_urgente_eleva_urgencia():
    assert definir_urgencia("Preciso disso urgente") == "alta"


def test_mensagem_comum_tem_urgencia_normal():
    assert definir_urgencia("Quando puderem, me retornem") == "normal"


def test_acento_nao_atrapalha():
    assert definir_urgencia("É urgência máxima") == "alta"


def test_indicacao_pontua_mais_que_instagram():
    mensagem = "Quero saber mais"
    assert calcular_score(mensagem, "indicacao") > calcular_score(mensagem, "instagram")


def test_telefone_na_mensagem_aumenta_score():
    com_telefone = calcular_score("Me liga no (21) 99999-8888", "site")
    sem_telefone = calcular_score("Me liga quando puder", "site")
    assert com_telefone > sem_telefone


def test_score_nunca_passa_de_cem():
    mensagem = "URGENTE, parou tudo, ligar (21) 99999-8888. " + "detalhes " * 50
    assert calcular_score(mensagem, "indicacao") == 100


def test_classificar_devolve_as_tres_chaves():
    resultado = classificar("Orcamento urgente por favor", "site")
    assert set(resultado) == {"categoria", "urgencia", "score"}
    assert resultado["categoria"] == "comercial"
    assert resultado["urgencia"] == "alta"
