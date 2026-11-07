# digna REST API 2026.11

Med *digna* REST API kan dine egne værktøjer og pipelines arbejde med *digna* over HTTP og JSON:
læse projekter og inspektionsresultater, administrere datakilder, datasæt og attributter og starte
inspektioner, for eksempel når en dataindlæsning er færdig. [Python SDK](../../sdk/Release%202026.11/index.md)
bruger det samme API.

Denne side beskriver det, som alle forespørgsler har til fælles. Ressourcesiderne viser hvert
endpoint med parametre, forespørgselsbody, svar og skemaer:

| Ressource | Endpoints |
|---|---|
| [Projects](projects.md) | Læse projekter |
| [DB Connections](db_connections.md) | Læse databaseforbindelser |
| [Data Sources](data_sources.md) | Oprette, læse, opdatere og slette datakilder |
| [Data Sets](data_sets.md) | Oprette, læse, opdatere og slette datasæt |
| [Attributes](attributes.md) | Oprette, læse, opdatere og slette attributter |
| [Check Definitions](check_definitions.md) | Læse kontroldefinitioner |
| [Inspection Requests](inspection_requests.md) | Starte inspektioner og følge deres fremdrift |
| [Inspection Statuses](inspection_statuses.md) | Læse inspektionsresultater pr. projekt, datakilde og datasæt |

---

## Basis-URL {: #base-url }

API'et er en del af *digna*-backenden. Hver sti begynder med `/v1` efter backendens adresse:

```text
https://digna.example.com/v1/projects
```

Backendens adresse er den samme, som dashboardet bruger, `baseUrl` i `[api]`-sektionen i
`dashboard/dashboard_config.toml`. Brug HTTPS, når det kaldende system og *digna* ikke er på samme
maskine, fordi hver forespørgsel indeholder en API-nøgle.

---

## Godkendelse {: #authentication }

Hver forespørgsel sender API-nøglen for en *digna*-bruger i `Authorization`-headeren:

```text
Authorization: Bearer <api key>
```

Du opretter en nøgle ved at åbne din brugerprofil i nederste venstre hjørne af dashboardet, klikke
på **API Keys** og derefter **Add API Key** og kopiere nøglen. Den vises kun én gang. De samme
nøgler virker også til [digna MCP Server](../../ai_agents/overview.md).

En forespørgsel kører med rettighederne for nøglens bruger. Oprettelse, ændring og sletning kræver
editorrollen i projektet; ellers afvises forespørgslen med `403` og meddelelsen
`You don't have permission to edit this project`.

!!! tip "Brug en dedikeret bruger til automatisering"

    Opret en *digna*-bruger til hver integration, giv den kun de projekter og roller, den har brug
    for, og opret dens nøgle med en udløbsdato. Så kan du tilbagekalde én integrations adgang ved at
    slette dens nøgle uden at påvirke andre.

---

## Send en forespørgsel {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Svarene er JSON. Lister returneres som et JSON-array. Forespørgselsbodyer er også JSON og sendes med
`Content-Type: application/json`.

---

## Grænser og filtre {: #limits-and-filters }

Listeendpoints returnerer højst `limit` elementer: 200 som standard og op til 5000. En værdi uden
for dette interval afvises med `400`. Der findes ingen offset eller sidetoken, så indsnævr i stedet
en liste med dens filtre, for eksempel `project_id`, `data_source_id` eller `start_date` og
`end_date` på inspektionsstatusserne.

En forespørgsel, der tager længere end 60 sekunder, annulleres med `408 Request Timeout`.

---

## Fejl {: #errors }

Et fejlsvar har en JSON-body med en kode og en meddelelse:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Status | Kode | Betydning |
|---|---|---|
| `400` | `BAD_REQUEST` | Forespørgslen er ugyldig, for eksempel en `limit` uden for intervallet |
| `401` | `NOT_AUTHENTICATED` | API-nøglen mangler, er forkert formateret, ukendt eller udløbet |
| `403` | `NOT_AUTHORIZED` | Nøglens bruger mangler den rolle, som forespørgslen kræver |
| `403` | `INVALID_LICENSE` | *digna*-licensen er udløbet |
| `404` | `NOT_FOUND` | Projektet, datakilden eller et andet element findes ikke |
| `500` | `INTERNAL_ERROR` | En uventet fejl i *digna*. Backend-loggen indeholder detaljerne |

`message` i et `401`-svar fortæller, hvad der er galt med nøglen:

| Meddelelse | Årsag |
|---|---|
| `Missing Authorization header` | Der blev ikke sendt nogen `Authorization`-header |
| `Invalid Authorization header format` | Værdien starter ikke med `Bearer ` |
| `Invalid API key` | Nøglen er forkert, eller den er slettet |
| `API key expired` | Nøglen er udløbet. Opret en ny |

---

## Kør en inspektion {: #running-an-inspection }

En typisk integration starter en inspektion, når en dataindlæsning er færdig, venter på den og
læser resultatet:

1. **Start inspektionen** med [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Svaret indeholder anmodningens `id`.
2. **Følg dens fremdrift** med [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Dens `status` går fra `PENDING` over `RUNNING` til `COMPLETED` eller ender som `FAILED`,
   `ABORTED` eller `CANCELLED`. Spørg igen med få sekunders mellemrum, indtil den ikke længere ændrer sig.
3. **Læs resultatet** med [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   for de inspicerede datoer. Hvert element har en samlet `status`: `0` (OK), `1` (advarsel),
   `2` (kritisk) eller `-1` (ingen status) samt en status pr. modul med antallet af beståede,
   usikre og fejlede kontroller.

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

Hver *digna*-installation beskriver dette API i et OpenAPI 3.1-dokument og tilbyder en interaktiv
Swagger UI, hvor du kan afprøve forespørgsler mod det:

| Hvad | Adresse |
|---|---|
| OpenAPI-dokument | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Dokumentet for Release 2026.11 er også tilgængeligt her: [openapi.json](openapi.json). Brug det til
at generere en klient i et andet sprog.

!!! note "Kun /v1-endpoints er omfattet"

    Dashboardet kommunikerer også med backenden via andre, interne endpoints. De er ikke en del af
    dette API og kan ændre sig med enhver udgivelse, så byg kun integrationer på `/v1`-endpoints.