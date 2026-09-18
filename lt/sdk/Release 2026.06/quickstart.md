# digna Python SDK greitoji pradžia 2026.06

Šiame puslapyje pateikiama minimali ***digna*** Python SDK sąranka ir pagrindiniai kliento darbo eigos scenarijai. Pradėkite nuo jo, prieš pereidami prie išteklių, modelių ir klaidų žinyno puslapių.

## API rakto kūrimas

Prieš jungdamiesi su SDK, ***digna*** sąsajoje sukurkite API raktą:

1. Prisijunkite prie ***digna*** sąsajoje.
2. Apatiniame kairiajame kampe atverkite savo naudotojo profilį.
3. Naudotojo profilyje spustelėkite **API Keys**.
4. Spustelėkite **Add API Key**.
5. Nurodykite prasmingą pavadinimą ir nustatykite galiojimo pabaigos datą. API raktą bet kada galite atšaukti arba pašalinti.
6. Nukopijuokite parodytą API raktą į iškarpinę. Raktas rodomas tik jį sukūrus.

Naudokite API raktą kaip SDK prieigos raktą. Tinkami būdai jį perduoti programai:

- Aplinkos kintamasis, pavyzdžiui `DIGNA_API_KEY`, vietiniam kūrimui ir automatizavimui.
- Jūsų CI/CD paslapčių saugykla, pavyzdžiui, „GitHub Actions“ paslaptys, „GitLab“ CI/CD kintamieji arba „Azure DevOps“ slapti kintamieji.
- Vykdymo metu veikianti paslapčių tvarkyklė, pavyzdžiui, „Kubernetes“ paslaptys, „Docker“ paslaptys, „HashiCorp Vault“ arba debesijos tiekėjo paslapčių saugykla.

Venkite API raktus įrašyti tiesiai į pirminį kodą, užrašines, komandų eilutės istoriją ar į versijų valdymą įtrauktus konfigūracijos failus.

## Prisijungimas

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Naudokite `DignaClient` kaip konteksto tvarkyklę, kad pagrindinis
ryšių telkinys būtų užvertas automatiškai:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Projektų sąrašas

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Duomenų šaltinio kūrimas

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

## Tikrinimo užklausos pateikimas ir laukimas, kol ji bus baigta

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

Visą eigą pateikimas → apklausa → rezultatų gavimas rasite saugyklos faile `examples/inspection_flow.py`.

## Klaidų apdorojimas

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```