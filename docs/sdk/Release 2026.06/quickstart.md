---
title: digna Python SDK Quickstart 2026.06 | digna Documentation
description: Quickstart guide for the digna Python SDK release 2026.06
image: /assets/logo_square.png
---

# digna Python SDK Quickstart 2026.06

This page shows the minimal setup and the core client workflows for the ***digna*** Python SDK. Use it as the starting point before moving on to the resource, model, and error reference pages.

## Create an API key

Create an API key in the ***digna*** frontend before connecting with the SDK:

1. Log in to ***digna*** in the frontend.
2. Open your user profile in the bottom-left corner.
3. In the user profile, click **API Keys**.
4. Click **Add API Key**.
5. Provide a meaningful name and set an expiration date. You can revoke or delete an API key at any time.
6. Copy the displayed API key to your clipboard. The key is shown only when it is created.

Use the API key as the SDK token. Good ways to provide it to your application include:

- An environment variable, for example `DIGNA_API_KEY`, for local development and automation.
- Your CI/CD secret store, such as GitHub Actions secrets, GitLab CI/CD variables, or Azure DevOps secret variables.
- A runtime secret manager, such as Kubernetes secrets, Docker secrets, HashiCorp Vault, or a cloud provider secret store.

Avoid hard-coding API keys in source code, notebooks, shell history, or committed configuration files.

## Connect

```python
import os

from digna_sdk import DignaClient

client = DignaClient(
    base_url="http://localhost:8000",  # your on-premises Digna backend
    token=os.environ["DIGNA_API_KEY"],
)
```

Use `DignaClient` as a context manager to have the underlying connection pool
closed automatically:

```python
with DignaClient(base_url="http://localhost:8000", token="<token>") as client:
    projects = client.projects.list()
```

## List projects

```python
for project in client.projects.list():
    print(project.id, project.name)
```

## Create a data source

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

## Submit an inspection request and wait for it to finish

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

See `examples/inspection_flow.py` in the repository for the full submit → poll → retrieve flow.

## Handle errors

```python
from digna_sdk import DignaAPIError, DignaNotFoundError

try:
    client.projects.get(999)
except DignaNotFoundError:
    print("no such project")
except DignaAPIError as exc:
    print(f"API error {exc.status_code}: {exc.message}")
```
