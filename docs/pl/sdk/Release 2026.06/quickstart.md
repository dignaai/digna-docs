---
title: Szybki start SDK Python digna 2026.06 | Dokumentacja digna
description: Przewodnik szybkiego startu dla SDK Python digna w wersji 2026.06
image: /assets/logo_square.png
---

# Szybki start SDK Python digna 2026.06

Ta strona pokazuje minimalną konfigurację i podstawowe scenariusze pracy z klientem SDK Python ***digna***. Potraktuj ją jako punkt wyjścia przed przejściem do stron referencyjnych o zasobach, modelach i błędach.

## Tworzenie klucza API

Przed połączeniem się z SDK utwórz klucz API w interfejsie ***digna***:

1. Zaloguj się do ***digna*** w interfejsie.
2. Otwórz profil użytkownika w lewym dolnym rogu.
3. W profilu użytkownika kliknij **API Keys**.
4. Kliknij **Add API Key**.
5. Podaj zrozumiałą nazwę i ustaw datę wygaśnięcia. Klucz API możesz w każdej chwili unieważnić lub usunąć.
6. Skopiuj wyświetlony klucz API do schowka. Klucz jest pokazywany tylko w momencie tworzenia.

Użyj klucza API jako tokenu SDK. Dobre sposoby przekazania go aplikacji to:

- Zmienna środowiskowa, na przykład `DIGNA_API_KEY`, do pracy lokalnej i automatyzacji.
- Magazyn sekretów w CI/CD, na przykład sekrety GitHub Actions, zmienne CI/CD w GitLab albo zmienne tajne Azure DevOps.
- Menedżer sekretów działający w czasie wykonania, na przykład sekrety Kubernetes, sekrety Docker, HashiCorp Vault albo magazyn sekretów dostawcy chmury.

Unikaj umieszczania kluczy API na stałe w kodzie źródłowym, notatnikach, historii powłoki oraz w plikach konfiguracyjnych trafiających do repozytorium.

## Połączenie

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Używaj `DignaClient` jako menedżera kontekstu, aby bazowa pula połączeń
zamykała się automatycznie:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Lista projektów

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Tworzenie źródła danych

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

## Wysłanie żądania inspekcji i oczekiwanie na jego zakończenie

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

Pełny przebieg wysłanie → odpytywanie → pobranie znajdziesz w pliku `examples/inspection_flow.py` w repozytorium.

## Obsługa błędów

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
