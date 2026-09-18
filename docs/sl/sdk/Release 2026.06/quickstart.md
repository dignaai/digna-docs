---
title: Hitri začetek SDK Python digna 2026.06 | Dokumentacija digna
description: Vodnik za hitri začetek z izdajo SDK Python digna 2026.06
image: /assets/logo_square.png
---

# Hitri začetek SDK Python digna 2026.06

Ta stran prikazuje najmanjšo potrebno nastavitev in osrednje delovne tokove odjemalca za SDK Python ***digna***. Uporabite jo kot izhodišče, preden nadaljujete na referenčne strani o virih, modelih in napakah.

## Ustvarjanje ključa API

Preden se povežete s SDK, v vmesniku ***digna*** ustvarite ključ API:

1. Prijavite se v ***digna*** v vmesniku.
2. V spodnjem levem kotu odprite svoj uporabniški profil.
3. V uporabniškem profilu kliknite **API Keys**.
4. Kliknite **Add API Key**.
5. Vnesite razumljivo ime in nastavite datum poteka. Ključ API lahko kadar koli prekličete ali izbrišete.
6. Prikazani ključ API kopirajte v odložišče. Ključ je prikazan samo ob ustvarjanju.

Ključ API uporabite kot žeton SDK. Primerni načini, kako ga posredovati aplikaciji:

- Spremenljivka okolja, na primer `DIGNA_API_KEY`, za lokalni razvoj in avtomatizacijo.
- Shramba skrivnosti vašega CI/CD, na primer skrivnosti GitHub Actions, spremenljivke CI/CD v GitLabu ali skrite spremenljivke v Azure DevOps.
- Upravitelj skrivnosti med izvajanjem, na primer skrivnosti Kubernetes, skrivnosti Docker, HashiCorp Vault ali shramba skrivnosti ponudnika oblaka.

Ključev API ne vpisujte neposredno v izvorno kodo, beležnice, zgodovino lupine ali konfiguracijske datoteke, ki so v sistemu za upravljanje različic.

## Povezovanje

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Uporabite `DignaClient` kot upravitelja konteksta, da se osnovni
nabor povezav samodejno zapre:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Izpis projektov

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Ustvarjanje vira podatkov

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

## Oddaja zahteve za pregled in čakanje na zaključek

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

Celoten potek oddaja → poizvedovanje → prevzem je prikazan v datoteki `examples/inspection_flow.py` v repozitoriju.

## Obravnavanje napak

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
