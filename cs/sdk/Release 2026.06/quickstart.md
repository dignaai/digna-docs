# Rychlý start digna Python SDK 2026.06

Tato stránka ukazuje minimální nastavení a základní pracovní postupy klienta Python SDK ***digna***. Použijte ji jako výchozí bod, než přejdete na referenční stránky o zdrojích, modelech a chybách.

## Vytvoření klíče API

Před připojením pomocí SDK vytvořte v rozhraní ***digna*** klíč API:

1. Přihlaste se do ***digna*** v rozhraní.
2. V levém dolním rohu otevřete svůj uživatelský profil.
3. V uživatelském profilu klikněte na **API Keys**.
4. Klikněte na **Add API Key**.
5. Zadejte srozumitelný název a nastavte datum vypršení platnosti. Klíč API můžete kdykoli odvolat nebo smazat.
6. Zkopírujte zobrazený klíč API do schránky. Klíč se zobrazí pouze při vytvoření.

Použijte klíč API jako token SDK. Vhodné způsoby, jak jej předat aplikaci:

- Proměnná prostředí, například `DIGNA_API_KEY`, pro lokální vývoj a automatizaci.
- Úložiště tajemství vašeho CI/CD, například tajemství GitHub Actions, proměnné CI/CD v GitLabu nebo tajné proměnné Azure DevOps.
- Správce tajemství za běhu, například tajemství Kubernetes, tajemství Dockeru, HashiCorp Vault nebo úložiště tajemství poskytovatele cloudu.

Nezapisujte klíče API napevno do zdrojového kódu, notebooků, historie shellu ani do konfiguračních souborů uložených ve verzovacím systému.

## Připojení

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Používejte `DignaClient` jako kontextový manažer, aby se podkladový
fond připojení zavíral automaticky:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Výpis projektů

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Vytvoření zdroje dat

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

## Odeslání požadavku na kontrolu a čekání na jeho dokončení

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

Kompletní postup odeslání → dotazování → načtení najdete v souboru `examples/inspection_flow.py` v repozitáři.

## Zpracování chyb

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```