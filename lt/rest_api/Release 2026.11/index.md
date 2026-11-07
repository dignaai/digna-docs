# digna REST API 2026.11

*digna* REST API leidžia jūsų įrankiams ir duomenų srautams dirbti su *digna* per HTTP ir JSON:
skaityti projektus ir inspekcijų rezultatus, valdyti duomenų šaltinius, duomenų rinkinius ir
atributus bei paleisti inspekcijas, pavyzdžiui, pasibaigus duomenų įkėlimui. [Python SDK](../../sdk/Release%202026.11/index.md)
naudoja tą pačią API.

Šiame puslapyje aprašoma tai, kas bendra visoms užklausoms. Išteklių puslapiuose pateikiamas
kiekvienas galinis taškas su jo parametrais, užklausos turiniu, atsakymais ir schemomis:

| Išteklius | Galiniai taškai |
|---|---|
| [Projects](projects.md) | Projektų skaitymas |
| [DB Connections](db_connections.md) | Duomenų bazių jungčių skaitymas |
| [Data Sources](data_sources.md) | Duomenų šaltinių kūrimas, skaitymas, keitimas ir šalinimas |
| [Data Sets](data_sets.md) | Duomenų rinkinių kūrimas, skaitymas, keitimas ir šalinimas |
| [Attributes](attributes.md) | Atributų kūrimas, skaitymas, keitimas ir šalinimas |
| [Check Definitions](check_definitions.md) | Patikrų apibrėžčių skaitymas |
| [Inspection Requests](inspection_requests.md) | Inspekcijų paleidimas ir jų eigos stebėjimas |
| [Inspection Statuses](inspection_statuses.md) | Inspekcijų rezultatų skaitymas pagal projektą, duomenų šaltinį ir duomenų rinkinį |

---

## Bazinis URL {: #base-url }

API yra *digna* backend'o dalis. Kiekvienas kelias prasideda `/v1` po backend'o adreso:

```text
https://digna.example.com/v1/projects
```

Backend'o adresas yra tas pats, kurį naudoja dashboard: `baseUrl` failo
`dashboard/dashboard_config.toml` skyriuje `[api]`. Naudokite HTTPS visada, kai kviečianti sistema ir
*digna* veikia ne tame pačiame kompiuteryje, nes kiekvienoje užklausoje yra API raktas.

---

## Autentifikavimas {: #authentication }

Kiekviena užklausa siunčia *digna* vartotojo API raktą antraštėje `Authorization`:

```text
Authorization: Bearer <api key>
```

Norėdami sukurti raktą, apatiniame kairiajame dashboard kampe atidarykite savo vartotojo profilį,
spauskite **API Keys**, tada **Add API Key**, ir nukopijuokite raktą. Jis rodomas tik vieną kartą.
Tie patys raktai tinka ir [digna MCP Server](../../ai_agents/overview.md).

Užklausa vykdoma su rakto vartotojo teisėmis. Kuriant, keičiant ir šalinant projekte reikia
redaktoriaus rolės; kitaip užklausa atmetama su `403` ir pranešimu
`You don't have permission to edit this project`.

!!! tip "Automatizavimui naudokite atskirą vartotoją"

    Kiekvienai integracijai sukurkite atskirą *digna* vartotoją, suteikite jam tik tuos projektus ir
    roles, kurių jam reikia, ir sukurkite jo raktą su galiojimo pabaigos data. Tada galėsite atšaukti
    vienos integracijos prieigą ištrindami jos raktą, nepaveikdami nieko kito.

---

## Užklausos siuntimas {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Atsakymai pateikiami JSON formatu. Sąrašai grąžinami kaip JSON masyvas. Užklausų turinys taip pat
yra JSON ir siunčiamas su `Content-Type: application/json`.

---

## Ribos ir filtrai {: #limits-and-filters }

Sąrašų galiniai taškai grąžina ne daugiau kaip `limit` elementų: pagal numatymą 200, daugiausia 5000.
Reikšmė už šio intervalo ribų atmetama su `400`. Poslinkio (offset) ar puslapio žetono nėra, todėl
sąrašą siaurinkite jo filtrais, pavyzdžiui, `project_id`, `data_source_id` arba inspekcijų būsenų
`start_date` ir `end_date`.

Užklausa, trunkanti ilgiau nei 60 sekundžių, nutraukiama su `408 Request Timeout`.

---

## Klaidos {: #errors }

Klaidos atsakymas turi JSON turinį su kodu ir pranešimu:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Būsena | Kodas | Reikšmė |
|---|---|---|
| `400` | `BAD_REQUEST` | Užklausa neteisinga, pavyzdžiui, `limit` už leistino intervalo ribų |
| `401` | `NOT_AUTHENTICATED` | API rakto nėra, jis netinkamo formato, nežinomas arba nebegalioja |
| `403` | `NOT_AUTHORIZED` | Rakto vartotojas neturi šiai užklausai reikalingos rolės |
| `403` | `INVALID_LICENSE` | *digna* licencijos galiojimas baigėsi |
| `404` | `NOT_FOUND` | Projektas, duomenų šaltinis ar kitas elementas neegzistuoja |
| `500` | `INTERNAL_ERROR` | Netikėta *digna* klaida. Išsami informacija yra backend'o žurnale |

`401` atsakymo `message` nurodo, kas negerai su raktu:

| Pranešimas | Priežastis |
|---|---|
| `Missing Authorization header` | Antraštė `Authorization` nebuvo išsiųsta |
| `Invalid Authorization header format` | Reikšmė neprasideda `Bearer ` |
| `Invalid API key` | Raktas neteisingas arba buvo ištrintas |
| `API key expired` | Rakto galiojimas baigėsi. Sukurkite naują |

---

## Inspekcijos paleidimas {: #running-an-inspection }

Įprasta integracija paleidžia inspekciją, kai baigiasi duomenų įkėlimas, palaukia, kol ji baigsis,
ir nuskaito rezultatą:

1. **Paleiskite inspekciją** užklausa [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Atsakyme yra užklausos `id`.
2. **Stebėkite jos eigą** užklausa [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Jos `status` pereina iš `PENDING` per `RUNNING` į `COMPLETED` arba baigiasi būsena `FAILED`,
   `ABORTED` ar `CANCELLED`. Klauskite pakartotinai kas kelias sekundes, kol būsena nebesikeis.
3. **Nuskaitykite rezultatą** užklausa [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   inspektuotoms datoms. Kiekvienas elementas turi bendrą `status`: `0` (OK), `1` (įspėjimas),
   `2` (kritinė) arba `-1` (būsenos nėra), ir kiekvieno modulio būseną su sėkmingų, neapibrėžtų ir
   nepavykusių patikrų skaičiumi.

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

## OpenAPI dokumentas {: #openapi-document }

Kiekviena *digna* diegtis aprašo šią API OpenAPI 3.1 dokumente ir siūlo interaktyvią Swagger UI,
kurioje galite išbandyti užklausas:

| Kas | Adresas |
|---|---|
| OpenAPI dokumentas | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Release 2026.11 dokumentas taip pat pasiekiamas čia: [openapi.json](openapi.json). Naudokite jį
klientui kita programavimo kalba sugeneruoti.

!!! note "Aprašyti tik /v1 galiniai taškai"

    Dashboard su backend'u bendrauja ir per kitus, vidinius galinius taškus. Jie nėra šios API dalis
    ir gali keistis bet kuriame leidime, todėl integracijas kurkite tik su `/v1` galiniais taškais.