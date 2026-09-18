---
title: Ressources du SDK Python digna 2026.06 | Documentation digna
description: Clients de ressources du SDK Python digna version 2026.06
image: /assets/logo_square.png
---

# Ressources du SDK Python digna 2026.06

Cette page documente les clients de ressources exposés par le SDK Python ***digna***. Chaque ressource encapsule les points de terminaison correspondants de l'API stable dans une interface cohérente et pythonique, aux noms de méthodes prévisibles.

`DignaClient` expose un objet ressource par domaine de l'API. Chaque ressource encapsule
les points de terminaison correspondants de l'API stable avec des noms de méthodes pythoniques.

| Ressource | Attribut | Points de terminaison |
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
