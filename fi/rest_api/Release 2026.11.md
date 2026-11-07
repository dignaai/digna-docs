# digna REST API 2026.11

*dignan* REST API:n avulla omat työkalusi ja putkesi voivat käyttää *dignaa* HTTP:n ja JSONin
kautta: lukea projekteja ja tarkastustuloksia, hallita tietolähteitä, datasettejä ja attribuutteja
sekä käynnistää tarkastuksia esimerkiksi datan latauksen päätteeksi. [Python SDK](../../sdk/Release%202026.11/index.md)
käyttää samaa API:a.

Tämä sivu kattaa sen, mikä on yhteistä kaikille pyynnöille. Resurssisivuilla on kuvattu jokainen
päätepiste parametreineen, pyynnön runkoineen, vastauksineen ja skeemoineen:

| Resurssi | Päätepisteet |
|---|---|
| [Projects](projects.md) | Projektien lukeminen |
| [DB Connections](db_connections.md) | Tietokantayhteyksien lukeminen |
| [Data Sources](data_sources.md) | Tietolähteiden luonti, luku, päivitys ja poisto |
| [Data Sets](data_sets.md) | Datasettien luonti, luku, päivitys ja poisto |
| [Attributes](attributes.md) | Attribuuttien luonti, luku, päivitys ja poisto |
| [Check Definitions](check_definitions.md) | Tarkistusmääritysten lukeminen |
| [Inspection Requests](inspection_requests.md) | Tarkastusten käynnistäminen ja niiden etenemisen seuraaminen |
| [Inspection Statuses](inspection_statuses.md) | Tarkastustulosten lukeminen projekteittain, tietolähteittäin ja dataseteittäin |

---

## Perus-URL {: #base-url }

API on osa *dignan* backendia. Jokainen polku alkaa backendin osoitteen jälkeen merkkijonolla `/v1`:

```text
https://digna.example.com/v1/projects
```

Backendin osoite on sama, jota dashboard käyttää: `baseUrl` tiedoston
`dashboard/dashboard_config.toml` osiossa `[api]`. Käytä HTTPS:ää aina, kun kutsuja ja *digna* eivät
ole samalla koneella, koska jokainen pyyntö sisältää API-avaimen.

---

## Todennus {: #authentication }

Jokainen pyyntö lähettää *digna*-käyttäjän API-avaimen `Authorization`-otsakkeessa:

```text
Authorization: Bearer <api key>
```

Luo avain avaamalla käyttäjäprofiilisi dashboardin vasemmasta alakulmasta, klikkaamalla
**API Keys** ja sitten **Add API Key** ja kopioimalla avain. Se näytetään vain kerran. Samat
avaimet toimivat myös [digna MCP Serverille](../../ai_agents/overview.md).

Pyyntö suoritetaan avaimen käyttäjän oikeuksilla. Luominen, muuttaminen ja poistaminen edellyttävät
projektissa editorin roolia; muuten pyyntö hylätään koodilla `403` ja viestillä
`You don't have permission to edit this project`.

!!! tip "Käytä automaatiolle omaa käyttäjää"

    Luo jokaista integraatiota varten oma *digna*-käyttäjä, anna sille vain sen tarvitsemat projektit
    ja roolit ja luo sen avain vanhenemispäivän kanssa. Silloin voit perua yksittäisen integraation
    pääsyn poistamalla sen avaimen vaikuttamatta keneenkään muuhun.

---

## Pyynnön tekeminen {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Vastaukset ovat JSONia. Listat palautetaan JSON-taulukkona. Myös pyyntöjen rungot ovat JSONia, ja ne
lähetetään otsakkeella `Content-Type: application/json`.

---

## Rajat ja suodattimet {: #limits-and-filters }

Listapäätepisteet palauttavat enintään `limit` kohdetta: oletuksena 200 ja enintään 5000. Tämän
välin ulkopuolinen arvo hylätään koodilla `400`. Offsetia tai sivutunnistetta ei ole, joten rajaa
listaa sen sijaan sen suodattimilla, esimerkiksi `project_id`, `data_source_id` tai tarkastusten
tiloissa `start_date` ja `end_date`.

Pyyntö, joka kestää yli 60 sekuntia, peruutetaan vastauksella `408 Request Timeout`.

---

## Virheet {: #errors }

Virhevastauksella on JSON-runko, jossa on koodi ja viesti:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Tila | Koodi | Merkitys |
|---|---|---|
| `400` | `BAD_REQUEST` | Pyyntö on virheellinen, esimerkiksi `limit` on sallitun välin ulkopuolella |
| `401` | `NOT_AUTHENTICATED` | API-avain puuttuu, on väärin muotoiltu, tuntematon tai vanhentunut |
| `403` | `NOT_AUTHORIZED` | Avaimen käyttäjältä puuttuu rooli, jota pyyntö edellyttää |
| `403` | `INVALID_LICENSE` | *digna*-lisenssi on vanhentunut |
| `404` | `NOT_FOUND` | Projektia, tietolähdettä tai muuta kohdetta ei ole olemassa |
| `500` | `INTERNAL_ERROR` | Odottamaton virhe *dignassa*. Yksityiskohdat löytyvät backendin lokista |

`401`-vastauksen `message` kertoo, mikä avaimessa on vialla:

| Viesti | Syy |
|---|---|
| `Missing Authorization header` | `Authorization`-otsaketta ei lähetetty |
| `Invalid Authorization header format` | Arvo ei ala `Bearer `-merkkijonolla |
| `Invalid API key` | Avain on väärä, tai se on poistettu |
| `API key expired` | Avain on vanhentunut. Luo uusi |

---

## Tarkastuksen ajaminen {: #running-an-inspection }

Tyypillinen integraatio käynnistää tarkastuksen, kun datan lataus on valmis, odottaa sen
valmistumista ja lukee tuloksen:

1. **Käynnistä tarkastus** pyynnöllä [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Vastaus sisältää pyynnön `id`:n.
2. **Seuraa sen etenemistä** pyynnöllä [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Sen `status` etenee tilasta `PENDING` tilan `RUNNING` kautta tilaan `COMPLETED` tai päättyy tilaan
   `FAILED`, `ABORTED` tai `CANCELLED`. Kysy uudelleen muutaman sekunnin välein, kunnes se ei enää muutu.
3. **Lue tulos** pyynnöllä [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   tarkastetuille päivämäärille. Jokaisella kohteella on kokonaistila `status`: `0` (OK), `1` (varoitus),
   `2` (kriittinen) tai `-1` (ei tilaa), sekä moduulikohtainen tila, jossa on läpäistyjen, epävarmojen
   ja epäonnistuneiden tarkistusten määrä.

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

## OpenAPI-dokumentti {: #openapi-document }

Jokainen *digna*-asennus kuvaa tämän API:n OpenAPI 3.1 -dokumentissa ja tarjoaa interaktiivisen
Swagger UI:n, jossa voit kokeilla pyyntöjä sitä vasten:

| Mikä | Osoite |
|---|---|
| OpenAPI-dokumentti | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Release 2026.11:n dokumentti on saatavilla myös täältä: [openapi.json](openapi.json). Voit
generoida sen avulla asiakasohjelman toisella ohjelmointikielellä.

!!! note "Vain /v1-päätepisteet ovat mukana"

    Dashboard viestii backendin kanssa myös muiden, sisäisten päätepisteiden kautta. Ne eivät kuulu
    tähän API:in ja voivat muuttua missä tahansa julkaisussa, joten rakenna integraatiot vain
    `/v1`-päätepisteiden varaan.