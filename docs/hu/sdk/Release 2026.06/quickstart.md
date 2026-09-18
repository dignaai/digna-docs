---
title: digna Python SDK gyors bevezető 2026.06 | digna dokumentáció
description: Gyors bevezető a digna Python SDK 2026.06 kiadásához
image: /assets/logo_square.png
---

# digna Python SDK gyors bevezető 2026.06

Ez az oldal a ***digna*** Python SDK minimális beállítását és a kliens legfontosabb munkafolyamatait mutatja be. Kiindulópontként használható, mielőtt az erőforrások, a modellek és a hibák referenciaoldalaira lépne.

## API-kulcs létrehozása

Hozzon létre egy API-kulcsot a ***digna*** felületén, mielőtt az SDK-val csatlakozna:

1. Jelentkezzen be a ***digna*** felületére.
2. Nyissa meg a felhasználói profilját a bal alsó sarokban.
3. A felhasználói profilban kattintson az **API Keys** elemre.
4. Kattintson az **Add API Key** gombra.
5. Adjon meg beszédes nevet, és állítson be lejárati dátumot. Az API-kulcs bármikor visszavonható vagy törölhető.
6. Másolja a megjelenített API-kulcsot a vágólapra. A kulcs csak a létrehozáskor látható.

Használja az API-kulcsot az SDK tokenjeként. Jó megoldások az alkalmazásnak való átadására:

- Környezeti változó, például `DIGNA_API_KEY`, helyi fejlesztéshez és automatizáláshoz.
- A CI/CD titkos tárolója, például GitHub Actions-titkok, GitLab CI/CD-változók vagy Azure DevOps titkos változók.
- Futásidejű titokkezelő, például Kubernetes-titkok, Docker-titkok, HashiCorp Vault vagy egy felhőszolgáltató titkos tárolója.

Kerülje az API-kulcsok beégetését a forráskódba, a notebookokba, a parancsértelmező előzményeibe vagy a verziókövetett konfigurációs fájlokba.

## Csatlakozás

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Használja a `DignaClient` osztályt környezetkezelőként, hogy a mögöttes
kapcsolatkészlet automatikusan lezáruljon:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Projektek listázása

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Adatforrás létrehozása

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

## Ellenőrzési kérés beküldése és a befejezés megvárása

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

A teljes beküldés → lekérdezés → letöltés folyamatot a tárolóban lévő `examples/inspection_flow.py` fájl mutatja be.

## Hibakezelés

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
