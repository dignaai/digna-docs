# digna Python SDK ātrais sākums 2026.06

Šajā lappusē ir parādīta ***digna*** Python SDK minimālā iestatīšana un klienta galvenās darbplūsmas. Izmantojiet to kā sākumpunktu, pirms pārejat uz resursu, modeļu un kļūdu rokasgrāmatas lappusēm.

## API atslēgas izveide

Pirms savienojuma izveides ar SDK izveidojiet API atslēgu ***digna*** saskarnē:

1. Pieteicieties ***digna*** saskarnē.
2. Atveriet savu lietotāja profilu apakšējā kreisajā stūrī.
3. Lietotāja profilā noklikšķiniet uz **API Keys**.
4. Noklikšķiniet uz **Add API Key**.
5. Norādiet saprotamu nosaukumu un iestatiet derīguma termiņu. API atslēgu jebkurā brīdī var atsaukt vai dzēst.
6. Kopējiet parādīto API atslēgu starpliktuvē. Atslēga tiek rādīta tikai tās izveides brīdī.

Izmantojiet API atslēgu kā SDK pilnvaru. Piemēroti veidi, kā to nodot lietojumprogrammai:

- Vides mainīgais, piemēram, `DIGNA_API_KEY`, lokālai izstrādei un automatizācijai.
- Jūsu CI/CD noslēpumu krātuve, piemēram, GitHub Actions noslēpumi, GitLab CI/CD mainīgie vai Azure DevOps slepenie mainīgie.
- Izpildlaika noslēpumu pārvaldnieks, piemēram, Kubernetes noslēpumi, Docker noslēpumi, HashiCorp Vault vai mākoņpakalpojumu sniedzēja noslēpumu krātuve.

Neierakstiet API atslēgas tieši pirmkodā, piezīmju grāmatās, čaulas vēsturē vai versiju kontrolē iekļautos konfigurācijas failos.

## Savienojuma izveide

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Izmantojiet `DignaClient` kā konteksta pārvaldnieku, lai pamatā esošais
savienojumu kopums tiktu aizvērts automātiski:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Projektu uzskaitīšana

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Datu avota izveide

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

## Pārbaudes pieprasījuma iesniegšana un gaidīšana, līdz tas pabeigts

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

Pilnu gaitu iesniegšana → aptauja → rezultātu saņemšana skatiet krātuves failā `examples/inspection_flow.py`.

## Kļūdu apstrāde

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```