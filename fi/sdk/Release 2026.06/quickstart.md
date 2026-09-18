# digna Python SDK -pikaopas 2026.06

Tällä sivulla esitellään ***digna*** Python SDK:n vähimmäisasetukset ja keskeiset asiakasohjelman työnkulut. Käytä sitä lähtökohtana ennen siirtymistä resurssi-, malli- ja virhesivuille.

## Luo API-avain

Luo API-avain ***digna***-käyttöliittymässä ennen kuin yhdistät SDK:lla:

1. Kirjaudu ***digna***-käyttöliittymään.
2. Avaa käyttäjäprofiilisi vasemmasta alakulmasta.
3. Valitse käyttäjäprofiilissa **API Keys**.
4. Valitse **Add API Key**.
5. Anna kuvaava nimi ja aseta vanhenemispäivä. Voit mitätöidä tai poistaa API-avaimen milloin tahansa.
6. Kopioi näytetty API-avain leikepöydälle. Avain näytetään vain luontihetkellä.

Käytä API-avainta SDK:n tokenina. Hyviä tapoja välittää se sovellukselle ovat:

- Ympäristömuuttuja, esimerkiksi `DIGNA_API_KEY`, paikalliseen kehitykseen ja automaatioon.
- CI/CD-ympäristön salaisuusvarasto, kuten GitHub Actions -salaisuudet, GitLabin CI/CD-muuttujat tai Azure DevOpsin salaiset muuttujat.
- Ajonaikainen salaisuuksien hallinta, kuten Kubernetes-salaisuudet, Docker-salaisuudet, HashiCorp Vault tai pilvipalvelun salaisuusvarasto.

Vältä API-avainten kovakoodaamista lähdekoodiin, notebookeihin, komentotulkin historiaan tai versionhallintaan tallennettuihin asetustiedostoihin.

## Yhdistäminen

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Käytä `DignaClient`-oliota kontekstinhallintana, jolloin taustalla oleva
yhteysvaranto suljetaan automaattisesti:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Projektien listaaminen

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Tietolähteen luominen

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

## Tarkastuspyynnön lähettäminen ja sen valmistumisen odottaminen

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

Koko kulku lähetys → kysely → nouto on esitetty tiedostossa `examples/inspection_flow.py` repositoriossa.

## Virheiden käsittely

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```