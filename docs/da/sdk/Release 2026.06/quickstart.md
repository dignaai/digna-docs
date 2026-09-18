---
title: digna Python SDK – hurtig start 2026.06 | digna-dokumentation
description: Vejledning til hurtig start med digna Python SDK-udgivelse 2026.06
image: /assets/logo_square.png
---

# digna Python SDK – hurtig start 2026.06

Denne side viser den minimale opsætning og de centrale klientarbejdsgange for ***digna*** Python SDK. Brug den som udgangspunkt, før du går videre til referencesiderne om ressourcer, modeller og fejl.

## Opret en API-nøgle

Opret en API-nøgle i ***digna***-brugerfladen, før du opretter forbindelse med SDK'et:

1. Log ind på ***digna*** i brugerfladen.
2. Åbn din brugerprofil nederst til venstre.
3. Klik på **API Keys** i brugerprofilen.
4. Klik på **Add API Key**.
5. Angiv et sigende navn, og fastsæt en udløbsdato. Du kan til enhver tid tilbagekalde eller slette en API-nøgle.
6. Kopier den viste API-nøgle til udklipsholderen. Nøglen vises kun, når den oprettes.

Brug API-nøglen som SDK-token. Gode måder at give den videre til din applikation på:

- En miljøvariabel, for eksempel `DIGNA_API_KEY`, til lokal udvikling og automatisering.
- Dit CI/CD-hemmelighedslager, såsom GitHub Actions-secrets, GitLab CI/CD-variabler eller hemmelige variabler i Azure DevOps.
- En hemmelighedsmanager i kørselstid, såsom Kubernetes-secrets, Docker-secrets, HashiCorp Vault eller en cloududbyders hemmelighedslager.

Undgå at hardkode API-nøgler i kildekode, notebooks, shell-historik eller versionsstyrede konfigurationsfiler.

## Opret forbindelse

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Brug `DignaClient` som kontekstmanager, så den underliggende
forbindelsespulje lukkes automatisk:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Vis projekter

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Opret en datakilde

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

## Send en inspektionsanmodning, og vent på, at den bliver færdig

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

Se `examples/inspection_flow.py` i repositoriet for hele forløbet send → poll → hent.

## Håndter fejl

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
