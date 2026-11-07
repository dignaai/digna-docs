# digna REST API 2026.11

Med *digna* REST API kan dine egne verktøy og pipelines jobbe med *digna* over HTTP og JSON: lese
prosjekter og inspeksjonsresultater, administrere datakilder, datasett og attributter og starte
inspeksjoner, for eksempel når en datalasting er ferdig. [Python SDK](../../sdk/Release%202026.11/index.md)
bruker det samme API-et.

Denne siden beskriver det alle forespørsler har til felles. Ressurssidene viser hvert endepunkt med
parametere, forespørselsbody, svar og skjemaer:

| Ressurs | Endepunkter |
|---|---|
| [Projects](projects.md) | Lese prosjekter |
| [DB Connections](db_connections.md) | Lese databasetilkoblinger |
| [Data Sources](data_sources.md) | Opprette, lese, oppdatere og slette datakilder |
| [Data Sets](data_sets.md) | Opprette, lese, oppdatere og slette datasett |
| [Attributes](attributes.md) | Opprette, lese, oppdatere og slette attributter |
| [Check Definitions](check_definitions.md) | Lese kontrolldefinisjoner |
| [Inspection Requests](inspection_requests.md) | Starte inspeksjoner og følge fremdriften deres |
| [Inspection Statuses](inspection_statuses.md) | Lese inspeksjonsresultater per prosjekt, datakilde og datasett |

---

## Basis-URL {: #base-url }

API-et er en del av *digna*-backenden. Hver sti begynner med `/v1`, etter backendens adresse:

```text
https://digna.example.com/v1/projects
```

Backendens adresse er den samme som dashboardet bruker, `baseUrl` i `[api]`-seksjonen i
`dashboard/dashboard_config.toml`. Bruk HTTPS når kallende system og *digna* ikke er på samme
maskin, fordi hver forespørsel inneholder en API-nøkkel.

---

## Autentisering {: #authentication }

Hver forespørsel sender API-nøkkelen til en *digna*-bruker i `Authorization`-headeren:

```text
Authorization: Bearer <api key>
```

For å opprette en nøkkel åpner du brukerprofilen din nederst til venstre i dashboardet, klikker
**API Keys** og deretter **Add API Key**, og kopierer nøkkelen. Den vises bare én gang. De samme
nøklene fungerer også for [digna MCP Server](../../ai_agents/overview.md).

En forespørsel kjøres med rettighetene til nøkkelens bruker. Å opprette, endre og slette krever
redaktørrollen i prosjektet; ellers avvises forespørselen med `403` og meldingen
`You don't have permission to edit this project`.

!!! tip "Bruk en egen bruker for automatisering"

    Opprett en *digna*-bruker for hver integrasjon, gi den bare prosjektene og rollene den trenger, og
    opprett nøkkelen dens med en utløpsdato. Da kan du tilbakekalle tilgangen til én integrasjon ved å
    slette nøkkelen dens, uten å påvirke noen andre.

---

## Sende en forespørsel {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Svarene er JSON. Lister returneres som en JSON-array. Forespørselsbodyer er også JSON og sendes med
`Content-Type: application/json`.

---

## Grenser og filtre {: #limits-and-filters }

Listeendepunkter returnerer høyst `limit` elementer: 200 som standard og opptil 5000. En verdi
utenfor dette området avvises med `400`. Det finnes ingen offset eller sidetoken, så snevre i stedet
inn en liste med filtrene dens, for eksempel `project_id`, `data_source_id`, eller `start_date` og
`end_date` på inspeksjonsstatusene.

En forespørsel som tar lengre tid enn 60 sekunder, avbrytes med `408 Request Timeout`.

---

## Feil {: #errors }

Et feilsvar har en JSON-body med en kode og en melding:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Status | Kode | Betydning |
|---|---|---|
| `400` | `BAD_REQUEST` | Forespørselen er ugyldig, for eksempel en `limit` utenfor området |
| `401` | `NOT_AUTHENTICATED` | API-nøkkelen mangler, er feilformatert, ukjent eller utløpt |
| `403` | `NOT_AUTHORIZED` | Nøkkelens bruker mangler rollen denne forespørselen krever |
| `403` | `INVALID_LICENSE` | *digna*-lisensen har utløpt |
| `404` | `NOT_FOUND` | Prosjektet, datakilden eller et annet element finnes ikke |
| `500` | `INTERNAL_ERROR` | En uventet feil i *digna*. Backend-loggen har detaljene |

`message` i et `401`-svar forteller hva som er galt med nøkkelen:

| Melding | Årsak |
|---|---|
| `Missing Authorization header` | Ingen `Authorization`-header ble sendt |
| `Invalid Authorization header format` | Verdien begynner ikke med `Bearer ` |
| `Invalid API key` | Nøkkelen er feil, eller den er slettet |
| `API key expired` | Nøkkelen har utløpt. Opprett en ny |

---

## Kjøre en inspeksjon {: #running-an-inspection }

En typisk integrasjon starter en inspeksjon når en datalasting er ferdig, venter på den og leser
resultatet:

1. **Start inspeksjonen** med [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Svaret inneholder forespørselens `id`.
2. **Følg fremdriften** med [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   `status` går fra `PENDING` via `RUNNING` til `COMPLETED`, eller ender som `FAILED`,
   `ABORTED` eller `CANCELLED`. Spør på nytt med noen sekunders mellomrom til den ikke lenger endrer seg.
3. **Les resultatet** med [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   for de inspiserte datoene. Hvert element har en samlet `status`: `0` (OK), `1` (advarsel),
   `2` (kritisk) eller `-1` (ingen status), og en status per modul med antall beståtte, usikre
   og mislykkede kontroller.

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

Hver *digna*-installasjon beskriver dette API-et i et OpenAPI 3.1-dokument og tilbyr et
interaktivt Swagger UI der du kan prøve forespørsler mot det:

| Hva | Adresse |
|---|---|
| OpenAPI-dokument | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Dokumentet for Release 2026.11 er også tilgjengelig her: [openapi.json](openapi.json). Bruk det til å
generere en klient i et annet språk.

!!! note "Bare /v1-endepunktene er dekket"

    Dashboardet kommuniserer også med backenden via andre, interne endepunkter. De er ikke en del av
    dette API-et og kan endres i enhver utgivelse, så bygg integrasjoner bare på `/v1`-endepunktene.