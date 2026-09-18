# digna Python SDK-snelstart 2026.06

Deze pagina toont de minimale configuratie en de belangrijkste clientworkflows voor de ***digna*** Python SDK. Gebruik deze pagina als startpunt voordat u verdergaat met de referentiepagina's over resources, modellen en fouten.

## Een API-sleutel aanmaken

Maak in de ***digna***-frontend een API-sleutel aan voordat u verbinding maakt met de SDK:

1. Meld u in de frontend aan bij ***digna***.
2. Open uw gebruikersprofiel linksonder.
3. Klik in het gebruikersprofiel op **API Keys**.
4. Klik op **Add API Key**.
5. Geef een duidelijke naam op en stel een vervaldatum in. U kunt een API-sleutel op elk moment intrekken of verwijderen.
6. Kopieer de getoonde API-sleutel naar het klembord. De sleutel wordt alleen bij het aanmaken weergegeven.

Gebruik de API-sleutel als SDK-token. Goede manieren om die aan uw toepassing door te geven zijn:

- Een omgevingsvariabele, bijvoorbeeld `DIGNA_API_KEY`, voor lokale ontwikkeling en automatisering.
- De secretsopslag van uw CI/CD, zoals GitHub Actions-secrets, GitLab CI/CD-variabelen of geheime variabelen in Azure DevOps.
- Een secretsmanager tijdens runtime, zoals Kubernetes-secrets, Docker-secrets, HashiCorp Vault of de secretsopslag van een cloudprovider.

Zet API-sleutels niet hard in broncode, notebooks, shellgeschiedenis of ingecheckte configuratiebestanden.

## Verbinding maken

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Gebruik `DignaClient` als contextmanager, zodat de onderliggende connectiepool
automatisch wordt gesloten:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Projecten weergeven

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Een gegevensbron aanmaken

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

## Een inspectieverzoek indienen en op de voltooiing wachten

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

Zie `examples/inspection_flow.py` in de repository voor de volledige flow van indienen → pollen → ophalen.

## Fouten afhandelen

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```