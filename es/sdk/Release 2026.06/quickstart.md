# Inicio rápido del SDK de Python de digna 2026.06

Esta página muestra la configuración mínima y los flujos de trabajo principales del cliente del SDK de Python de ***digna***. Úsela como punto de partida antes de pasar a las páginas de referencia de recursos, modelos y errores.

## Crear una clave de API

Cree una clave de API en el frontend de ***digna*** antes de conectarse con el SDK:

1. Inicie sesión en ***digna*** en el frontend.
2. Abra su perfil de usuario en la esquina inferior izquierda.
3. En el perfil de usuario, haga clic en **API Keys**.
4. Haga clic en **Add API Key**.
5. Indique un nombre descriptivo y establezca una fecha de caducidad. Puede revocar o eliminar una clave de API en cualquier momento.
6. Copie la clave de API mostrada en el portapapeles. La clave solo se muestra en el momento de crearla.

Use la clave de API como token del SDK. Buenas formas de proporcionarla a su aplicación:

- Una variable de entorno, por ejemplo `DIGNA_API_KEY`, para el desarrollo local y la automatización.
- El almacén de secretos de su CI/CD, como los secretos de GitHub Actions, las variables de CI/CD de GitLab o las variables secretas de Azure DevOps.
- Un gestor de secretos en tiempo de ejecución, como los secretos de Kubernetes, los secretos de Docker, HashiCorp Vault o el almacén de secretos de un proveedor de nube.

Evite incluir claves de API directamente en el código fuente, los notebooks, el historial del shell o los archivos de configuración versionados.

## Conectarse

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Use `DignaClient` como gestor de contexto para que el grupo de conexiones
subyacente se cierre automáticamente:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## Listar proyectos

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Crear un origen de datos

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

## Enviar una solicitud de inspección y esperar a que finalice

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

Consulte `examples/inspection_flow.py` en el repositorio para ver el flujo completo de envío → sondeo → recuperación.

## Gestionar errores

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```