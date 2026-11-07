# digna REST API 2026.11

Met de *digna* REST API kunnen je eigen tools en pipelines via HTTP en JSON met *digna* werken:
projecten en inspectieresultaten lezen, datasources, datasets en attributen beheren en inspecties
starten, bijvoorbeeld aan het einde van een datalaadproces. De [Python SDK](../../sdk/Release%202026.11/index.md)
gebruikt dezelfde API.

Deze pagina behandelt wat alle verzoeken gemeen hebben. De resourcepagina's beschrijven elk endpoint
met zijn parameters, request body, responses en schema's:

| Resource | Endpoints |
|---|---|
| [Projects](projects.md) | Projecten lezen |
| [DB Connections](db_connections.md) | Databaseverbindingen lezen |
| [Data Sources](data_sources.md) | Datasources aanmaken, lezen, bijwerken en verwijderen |
| [Data Sets](data_sets.md) | Datasets aanmaken, lezen, bijwerken en verwijderen |
| [Attributes](attributes.md) | Attributen aanmaken, lezen, bijwerken en verwijderen |
| [Check Definitions](check_definitions.md) | Controledefinities lezen |
| [Inspection Requests](inspection_requests.md) | Inspecties starten en de voortgang ervan volgen |
| [Inspection Statuses](inspection_statuses.md) | Inspectieresultaten lezen per project, datasource en dataset |

---

## Basis-URL {: #base-url }

De API maakt deel uit van de *digna*-backend. Elk pad begint na het adres van de backend met `/v1`:

```text
https://digna.example.com/v1/projects
```

Het adres van de backend is hetzelfde als dat van het dashboard: `baseUrl` in de sectie `[api]` van
`dashboard/dashboard_config.toml`. Gebruik HTTPS zodra de aanroeper en *digna* niet op dezelfde
machine draaien, want elk verzoek bevat een API-key.

---

## Authenticatie {: #authentication }

Elk verzoek stuurt de API-key van een *digna*-gebruiker mee in de header `Authorization`:

```text
Authorization: Bearer <api key>
```

Om een key aan te maken, open je je gebruikersprofiel linksonder in het dashboard, klik je op
**API Keys** en daarna op **Add API Key**, en kopieer je de key. Hij wordt maar één keer getoond.
Dezelfde keys werken ook voor de [digna MCP Server](../../ai_agents/overview.md).

Een verzoek wordt uitgevoerd met de rechten van de gebruiker van de key. Voor aanmaken, wijzigen en
verwijderen is de rol editor in het project nodig; anders wordt het verzoek geweigerd met `403` en
de melding `You don't have permission to edit this project`.

!!! tip "Gebruik een aparte gebruiker voor automatisering"

    Maak voor elke integratie een eigen *digna*-gebruiker aan, geef die alleen de projecten en rollen
    die hij nodig heeft, en maak zijn key aan met een vervaldatum. Dan kun je de toegang van één
    integratie intrekken door de key ervan te verwijderen, zonder dat iemand anders daar last van heeft.

---

## Een verzoek doen {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Responses zijn JSON. Lijsten worden geretourneerd als een JSON-array. Request bodies zijn ook JSON
en worden verstuurd met `Content-Type: application/json`.

---

## Limieten en filters {: #limits-and-filters }

List-endpoints geven maximaal `limit` items terug: standaard 200 en tot 5000. Een waarde buiten dat
bereik wordt geweigerd met `400`. Er is geen offset of paginatoken, dus beperk een lijst in plaats
daarvan met de filters ervan, bijvoorbeeld `project_id`, `data_source_id`, of `start_date` en
`end_date` bij de inspectiestatussen.

Een verzoek dat langer duurt dan 60 seconden, wordt afgebroken met `408 Request Timeout`.

---

## Fouten {: #errors }

Een foutresponse heeft een JSON-body met een code en een melding:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Status | Code | Betekenis |
|---|---|---|
| `400` | `BAD_REQUEST` | Het verzoek is ongeldig, bijvoorbeeld een `limit` buiten het bereik |
| `401` | `NOT_AUTHENTICATED` | De API-key ontbreekt, is onjuist opgemaakt, onbekend of verlopen |
| `403` | `NOT_AUTHORIZED` | De gebruiker van de key heeft niet de rol die dit verzoek vereist |
| `403` | `INVALID_LICENSE` | De *digna*-licentie is verlopen |
| `404` | `NOT_FOUND` | Het project, de datasource of een ander item bestaat niet |
| `500` | `INTERNAL_ERROR` | Een onverwachte fout in *digna*. Het backendlog bevat de details |

De `message` van een `401` vertelt wat er mis is met de key:

| Melding | Oorzaak |
|---|---|
| `Missing Authorization header` | Er is geen `Authorization`-header meegestuurd |
| `Invalid Authorization header format` | De waarde begint niet met `Bearer ` |
| `Invalid API key` | De key is onjuist of is verwijderd |
| `API key expired` | De key is verlopen. Maak een nieuwe aan |

---

## Een inspectie uitvoeren {: #running-an-inspection }

Een typische integratie start een inspectie zodra een datalaadproces klaar is, wacht erop en leest
het resultaat:

1. **Start de inspectie** met [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   De response bevat de `id` van het verzoek.
2. **Volg de voortgang** met [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   De `status` gaat van `PENDING` via `RUNNING` naar `COMPLETED`, of eindigt als `FAILED`,
   `ABORTED` of `CANCELLED`. Vraag om de paar seconden opnieuw op tot hij niet meer verandert.
3. **Lees het resultaat** met [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   voor de geïnspecteerde datums. Elk item heeft een algehele `status`: `0` (OK), `1` (waarschuwing),
   `2` (kritiek) of `-1` (geen status), en een status per module met het aantal geslaagde, onzekere
   en mislukte controles.

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

## OpenAPI-document {: #openapi-document }

Elke *digna*-installatie beschrijft deze API in een OpenAPI 3.1-document en biedt een interactieve
Swagger UI om er verzoeken tegen uit te proberen:

| Wat | Adres |
|---|---|
| OpenAPI-document | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Het document van Release 2026.11 is ook hier beschikbaar: [openapi.json](openapi.json). Gebruik het
om een client in een andere programmeertaal te genereren.

!!! note "Alleen de /v1-endpoints vallen eronder"

    Het dashboard communiceert ook via andere, interne endpoints met de backend. Die maken geen deel
    uit van deze API en kunnen bij elke release veranderen, dus bouw integraties alleen op de
    `/v1`-endpoints.