# Yhdistä Gemini dignaan

Tämä ohje yhdistää Googlen Gemini-työkalut **digna MCP Serveriin**. Tarvitset *digna*-asennuksesi
MCP-päätepisteen ja API-avaimen, kuten [tekoälyagenttien yleiskatsauksessa](overview.md) kuvataan.

Esimerkeissä päätepisteenä on `https://digna.example.com/mcp`. Korvaa se omallasi.

## Valitse työkalu {: #choose-your-tool }

| Työkalu | Kenelle | Konfiguraatio |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE ja sovellus | Googlen agenttityökalut. Antigravity CLI korvasi Gemini CLI:n henkilökohtaisille Google-tileille kesäkuussa 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard- ja Enterprise-lisenssit sekä maksulliset Gemini API -avaimet | `settings.json` tai `gemini mcp add` |
| Gemini Enterprise -sovellus | — | Ei tuettu. Sen mukautettu MCP-connector kirjautuu OAuthilla tai Google Cloud -palvelutilillä, kun taas digna MCP Server todentaa API-avaimilla |

Kaikki nämä työkalut yhdistävät siltä koneelta, jolla ne toimivat, joten ne toimivat *dignan*
kanssa yrityksesi verkon sisällä, kunhan kyseinen kone tavoittaa päätepisteen.

---

## Antigravity {: #antigravity }

Antigravity lukee MCP-palvelimensa tiedostosta `mcp_config.json`, jota CLI, IDE ja sovellus käyttävät
yhdessä.

### 1. Avaa mcp_config.json {: #1-open-mcp-config-json }

| Scope | Tiedosto |
|---|---|
| Kaikki projektisi | `~/.gemini/config/mcp_config.json` |
| Yksi työtila | `.agents/mcp_config.json` työtilassa |

Käytössä olevan tiedoston avaaminen:

- **CLI**: kirjoita `/mcp` ja paina ++enter++ avataksesi MCP-hallinnan.
- **IDE**: avaa agentin sivupaneelissa valikko **…**, valitse **MCP Servers**, sitten
  **Manage MCP Servers** ja sitten **View raw config**.
- **Sovellus**: siirry kohtaan **Customizations** > **Installed** > **MCP Servers** ja käytä
  toimintoa **Copy Config File Path**.

### 2. Lisää digna-palvelin {: #2-add-the-digna-server }

Lisää `digna`-merkintä. Jos tiedostossa on jo `mcpServers`-osio, lisää se sinne:

```json
{
  "mcpServers": {
    "digna": {
      "serverUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

Antigravity tavoittaa etäpalvelimet vain streamable HTTP:n kautta, jota digna MCP Server käyttää.
Kirjoita päätepiste avaimella `serverUrl`; Gemini CLI:n `httpUrl`-avainta ei tueta.

### 3. Tarkista yhteys {: #3-verify-the-connection }

Kirjoita CLI:ssä `/mcp`: MCP-hallinta näyttää palvelimen `digna` tilan ja työkalut, ja se voi
ladata konfiguraation uudelleen ja näyttää yhteyslokit. IDE:ssä palvelin näkyy kohdassa
**Manage MCP Servers**.

!!! warning "Suojaa tiedosto"

    `mcp_config.json` sisältää API-avaimen selväkielisenä. Pidä työtilan `.agents/mcp_config.json`
    poissa versionhallinnasta, ja anna vain oman tilisi lukea globaalia tiedostoa.

---

## Gemini CLI {: #gemini-cli }

### 1. Lisää palvelin {: #1-add-the-server }

Tallenna API-avain ympäristömuuttujaan ja lisää sitten palvelin:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Shell täyttää `$DIGNA_API_KEY`:n arvon, kun suoritat komennon, joten Gemini CLI tallentaa avaimen
asetuksiinsa. Ilman `--scope user` -valitsinta palvelin lisätään vain nykyiseen projektiin.

### 2. Tai muokkaa settings.json-tiedostoa {: #2-or-edit-settings-json }

Yllä oleva komento kirjoittaa tiedostoon `settings.json`. Tiedoston muokkaaminen itse:

| Scope | Tiedosto |
|---|---|
| Kaikki projektisi | `~/.gemini/settings.json` |
| Yksi projekti | `.gemini/settings.json` projektissa |

```json
{
  "mcpServers": {
    "digna": {
      "httpUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

Käytä avainta `httpUrl`, joka on streamable HTTP:n avain. Samankaltainen `url`-avain valitsee
vanhemman SSE-siirtotavan, jota digna MCP Server ei tarjoa. Älä käytä alaviivoja palvelimen nimessä.

!!! tip "Jätä trust pois päältä"

    Gemini CLI kysyy ennen jokaista työkalukutsua, ellei palvelimella ole asetusta `"trust": true`.
    Jätä `trust` pois päältä *dignan* kohdalla, jotta vahvistat jokaisen muutoksen, jonka agentti
    tekee konfiguraatioosi.

### 3. Tarkista yhteys {: #3-verify-the-connection-gemini-cli }

Shellistä:

```bash
gemini mcp list
```

Palvelimen `digna` täytyy näkyä yhdistettynä. Gemini CLI -istunnossa voit suorittaa `/mcp`
nähdäksesi palvelimen ja sen työkalut.

---

## Geminin vianetsintä {: #troubleshooting-gemini }

### Palvelin näkyy katkaistuna

- Tarkista, että päätepiste päättyy `/mcp` ja on tavoitettavissa koneeltasi.
- Tarkista avaimen nimi: `serverUrl` Antigravityssa, `httpUrl` Gemini CLI:ssä.
- `401` tarkoittaa, että avain hylättiin; katso [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI ei enää käynnisty tililläni

Kesäkuusta 2026 lähtien henkilökohtaiset Google-tilit käyttävät Antigravity CLI:tä Gemini CLI:n
sijaan. Siirrä `digna`-merkintä tiedostoon `mcp_config.json` kohdan [Antigravity](#antigravity)
mukaisesti ja nimeä `httpUrl` uudelleen muotoon `serverUrl`.

---

## Katso myös {: #see-also }

- [Tekoälyagenttien yleiskatsaus](overview.md): päätepiste, API-avain, tietoturva ja yleinen vianetsintä
- [Claude](claude_mcp_guide.md): yhdistä Claude Code, Claude Desktop tai custom connector
- [digna Agentic](../platform/agentic/Introduction.md): mitä tekoälyagentit voivat tehdä *dignan* kanssa