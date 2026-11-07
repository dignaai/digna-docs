---
title: REST API ülevaade 2026.11 | digna dokumentatsioon
description: Kasuta digna REST API v1 projektide ja inspektsioonitulemuste lugemiseks, andmeallikate, andmekogumite ja atribuutide haldamiseks ning inspektsioonide käivitamiseks — baas-URL, autentimine API võtmega, lehekülgedeks jagamine, vead ja OpenAPI dokument.
image: /assets/logo_square.png
keywords: digna REST API, digna API, digna OpenAPI, digna API võti, inspektsioonipäringute API, andmekvaliteedi API, Swagger UI
---

# digna REST API 2026.11

*digna* REST API võimaldab sinu enda tööriistadel ja andmekonveieritel töötada *dignaga* üle HTTP ja
JSON-i: lugeda projekte ja inspektsioonitulemusi, hallata andmeallikaid, andmekogumeid ja atribuute
ning käivitada inspektsioone, näiteks andmelaadimise lõpus. [Python SDK](../../sdk/Release%202026.11/index.md)
kasutab sama API-t.

See leht kirjeldab seda, mis on kõigile päringutele ühine. Ressursilehed loetlevad iga lõpp-punkti
koos parameetrite, päringu keha, vastuste ja skeemidega:

| Ressurss | Lõpp-punktid |
|---|---|
| [Projects](projects.md) | Projektide lugemine |
| [DB Connections](db_connections.md) | Andmebaasiühenduste lugemine |
| [Data Sources](data_sources.md) | Andmeallikate loomine, lugemine, muutmine ja kustutamine |
| [Data Sets](data_sets.md) | Andmekogumite loomine, lugemine, muutmine ja kustutamine |
| [Attributes](attributes.md) | Atribuutide loomine, lugemine, muutmine ja kustutamine |
| [Check Definitions](check_definitions.md) | Kontrollide definitsioonide lugemine |
| [Inspection Requests](inspection_requests.md) | Inspektsioonide käivitamine ja nende edenemise jälgimine |
| [Inspection Statuses](inspection_statuses.md) | Inspektsioonitulemuste lugemine projekti, andmeallika ja andmekogumi kaupa |

---

## Baas-URL {: #base-url }

API on osa *digna* backendist. Iga tee algab pärast backendi aadressi osaga `/v1`:

```text
https://digna.example.com/v1/projects
```

Backendi aadress on sama, mida kasutab dashboard: `baseUrl` faili `dashboard/dashboard_config.toml`
jaotises `[api]`. Kasuta HTTPS-i alati, kui päringu saatja ja *digna* ei asu samas masinas, sest iga
päring sisaldab API võtit.

---

## Autentimine {: #authentication }

Iga päring saadab *digna* kasutaja API võtme päises `Authorization`:

```text
Authorization: Bearer <api key>
```

Võtme loomiseks ava dashboardi vasakus alanurgas oma kasutajaprofiil, klõpsa **API Keys** ja
seejärel **Add API Key** ning kopeeri võti. Seda näidatakse ainult üks kord. Samad võtmed töötavad
ka [digna MCP Serveriga](../../ai_agents/overview.md).

Päring täidetakse võtme kasutaja õigustega. Loomiseks, muutmiseks ja kustutamiseks on projektis
vaja toimetaja rolli; vastasel juhul lükatakse päring tagasi koodiga `403` ja teatega
`You don't have permission to edit this project`.

!!! tip "Kasuta automatiseerimiseks eraldi kasutajat"

    Loo iga integratsiooni jaoks oma *digna* kasutaja, anna talle ainult need projektid ja rollid,
    mida ta vajab, ning loo tema võti aegumiskuupäevaga. Siis saad ühe integratsiooni juurdepääsu
    tühistada, kustutades selle võtme, ilma et see kedagi teist mõjutaks.

---

## Päringu tegemine {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Vastused on JSON-vormingus. Loendid tagastatakse JSON-massiivina. Ka päringute kehad on JSON-is ja
need saadetakse päisega `Content-Type: application/json`.

---

## Piirangud ja filtrid {: #limits-and-filters }

Loendite lõpp-punktid tagastavad kõige rohkem `limit` elementi: vaikimisi 200 ja kuni 5000. Sellest
vahemikust väljas olev väärtus lükatakse tagasi koodiga `400`. Nihet (offset) ega lehe tõendit pole,
seega kitsenda loendit selle asemel filtritega, näiteks `project_id`, `data_source_id` või
inspektsiooni olekute puhul `start_date` ja `end_date`.

Päring, mis kestab kauem kui 60 sekundit, katkestatakse vastusega `408 Request Timeout`.

---

## Vead {: #errors }

Veavastusel on JSON-keha koodi ja teatega:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Olek | Kood | Tähendus |
|---|---|---|
| `400` | `BAD_REQUEST` | Päring on vigane, näiteks on `limit` lubatud vahemikust väljas |
| `401` | `NOT_AUTHENTICATED` | API võti puudub, on vales vormingus, tundmatu või aegunud |
| `403` | `NOT_AUTHORIZED` | Võtme kasutajal puudub roll, mida see päring nõuab |
| `403` | `INVALID_LICENSE` | *digna* litsents on aegunud |
| `404` | `NOT_FOUND` | Projekti, andmeallikat või muud elementi ei ole olemas |
| `500` | `INTERNAL_ERROR` | Ootamatu viga *dignas*. Üksikasjad on backendi logis |

`401` vastuse `message` ütleb, mis võtmega valesti on:

| Teade | Põhjus |
|---|---|
| `Missing Authorization header` | Päist `Authorization` ei saadetud |
| `Invalid Authorization header format` | Väärtus ei alga sõnaga `Bearer ` |
| `Invalid API key` | Võti on vale või see on kustutatud |
| `API key expired` | Võti on aegunud. Loo uus |

---

## Inspektsiooni käivitamine {: #running-an-inspection }

Tüüpiline integratsioon käivitab inspektsiooni, kui andmelaadimine on lõppenud, ootab selle
valmimist ja loeb tulemuse:

1. **Käivita inspektsioon** päringuga [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Vastus sisaldab päringu `id`-d.
2. **Jälgi selle edenemist** päringuga [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Selle `status` liigub olekust `PENDING` oleku `RUNNING` kaudu olekusse `COMPLETED` või lõpeb
   olekuga `FAILED`, `ABORTED` või `CANCELLED`. Küsi uuesti iga paari sekundi järel, kuni see enam ei muutu.
3. **Loe tulemus** päringuga [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   inspekteeritud kuupäevade kohta. Igal elemendil on üldine `status`: `0` (OK), `1` (hoiatus),
   `2` (kriitiline) või `-1` (olek puudub), ning iga mooduli olek koos läbitud, ebakindlate ja
   ebaõnnestunud kontrollide arvuga.

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

## OpenAPI dokument {: #openapi-document }

Iga *digna* paigaldus kirjeldab seda API-t OpenAPI 3.1 dokumendis ja pakub interaktiivset
Swagger UI-d, kus saad päringuid selle vastu proovida:

| Mis | Aadress |
|---|---|
| OpenAPI dokument | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Release 2026.11 dokument on saadaval ka siin: [openapi.json](openapi.json). Kasuta seda kliendi
genereerimiseks mõnes teises programmeerimiskeeles.

!!! note "Kaetud on ainult /v1 lõpp-punktid"

    Dashboard suhtleb backendiga ka teiste, sisemiste lõpp-punktide kaudu. Need ei kuulu selle API
    juurde ja võivad muutuda igas väljalaskes, seega ehita integratsioonid ainult `/v1` lõpp-punktidele.
