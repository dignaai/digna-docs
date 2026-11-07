# digna REST API 2026.11

A *digna* REST API-jával saját eszközei és pipeline-jai HTTP-n és JSON-on keresztül dolgozhatnak
a *digna* rendszerrel: projekteket és inspekciós eredményeket olvashatnak, adatforrásokat,
adathalmazokat és attribútumokat kezelhetnek, és inspekciókat indíthatnak, például egy adatbetöltés
végén. A [Python SDK](../../sdk/Release%202026.11/index.md) ugyanezt az API-t használja.

Ez az oldal azt ismerteti, ami minden kérésben közös. Az erőforrásoldalak minden végpontot
felsorolnak a paramétereivel, a kérés törzsével, a válaszokkal és a sémákkal együtt:

| Erőforrás | Végpontok |
|---|---|
| [Projects](projects.md) | Projektek olvasása |
| [DB Connections](db_connections.md) | Adatbázis-kapcsolatok olvasása |
| [Data Sources](data_sources.md) | Adatforrások létrehozása, olvasása, frissítése és törlése |
| [Data Sets](data_sets.md) | Adathalmazok létrehozása, olvasása, frissítése és törlése |
| [Attributes](attributes.md) | Attribútumok létrehozása, olvasása, frissítése és törlése |
| [Check Definitions](check_definitions.md) | Ellenőrzésdefiníciók olvasása |
| [Inspection Requests](inspection_requests.md) | Inspekciók indítása és előrehaladásuk követése |
| [Inspection Statuses](inspection_statuses.md) | Inspekciós eredmények olvasása projektenként, adatforrásonként és adathalmazonként |

---

## Alap URL {: #base-url }

Az API a *digna* backend része. Minden útvonal `/v1` előtaggal kezdődik, a backend címe után:

```text
https://digna.example.com/v1/projects
```

A backend címe ugyanaz, amelyet a dashboard is használ: a `dashboard/dashboard_config.toml` fájl
`[api]` szakaszában megadott `baseUrl`. Használjon HTTPS-t, ha a hívó fél és a *digna* nem
ugyanazon a gépen fut, mert minden kérés API-kulcsot tartalmaz.

---

## Hitelesítés {: #authentication }

Minden kérés egy *digna* felhasználó API-kulcsát küldi el az `Authorization` fejlécben:

```text
Authorization: Bearer <api key>
```

Kulcs létrehozásához nyissa meg a felhasználói profilját a dashboard bal alsó sarkában, kattintson
az **API Keys**, majd az **Add API Key** elemre, és másolja ki a kulcsot. A kulcs csak egyszer
jelenik meg. Ugyanezek a kulcsok a [digna MCP Server](../../ai_agents/overview.md) esetében is
működnek.

A kérés a kulcshoz tartozó felhasználó jogosultságaival fut. A létrehozáshoz, módosításhoz és
törléshez editor szerepkör szükséges a projektben; ellenkező esetben a rendszer a kérést `403`
kóddal és a `You don't have permission to edit this project` üzenettel elutasítja.

!!! tip "Automatizáláshoz használjon külön felhasználót"

    Minden integrációhoz hozzon létre egy saját *digna* felhasználót, csak azokat a projekteket és
    szerepköröket adja meg neki, amelyekre szüksége van, és a kulcsát lejárati dátummal hozza
    létre. Így egy integráció hozzáférését a kulcsa törlésével visszavonhatja anélkül, hogy ez
    bárki mást érintene.

---

## Kérés küldése {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

A válaszok JSON formátumúak. A listák JSON-tömbként érkeznek. A kéréstörzsek szintén JSON
formátumúak, és `Content-Type: application/json` fejléccel kell elküldeni őket.

---

## Korlátok és szűrők {: #limits-and-filters }

A listázó végpontok legfeljebb `limit` elemet adnak vissza: alapértelmezés szerint 200-at, de
legfeljebb 5000-et. Az e tartományon kívüli értéket a rendszer `400` kóddal elutasítja. Nincs
eltolás (offset) és oldaltoken, ezért a listát a szűrőivel szűkítse, például a `project_id`, a
`data_source_id`, illetve az inspekciós állapotoknál a `start_date` és az `end_date` segítségével.

A 60 másodpercnél tovább tartó kérést a rendszer `408 Request Timeout` válasszal megszakítja.

---

## Hibák {: #errors }

A hibaválasz JSON-törzse egy kódot és egy üzenetet tartalmaz:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Állapot | Kód | Jelentés |
|---|---|---|
| `400` | `BAD_REQUEST` | A kérés érvénytelen, például a `limit` értéke a tartományon kívül esik |
| `401` | `NOT_AUTHENTICATED` | Az API-kulcs hiányzik, hibás formátumú, ismeretlen vagy lejárt |
| `403` | `NOT_AUTHORIZED` | A kulcs felhasználója nem rendelkezik a kéréshez szükséges szerepkörrel |
| `403` | `INVALID_LICENSE` | A *digna* licenc lejárt |
| `404` | `NOT_FOUND` | A projekt, az adatforrás vagy más elem nem létezik |
| `500` | `INTERNAL_ERROR` | Váratlan hiba a *digna* rendszerben. A részletek a backend naplójában találhatók |

Egy `401` válasz `message` mezője megmondja, mi a probléma a kulccsal:

| Üzenet | Ok |
|---|---|
| `Missing Authorization header` | Nem érkezett `Authorization` fejléc |
| `Invalid Authorization header format` | Az érték nem `Bearer ` előtaggal kezdődik |
| `Invalid API key` | A kulcs hibás, vagy törölték |
| `API key expired` | A kulcs lejárt. Hozzon létre újat |

---

## Inspekció futtatása {: #running-an-inspection }

Egy tipikus integráció egy adatbetöltés befejeztével elindít egy inspekciót, megvárja a végét, majd
beolvassa az eredményt:

1. **Indítsa el az inspekciót** a [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request)
   hívással. A válasz tartalmazza a kérés `id` azonosítóját.
2. **Kövesse az előrehaladását** a [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request)
   hívással. A `status` értéke `PENDING` értékről `RUNNING` értéken át `COMPLETED` értékre vált,
   vagy `FAILED`, `ABORTED` vagy `CANCELLED` értékkel zárul. Néhány másodpercenként kérdezze le
   újra, amíg már nem változik.
3. **Olvassa be az eredményt** a [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   hívással a vizsgált napokra. Minden elemnek van egy összesített `status` értéke: `0` (OK),
   `1` (figyelmeztetés), `2` (kritikus) vagy `-1` (nincs állapot), valamint modulonként egy
   állapota a sikeres, bizonytalan és sikertelen ellenőrzések számával.

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

## OpenAPI-dokumentum {: #openapi-document }

Minden *digna* telepítés egy OpenAPI 3.1 dokumentumban írja le ezt az API-t, és interaktív
Swagger UI-t kínál, amelyben kipróbálhatók a kérések:

| Mi | Cím |
|---|---|
| OpenAPI-dokumentum | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

A Release 2026.11 dokumentuma itt is elérhető: [openapi.json](openapi.json). Ezzel klienst
generálhat más programozási nyelvre.

!!! note "Csak a /v1 végpontokra vonatkozik"

    A dashboard más, belső végpontokon keresztül is kommunikál a backenddel. Ezek nem részei ennek
    az API-nak, és bármely kiadással megváltozhatnak, ezért az integrációkat kizárólag a `/v1`
    végpontokra építse.