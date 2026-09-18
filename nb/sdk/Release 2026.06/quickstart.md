# digna Python SDK-hurtigstart 2026.06

Denne siden viser det minimale oppsettet og de sentrale klientflytene for ***digna*** Python SDK. Bruk den som utgangspunkt før du går videre til referansesidene om ressurser, modeller og feil.

## Opprett en API-nøkkel

Opprett en API-nøkkel i ***digna***-grensesnittet før du kobler til med SDK-et:

1. Logg inn i ***digna*** i grensesnittet.
2. Åpne brukerprofilen din nederst til venstre.
3. Klikk på **API Keys** i brukerprofilen.
4. Klikk på **Add API Key**.
5. Gi nøkkelen et beskrivende navn og sett en utløpsdato. Du kan når som helst tilbakekalle eller slette en API-nøkkel.
6. Kopier den viste API-nøkkelen til utklippstavlen. Nøkkelen vises bare når den opprettes.

Bruk API-nøkkelen som SDK-token. Gode måter å gjøre den tilgjengelig for applikasjonen på:

- En miljøvariabel, for eksempel `DIGNA_API_KEY`, til lokal utvikling og automatisering.
- Hemmelighetslageret i CI/CD-en din, som GitHub Actions-secrets, GitLab CI/CD-variabler eller hemmelige variabler i Azure DevOps.
- En hemmelighetsbehandler i kjøretid, som Kubernetes-secrets, Docker-secrets, HashiCorp Vault eller hemmelighetslageret til en skyleverandør.

Unngå å hardkode API-nøkler i kildekode, notatbøker, shell-historikk eller innsjekkede konfigurasjonsfiler.

## Koble til

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Bruk `DignaClient` som kontekstbehandler slik at den underliggende
tilkoblingspoolen lukkes automatisk:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## List opp prosjekter

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Opprett en datakilde

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

## Send en inspeksjonsforespørsel og vent til den er ferdig

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

Se `examples/inspection_flow.py` i repoet for hele flyten send → poll → hent.

## Håndter feil

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```