# Yhdistä Claude dignaan

Tämä ohje yhdistää Clauden **digna MCP Serveriin**. Tarvitset *digna*-asennuksesi MCP-päätepisteen
ja API-avaimen, kuten [tekoälyagenttien yleiskatsauksessa](overview.md) kuvataan.

Esimerkeissä päätepisteenä on `https://digna.example.com/mcp`. Korvaa se omallasi.

## Valitse yhteystapa {: #choose-how-to-connect }

| Claude-tuote | Yhdistää | Toimii *dignan* kanssa verkkosi sisällä |
|---|---|---|
| [Claude Code](#claude-code) | Omalta koneeltasi | Kyllä |
| [Claude Desktop paikallisen sillan kanssa](#claude-desktop-with-a-local-bridge) | Omalta koneeltasi | Kyllä |
| [Custom connector](#custom-connector) claude.aissa, Claude Desktopissa ja Claude-mobiilisovelluksessa | Anthropicin pilvestä | Ei. Päätepisteen täytyy olla tavoitettavissa internetistä |

Jos *digna*-asennus toimii yrityksesi verkon sisällä, käytä Claude Codea tai Claude Desktopia
paikallisen sillan kanssa.

---

## Claude Code {: #claude-code }

### 1. Lisää palvelin {: #1-add-the-server }

Tallenna API-avain ympäristömuuttujaan ja lisää sitten palvelin:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Shell täyttää `$DIGNA_API_KEY`:n arvon, kun suoritat komennon, joten Claude Code tallentaa avaimen
omaan konfiguraatioonsa.

`--scope` määrää, missä palvelin on käytettävissä:

| Scope | Käytettävissä |
|---|---|
| `local` (oletus) | Sinulle, vain nykyisessä projektissa |
| `user` | Sinulle, kaikissa projekteissa |
| `project` | Kaikille projektissa työskenteleville, projektin `.mcp.json`-tiedoston kautta |

### 2. Jaa palvelin tiimisi kanssa (valinnainen) {: #2-share-the-server-with-your-team }

Jos haluat antaa kaikille projektissa saman palvelimen, lisää `.mcp.json`-tiedosto projektin
juureen. Älä kirjoita avainta tiedostoon. Claude Code täyttää `${DIGNA_API_KEY}`:n kunkin henkilön
omasta ympäristöstä:

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${DIGNA_API_KEY}"
      }
    }
  }
}
```

Jokainen asettaa `DIGNA_API_KEY`:n arvoksi oman avaimensa. Kun Claude Code löytää tiedoston
ensimmäisen kerran, se kysyy, käytetäänkö sen palvelimia.

### 3. Tarkista yhteys {: #3-verify-the-connection }

Shellistä:

```bash
claude mcp list
```

Palvelimen `digna` täytyy näyttää `✔ Connected`. Claude Code -istunnossa voit suorittaa `/mcp`
nähdäksesi palvelimen ja sen työkalut.

---

## Claude Desktop paikallisen sillan kanssa {: #claude-desktop-with-a-local-bridge }

Claude Desktopin konfiguraatiotiedosto käynnistää paikallisia MCP-palvelimia koneellasi. Pieni
silta, avoimen lähdekoodin [`mcp-remote`](https://github.com/geelen/mcp-remote)-paketti, toimii
siellä ja välittää jokaisen pyynnön *dignan* päätepisteeseen API-avaimesi kanssa. Koska silta toimii
koneellasi, tämä toimii *dignan* kanssa yrityksesi verkon sisällä.

!!! note "Yhteisön paketti"

    `mcp-remote`-pakettia ylläpitää sen avoimen lähdekoodin yhteisö, ei Anthropic eikä digna.
    Tarkista ennen käyttöä, että organisaatiosi sallii sen.

### 1. Asenna Node.js {: #1-install-nodejs }

Silta vaatii [Node.js](https://nodejs.org):n version 18 tai uudemman. Claude Desktop käyttää
järjestelmääsi asennettua Node.js-versiota. Tarkista se komennolla:

```bash
node --version
```

### 2. Muokkaa konfiguraatiotiedostoa {: #2-edit-the-configuration-file }

Avaa `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Lisää palvelin `digna`. Jos tiedostossa on jo `mcpServers`-osio, lisää `digna`-merkintä siihen:

```json
{
  "mcpServers": {
    "digna": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://digna.example.com/mcp",
        "--transport",
        "http-only",
        "--header",
        "Authorization:${AUTH_HEADER}"
      ],
      "env": {
        "AUTH_HEADER": "Bearer <api key>"
      }
    }
  }
}
```

!!! warning "Pidä otsake täsmälleen esitetyssä muodossa"

    Kirjoita `Authorization:${AUTH_HEADER}` ilman välilyöntejä ja laita `Bearer <api key>`
    kohtaan `env`. Windowsin Claude Desktop ei escapeoi `args`-kohdan välilyöntejä, joten siellä
    oleva välilyönti rikkoo otsakkeen.

### 3. Käynnistä Claude Desktop uudelleen {: #3-restart-claude-desktop }

Sulje Claude Desktop kokonaan ja käynnistä se uudelleen. Klikkaa uudessa keskustelussa **+** ja avaa
**Connectors**: `digna` täytyy olla listalla ja päällä.

---

## Custom connector {: #custom-connector }

Custom connector tuo *dignan* käyttöön claude.aissa, Claude Desktopissa ja Clauden
mobiilisovelluksissa ilman paikallista asennusta. Anthropicin pilvi yhdistää päätepisteeseen, joten
tämä toimii vain, kun:

- *dignan* päätepiste on tavoitettavissa internetistä HTTPS:n kautta
- Claude-organisaatiollasi on **Request headers** -vaihtoehto **Add custom connector** -valintaikkunassa.
  Anthropic tarjoaa sitä beetana rajatulle joukolle organisaatioita

!!! warning "Ei verkkosi sisällä olevalle dignalle"

    Clauden MCP-tunnelit, jotka tavoittavat yksityisen verkon sisällä olevia palvelimia, vaativat
    MCP-palvelimelta OAuthin. digna MCP Server todentaa API-avaimilla, joten tunnelia ei voi käyttää.
    Käytä sen sijaan [Claude Codea](#claude-code) tai
    [Claude Desktopia paikallisen sillan kanssa](#claude-desktop-with-a-local-bridge).

### 1. Avaa connector-asetukset {: #1-open-the-connector-settings }

- **Free-, Pro-, Max- ja Ultra-tilaukset**: siirry kohtaan **Customize > Connectors** ja klikkaa
  **Add custom connector**.
- **Team- ja Enterprise-tilaukset**: Owner siirtyy kohtaan **Organization settings > Connectors**,
  klikkaa **Add** ja sitten **Custom** ja valitsee **Web**, jos tyyppiä kysytään.

### 2. Syötä connectorin tiedot {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: valitse otsakkeen nimeksi `authorization`, syötä arvoksi `Bearer <api key>`
   sanan `Bearer` ja välilyönnin kanssa, ja merkitse se **Required**.
4. Klikkaa **Add**.

!!! warning "Kaikki jakavat saman avaimen"

    Jokainen connectoria käyttävä jäsen työskentelee samalla API-avaimella ja siten samalla
    *digna*-käyttäjällä. Luo connectorille oma *digna*-käyttäjä ja anna sille vain ne projektit ja
    roolit, jotka kaikilla saa olla, esim. lukijan rooli.

Team- ja Enterprise-tilauksissa jäsenet yhdistävät sitten kohdassa **Customize > Connectors**, jossa
connectorilla on tunniste **Custom**.

Claude ei voi muuttaa olemassa olevan connectorin otsaketta. Jos haluat käyttää uutta avainta,
poista connector ja lisää se uudelleen.

---

## Clauden vianetsintä {: #troubleshooting-claude }

### claude mcp list näyttää Failed to connect

Suorita `claude mcp get digna` nähdäksesi syyn. `401` tarkoittaa, että avain hylättiin; katso
[401 Unauthorized](overview.md#troubleshooting). Claude Code varoittaa myös välilyönneistä tai
rivinvaihdosta avaimen alussa tai lopussa, joita tulee usein mukaan kopioitaessa.

### digna ei näy Claude Desktopissa

- Tarkista, että Node.js 18 tai uudempi on asennettu: `node --version`.
- Tarkista, että `claude_desktop_config.json` on kelvollista JSONia. Puuttuva pilkku estää kaikkien
  tiedoston palvelimien latautumisen.
- Sulje Claude Desktop kokonaan, ei vain ikkunaa, ja käynnistä se uudelleen.

### Custom connector ei tavoita palvelinta

Anthropicin pilvi ei tavoita päätepistettä. Tarkista, että se on tavoitettavissa internetistä
HTTPS:n kautta kelvollisella varmenteella, tai yhdistä sen sijaan [Claude Coden](#claude-code)
kautta.

---

## Katso myös {: #see-also }

- [Tekoälyagenttien yleiskatsaus](overview.md): päätepiste, API-avain, tietoturva ja yleinen vianetsintä
- [Gemini](gemini_mcp_guide.md): yhdistä Antigravity tai Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): mitä tekoälyagentit voivat tehdä *dignan* kanssa