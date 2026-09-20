"""Regra de negocio da triagem.

Funcoes puras: recebem texto, devolvem classificacao. Sem Django, sem banco,
sem rede. E por isso que sao faceis de testar e de mudar sem quebrar o resto.
"""

import re

PALAVRAS_COMERCIAL = ["orcamento", "preco", "valor", "contratar", "proposta", "plano"]
PALAVRAS_SUPORTE = ["erro", "nao funciona", "bug", "problema", "travando", "parou"]
PALAVRAS_URGENTE = ["urgente", "urgencia", "hoje", "parou", "imediato", "agora"]

ORIGENS_PONTUADAS = {
    "indicacao": 30,
    "site": 20,
    "email": 15,
    "instagram": 10,
}

REGEX_TELEFONE = re.compile(r"\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}")


def _normalizar(texto):
    """Minusculas e sem acento, para comparar palavra-chave sem surpresa."""
    texto = texto.lower()
    trocas = {"á": "a", "â": "a", "ã": "a", "é": "e", "ê": "e", "í": "i",
              "ó": "o", "ô": "o", "õ": "o", "ú": "u", "ç": "c"}
    for acentuada, simples in trocas.items():
        texto = texto.replace(acentuada, simples)
    return texto


def definir_categoria(mensagem):
    texto = _normalizar(mensagem)
    if any(palavra in texto for palavra in PALAVRAS_SUPORTE):
        return "suporte"
    if any(palavra in texto for palavra in PALAVRAS_COMERCIAL):
        return "comercial"
    return "geral"


def definir_urgencia(mensagem):
    texto = _normalizar(mensagem)
    if any(palavra in texto for palavra in PALAVRAS_URGENTE):
        return "alta"
    return "normal"


def calcular_score(mensagem, origem):
    """Pontuacao de 0 a 100 indicando o quanto o lead merece atencao."""
    score = ORIGENS_PONTUADAS.get(origem.lower(), 5)

    tamanho = len(mensagem.strip())
    if tamanho > 200:
        score += 30
    elif tamanho > 80:
        score += 20
    elif tamanho > 20:
        score += 10

    if REGEX_TELEFONE.search(mensagem):
        score += 20

    if definir_urgencia(mensagem) == "alta":
        score += 20

    return min(score, 100)


def classificar(mensagem, origem):
    """Ponto de entrada unico usado pela view."""
    return {
        "categoria": definir_categoria(mensagem),
        "urgencia": definir_urgencia(mensagem),
        "score": calcular_score(mensagem, origem),
    }
