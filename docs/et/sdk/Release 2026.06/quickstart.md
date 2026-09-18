---
title: digna Python SDK kiirjuhend 2026.06 | digna dokumentatsioon
description: Kiirjuhend digna Python SDK versiooni 2026.06 jaoks
image: /assets/logo_square.png
---

# digna Python SDK kiirjuhend 2026.06

See leht näitab ***digna*** Python SDK minimaalset seadistust ja kliendi peamisi töövooge. Kasuta seda lähtepunktina, enne kui liigud ressursside, mudelite ja vigade teatmikulehtedele.

## API võtme loomine

Loo ***digna*** kasutajaliideses API võti, enne kui SDK-ga ühenduse lood:

1. Logi kasutajaliideses ***digna*** sisse.
2. Ava vasakus alanurgas oma kasutajaprofiil.
3. Klõpsa kasutajaprofiilis valikul **API Keys**.
4. Klõpsa nupul **Add API Key**.
5. Anna sisukas nimi ja määra aegumiskuupäev. API võtme saab igal ajal tühistada või kustutada.
6. Kopeeri kuvatud API võti lõikelauale. Võtit näidatakse ainult loomise hetkel.

Kasuta API võtit SDK loana. Head viisid selle rakendusele edastamiseks:

- Keskkonnamuutuja, näiteks `DIGNA_API_KEY`, kohaliku arenduse ja automatiseerimise jaoks.
- CI/CD saladuste hoidla, näiteks GitHub Actionsi saladused, GitLabi CI/CD muutujad või Azure DevOpsi salamuutujad.
- Käitusaegne saladuste haldur, näiteks Kubernetese saladused, Dockeri saladused, HashiCorp Vault või pilveteenuse pakkuja saladuste hoidla.

Väldi API võtmete kirjutamist otse lähtekoodi, märkmikesse, käsuajalukku või versioonihaldusesse lisatud seadistusfailidesse.

## Ühenduse loomine

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Kasuta objekti `DignaClient` kontekstihaldurina, et aluseks olev
ühenduste kogum suletaks automaatselt:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Projektide loendamine

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Andmeallika loomine

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

## Kontrollipäringu esitamine ja selle lõppemise ootamine

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

Täielikku voogu esitamine → pärimine → tulemuste laadimine vaata failist `examples/inspection_flow.py` hoidlas.

## Vigade käsitlemine

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
