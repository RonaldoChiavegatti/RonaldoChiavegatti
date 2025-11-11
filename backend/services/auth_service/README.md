# Serviço de Autenticação (`auth_service`)

Este serviço é responsável por todas as operações relacionadas à autenticação e gerenciamento de usuários.

## Responsabilidades

- **Registro de Usuários:** Permite que novos usuários se registrem no sistema.
- **Autenticação:** Verifica as credenciais do usuário e emite um token de acesso (JWT).
- **Gerenciamento de Senhas:** Armazena senhas de forma segura usando hashing.

## API Endpoints

A base da URL para este serviço é `/auth`.

### `POST /register`

Registra um novo usuário no sistema.

- **Request Body:**
  ```json
  {
    "full_name": "string",
    "email": "user@example.com",
    "password": "string"
  }
  ```

- **Response (201 CREATED):**
  ```json
  {
    "id": "uuid",
    "full_name": "string",
    "email": "user@example.com"
  }
  ```

- **Possíveis Erros:**
  - `409 CONFLICT`: Se o email já estiver em uso.
  - `500 INTERNAL SERVER ERROR`: Erro interno no servidor.

### `POST /login`

Autentica um usuário e retorna um token de acesso.

- **Request Body (form-data):**
  - `username`: O email do usuário.
  - `password`: A senha do usuário.

- **Response (200 OK):**
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

- **Possíveis Erros:**
  - `401 UNAUTHORIZED`: Credenciais inválidas.
  - `500 INTERNAL SERVER ERROR`: Erro interno no servidor.

## Dependências

As principais dependências deste serviço são:

- `fastapi`: Para a criação da API.
- `pydantic`: Para validação de dados.
- `passlib`: Para hashing de senhas.
- `python-jose`: Para a criação e validação de tokens JWT.
- `psycopg2-binary`: Driver do PostgreSQL.

## Variáveis de Ambiente

Estas são as variáveis de ambiente necessárias para configurar o serviço:

- `DATABASE_URL`: URL de conexão com o banco de dados PostgreSQL. Ex: `postgresql://user:password@host:port/database`
- `SECRET_KEY`: Chave secreta para assinar os tokens JWT.
- `ALGORITHM`: Algoritmo de assinatura do JWT (padrão: `HS256`).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tempo de expiração do token de acesso em minutos (padrão: `30`).
