# digna REST API 2026.11

*digna* REST API ļauj jūsu rīkiem un datu konveijeriem strādāt ar *digna*, izmantojot HTTP un JSON:
lasīt projektus un inspekciju rezultātus, pārvaldīt datu avotus, datu kopas un atribūtus un palaist
inspekcijas, piemēram, datu ielādes beigās. [Python SDK](../../sdk/Release%202026.11/index.md)
izmanto to pašu API.

Šajā lappusē aprakstīts tas, kas ir kopīgs visiem pieprasījumiem. Resursu lappusēs ir uzskaitīts
katrs galapunkts ar tā parametriem, pieprasījuma pamattekstu, atbildēm un shēmām:

| Resurss | Galapunkti |
|---|---|
| [Projects](projects.md) | Projektu lasīšana |
| [DB Connections](db_connections.md) | Datu bāzes savienojumu lasīšana |
| [Data Sources](data_sources.md) | Datu avotu izveide, lasīšana, atjaunināšana un dzēšana |
| [Data Sets](data_sets.md) | Datu kopu izveide, lasīšana, atjaunināšana un dzēšana |
| [Attributes](attributes.md) | Atribūtu izveide, lasīšana, atjaunināšana un dzēšana |
| [Check Definitions](check_definitions.md) | Pārbaužu definīciju lasīšana |
| [Inspection Requests](inspection_requests.md) | Inspekciju palaišana un to norises sekošana |
| [Inspection Statuses](inspection_statuses.md) | Inspekciju rezultātu lasīšana pa projektiem, datu avotiem un datu kopām |

---

## Bāzes URL {: #base-url }

API ir daļa no *digna* backend. Katrs ceļš sākas ar `/v1` aiz backend adreses:

```text
https://digna.example.com/v1/projects
```

Backend adrese ir tā pati, ko izmanto dashboard: `baseUrl` faila `dashboard/dashboard_config.toml`
sadaļā `[api]`. Izmantojiet HTTPS vienmēr, kad izsaucējs un *digna* nedarbojas vienā datorā, jo katrs
pieprasījums satur API atslēgu.

---

## Autentifikācija {: #authentication }

Katrs pieprasījums nosūta *digna* lietotāja API atslēgu galvenē `Authorization`:

```text
Authorization: Bearer <api key>
```

Lai izveidotu atslēgu, atveriet savu lietotāja profilu dashboard apakšējā kreisajā stūrī,
noklikšķiniet uz **API Keys**, pēc tam uz **Add API Key** un nokopējiet atslēgu. Tā tiek parādīta
tikai vienu reizi. Tās pašas atslēgas der arī [digna MCP Server](../../ai_agents/overview.md).

Pieprasījums tiek izpildīts ar atslēgas lietotāja atļaujām. Izveidei, mainīšanai un dzēšanai
projektā ir nepieciešama editor loma; pretējā gadījumā pieprasījums tiek noraidīts ar `403` un
ziņojumu `You don't have permission to edit this project`.

!!! tip "Automatizācijai izmantojiet atsevišķu lietotāju"

    Katrai integrācijai izveidojiet savu *digna* lietotāju, piešķiriet tam tikai nepieciešamos
    projektus un lomas un izveidojiet tā atslēgu ar derīguma termiņu. Tad varat atsaukt vienas
    integrācijas piekļuvi, izdzēšot tās atslēgu, neietekmējot nevienu citu.

---

## Pieprasījuma veikšana {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Atbildes ir JSON formātā. Saraksti tiek atgriezti kā JSON masīvs. Arī pieprasījumu pamatteksts ir
JSON, un to nosūta ar `Content-Type: application/json`.

---

## Ierobežojumi un filtri {: #limits-and-filters }

Sarakstu galapunkti atgriež ne vairāk kā `limit` vienumus: pēc noklusējuma 200 un līdz 5000. Vērtība
ārpus šī diapazona tiek noraidīta ar `400`. Nobīdes (offset) vai lappuses marķiera nav, tāpēc
sašauriniet sarakstu ar tā filtriem, piemēram, `project_id`, `data_source_id` vai inspekciju statusu
`start_date` un `end_date`.

Pieprasījums, kas ilgst vairāk nekā 60 sekundes, tiek atcelts ar `408 Request Timeout`.

---

## Kļūdas {: #errors }

Kļūdas atbildei ir JSON pamatteksts ar kodu un ziņojumu:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Statuss | Kods | Nozīme |
|---|---|---|
| `400` | `BAD_REQUEST` | Pieprasījums nav derīgs, piemēram, `limit` ir ārpus diapazona |
| `401` | `NOT_AUTHENTICATED` | API atslēgas nav, tai ir nepareizs formāts, tā ir nezināma vai beigusies |
| `403` | `NOT_AUTHORIZED` | Atslēgas lietotājam nav šim pieprasījumam nepieciešamās lomas |
| `403` | `INVALID_LICENSE` | *digna* licences derīgums ir beidzies |
| `404` | `NOT_FOUND` | Projekts, datu avots vai cits vienums neeksistē |
| `500` | `INTERNAL_ERROR` | Neparedzēta kļūda *digna*. Sīkāka informācija ir backend žurnālā |

`401` atbildes `message` norāda, kas ir nepareizi ar atslēgu:

| Ziņojums | Cēlonis |
|---|---|
| `Missing Authorization header` | Galvene `Authorization` netika nosūtīta |
| `Invalid Authorization header format` | Vērtība nesākas ar `Bearer ` |
| `Invalid API key` | Atslēga ir nepareiza vai ir dzēsta |
| `API key expired` | Atslēgas derīgums ir beidzies. Izveidojiet jaunu |

---

## Inspekcijas palaišana {: #running-an-inspection }

Tipiska integrācija palaiž inspekciju, kad datu ielāde ir pabeigta, gaida tās beigas un nolasa
rezultātu:

1. **Palaidiet inspekciju** ar [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Atbildē ir pieprasījuma `id`.
2. **Sekojiet tās norisei** ar [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Tās `status` mainās no `PENDING` caur `RUNNING` uz `COMPLETED` vai beidzas kā `FAILED`,
   `ABORTED` vai `CANCELLED`. Vaicājiet atkārtoti ik pēc dažām sekundēm, līdz tas vairs nemainās.
3. **Nolasiet rezultātu** ar [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   par inspicētajiem datumiem. Katram vienumam ir kopējais `status`: `0` (OK), `1` (brīdinājums),
   `2` (kritisks) vai `-1` (nav statusa), un katra moduļa statuss ar sekmīgo, nenoteikto un
   neizdevušos pārbaužu skaitu.

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

## OpenAPI dokuments {: #openapi-document }

Katra *digna* instalācija apraksta šo API OpenAPI 3.1 dokumentā un piedāvā interaktīvu Swagger UI,
kurā varat izmēģināt pieprasījumus:

| Kas | Adrese |
|---|---|
| OpenAPI dokuments | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Release 2026.11 dokuments ir pieejams arī šeit: [openapi.json](openapi.json). Izmantojiet to, lai
ģenerētu klientu citā programmēšanas valodā.

!!! note "Aprakstīti tikai /v1 galapunkti"

    Dashboard sazinās ar backend arī caur citiem, iekšējiem galapunktiem. Tie nav daļa no šī API un
    var mainīties jebkurā laidienā, tāpēc veidojiet integrācijas tikai uz `/v1` galapunktiem.