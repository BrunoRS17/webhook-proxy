# Webhook Proxy

**Uma jornada de engenharia backend, de uma API simples a um serviço de entrega de eventos confiável.**

![Status: em construção](https://img.shields.io/badge/status-em_construção-yellow)
![Python](https://img.shields.io/badge/stack-Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Foco: backend](https://img.shields.io/badge/foco-Backend_Engineering-334155)

O **Webhook Proxy** é um projeto de backend em desenvolvimento, com a proposta de receber eventos via HTTP e encaminhá-los para endpoints cadastrados. A evolução do serviço explora desafios reais de integração entre sistemas: persistência, autenticidade das mensagens, falhas de rede, processamento assíncrono e rastreabilidade das entregas.

> **Projeto em andamento e construção.** A primeira versão é intencionalmente simples. A proposta é consolidar os fundamentos e aumentar gradualmente a complexidade, a segurança, a confiabilidade e a escalabilidade, seguindo a [trilha de desenvolvimento](docs/trilha.md).

## A proposta

Construir uma base pequena, compreensível e executável, evoluindo a arquitetura conforme novos problemas surgem. Cada etapa da trilha define um objetivo, as funcionalidades a implementar e um critério de conclusão.

O projeto serve como portfólio técnico e laboratório de aprendizado prático em **Python, desenvolvimento de APIs, integração de sistemas e arquitetura orientada a eventos**. O foco é demonstrar a evolução das decisões de engenharia, desde o fluxo HTTP inicial até os mecanismos de resiliência e operação do serviço.

## Estado atual

O repositório está na fase inicial de estruturação, anterior à conclusão da primeira etapa da trilha.

| Disponível hoje | Descrição |
| --- | --- |
| Aplicação FastAPI | Ponto de entrada em `app/main.py`, com metadados da API. |
| Endpoint de saúde | `GET /health` para uma verificação básica de resposta da aplicação. |
| Documentação automática | Swagger UI, ReDoc e schema OpenAPI fornecidos pelo FastAPI. |
| Dependências iniciais | Dependências Python declaradas em `requirements.txt`, incluindo FastAPI, Pydantic e SQLAlchemy. |
| Planejamento de evolução | Trilha incremental e diagrama inicial de banco de dados em `docs/`. |

O cadastro de webhooks, a persistência no banco e o encaminhamento de eventos ainda serão implementados. O endpoint de saúde atual verifica apenas a resposta da aplicação; não valida conexões com banco de dados ou outros serviços.

## Stack e conceitos técnicos

As tecnologias abaixo distinguem a base existente das próximas etapas de implementação.

| Camada | Tecnologias e conceitos | Situação |
| --- | --- | --- |
| API HTTP | **Python, FastAPI, ASGI, endpoint assíncrono, OpenAPI, Swagger UI** | Base implementada. |
| Contratos e validação | **Pydantic, schemas, validação de payloads, APIs REST** | Pydantic nas dependências; contratos de domínio previstos no CRUD. |
| Persistência | **PostgreSQL, SQLAlchemy, ORM, modelagem relacional, Alembic, migrations** | SQLAlchemy nas dependências; integração e migrações planejadas. |
| Integração HTTP | **HTTPX, `httpx.AsyncClient`, webhooks, encaminhamento de eventos** | Planejado. |
| Segurança | **HMAC-SHA256, integridade de mensagens, proteção contra replay, SSRF, rate limiting** | Planejado em etapas. |
| Resiliência | **Retries, exponential backoff, jitter, timeouts, histórico de tentativas** | Planejado. |
| Processamento assíncrono | **Redis, filas, workers, asyncio, controle de concorrência, padrão Outbox** | Planejado. |
| Observabilidade | **Logs estruturados, auditoria, rastreamento por evento, latência, throughput, testes de carga** | Planejado. |

## Fluxo proposto

```text
Sistema de origem → Webhook Proxy → Endpoint de destino
                          │
                          └─ Registro de eventos, entregas e tentativas
```

Inicialmente, o encaminhamento poderá ocorrer dentro da própria requisição HTTP. Nas etapas seguintes, a persistência dos eventos e o uso de filas e workers permitirão desacoplar o recebimento da entrega, controlar a concorrência e recuperar tarefas pendentes.

Essa evolução abre espaço para estudar **sistemas distribuídos, consistência entre banco e fila, tolerância a falhas e escalabilidade**, com implementação progressiva e critérios de validação definidos na trilha.

## Roadmap

- [ ] **01 · CRUD de webhooks** — cadastro e gerenciamento de destinos com PostgreSQL, SQLAlchemy, Alembic e validação com Pydantic.
- [ ] **02 · Recebimento e encaminhamento** — entrega de payloads JSON por meio de um cliente HTTP assíncrono.
- [ ] **03 · Histórico de processamento** — persistência de eventos, entregas, estados e tentativas.
- [ ] **04 · Autenticação HMAC** — assinatura HMAC-SHA256, validação de timestamp e proteção dos segredos.
- [ ] **05 · Retentativas inteligentes** — backoff exponencial, jitter, timeouts e classificação de falhas.
- [ ] **06 · Filas e workers** — Redis, controle de concorrência, padrão Outbox e recuperação de tarefas pendentes.
- [ ] **07 · Operação e performance** — auditoria, observabilidade, rate limiting, proteção contra SSRF e testes de carga.

A [trilha completa](docs/trilha.md) detalha o escopo e os critérios de conclusão de cada etapa. As funcionalidades de segurança e escala fazem parte desse planejamento; a base atual ainda não representa um serviço pronto para produção.

## Executando localmente

É necessário ter Python e `pip` disponíveis. A base atual pode ser executada sem PostgreSQL ou Redis, pois essas integrações ainda não foram implementadas.

Na raiz do projeto, crie e ative um ambiente virtual:

**Windows · PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências e o servidor ASGI:

```bash
python -m pip install -r requirements.txt
python -m pip install "uvicorn[standard]"
```

O Uvicorn é instalado separadamente porque ainda não consta em `requirements.txt`.

Inicie o servidor de desenvolvimento:

```bash
python -m uvicorn app.main:app --reload
```

| Recurso | Endereço local |
| --- | --- |
| Saúde da aplicação | [localhost:8000/health](http://localhost:8000/health) |
| Swagger UI | [localhost:8000/docs](http://localhost:8000/docs) |
| ReDoc | [localhost:8000/redoc](http://localhost:8000/redoc) |
| Schema OpenAPI | [localhost:8000/openapi.json](http://localhost:8000/openapi.json) |

## Estrutura do projeto

```text
webhook-proxy/
├── app/
│   └── main.py                   # Aplicação FastAPI e endpoint de saúde
├── docs/
│   ├── database/
│   │   └── modelo_v1.0.0.png      # Diagrama inicial do banco de dados
│   └── trilha.md                 # Etapas e critérios de desenvolvimento
├── .gitignore
├── README.md
└── requirements.txt
```

## Documentação

- [Trilha de desenvolvimento](docs/trilha.md) — sequência de implementação e critérios de conclusão.
- [Modelagem inicial do banco de dados](docs/database/modelo_v1.0.0.png) — referência visual para a evolução da persistência.

## Autor

Desenvolvido por **Bruno Ribeiro** como projeto de evolução prática em **Backend Engineering**, com foco em APIs, integrações, segurança, confiabilidade e escalabilidade.
