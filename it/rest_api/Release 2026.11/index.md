# REST API di digna 2026.11

La REST API di *digna* permette ai tuoi strumenti e alle tue pipeline di lavorare con *digna* tramite
HTTP e JSON: leggere progetti e risultati delle ispezioni, gestire sorgenti di dati, dataset e
attributi e avviare ispezioni, ad esempio al termine di un caricamento dati. Il [Python SDK](../../sdk/Release%202026.11/index.md)
usa la stessa API.

Questa pagina descrive ciò che tutte le richieste hanno in comune. Le pagine delle risorse elencano
ogni endpoint con i suoi parametri, il corpo della richiesta, le risposte e gli schemi:

| Risorsa | Endpoint |
|---|---|
| [Projects](projects.md) | Leggere i progetti |
| [DB Connections](db_connections.md) | Leggere le connessioni al database |
| [Data Sources](data_sources.md) | Creare, leggere, aggiornare ed eliminare sorgenti di dati |
| [Data Sets](data_sets.md) | Creare, leggere, aggiornare ed eliminare dataset |
| [Attributes](attributes.md) | Creare, leggere, aggiornare ed eliminare attributi |
| [Check Definitions](check_definitions.md) | Leggere le definizioni dei controlli |
| [Inspection Requests](inspection_requests.md) | Avviare ispezioni e seguirne l'avanzamento |
| [Inspection Statuses](inspection_statuses.md) | Leggere i risultati delle ispezioni per progetto, sorgente di dati e dataset |

---

## URL di base {: #base-url }

L'API fa parte del backend di *digna*. Ogni percorso inizia con `/v1`, dopo l'indirizzo del backend:

```text
https://digna.example.com/v1/projects
```

L'indirizzo del backend è quello usato dalla dashboard: `baseUrl` nella sezione `[api]` di
`dashboard/dashboard_config.toml`. Usa HTTPS ogni volta che il chiamante e *digna* non si trovano sulla
stessa macchina, perché ogni richiesta contiene una chiave API.

---

## Autenticazione {: #authentication }

Ogni richiesta invia la chiave API di un utente *digna* nell'header `Authorization`:

```text
Authorization: Bearer <api key>
```

Per creare una chiave, apri il tuo profilo utente in basso a sinistra nella dashboard, clicca
**API Keys**, poi **Add API Key**, e copia la chiave. Viene mostrata una sola volta. Le stesse chiavi
funzionano anche per il [digna MCP Server](../../ai_agents/overview.md).

Una richiesta viene eseguita con i permessi dell'utente a cui appartiene la chiave. Per creare,
modificare ed eliminare serve il ruolo di editor nel progetto; altrimenti la richiesta viene rifiutata
con `403` e il messaggio `You don't have permission to edit this project`.

!!! tip "Usa un utente dedicato per l'automazione"

    Crea un utente *digna* per ogni integrazione, assegnagli solo i progetti e i ruoli di cui ha
    bisogno e crea la sua chiave con una data di scadenza. Così puoi revocare l'accesso di una singola
    integrazione eliminandone la chiave, senza influire su nessun altro.

---

## Inviare una richiesta {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Le risposte sono in JSON. Gli elenchi vengono restituiti come array JSON. Anche i corpi delle
richieste sono in JSON e vengono inviati con `Content-Type: application/json`.

---

## Limiti e filtri {: #limits-and-filters }

Gli endpoint di elenco restituiscono al massimo `limit` elementi: 200 per impostazione predefinita e
fino a 5000. Un valore fuori da questo intervallo viene rifiutato con `400`. Non esistono offset né
token di pagina, quindi restringi un elenco con i suoi filtri, ad esempio `project_id`,
`data_source_id`, oppure `start_date` e `end_date` per gli stati delle ispezioni.

Una richiesta che dura più di 60 secondi viene annullata con `408 Request Timeout`.

---

## Errori {: #errors }

Una risposta di errore ha un corpo JSON con un codice e un messaggio:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Stato | Codice | Significato |
|---|---|---|
| `400` | `BAD_REQUEST` | La richiesta non è valida, ad esempio un `limit` fuori intervallo |
| `401` | `NOT_AUTHENTICATED` | La chiave API manca, è malformata, sconosciuta o scaduta |
| `403` | `NOT_AUTHORIZED` | L'utente della chiave non ha il ruolo richiesto da questa richiesta |
| `403` | `INVALID_LICENSE` | La licenza di *digna* è scaduta |
| `404` | `NOT_FOUND` | Il progetto, la sorgente di dati o un altro elemento non esiste |
| `500` | `INTERNAL_ERROR` | Un errore imprevisto in *digna*. Il log del backend contiene i dettagli |

Il `message` di una risposta `401` indica cosa c'è che non va nella chiave:

| Messaggio | Causa |
|---|---|
| `Missing Authorization header` | Non è stato inviato alcun header `Authorization` |
| `Invalid Authorization header format` | Il valore non inizia con `Bearer ` |
| `Invalid API key` | La chiave è errata oppure è stata eliminata |
| `API key expired` | La chiave è scaduta. Creane una nuova |

---

## Eseguire un'ispezione {: #running-an-inspection }

Un'integrazione tipica avvia un'ispezione quando un caricamento dati è terminato, ne attende la fine e
legge il risultato:

1. **Avvia l'ispezione** con [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   La risposta contiene l'`id` della richiesta.
2. **Seguine l'avanzamento** con [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Il suo `status` passa da `PENDING` a `RUNNING` fino a `COMPLETED`, oppure termina come `FAILED`,
   `ABORTED` o `CANCELLED`. Interrogalo di nuovo ogni pochi secondi finché non cambia più.
3. **Leggi il risultato** con [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   per le date ispezionate. Ogni elemento ha uno `status` complessivo: `0` (OK), `1` (avviso),
   `2` (critico) o `-1` (nessuno stato), e uno stato per modulo con il numero di controlli superati,
   incerti e falliti.

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

## Documento OpenAPI {: #openapi-document }

Ogni installazione di *digna* descrive questa API in un documento OpenAPI 3.1 e offre una Swagger UI
interattiva per provare le richieste:

| Cosa | Indirizzo |
|---|---|
| Documento OpenAPI | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Il documento di Release 2026.11 è disponibile anche qui: [openapi.json](openapi.json). Usalo per
generare un client in un altro linguaggio.

!!! note "Sono coperti solo gli endpoint /v1"

    La dashboard comunica con il backend anche tramite altri endpoint interni. Non fanno parte di
    questa API e possono cambiare con qualsiasi release, quindi costruisci le integrazioni solo sugli
    endpoint `/v1`.