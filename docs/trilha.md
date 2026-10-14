# Trilha de Desenvolvimento — Webhook Proxy com FastAPI

## 01. CRUD de Webhooks

**Objetivo:** Criar a API para que os usuários possam cadastrar e gerenciar seus endpoints.

**Implementar:** FastAPI, PostgreSQL, SQLAlchemy 2.x, Alembic e Pydantic.

**Endpoints:**

- `POST /webhooks` — cadastrar um webhook.
- `GET /webhooks` — listar os webhooks.
- `GET /webhooks/{id}` — consultar um webhook.
- `PATCH /webhooks/{id}` — atualizar configurações.
- `DELETE /webhooks/{id}` — excluir um webhook.

**Critério de conclusão:** Os dados devem persistir no PostgreSQL, e todas as operações devem estar validadas e testadas.

## 02. Receber e Encaminhar Eventos

**Objetivo:** Implementar o fluxo principal do produto.

**Implementar:** Um endpoint que receba um JSON, consulte o webhook cadastrado e encaminhe o payload para a URL de destino usando um cliente HTTP assíncrono, como `httpx.AsyncClient`.

**Endpoint:**

`POST /webhooks/{id}/dispatch`

**Critério de conclusão:** Enviar um evento para a API e verificar que ele chega corretamente ao servidor de destino.

Nesta etapa, o processamento pode ocorrer diretamente na requisição, sem Redis.

## 03. Persistir Eventos e Entregas

**Objetivo:** Registrar o histórico de processamento e entrega dos eventos.

**Implementar:**

- Tabela `webhook_events` — eventos recebidos.
- Tabela `webhook_deliveries` — entregas realizadas ou pendentes para cada destino.
- Tabela `delivery_attempts` — histórico de tentativas de entrega.
- Estados de entrega, como `pending`, `processing`, `delivered` e `failed`.

**Critério de conclusão:** Conseguir consultar um evento, identificar para qual destino foi enviado e verificar se a entrega teve sucesso ou falhou.

## 04. Adicionar Autenticação HMAC

**Objetivo:** Garantir a autenticidade e a integridade das mensagens.

**Implementar:**

- Segredo por webhook.
- Assinatura HMAC-SHA256.
- Validação de timestamp para reduzir ataques de repetição (*replay attacks*).
- Comparação segura de assinaturas.
- Armazenamento protegido dos segredos.

**Critério de conclusão:** Uma assinatura válida deve ser aceita, enquanto uma assinatura inválida deve ser rejeitada.

Não é necessário implementar rotação sofisticada de chaves nesta etapa.

## 05. Implementar Retentativas Inteligentes

**Objetivo:** Evitar que falhas temporárias de rede causem a perda definitiva dos eventos.

**Implementar:**

- Backoff exponencial.
- Jitter para distribuir as retentativas.
- Limite máximo de tentativas.
- Timeouts configuráveis.
- Classificação de erros transitórios e permanentes.
- Registro do histórico de cada tentativa.

**Critério de conclusão:** Uma entrega que falha inicialmente deve poder ser realizada com sucesso em uma tentativa posterior, preservando o histórico de falhas.

## 06. Implementar Processamento Assíncrono com Redis

**Objetivo:** Desacoplar a entrega dos eventos do ciclo de vida das requisições HTTP.

**Implementar:**

- Redis.
- Uma biblioteca de filas compatível com `asyncio`.
- Workers assíncronos.
- Controle de concorrência.
- Agendamento de retentativas.
- Padrão Outbox no PostgreSQL.
- Processo de recuperação e reconciliação de tarefas pendentes.

**Critério de conclusão:** A API deve conseguir aceitar um evento e responder sem aguardar a conclusão da entrega HTTP ao destino.

A persistência no PostgreSQL deve permitir recuperar tarefas pendentes mesmo quando houver falhas na publicação ou no processamento das mensagens no Redis.

## 07. Auditoria, Observabilidade e Performance

**Objetivo:** Transformar o protótipo em um serviço confiável, monitorável e preparado para crescer.

**Implementar:**

- Logs estruturados.
- Métricas de latência, throughput e taxa de sucesso.
- Rastreamento por `event_id`.
- Logs de auditoria.
- Rate limiting.
- Proteção contra SSRF (*Server-Side Request Forgery*).
- Testes de carga.
- Política de retenção de dados.
- Recuperação de tarefas abandonadas.

**Critério de conclusão:** Conseguir medir a performance do sistema, acompanhar o ciclo de vida dos eventos e avaliar o comportamento da aplicação sob falhas e carga elevada.

---

## Ordem de execução

1. CRUD de webhooks.
2. Recebimento e encaminhamento de eventos.
3. Persistência de eventos e entregas.
4. Autenticação HMAC.
5. Retentativas inteligentes.
6. Processamento assíncrono com Redis.
7. Auditoria, observabilidade e otimização de performance.

**Princípio de desenvolvimento:** construir primeiro uma versão funcional e simples, evoluindo gradualmente a segurança, a confiabilidade e a escalabilidade. Cada etapa deve resultar em uma versão executável, testada e documentada.