# Triagem Automatica de Leads

Automacao que recebe leads de qualquer canal, classifica por categoria,
urgencia e pontuacao, e distribui para a pessoa certa — sem ninguem ler nada
manualmente.

---

## Em palavras simples

Uma empresa recebe contatos pelo formulario do site, por e-mail e por rede
social. Alguem precisa abrir cada um, ler, decidir se e venda ou suporte, ver
se e urgente e repassar para o responsavel. Enquanto isso o cliente espera, e
lead parado esfria.

Este projeto faz essa triagem sozinho. O lead chega, o sistema le a mensagem,
decide a categoria e a urgencia, da uma nota de 0 a 100 e avisa o responsavel
na hora — o urgente com destaque.

---

## Arquitetura

```
Formulario / e-mail
        │
        ▼
   ┌─────────┐   POST /classificar   ┌──────────────┐
   │   n8n   │ ────────────────────▶ │  API Django  │
   │         │ ◀──────────────────── │   (Python)   │
   └────┬────┘   categoria, urgencia └──────┬───────┘
        │        e score                    │
        │                                   ▼
        ├──▶ Telegram (urgente)       ┌──────────────┐
        └──▶ Telegram (normal)        │  PostgreSQL  │
                                      └──────────────┘
```

### Divisao de responsabilidade

| Camada | Faz o que | Por que ali |
|---|---|---|
| **n8n** | Recebe o lead e distribui para os canais | Integracao com Slack, Sheets, e-mail e um no na interface, nao codigo |
| **Python** | Decide categoria, urgencia e score | Regra de negocio precisa de teste automatizado e historico no Git |

Esse e o ponto central do projeto. Ferramenta low-code e otima para conectar
sistemas e pessima para guardar regra de negocio: logica dentro de nos do n8n
nao tem teste, nao tem code review e nao tem historico. Aqui a regra vive em
`core/classificacao.py`, coberta por testes, e o n8n so orquestra.

---

## Como a classificacao funciona

Tres decisoes independentes, todas em `core/classificacao.py`:

| Saida | Regra |
|---|---|
| `categoria` | `suporte` se a mensagem cita erro/problema; `comercial` se cita orcamento/preco; senao `geral` |
| `urgencia` | `alta` se cita urgente/hoje/parou; senao `normal` |
| `score` | 0 a 100, somando origem do lead, tamanho da mensagem, presenca de telefone e urgencia |

Suporte tem prioridade sobre comercial: quem escreve "deu erro ao pagar, qual
o valor?" tem um problema, nao uma duvida de preco.

Sao funcoes puras — recebem texto, devolvem valor, sem banco e sem rede. Por
isso os testes rodam em milissegundos e sem infraestrutura.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Framework | Django 5 + Django REST Framework |
| Orquestracao | n8n |
| Banco | PostgreSQL 16 |
| Containers | Docker + Docker Compose |
| Testes | pytest |
| CI | GitHub Actions |

---

## Como rodar

```bash
cp .env.example .env
docker compose up --build
```

Em outro terminal:

```bash
docker compose exec api python manage.py migrate
```

- API: `http://localhost:8000`
- n8n: `http://localhost:5678`

Para montar o fluxo no n8n, siga [`n8n/README.md`](n8n/README.md).

---

## Endpoints

| Metodo | Rota | Descricao |
|---|---|---|
| `POST` | `/classificar` | Recebe o lead, classifica, grava e devolve o resultado |
| `GET` | `/leads` | Lista os leads recebidos, ordenados por score |

### Exemplo

Dois leads, duas triagens

Mesma rota, mensagens diferentes — e o sistema decide sozinho:

**Entrada A**

```json
{
  "nome": "Ana Souza",
  "email": "ana@empresa.com",
  "mensagem": "O sistema parou e preciso resolver hoje. Ligar (21) 99999-8888",
  "origem": "indicacao"
}
```

**Entrada B**

```json
{
  "nome": "Carlos Lima",
  "email": "carlos@empresa.com",
  "mensagem": "Gostaria de saber o valor dos planos",
  "origem": "instagram"
}
```

**Resultado**

| | Ana | Carlos |
|---|---|---|
| categoria | `suporte` | `comercial` |
| urgencia | `alta` | `normal` |
| score | `80` | `20` |
| destino no n8n | alerta imediato | fila normal |

A diferenca de 60 pontos nao e arbitraria. O score da Ana soma quatro
criterios:

| Criterio | Pontos |
|---|---|
| origem `indicacao` | 30 |
| mensagem de 62 caracteres | 10 |
| telefone na mensagem | 20 |
| urgencia alta | 20 |
| **total** | **80** |

Carlos e um lead legitimo — 10 pela origem e 10 pelo tamanho da mensagem —
mas pode esperar. E exatamente essa decisao que hoje alguem toma lendo
e-mail a e-mail.

---

## Testes

```bash
docker compose exec api pytest -v
```

Cobrem as tres decisoes da classificacao, incluindo os casos de borda:
mensagem com palavras das duas categorias, acentuacao, e o teto do score.

O CI executa a suite a cada push.

---

## Licenca

MIT

## Autor

Lucas Moura
