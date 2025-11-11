# Serviço de Orquestração de Agentes (`agent_orchestrator`)

Este serviço atua como o cérebro da aplicação, orquestrando as interações entre os usuários e os agentes de IA.

## Responsabilidades

- **Gerenciamento de Chat:** Processa as mensagens enviadas pelos usuários para os agentes de IA.
- **Histórico de Conversa:** Mantém o contexto da conversa para interações mais ricas.
- **Integração com LLM:** Comunica-se com o provedor de LLM (neste caso, Gemini) para gerar as respostas do agente.
- **Integração com Faturamento:** Antes de processar uma mensagem, verifica com o `billing_service` se o usuário possui saldo suficiente.

## API Endpoints

A base da URL para este serviço é `/` (através do API Gateway, o prefixo será `/agent`).

### `POST /chat`

Envia uma mensagem para um agente de IA e recebe uma resposta.

- **Header de Autenticação:**
  - `Authorization: Bearer <seu-token-jwt>`

- **Request Body:**
  ```json
  {
    "agent_id": "uuid",
    "user_message": "string",
    "conversation_history": [
      {
        "role": "user" | "assistant",
        "content": "string"
      }
    ]
  }
  ```

- **Response (200 OK):**
  ```json
  {
    "assistant_message": "string"
  }
  ```

- **Possíveis Erros:**
  - `401 UNAUTHORIZED`: Token de autenticação inválido ou ausente.
  - `402 PAYMENT_REQUIRED`: Saldo insuficiente.
  - `404 NOT_FOUND`: Agente não encontrado.
  - `500 INTERNAL SERVER ERROR`: Erro interno no servidor.

## Dependências

As principais dependências deste serviço são:

- `fastapi`: Para a criação da API.
- `pydantic`: Para validação de dados.
- `psycopg2-binary`: Driver do PostgreSQL.
- `google-generativeai`: Cliente para a API do Gemini.
- `requests`: Para comunicação com o `billing_service`.

## Variáveis de Ambiente

Estas são as variáveis de ambiente necessárias para configurar o serviço:

- `DATABASE_URL`: URL de conexão com o banco de dados PostgreSQL. Ex: `postgresql://user:password@host:port/database`
- `GEMINI_API_KEY`: Chave de API para o serviço Gemini.
- `BILLING_SERVICE_URL`: URL do serviço de faturamento. Ex: `http://billing-service:8004`
