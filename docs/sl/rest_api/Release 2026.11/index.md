---
title: Pregled REST API 2026.11 | Dokumentacija digna
description: Z digna REST API v1 berite projekte in rezultate inšpekcij, upravljajte podatkovne vire, nabore podatkov in atribute ter zaganjajte inšpekcije — osnovni URL, overjanje s ključem API, ostranjevanje, napake in dokument OpenAPI.
image: /assets/logo_square.png
keywords: digna REST API, digna API, digna OpenAPI, digna ključ API, API za zahteve za inšpekcijo, API za kakovost podatkov, Swagger UI
---

# digna REST API 2026.11

REST API *digna* omogoča vašim lastnim orodjem in cevovodom, da z *digna* delajo prek HTTP in JSON:
berejo projekte in rezultate inšpekcij, upravljajo podatkovne vire, nabore podatkov in atribute ter
zaganjajo inšpekcije, na primer ob koncu nalaganja podatkov. Isti API uporablja tudi
[Python SDK](../../sdk/Release%202026.11/index.md).

Ta stran opisuje, kar je skupno vsem zahtevam. Strani virov navajajo vsako končno točko z njenimi
parametri, telesom zahteve, odgovori in shemami:

| Vir | Končne točke |
|---|---|
| [Projects](projects.md) | Branje projektov |
| [DB Connections](db_connections.md) | Branje povezav z bazami podatkov |
| [Data Sources](data_sources.md) | Ustvarjanje, branje, posodabljanje in brisanje podatkovnih virov |
| [Data Sets](data_sets.md) | Ustvarjanje, branje, posodabljanje in brisanje naborov podatkov |
| [Attributes](attributes.md) | Ustvarjanje, branje, posodabljanje in brisanje atributov |
| [Check Definitions](check_definitions.md) | Branje definicij preverjanj |
| [Inspection Requests](inspection_requests.md) | Zagon inšpekcij in spremljanje njihovega poteka |
| [Inspection Statuses](inspection_statuses.md) | Branje rezultatov inšpekcij po projektih, podatkovnih virih in naborih podatkov |

---

## Osnovni URL {: #base-url }

API je del zaledja *digna*. Vsaka pot se za naslovom zaledja začne z `/v1`:

```text
https://digna.example.com/v1/projects
```

Naslov zaledja je isti, kot ga uporablja nadzorna plošča: `baseUrl` v razdelku `[api]` datoteke
`dashboard/dashboard_config.toml`. HTTPS uporabljajte vedno, kadar klicatelj in *digna* nista na
istem računalniku, saj vsaka zahteva vsebuje ključ API.

---

## Overjanje {: #authentication }

Vsaka zahteva pošlje ključ API uporabnika *digna* v glavi `Authorization`:

```text
Authorization: Bearer <api key>
```

Ključ ustvarite tako, da v spodnjem levem kotu nadzorne plošče odprete svoj uporabniški profil,
kliknete **API Keys**, nato **Add API Key** in kopirate ključ. Prikazan je le enkrat. Isti ključi
delujejo tudi za [digna MCP Server](../../ai_agents/overview.md).

Zahteva se izvede z dovoljenji uporabnika, ki mu ključ pripada. Ustvarjanje, spreminjanje in
brisanje zahteva vlogo urejevalca v projektu; sicer je zahteva zavrnjena s kodo `403` in
sporočilom `You don't have permission to edit this project`.

!!! tip "Za avtomatizacijo uporabite namenskega uporabnika"

    Za vsako integracijo ustvarite svojega uporabnika *digna*, dodelite mu le projekte in vloge, ki
    jih potrebuje, in njegov ključ ustvarite z rokom veljavnosti. Tako lahko dostop posamezne
    integracije prekličete z brisanjem njenega ključa, ne da bi vplivali na kogar koli drugega.

---

## Pošiljanje zahteve {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Odgovori so v obliki JSON. Seznami so vrnjeni kot polje JSON. Tudi telesa zahtev so v obliki JSON in
se pošiljajo z glavo `Content-Type: application/json`.

---

## Omejitve in filtri {: #limits-and-filters }

Končne točke za sezname vrnejo največ `limit` elementov: privzeto 200 in največ 5000. Vrednost
zunaj tega razpona je zavrnjena s kodo `400`. Odmika (offset) ali žetona strani ni, zato seznam
zožite z njegovimi filtri, na primer z `project_id`, `data_source_id` ali z `start_date` in
`end_date` pri statusih inšpekcij.

Zahteva, ki traja dlje kot 60 sekund, je preklicana z `408 Request Timeout`.

---

## Napake {: #errors }

Odgovor z napako ima telo JSON s kodo in sporočilom:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Status | Koda | Pomen |
|---|---|---|
| `400` | `BAD_REQUEST` | Zahteva je neveljavna, na primer `limit` zunaj razpona |
| `401` | `NOT_AUTHENTICATED` | Ključ API manjka, je napačno oblikovan, neznan ali potekel |
| `403` | `NOT_AUTHORIZED` | Uporabnik ključa nima vloge, ki jo ta zahteva potrebuje |
| `403` | `INVALID_LICENSE` | Licenca *digna* je potekla |
| `404` | `NOT_FOUND` | Projekt, podatkovni vir ali drug element ne obstaja |
| `500` | `INTERNAL_ERROR` | Nepričakovana napaka v *digna*. Podrobnosti so v dnevniku zaledja |

Polje `message` odgovora `401` pove, kaj je narobe s ključem:

| Sporočilo | Vzrok |
|---|---|
| `Missing Authorization header` | Glava `Authorization` ni bila poslana |
| `Invalid Authorization header format` | Vrednost se ne začne z `Bearer ` |
| `Invalid API key` | Ključ je napačen ali je bil izbrisan |
| `API key expired` | Ključ je potekel. Ustvarite novega |

---

## Zagon inšpekcije {: #running-an-inspection }

Tipična integracija zažene inšpekcijo, ko se nalaganje podatkov konča, počaka, da se konča, in
prebere rezultat:

1. **Zaženite inšpekcijo** z [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Odgovor vsebuje `id` zahteve.
2. **Spremljajte njen potek** z [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Njen `status` se spreminja od `PENDING` prek `RUNNING` do `COMPLETED` ali pa se konča kot
   `FAILED`, `ABORTED` ali `CANCELLED`. Poizvedbo ponavljajte na nekaj sekund, dokler se ne
   preneha spreminjati.
3. **Preberite rezultat** z [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   za datume, ki jih je zajela inšpekcija. Vsak element ima skupni `status`: `0` (OK),
   `1` (opozorilo), `2` (kritično) ali `-1` (brez statusa), ter status za vsak modul s številom
   uspešnih, negotovih in neuspešnih preverjanj.

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

## Dokument OpenAPI {: #openapi-document }

Vsaka namestitev *digna* opisuje ta API v dokumentu OpenAPI 3.1 in ponuja interaktivni Swagger UI,
v katerem lahko preizkusite zahteve:

| Kaj | Naslov |
|---|---|
| Dokument OpenAPI | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Dokument za Release 2026.11 je na voljo tudi tukaj: [openapi.json](openapi.json). Z njim lahko
ustvarite odjemalca v drugem programskem jeziku.

!!! note "Zajete so le končne točke /v1"

    Nadzorna plošča z zaledjem komunicira tudi prek drugih, internih končnih točk. Te niso del tega
    API in se lahko spremenijo s katero koli izdajo, zato integracije gradite le na končnih točkah
    `/v1`.
