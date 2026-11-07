---
title: Översikt över REST-API:t 2026.11 | digna Dokumentation
description: Använd digna REST-API v1 för att läsa projekt och inspektionsresultat, hantera datakällor, dataset och attribut och starta inspektioner — bas-URL, autentisering med API-nyckel, paginering, fel och OpenAPI-dokumentet.
image: /assets/logo_square.png
keywords: digna REST-API, digna API, digna OpenAPI, digna API-nyckel, API för inspektionsbegäranden, API för datakvalitet, Swagger UI
---

# digna REST-API 2026.11

Med *digna* REST-API:t kan dina egna verktyg och pipelines arbeta med *digna* över HTTP och JSON: läsa
projekt och inspektionsresultat, hantera datakällor, dataset och attribut och starta inspektioner,
till exempel i slutet av en dataladdning. [Python SDK](../../sdk/Release%202026.11/index.md) använder
samma API.

Den här sidan beskriver det som alla anrop har gemensamt. Resurssidorna listar varje endpoint med dess
parametrar, request-body, svar och scheman:

| Resurs | Endpoints |
|---|---|
| [Projects](projects.md) | Läsa projekt |
| [DB Connections](db_connections.md) | Läsa databasanslutningar |
| [Data Sources](data_sources.md) | Skapa, läsa, uppdatera och ta bort datakällor |
| [Data Sets](data_sets.md) | Skapa, läsa, uppdatera och ta bort dataset |
| [Attributes](attributes.md) | Skapa, läsa, uppdatera och ta bort attribut |
| [Check Definitions](check_definitions.md) | Läsa kontrolldefinitioner |
| [Inspection Requests](inspection_requests.md) | Starta inspektioner och följa deras förlopp |
| [Inspection Statuses](inspection_statuses.md) | Läsa inspektionsresultat per projekt, datakälla och dataset |

---

## Bas-URL {: #base-url }

API:t är en del av *digna*s backend. Varje sökväg börjar med `/v1`, efter backendens adress:

```text
https://digna.example.com/v1/projects
```

Backendens adress är densamma som dashboarden använder: `baseUrl` i avsnittet `[api]` i
`dashboard/dashboard_config.toml`. Använd HTTPS så snart anroparen och *digna* inte körs på samma
maskin, eftersom varje anrop innehåller en API-nyckel.

---

## Autentisering {: #authentication }

Varje anrop skickar API-nyckeln för en *digna*-användare i headern `Authorization`:

```text
Authorization: Bearer <api key>
```

Skapa en nyckel genom att öppna din användarprofil längst ned till vänster i dashboarden, klicka på
**API Keys** och sedan på **Add API Key**, och kopiera nyckeln. Den visas bara en gång. Samma nycklar
fungerar för [digna MCP Server](../../ai_agents/overview.md).

Ett anrop körs med behörigheterna för den användare som äger nyckeln. För att skapa, ändra och ta bort
krävs editorrollen i projektet; annars avvisas anropet med `403` och meddelandet
`You don't have permission to edit this project`.

!!! tip "Använd en dedikerad användare för automatisering"

    Skapa en *digna*-användare för varje integration, ge den bara de projekt och roller den behöver
    och skapa dess nyckel med ett utgångsdatum. Då kan du återkalla en integrations åtkomst genom att
    ta bort dess nyckel, utan att påverka någon annan.

---

## Skicka ett anrop {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Svaren är JSON. Listor returneras som en JSON-array. Även request-bodies är JSON och skickas med
`Content-Type: application/json`.

---

## Gränser och filter {: #limits-and-filters }

List-endpoints returnerar högst `limit` poster: 200 som standard och upp till 5000. Ett värde utanför
det intervallet avvisas med `400`. Det finns ingen offset eller sidtoken, så avgränsa i stället en
lista med dess filter, till exempel `project_id`, `data_source_id`, eller `start_date` och `end_date`
för inspektionsstatusarna.

Ett anrop som tar längre tid än 60 sekunder avbryts med `408 Request Timeout`.

---

## Fel {: #errors }

Ett felsvar har en JSON-body med en kod och ett meddelande:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Status | Kod | Betydelse |
|---|---|---|
| `400` | `BAD_REQUEST` | Anropet är ogiltigt, till exempel ett `limit` utanför intervallet |
| `401` | `NOT_AUTHENTICATED` | API-nyckeln saknas, är felformaterad, okänd eller har gått ut |
| `403` | `NOT_AUTHORIZED` | Nyckelns användare saknar den roll som anropet kräver |
| `403` | `INVALID_LICENSE` | *digna*-licensen har gått ut |
| `404` | `NOT_FOUND` | Projektet, datakällan eller ett annat objekt finns inte |
| `500` | `INTERNAL_ERROR` | Ett oväntat fel i *digna*. Backendloggen innehåller detaljerna |

`message` i ett `401`-svar talar om vad som är fel med nyckeln:

| Meddelande | Orsak |
|---|---|
| `Missing Authorization header` | Ingen `Authorization`-header skickades |
| `Invalid Authorization header format` | Värdet börjar inte med `Bearer ` |
| `Invalid API key` | Nyckeln är fel, eller så har den tagits bort |
| `API key expired` | Nyckeln har gått ut. Skapa en ny |

---

## Köra en inspektion {: #running-an-inspection }

En typisk integration startar en inspektion när en dataladdning är klar, väntar på den och läser
resultatet:

1. **Starta inspektionen** med [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Svaret innehåller begärans `id`.
2. **Följ dess förlopp** med [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Dess `status` går från `PENDING` via `RUNNING` till `COMPLETED`, eller slutar som `FAILED`,
   `ABORTED` eller `CANCELLED`. Fråga igen med några sekunders mellanrum tills den inte längre ändras.
3. **Läs resultatet** med [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   för de inspekterade datumen. Varje post har en övergripande `status`: `0` (OK), `1` (varning),
   `2` (kritisk) eller `-1` (ingen status), och en status per modul med antalet godkända, osäkra och
   misslyckade kontroller.

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

## OpenAPI-dokument {: #openapi-document }

Varje *digna*-installation beskriver detta API i ett OpenAPI 3.1-dokument och erbjuder ett interaktivt
Swagger UI där du kan prova anrop mot det:

| Vad | Adress |
|---|---|
| OpenAPI-dokument | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Dokumentet för Release 2026.11 finns också här: [openapi.json](openapi.json). Använd det för att
generera en klient i ett annat språk.

!!! note "Endast /v1-endpoints omfattas"

    Dashboarden kommunicerar också med backenden via andra, interna endpoints. De ingår inte i detta
    API och kan ändras i vilken release som helst, så bygg integrationer enbart på `/v1`-endpoints.
