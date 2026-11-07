---
title: REST API Overview 2026.11 | digna Documentation
description: Use the digna REST API v1 to read projects and inspection results, manage data sources, datasets and attributes, and start inspections — base URL, API key authentication, pagination, errors and the OpenAPI document.
image: /assets/logo_square.png
keywords: digna REST API, digna API, digna OpenAPI, digna API key, inspection requests API, data quality API, Swagger UI
---

# digna REST API 2026.11

The *digna* REST API lets your own tools and pipelines work with *digna* over HTTP and JSON: read
projects and inspection results, manage data sources, datasets and attributes, and start
inspections, for example at the end of a data load. The [Python SDK](../../sdk/Release%202026.11/index.md)
uses the same API.

This page covers what every request has in common. The resource pages list each endpoint with its
parameters, request body, responses and schemas:

| Resource | Endpoints |
|---|---|
| [Projects](projects.md) | Read projects |
| [DB Connections](db_connections.md) | Read database connections |
| [Data Sources](data_sources.md) | Create, read, update and delete data sources |
| [Data Sets](data_sets.md) | Create, read, update and delete datasets |
| [Attributes](attributes.md) | Create, read, update and delete attributes |
| [Check Definitions](check_definitions.md) | Read check definitions |
| [Inspection Requests](inspection_requests.md) | Start inspections and follow their progress |
| [Inspection Statuses](inspection_statuses.md) | Read inspection results per project, data source and dataset |

---

## Base URL {: #base-url }

The API is part of the *digna* backend. Every path starts with `/v1`, after the backend's address:

```text
https://digna.example.com/v1/projects
```

The backend's address is the one the dashboard uses, `baseUrl` in the `[api]` section of
`dashboard/dashboard_config.toml`. Use HTTPS whenever the caller and *digna* are not on the same
machine, because every request carries an API key.

---

## Authentication {: #authentication }

Every request sends the API key of a *digna* user in the `Authorization` header:

```text
Authorization: Bearer <api key>
```

To create a key, open your user profile in the bottom-left corner of the dashboard, click
**API Keys**, then **Add API Key**, and copy the key. It is shown only once. The same keys work
for the [digna MCP Server](../../ai_agents/overview.md).

A request runs with the permissions of the key's user. Creating, changing and deleting needs the
editor role in the project; otherwise the request is refused with `403` and the message
`You don't have permission to edit this project`.

!!! tip "Use a dedicated user for automation"

    Create a *digna* user for each integration, give it only the projects and roles it needs, and
    create its key with an expiry date. Then you can revoke one integration's access by deleting
    its key, without affecting anyone else.

---

## Making a Request {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Responses are JSON. Lists are returned as a JSON array. Request bodies are JSON as well, sent with
`Content-Type: application/json`.

---

## Limits and Filters {: #limits-and-filters }

List endpoints return at most `limit` items: 200 by default, and up to 5000. A value outside that
range is rejected with `400`. There is no offset or page token, so narrow a list with its filters
instead, for example `project_id`, `data_source_id`, or `start_date` and `end_date` on the
inspection statuses.

A request that takes longer than 60 seconds is cancelled with `408 Request Timeout`.

---

## Errors {: #errors }

An error response has a JSON body with a code and a message:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Status | Code | Meaning |
|---|---|---|
| `400` | `BAD_REQUEST` | The request is invalid, for example a `limit` out of range |
| `401` | `NOT_AUTHENTICATED` | The API key is missing, malformed, unknown or expired |
| `403` | `NOT_AUTHORIZED` | The key's user lacks the role this request needs |
| `403` | `INVALID_LICENSE` | The *digna* license has expired |
| `404` | `NOT_FOUND` | The project, data source or other item doesn't exist |
| `500` | `INTERNAL_ERROR` | An unexpected error in *digna*. The backend log has the details |

The `message` of a `401` says what is wrong with the key:

| Message | Cause |
|---|---|
| `Missing Authorization header` | No `Authorization` header was sent |
| `Invalid Authorization header format` | The value doesn't start with `Bearer ` |
| `Invalid API key` | The key is wrong, or it was deleted |
| `API key expired` | The key has expired. Create a new one |

---

## Running an Inspection {: #running-an-inspection }

A typical integration starts an inspection when a data load has finished, waits for it, and reads
the result:

1. **Start the inspection** with [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   The response holds the request's `id`.
2. **Follow its progress** with [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Its `status` moves from `PENDING` through `RUNNING` to `COMPLETED`, or ends as `FAILED`,
   `ABORTED` or `CANCELLED`. Ask again every few seconds until it no longer changes.
3. **Read the result** with [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   for the inspected dates. Each item has an overall `status`: `0` (OK), `1` (warning),
   `2` (critical) or `-1` (no status), and a status per module with the number of passed, uncertain
   and failed checks.

```bash
curl -X POST https://digna.example.com/v1/inspection-requests \
  -H "Authorization: Bearer $DIGNA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "project_id": 1,
    "include_all_data_sources": true,
    "data_source_ids": [],
    "start_date": "2026-11-06",
    "end_date": "2026-11-06",
    "mode": "DAILY",
    "weekly_mode_weekdays": [],
    "monthly_mode_days": [],
    "use_notification": true
  }'
```

---

## OpenAPI Document {: #openapi-document }

Every *digna* installation describes this API in an OpenAPI 3.1 document, and offers an
interactive Swagger UI to try requests against it:

| What | Address |
|---|---|
| OpenAPI document | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

The document of Release 2026.11 is also available here: [openapi.json](openapi.json). Use it to
generate a client in another language.

!!! note "Only the /v1 endpoints are covered"

    The dashboard also talks to the backend through other, internal endpoints. They are not part of
    this API and can change with any release, so build integrations on the `/v1` endpoints only.
