---
title: Přehled REST API 2026.11 | Dokumentace digna
description: Pomocí digna REST API v1 můžete číst projekty a výsledky inspekcí, spravovat datové zdroje, datové sady a atributy a spouštět inspekce — základní URL, ověřování klíčem API, stránkování, chyby a dokument OpenAPI.
image: /assets/logo_square.png
keywords: digna REST API, digna API, digna OpenAPI, klíč API digna, API požadavků na inspekci, API pro kvalitu dat, Swagger UI
---

# digna REST API 2026.11

REST API *digna* umožňuje vašim vlastním nástrojům a pipelinám pracovat s *digna* přes HTTP a JSON:
číst projekty a výsledky inspekcí, spravovat datové zdroje, datové sady a atributy a spouštět
inspekce, například na konci načítání dat. [Python SDK](../../sdk/Release%202026.11/index.md)
používá stejné API.

Tato stránka popisuje, co mají všechny požadavky společné. Stránky jednotlivých zdrojů uvádějí každý
koncový bod s jeho parametry, tělem požadavku, odpověďmi a schématy:

| Zdroj | Koncové body |
|---|---|
| [Projects](projects.md) | Čtení projektů |
| [DB Connections](db_connections.md) | Čtení databázových připojení |
| [Data Sources](data_sources.md) | Vytváření, čtení, aktualizace a mazání datových zdrojů |
| [Data Sets](data_sets.md) | Vytváření, čtení, aktualizace a mazání datových sad |
| [Attributes](attributes.md) | Vytváření, čtení, aktualizace a mazání atributů |
| [Check Definitions](check_definitions.md) | Čtení definic kontrol |
| [Inspection Requests](inspection_requests.md) | Spouštění inspekcí a sledování jejich průběhu |
| [Inspection Statuses](inspection_statuses.md) | Čtení výsledků inspekcí podle projektu, datového zdroje a datové sady |

---

## Základní URL {: #base-url }

API je součástí backendu *digna*. Každá cesta začíná `/v1`, které následuje za adresou backendu:

```text
https://digna.example.com/v1/projects
```

Adresa backendu je stejná, jakou používá dashboard: `baseUrl` v sekci `[api]` souboru
`dashboard/dashboard_config.toml`. Používejte HTTPS vždy, když volající a *digna* neběží na stejném
počítači, protože každý požadavek nese klíč API.

---

## Ověřování {: #authentication }

Každý požadavek posílá klíč API uživatele *digna* v hlavičce `Authorization`:

```text
Authorization: Bearer <api key>
```

Klíč vytvoříte tak, že otevřete svůj uživatelský profil v levém dolním rohu dashboardu, kliknete na
**API Keys**, poté na **Add API Key** a klíč zkopírujete. Zobrazí se pouze jednou. Stejné klíče
fungují i pro [digna MCP Server](../../ai_agents/overview.md).

Požadavek se provádí s oprávněními uživatele, kterému klíč patří. Vytváření, změny a mazání vyžadují
v projektu roli editor; jinak je požadavek odmítnut s kódem `403` a zprávou
`You don't have permission to edit this project`.

!!! tip "Pro automatizaci používejte vyhrazeného uživatele"

    Pro každou integraci vytvořte samostatného uživatele *digna*, přidělte mu jen projekty a role,
    které potřebuje, a jeho klíč vytvořte s datem vypršení platnosti. Přístup jedné integrace pak
    můžete odvolat smazáním jejího klíče, aniž byste ovlivnili kohokoli jiného.

---

## Odeslání požadavku {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Odpovědi jsou ve formátu JSON. Seznamy se vracejí jako pole JSON. Těla požadavků jsou rovněž ve
formátu JSON a posílají se s hlavičkou `Content-Type: application/json`.

---

## Limity a filtry {: #limits-and-filters }

Koncové body vracející seznamy vrátí nejvýše `limit` položek: ve výchozím nastavení 200, maximálně
5000. Hodnota mimo tento rozsah je odmítnuta s kódem `400`. Neexistuje žádný offset ani token
stránky, proto seznam zužujte jeho filtry, například `project_id`, `data_source_id` nebo
`start_date` a `end_date` u stavů inspekcí.

Požadavek, který trvá déle než 60 sekund, je zrušen s `408 Request Timeout`.

---

## Chyby {: #errors }

Chybová odpověď má tělo JSON s kódem a zprávou:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Stav | Kód | Význam |
|---|---|---|
| `400` | `BAD_REQUEST` | Požadavek je neplatný, například `limit` mimo rozsah |
| `401` | `NOT_AUTHENTICATED` | Klíč API chybí, má chybný formát, je neznámý nebo vypršela jeho platnost |
| `403` | `NOT_AUTHORIZED` | Uživatel klíče nemá roli, kterou tento požadavek vyžaduje |
| `403` | `INVALID_LICENSE` | Vypršela platnost licence *digna* |
| `404` | `NOT_FOUND` | Projekt, datový zdroj nebo jiná položka neexistuje |
| `500` | `INTERNAL_ERROR` | Neočekávaná chyba v *digna*. Podrobnosti najdete v logu backendu |

Pole `message` odpovědi `401` uvádí, co je s klíčem špatně:

| Zpráva | Příčina |
|---|---|
| `Missing Authorization header` | Nebyla odeslána hlavička `Authorization` |
| `Invalid Authorization header format` | Hodnota nezačíná `Bearer ` |
| `Invalid API key` | Klíč je chybný, nebo byl smazán |
| `API key expired` | Platnost klíče vypršela. Vytvořte nový |

---

## Spuštění inspekce {: #running-an-inspection }

Typická integrace spustí inspekci po dokončení načítání dat, počká na její dokončení a přečte
výsledek:

1. **Spusťte inspekci** pomocí [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Odpověď obsahuje `id` požadavku.
2. **Sledujte její průběh** pomocí [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Její `status` přechází z `PENDING` přes `RUNNING` do `COMPLETED`, nebo skončí jako `FAILED`,
   `ABORTED` či `CANCELLED`. Dotazujte se znovu každých několik sekund, dokud se přestane měnit.
3. **Přečtěte výsledek** pomocí [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   pro dny, které inspekce zpracovala. Každá položka má celkový `status`: `0` (OK), `1` (varování),
   `2` (kritický) nebo `-1` (bez stavu), a stav pro každý modul s počtem úspěšných, nejistých
   a neúspěšných kontrol.

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

Každá instalace *digna* popisuje toto API v dokumentu OpenAPI 3.1 a nabízí interaktivní Swagger UI,
ve kterém si můžete požadavky vyzkoušet:

| Co | Adresa |
|---|---|
| Dokument OpenAPI | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Dokument pro Release 2026.11 je k dispozici také zde: [openapi.json](openapi.json). Můžete z něj
vygenerovat klienta v jiném jazyce.

!!! note "Pokryty jsou pouze koncové body /v1"

    Dashboard komunikuje s backendem i přes jiné, interní koncové body. Ty nejsou součástí tohoto
    API a mohou se změnit s kterýmkoli vydáním, proto integrace stavějte pouze na koncových bodech
    `/v1`.
