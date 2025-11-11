# Arquitetura do Sistema

Este documento descreve em detalhes a arquitetura do sistema, os padrões utilizados e as decisões de design.

## Padrão de Arquitetura: Microserviços e Arquitetura Hexagonal

O sistema utiliza uma combinação de dois padrões de arquitetura principais:

- **Microserviços:** O sistema é dividido em serviços independentes, cada um com sua própria responsabilidade, banco de dados e ciclo de vida. Isso permite o desenvolvimento, implantação e escalonamento independentes de cada serviço.

- **Arquitetura Hexagonal (Portas e Adaptadores):** Cada serviço é estruturado internamente seguindo a Arquitetura Hexagonal. Isso significa que o núcleo da aplicação (domínio e lógica de negócio) é isolado das dependências externas (como banco de dados, APIs externas, etc.) através de "portas" e "adaptadores".

  - **Portas (`ports`):** Definem a interface de comunicação com o núcleo da aplicação. Existem portas de entrada (para serem chamadas por drivers como a API web) e portas de saída (para interagir com sistemas externos como bancos de dados).

  - **Adaptadores (`adapters`):** Implementam a lógica de comunicação com sistemas externos. Por exemplo, um adaptador de persistência para PostgreSQL implementa a porta de repositório.

## Componentes

O diagrama abaixo ilustra a interação entre os principais componentes do sistema:

```
[Frontend] -> [API Gateway (Nginx)] -> [Serviços de Backend]
                                          |
                                          +-> [Serviço de Autenticação]
                                          |   |-> [PostgreSQL (auth_db)]
                                          |
                                          +-> [Serviço de Orquestração de Agentes]
                                          |   |-> [PostgreSQL (agent_db)]
                                          |
                                          +-> [Serviço de Faturamento]
                                          |   |-> [PostgreSQL (billing_db)]
                                          |
                                          +-> [Serviço de Documentos]
                                              |-> [PostgreSQL (document_db)]
                                              |-> [Redis (Fila de Processamento)]
                                              |-> [Minio (Armazenamento de Arquivos)]
```

### API Gateway

O API Gateway, implementado com Nginx, serve como um ponto de entrada único para todas as requisições externas. Ele é responsável por:

- **Roteamento:** Encaminhar as requisições para o serviço de backend apropriado com base na URL.
- **Segurança:** Pode ser configurado para lidar com SSL, CORS e outras políticas de segurança.
- **Load Balancing:** Distribuir a carga entre múltiplas instâncias de um serviço.

### Serviços de Backend

Cada serviço é uma aplicação Python com FastAPI, seguindo a estrutura da Arquitetura Hexagonal:

- **`application/domain`:** Contém os modelos de domínio e a lógica de negócio pura.
- **`application/ports/input`:** Define as interfaces (casos de uso) que a aplicação expõe.
- **`application/ports/output`:** Define as interfaces para interagir com sistemas externos (banco de dados, serviços de terceiros, etc.).
- **`application/services`:** Implementa os casos de uso definidos nas portas de entrada.
- **`infrastructure/adapters`:** Implementa os adaptadores para as portas de saída (ex: repositórios de banco de dados, clientes HTTP para outros serviços).
- **`infrastructure/web`:** Expõe a API REST usando FastAPI, que por sua vez chama os serviços da aplicação.

### Banco de Dados

Cada serviço possui seu próprio banco de dados PostgreSQL, garantindo o isolamento dos dados. As migrações e o esquema inicial do banco de dados são gerenciados através de scripts SQL.

### Mensageria e Cache

O Redis é utilizado para duas finalidades principais:

- **Fila de Mensagens:** No `document_service`, o Redis é usado como uma fila para processamento assíncrono de documentos. A API web publica uma mensagem na fila, e um `worker` consome a mensagem para processar o documento.
- **Cache:** Pode ser utilizado para armazenar em cache dados frequentemente acessados, reduzindo a carga no banco de dados.

### Armazenamento de Arquivos

O Minio, um serviço de armazenamento de objetos compatível com a API do Amazon S3, é usado para armazenar os arquivos enviados para o `document_service`.

## Fluxo de Dados

Um exemplo de fluxo de dados para o upload de um documento seria:

1. O usuário envia um arquivo para o `document_service` através do API Gateway.
2. A API do `document_service` recebe a requisição, salva o arquivo no Minio e cria um registro de `DocumentJob` no banco de dados com o status "pendente".
3. A API publica uma mensagem no Redis com o ID do `DocumentJob`.
4. O `document-worker` consome a mensagem da fila.
5. O worker recupera as informações do `DocumentJob` do banco de dados.
6. O worker baixa o arquivo do Minio, o processa (ex: extrai o texto com OCR) e atualiza o status do `DocumentJob` no banco de dados para "concluído".
