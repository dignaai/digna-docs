# Yhdistä tekoälyagentit dignaan

**digna MCP Server** antaa tekoälyagenttien työskennellä *dignan* kanssa
[Model Context Protocolin](https://modelcontextprotocol.io) (MCP) avulla. Se on avoin standardi,
jota Claude, Gemini ja monet muut tekoälytyökalut tukevat. *dignaan* yhdistetty agentti voi vastata
kysymyksiin datastasi, tutkia hälytyksiä ja auttaa *dignan* konfiguroinnissa. Katso
[digna Agentic](../platform/agentic/Introduction.md), mitä agentit voivat tehdä.

Tämä sivu käsittelee *dignan* puolta, joka on sama kaikille tekoälyasiakkaille. Asiakaskohtaiset
ohjeet näyttävät sitten, mihin tiedot syötetään:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop ja custom connectorit
- [Gemini](gemini_mcp_guide.md): Antigravity ja Gemini CLI

!!! info "Beta"

    digna Agentic ja sen mukana digna MCP Server toimitetaan beetaversiona versiossa
    [Release 2026.11](../changelog/Release_202611.md).

---

## Ennen kuin aloitat {: #before-you-start }

Tarvitset:

- *dignan* Release 2026.11 tai uudemman
- Lisenssin, joka sisältää **digna Agenticin**. Ilman sitä MCP-palvelin hylkää jokaisen pyynnön
- *digna*-käyttäjätilin. Agentti toimii kussakin projektissa tämän käyttäjän oikeuksilla, katso
  [Oikeudet](../platform/agentic/how_it_works.md#permissions)
- Tekoälyasiakkaan, joka yhdistää etä-MCP-palvelimiin **streamable HTTP**:n kautta ja voi lähettää
  `Authorization`-otsakkeen

---

## 1. Selvitä MCP-päätepiste {: #1-find-the-mcp-endpoint }

MCP-palvelin on osa *dignan* backendia, joten mitään ylimääräistä ei tarvitse asentaa tai
käynnistää. Sen päätepiste on backendin osoite, jonka perään tulee `/mcp`:

```text
https://digna.example.com/mcp
```

Jos backend toimii suoraan isännässä ja portissa, esimerkiksi komennon
`digna serve --address 0.0.0.0 --port 8082` jälkeen, päätepiste on tämä osoite ja `/mcp`:

```text
http://digna-host:8082/mcp
```

Jos backendin edessä on käänteinen välityspalvelin (reverse proxy), sen täytyy välittää `/mcp`
backendille yhdessä `Authorization`-otsakkeen kanssa.

!!! warning "Käytä HTTPS:ää verkossa"

    Jokainen pyyntö sisältää API-avaimen. Käytä HTTPS:ää aina, kun tekoälyasiakas ja *digna* eivät
    ole samalla koneella.

### Mistä yhteys tulee {: #where-the-connection-comes-from }

Useimmat tekoälyasiakkaat yhdistävät siltä koneelta, jolla ne toimivat: Claude Code, Claude Desktop
paikallisen sillan kanssa, Antigravity ja Gemini CLI. Niitä varten *dignan* täytyy olla
tavoitettavissa vain kyseiseltä koneelta, esimerkiksi yrityksesi verkon sisällä.

Clauden **custom connectorit** toimivat toisin: Anthropicin pilvi yhdistää päätepisteeseen. Ne
toimivat vain, kun päätepiste on tavoitettavissa internetistä HTTPS:n kautta. Jos *digna*-asennus
on tavoitettavissa vain verkkosi sisältä, käytä asiakasta, joka toimii omalla koneellasi.

---

## 2. Luo API-avain {: #2-create-an-api-key }

Tekoälyasiakas todentaa itsensä *digna*-käyttäjän API-avaimella.

1. Kirjaudu sisään *dignaan*.
2. Avaa käyttäjäprofiilisi vasemmasta alakulmasta.
3. Klikkaa **API Keys** ja sitten **Add API Key**.
4. Anna nimi, joka kertoo, mihin avainta käytetään, esim. *Claude Code – Marcin*, ja valitse,
   milloin se vanhenee.
5. Kopioi avain. Se näytetään vain kerran.

Jokainen MCP-palvelimelle lähetettävä pyyntö sisältää avaimen tässä otsakkeessa:

```text
Authorization: Bearer <api key>
```

Sana `Bearer` ja sen jälkeinen välilyönti ovat osa otsakkeen arvoa.

---

## 3. Yhdistä tekoälyasiakkaasi {: #3-connect-your-ai-client }

| Tekoälyasiakas | Yhdistää | Ohje |
|---|---|---|
| Claude Code | Omalta koneeltasi | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop paikallisen sillan kanssa | Omalta koneeltasi | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Claude custom connector (claude.ai, Claude Desktop, Claude-mobiilisovellus) | Anthropicin pilvestä | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE ja sovellus | Omalta koneeltasi | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Omalta koneeltasi | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Myös muut MCP-asiakkaat toimivat, jos ne tukevat etäpalvelimia streamable HTTP:n kautta mukautetulla
otsakkeella. Useimmat niistä lukevat tämänkaltaisen konfiguraation. Tarkista tiedoston ja avainten
tarkat nimet asiakkaasi dokumentaatiosta:

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

---

## 4. Kokeile {: #4-try-it }

Kysy agentilta jotain, mihin vain *digna* osaa vastata:

- *"Listaa digna-projektini."*
- *"Mitkä projektin X datalähteet eivät ole tänään vihreitä?"*
- *"Selitä datalähteen Y viimeisin epäonnistunut tarkistus."*

Jos agentti listaa projektisi, yhteys toimii.

---

## Tietoturva {: #security }

- **Yksi avain henkilöä ja asiakasta kohden.** Silloin voit perua yksittäisen avaimen
  **Delete API Key** -toiminnolla vaikuttamatta keneenkään muuhun.
- **Valitse käyttäjä harkiten.** Agentti voi tehdä kaiken, mitä avaimen käyttäjä voi tehdä. Pelkkää
  datan tutkimista varten käytä käyttäjää, jolla on projekteissa lukijan rooli.
- **Pidä avaimet poissa jaetuista tiedostoista.** Älä commitoi konfiguraatiotiedostoa, joka sisältää
  avaimen. Jos asiakas tukee sitä, lue avain ympäristömuuttujasta.
- **Aseta vanhenemisaika.** Luo uusi avain ennen kuin vanha vanhenee, ja päivitä asiakas.
- **Tarkista työkalukutsut.** Pidä asiakkaan työkalukutsujen vahvistus päällä ainakin kutsuille,
  jotka muuttavat konfiguraatiota.

---

## Vianetsintä {: #troubleshooting }

### 401 Unauthorized

Vastaus kertoo syyn:

| Viesti | Syy |
|---|---|
| `Missing or malformed Authorization header` | Otsaketta ei lähetetty, tai arvo ei ala `Bearer `-merkkijonolla |
| `Invalid API key` | Avain on väärä, tai se on poistettu |
| `API key expired` | Avain on vanhentunut. Luo uusi |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

*dignan* lisenssissä ei ole digna Agentic -merkintää, tai merkintä on vanhentunut. Pyydä digna-tiimiltä
lisenssi, joka sisältää digna Agenticin, ja asenna se käyttöjärjestelmäsi asennusohjeen mukaisesti.

### Jokainen pyyntö epäonnistuu virheeseen virheellisestä lisenssistä

*dignan* lisenssi itsessään on vanhentunut. MCP-palvelin lakkaa vastaamasta yhdessä kojelaudan
kanssa, kunnes uusi lisenssi on asennettu.

### Agentti voi lukea mutta ei muuttaa konfiguraatiota

API-avaimen takana olevalla käyttäjällä ei ole kyseisessä projektissa editorin roolia. Käytä
käyttäjän avainta, jolla on editorin rooli, tai pyydä projektin ylläpitäjää muuttamaan roolia.

### Asiakas ei saa yhteyttä lainkaan

Yhdistävä kone ei tavoita päätepistettä. Avaa päätepisteen osoite kyseiseltä koneelta ja tarkista
palomuurit, välityspalvelimet ja varmenne. Clauden custom connectorin kohdalla tämä kone on
Anthropicin pilvessä, katso [Mistä yhteys tulee](#where-the-connection-comes-from).