---
title: Início Rápido do SDK Python digna 2026.06 | Documentação digna
description: Guia de início rápido do SDK Python digna versão 2026.06
image: /assets/logo_square.png
---

# Início Rápido do SDK Python digna 2026.06

Esta página mostra a configuração mínima e os principais fluxos de trabalho do cliente do SDK Python do ***digna***. Use-a como ponto de partida antes de avançar para as páginas de referência de recursos, modelos e erros.

## Criar uma Chave de API

Crie uma chave de API no frontend do ***digna*** antes de se conectar com o SDK:

1. Faça login no ***digna*** pelo frontend.
2. Abra seu perfil de usuário no canto inferior esquerdo.
3. No perfil de usuário, clique em **API Keys**.
4. Clique em **Add API Key**.
5. Informe um nome significativo e defina uma data de expiração. Você pode revogar ou excluir uma chave de API a qualquer momento.
6. Copie a chave de API exibida para a área de transferência. A chave é mostrada apenas no momento da criação.

Use a chave de API como token do SDK. Boas maneiras de fornecê-la ao seu aplicativo incluem:

- Uma variável de ambiente, por exemplo `DIGNA_API_KEY`, para desenvolvimento local e automação.
- O cofre de segredos do seu CI/CD, como os segredos do GitHub Actions, as variáveis de CI/CD do GitLab ou as variáveis secretas do Azure DevOps.
- Um gerenciador de segredos em tempo de execução, como os segredos do Kubernetes, os segredos do Docker, o HashiCorp Vault ou o cofre de segredos de um provedor de nuvem.

Evite escrever chaves de API diretamente no código-fonte, em notebooks, no histórico do shell ou em arquivos de configuração versionados.

## Conectar

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Use `DignaClient` como gerenciador de contexto para que o pool de conexões
subjacente seja fechado automaticamente:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Listar Projetos

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Criar uma Fonte de Dados

```python
from digna_sdk.models import (
    DataSourceModules,
    DataSourceObject,
    StableDataSourceKind,
    StableDataSourceQueryMode,
)

data_source = client.data_sources.create(
    project_id=1,
    db_connection_id=10,
    name="orders_table",
    kind=StableDataSourceKind.TABLE,
    query_mode=StableDataSourceQueryMode.SINGLE,
    object=DataSourceObject(catalog_name="prod", schema_name="public", table_name="orders"),
    modules=DataSourceModules(
        data_analytics=True,
        data_anomaly=True,
        data_validation=True,
        schema_tracker=False,
        timeliness=False,
    ),
)
```

## Enviar uma Solicitação de Inspeção e Aguardar sua Conclusão

```python
import datetime
from digna_sdk import DignaInspectionRequestFailed
from digna_sdk.models import StableInspectionRequestMode

request = client.inspection_requests.submit(
    project_id=1,
    data_source_ids=[data_source.id],
    start_date=datetime.date(2026, 1, 1),
    end_date=datetime.date(2026, 1, 31),
    mode=StableInspectionRequestMode.DAILY,
)

try:
    client.inspection_requests.wait_until_finished(request.id, poll_interval=2.0, timeout=300.0)
except DignaInspectionRequestFailed as exc:
    print(f"Inspection failed: {exc.status.value}")

# Once finished, retrieve the resulting statuses.
statuses = client.inspection_statuses.for_data_sources(
    data_source_id=data_source.id,
    start_date=datetime.date(2026, 1, 1),
    end_date=datetime.date(2026, 1, 31),
)
```

Consulte `examples/inspection_flow.py` no repositório para ver o fluxo completo de envio → consulta → recuperação.

## Tratar Erros

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
