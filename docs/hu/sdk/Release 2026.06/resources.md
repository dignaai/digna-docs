---
title: digna Python SDK erőforrások 2026.06 | digna dokumentáció
description: Erőforrás-kliensek a digna Python SDK 2026.06 kiadásához
image: /assets/logo_square.png
---

# digna Python SDK erőforrások 2026.06

Ez az oldal a ***digna*** Python SDK erőforrás-klienseit mutatja be. Minden erőforrás a stabil API megfelelő végpontjait csomagolja egységes, pythonos felületbe, kiszámítható metódusnevekkel.

A `DignaClient` API-területenként egy erőforrás-objektumot tesz elérhetővé. Minden erőforrás
a stabil API megfelelő végpontjait csomagolja pythonos metódusnevekkel.

| Erőforrás | Attribútum | Végpontok |
|---|---|---|
| [`ProjectsResource`][digna_sdk.resources.projects.ProjectsResource] | `client.projects` | `/v1/projects` |
| [`DataSourcesResource`][digna_sdk.resources.data_sources.DataSourcesResource] | `client.data_sources` | `/v1/data-sources` |
| [`DataSetsResource`][digna_sdk.resources.data_sets.DataSetsResource] | `client.data_sets` | `/v1/data-sets` |
| [`AttributesResource`][digna_sdk.resources.attributes.AttributesResource] | `client.attributes` | `/v1/attributes` |
| [`CheckDefinitionsResource`][digna_sdk.resources.check_definitions.CheckDefinitionsResource] | `client.check_definitions` | `/v1/check-definitions` |
| [`DbConnectionsResource`][digna_sdk.resources.db_connections.DbConnectionsResource] | `client.db_connections` | `/v1/db-connections` |
| [`InspectionRequestsResource`][digna_sdk.resources.inspection_requests.InspectionRequestsResource] | `client.inspection_requests` | `/v1/inspection-requests` |
| [`InspectionStatusesResource`][digna_sdk.resources.inspection_statuses.InspectionStatusesResource] | `client.inspection_statuses` | `/v1/inspection-statuses/*` |

::: digna_sdk.resources.projects.ProjectsResource

::: digna_sdk.resources.data_sources.DataSourcesResource

::: digna_sdk.resources.data_sets.DataSetsResource

::: digna_sdk.resources.attributes.AttributesResource

::: digna_sdk.resources.check_definitions.CheckDefinitionsResource

::: digna_sdk.resources.db_connections.DbConnectionsResource

::: digna_sdk.resources.inspection_requests.InspectionRequestsResource

::: digna_sdk.resources.inspection_statuses.InspectionStatusesResource
