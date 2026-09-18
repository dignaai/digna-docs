# Guida rapida SDK Python digna 2026.06

Questa pagina mostra la configurazione minima e i flussi di lavoro principali del client per l'SDK Python ***digna***. Usala come punto di partenza prima di passare alle pagine di riferimento su risorse, modelli ed errori.

## Creare una chiave API

Crea una chiave API nel frontend di ***digna*** prima di connetterti con l'SDK:

1. Accedi a ***digna*** dal frontend.
2. Apri il tuo profilo utente in basso a sinistra.
3. Nel profilo utente, fai clic su **API Keys**.
4. Fai clic su **Add API Key**.
5. Assegna un nome significativo e imposta una data di scadenza. Puoi revocare o eliminare una chiave API in qualsiasi momento.
6. Copia negli appunti la chiave API visualizzata. La chiave viene mostrata soltanto al momento della creazione.

Usa la chiave API come token dell'SDK. Modi validi per fornirla all'applicazione:

- Una variabile d'ambiente, ad esempio `DIGNA_API_KEY`, per sviluppo locale e automazione.
- L'archivio dei segreti della tua CI/CD, come i secret di GitHub Actions, le variabili CI/CD di GitLab o le variabili segrete di Azure DevOps.
- Un gestore di segreti a runtime, come i secret di Kubernetes, i secret di Docker, HashiCorp Vault o l'archivio dei segreti di un provider cloud.

Evita di inserire chiavi API direttamente nel codice sorgente, nei notebook, nella cronologia della shell o nei file di configurazione versionati.

## Connessione

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Usa `DignaClient` come context manager per far chiudere automaticamente il pool
di connessioni sottostante:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Elencare i progetti

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Creare un'origine dati

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

## Inviare una richiesta di ispezione e attenderne il completamento

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

Per il flusso completo invio → polling → recupero, vedi `examples/inspection_flow.py` nel repository.

## Gestire gli errori

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```