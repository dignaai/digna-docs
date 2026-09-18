---
title: digna Python SDK Quickstart 2026.06 | digna Dokumentation
description: Quickstart-Anleitung für das digna Python SDK Release 2026.06
image: /assets/logo_square.png
---

# digna Python SDK Quickstart 2026.06

Diese Seite zeigt die minimale Einrichtung und die zentralen Client-Abläufe für das ***digna*** Python SDK. Nutzen Sie sie als Ausgangspunkt, bevor Sie zu den Referenzseiten zu Ressourcen, Modellen und Fehlern weitergehen.

## API-Schlüssel erstellen

Erstellen Sie im ***digna***-Frontend einen API-Schlüssel, bevor Sie sich mit dem SDK verbinden:

1. Melden Sie sich im Frontend bei ***digna*** an.
2. Öffnen Sie Ihr Benutzerprofil unten links.
3. Klicken Sie im Benutzerprofil auf **API Keys**.
4. Klicken Sie auf **Add API Key**.
5. Vergeben Sie einen aussagekräftigen Namen und legen Sie ein Ablaufdatum fest. Sie können einen API-Schlüssel jederzeit widerrufen oder löschen.
6. Kopieren Sie den angezeigten API-Schlüssel in die Zwischenablage. Der Schlüssel wird nur bei der Erstellung angezeigt.

Verwenden Sie den API-Schlüssel als SDK-Token. Bewährte Wege, ihn Ihrer Anwendung bereitzustellen:

- Eine Umgebungsvariable, zum Beispiel `DIGNA_API_KEY`, für lokale Entwicklung und Automatisierung.
- Ihr CI/CD-Secret-Store, etwa GitHub Actions Secrets, GitLab CI/CD-Variablen oder Azure DevOps Secret Variables.
- Ein Secret-Manager zur Laufzeit, etwa Kubernetes Secrets, Docker Secrets, HashiCorp Vault oder der Secret-Store eines Cloud-Anbieters.

Vermeiden Sie es, API-Schlüssel fest in Quellcode, Notebooks, Shell-Historie oder eingecheckte Konfigurationsdateien zu schreiben.

## Verbinden

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Verwenden Sie `DignaClient` als Context Manager, damit der zugrunde liegende
Connection Pool automatisch geschlossen wird:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Projekte auflisten

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Eine Datenquelle erstellen

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

## Eine Prüfanfrage absenden und auf ihren Abschluss warten

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

Den vollständigen Ablauf submit → poll → retrieve finden Sie in `examples/inspection_flow.py` im Repository.

## Fehler behandeln

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
