---
title: Visão Geral da API REST 2026.11 | Documentação digna
description: Use a API REST v1 do digna para ler projetos e resultados de inspeção, gerenciar fontes de dados, conjuntos de dados e atributos e iniciar inspeções — URL base, autenticação por chave de API, paginação, erros e o documento OpenAPI.
image: /assets/logo_square.png
keywords: API REST do digna, API do digna, OpenAPI do digna, chave de API do digna, API de solicitações de inspeção, API de qualidade de dados, Swagger UI
---

# API REST do digna 2026.11

A API REST do *digna* permite que suas próprias ferramentas e pipelines trabalhem com o *digna* por
HTTP e JSON: ler projetos e resultados de inspeção, gerenciar fontes de dados, conjuntos de dados e
atributos e iniciar inspeções, por exemplo ao final de uma carga de dados. O [Python SDK](../../sdk/Release%202026.11/index.md)
usa a mesma API.

Esta página descreve o que todas as solicitações têm em comum. As páginas de recursos listam cada
endpoint com seus parâmetros, corpo da solicitação, respostas e esquemas:

| Recurso | Endpoints |
|---|---|
| [Projects](projects.md) | Ler projetos |
| [DB Connections](db_connections.md) | Ler conexões de banco de dados |
| [Data Sources](data_sources.md) | Criar, ler, atualizar e excluir fontes de dados |
| [Data Sets](data_sets.md) | Criar, ler, atualizar e excluir conjuntos de dados |
| [Attributes](attributes.md) | Criar, ler, atualizar e excluir atributos |
| [Check Definitions](check_definitions.md) | Ler definições de verificação |
| [Inspection Requests](inspection_requests.md) | Iniciar inspeções e acompanhar seu progresso |
| [Inspection Statuses](inspection_statuses.md) | Ler resultados de inspeção por projeto, fonte de dados e conjunto de dados |

---

## URL Base {: #base-url }

A API faz parte do backend do *digna*. Todo caminho começa com `/v1`, depois do endereço do backend:

```text
https://digna.example.com/v1/projects
```

O endereço do backend é o mesmo que o dashboard usa: `baseUrl` na seção `[api]` de
`dashboard/dashboard_config.toml`. Use HTTPS sempre que o chamador e o *digna* não estiverem na mesma
máquina, porque toda solicitação carrega uma chave de API.

---

## Autenticação {: #authentication }

Toda solicitação envia a chave de API de um usuário do *digna* no cabeçalho `Authorization`:

```text
Authorization: Bearer <api key>
```

Para criar uma chave, abra seu perfil de usuário no canto inferior esquerdo do dashboard, clique em
**API Keys** e depois em **Add API Key**, e copie a chave. Ela é exibida apenas uma vez. As mesmas
chaves funcionam para o [digna MCP Server](../../ai_agents/overview.md).

Uma solicitação é executada com as permissões do usuário da chave. Criar, alterar e excluir exige a
função de editor no projeto; caso contrário, a solicitação é recusada com `403` e a mensagem
`You don't have permission to edit this project`.

!!! tip "Use um usuário dedicado para automação"

    Crie um usuário do *digna* para cada integração, dê a ele apenas os projetos e funções de que
    precisa e crie a chave dele com uma data de expiração. Assim, você pode revogar o acesso de uma
    integração excluindo a chave dela, sem afetar mais ninguém.

---

## Fazendo uma Solicitação {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

As respostas são em JSON. Listas são retornadas como um array JSON. Os corpos das solicitações também
são em JSON, enviados com `Content-Type: application/json`.

---

## Limites e Filtros {: #limits-and-filters }

Endpoints de listagem retornam no máximo `limit` itens: 200 por padrão e até 5000. Um valor fora desse
intervalo é rejeitado com `400`. Não há offset nem token de página, então restrinja uma lista com os
filtros dela, por exemplo `project_id`, `data_source_id`, ou `start_date` e `end_date` nos status de
inspeção.

Uma solicitação que demora mais de 60 segundos é cancelada com `408 Request Timeout`.

---

## Erros {: #errors }

Uma resposta de erro tem um corpo JSON com um código e uma mensagem:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Status | Código | Significado |
|---|---|---|
| `400` | `BAD_REQUEST` | A solicitação é inválida, por exemplo um `limit` fora do intervalo |
| `401` | `NOT_AUTHENTICATED` | A chave de API está ausente, malformada, é desconhecida ou expirou |
| `403` | `NOT_AUTHORIZED` | O usuário da chave não tem a função exigida por esta solicitação |
| `403` | `INVALID_LICENSE` | A licença do *digna* expirou |
| `404` | `NOT_FOUND` | O projeto, a fonte de dados ou outro item não existe |
| `500` | `INTERNAL_ERROR` | Um erro inesperado no *digna*. O log do backend tem os detalhes |

A `message` de uma resposta `401` informa o que há de errado com a chave:

| Mensagem | Causa |
|---|---|
| `Missing Authorization header` | Nenhum cabeçalho `Authorization` foi enviado |
| `Invalid Authorization header format` | O valor não começa com `Bearer ` |
| `Invalid API key` | A chave está errada ou foi excluída |
| `API key expired` | A chave expirou. Crie uma nova |

---

## Executando uma Inspeção {: #running-an-inspection }

Uma integração típica inicia uma inspeção quando uma carga de dados termina, aguarda sua conclusão e
lê o resultado:

1. **Inicie a inspeção** com [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   A resposta contém o `id` da solicitação.
2. **Acompanhe o progresso** com [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   O `status` passa de `PENDING` por `RUNNING` até `COMPLETED`, ou termina como `FAILED`,
   `ABORTED` ou `CANCELLED`. Consulte novamente a cada poucos segundos até que ele não mude mais.
3. **Leia o resultado** com [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   para as datas inspecionadas. Cada item tem um `status` geral: `0` (OK), `1` (aviso),
   `2` (crítico) ou `-1` (sem status), e um status por módulo com o número de verificações aprovadas,
   incertas e com falha.

```bash
curl -X POST https://digna.example.com/v1/inspection-requests \
  -H "Authorization: Bearer $DIGNA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "project_id": 1,
    "include_all_data_sources": true,
    "data_source_ids": [],
    "start_date": "2026-11-06",
    "end_date": "2026-11-06",
    "mode": "DAILY",
    "weekly_mode_weekdays": [],
    "monthly_mode_days": [],
    "use_notification": true
  }'
```

---

## Documento OpenAPI {: #openapi-document }

Toda instalação do *digna* descreve esta API em um documento OpenAPI 3.1 e oferece uma Swagger UI
interativa para testar solicitações com ela:

| O quê | Endereço |
|---|---|
| Documento OpenAPI | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

O documento do Release 2026.11 também está disponível aqui: [openapi.json](openapi.json). Use-o para
gerar um cliente em outra linguagem.

!!! note "Somente os endpoints /v1 são cobertos"

    O dashboard também se comunica com o backend por outros endpoints internos. Eles não fazem parte
    desta API e podem mudar em qualquer versão, então construa integrações apenas sobre os endpoints
    `/v1`.
