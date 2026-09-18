---
title: Pornire rapidă SDK Python digna 2026.06 | Documentație digna
description: Ghid de pornire rapidă pentru versiunea 2026.06 a SDK-ului Python digna
image: /assets/logo_square.png
---

# Pornire rapidă SDK Python digna 2026.06

Această pagină prezintă configurarea minimă și principalele fluxuri de lucru ale clientului pentru SDK-ul Python ***digna***. Folosiți-o ca punct de plecare înainte de a trece la paginile de referință despre resurse, modele și erori.

## Crearea unei chei API

Creați o cheie API în interfața ***digna*** înainte de a vă conecta cu SDK-ul:

1. Autentificați-vă în ***digna*** din interfață.
2. Deschideți profilul de utilizator din colțul din stânga jos.
3. În profilul de utilizator, faceți clic pe **API Keys**.
4. Faceți clic pe **Add API Key**.
5. Dați un nume sugestiv și stabiliți o dată de expirare. Puteți revoca sau șterge oricând o cheie API.
6. Copiați cheia API afișată în clipboard. Cheia este afișată doar la crearea ei.

Folosiți cheia API drept token al SDK-ului. Modalități bune de a o furniza aplicației:

- O variabilă de mediu, de exemplu `DIGNA_API_KEY`, pentru dezvoltare locală și automatizare.
- Depozitul de secrete din CI/CD, precum secretele GitHub Actions, variabilele CI/CD din GitLab sau variabilele secrete din Azure DevOps.
- Un manager de secrete la rulare, precum secretele Kubernetes, secretele Docker, HashiCorp Vault sau depozitul de secrete al unui furnizor de cloud.

Evitați să scrieți chei API direct în codul sursă, în notebook-uri, în istoricul shell-ului sau în fișierele de configurare adăugate în sistemul de versionare.

## Conectarea

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Folosiți `DignaClient` ca manager de context pentru ca grupul de conexiuni
subiacent să fie închis automat:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Listarea proiectelor

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Crearea unei surse de date

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

## Trimiterea unei cereri de inspecție și așteptarea finalizării

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

Pentru fluxul complet trimitere → interogare → preluare, consultați `examples/inspection_flow.py` din depozit.

## Tratarea erorilor

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
