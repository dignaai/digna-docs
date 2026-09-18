---
title: digna Python SDK 리소스 2026.06 | digna 문서
description: digna Python SDK 릴리스 2026.06의 리소스 클라이언트
image: /assets/logo_square.png
---

# digna Python SDK 리소스 2026.06

이 페이지에서는 ***digna*** Python SDK가 제공하는 리소스 클라이언트를 설명합니다. 각 리소스는 안정 API의 해당 엔드포인트를 일관되고 파이썬다운 인터페이스와 예측 가능한 메서드 이름으로 감쌉니다.

`DignaClient`는 API 영역마다 리소스 객체를 하나씩 제공합니다. 각 리소스는
안정 API의 해당 엔드포인트를 파이썬다운 메서드 이름으로 감쌉니다.

| 리소스 | 속성 | 엔드포인트 |
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
