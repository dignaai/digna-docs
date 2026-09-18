---
title: digna Python SDK-snabbstart 2026.06 | digna Dokumentation
description: Snabbstartsguide för digna Python SDK-release 2026.06
image: /assets/logo_square.png
---

# digna Python SDK-snabbstart 2026.06

Den här sidan visar den minimala konfigurationen och de centrala klientflödena för ***digna*** Python SDK. Använd den som utgångspunkt innan du går vidare till referenssidorna om resurser, modeller och fel.

## Skapa en API-nyckel

Skapa en API-nyckel i ***digna***-gränssnittet innan du ansluter med SDK:t:

1. Logga in i ***digna*** i gränssnittet.
2. Öppna din användarprofil längst ned till vänster.
3. Klicka på **API Keys** i användarprofilen.
4. Klicka på **Add API Key**.
5. Ange ett tydligt namn och sätt ett utgångsdatum. Du kan när som helst återkalla eller ta bort en API-nyckel.
6. Kopiera den visade API-nyckeln till urklipp. Nyckeln visas bara när den skapas.

Använd API-nyckeln som SDK-token. Bra sätt att göra den tillgänglig för din applikation:

- En miljövariabel, till exempel `DIGNA_API_KEY`, för lokal utveckling och automatisering.
- Ditt CI/CD-hemlighetsarkiv, som GitHub Actions-secrets, GitLab CI/CD-variabler eller hemliga variabler i Azure DevOps.
- En hemlighetshanterare i körtid, som Kubernetes-secrets, Docker-secrets, HashiCorp Vault eller en molnleverantörs hemlighetsarkiv.

Undvik att hårdkoda API-nycklar i källkod, notebooks, shell-historik eller incheckade konfigurationsfiler.

## Anslut

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Använd `DignaClient` som kontexthanterare så att den underliggande
anslutningspoolen stängs automatiskt:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Lista projekt

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Skapa en datakälla

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

## Skicka en inspektionsbegäran och vänta tills den är klar

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

Se `examples/inspection_flow.py` i repot för hela flödet skicka → polla → hämta.

## Hantera fel

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
