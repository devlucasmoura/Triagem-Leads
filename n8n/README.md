# Workflow do n8n

O fluxo tem 4 nos. Monte pela interface em http://localhost:5678 e, ao
terminar, exporte com `...` > `Download` e salve o JSON nesta pasta como
`workflow.json`.

## Nos

### 1. Webhook (gatilho)

- HTTP Method: `POST`
- Path: `lead`
- Respond: `Using Respond to Webhook node` ou `Immediately`

A URL de teste aparece no proprio no. E nela que o formulario do site
mandaria o lead.

### 2. HTTP Request (chama a API Python)

- Method: `POST`
- URL: `http://api:8000/classificar`
- Body Content Type: `JSON`
- Specify Body: `Using Fields Below` (ou JSON, mapeando os campos do webhook)

Campos: `nome`, `email`, `mensagem`, `origem`.

> Use `api:8000` e nao `localhost:8000`. Os dois rodam em containers
> diferentes e se enxergam pelo nome do servico no Compose.

### 3. IF (separa por urgencia)

- Condicao: `{{ $json.urgencia }}` igual a `alta`

### 4a. Telegram (ramo verdadeiro - urgente)

Mensagem sugerida:

```
LEAD URGENTE
{{ $json.nome }} ({{ $json.categoria }}) - score {{ $json.score }}
{{ $json.mensagem }}
```

### 4b. Telegram (ramo falso - normal)

Mesma ideia, sem o alarme.

## Credencial do Telegram

1. Fale com o @BotFather no Telegram e crie um bot (`/newbot`)
2. Copie o token
3. No n8n: Credentials > New > Telegram API > cole o token
4. Para descobrir seu chat_id, fale com o @userinfobot

## Trocando o canal de saida

Os nos 4a/4b podem ser trocados por Slack, Google Sheets ou Send Email sem
mudar uma linha de Python. E esse o ponto do projeto: a regra de negocio
fica versionada e testada na API; a integracao fica no n8n.
