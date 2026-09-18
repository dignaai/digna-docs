---
title: digna Python SDK-ressourcer 2026.06 | digna-dokumentation
description: Ressourceklienter til digna Python SDK-udgivelse 2026.06
image: /assets/logo_square.png
---

# digna Python SDK-ressourcer 2026.06

Denne side dokumenterer de ressourceklienter, som ***digna*** Python SDK stiller til rådighed. Hver ressource pakker de tilsvarende endepunkter i det stabile API ind i en ensartet, pythonisk grænseflade med forudsigelige metodenavne.

`DignaClient` stiller ét ressourceobjekt til rådighed pr. API-område. Hver ressource pakker
de tilsvarende endepunkter i det stabile API ind med pythoniske metodenavne.

| Ressource | Attribut | Endepunkter |
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
