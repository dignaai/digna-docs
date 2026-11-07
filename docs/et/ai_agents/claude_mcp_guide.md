---
title: Claude – ühenda Claude MCP kaudu dignaga | digna dokumentatsioon
description: Ühenda Claude dignaga digna MCP Serveri kaudu — Claude Code käsurealt või jagatud .mcp.json failiga, Claude Desktop kohaliku sillaga ja custom connectorid claude.ai-s, API võti Authorization päises.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, claude.ai custom connector, digna MCP server, mcp-remote, Authorization Bearer, digna API võti
---

# Ühenda Claude dignaga

See juhend ühendab Claude'i **digna MCP Serveriga**. Sul on vaja oma *digna* paigalduse MCP
lõpp-punkti ja API võtit, nagu on kirjeldatud [AI-agentide ülevaates](overview.md).

Näidetes on lõpp-punktiks `https://digna.example.com/mcp`. Asenda see enda omaga.

## Vali ühendamise viis {: #choose-how-to-connect }

| Claude'i toode | Ühendub | Töötab *dignaga* sinu võrgu sees |
|---|---|---|
| [Claude Code](#claude-code) | Sinu masinast | Jah |
| [Claude Desktop kohaliku sillaga](#claude-desktop-with-a-local-bridge) | Sinu masinast | Jah |
| [Custom connector](#custom-connector) claude.ai-s, Claude Desktopis ja Claude mobiilirakenduses | Anthropicu pilvest | Ei. Lõpp-punkt peab olema internetist kättesaadav |

Kui *digna* paigaldus töötab sinu ettevõtte võrgu sees, kasuta Claude Code'i või Claude Desktopi
kohaliku sillaga.

---

## Claude Code {: #claude-code }

### 1. Lisa server {: #1-add-the-server }

Pane API võti keskkonnamuutujasse ja lisa seejärel server:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Sinu shell asendab käsu käivitamisel `$DIGNA_API_KEY` väärtusega, seega salvestab Claude Code võtme
oma konfiguratsiooni.

`--scope` määrab, kus server on saadaval:

| Scope | Saadaval |
|---|---|
| `local` (vaikimisi) | Sinule, ainult praeguses projektis |
| `user` | Sinule, kõigis projektides |
| `project` | Kõigile, kes projektis töötavad, projekti `.mcp.json` faili kaudu |

### 2. Jaga serverit oma meeskonnaga (valikuline) {: #2-share-the-server-with-your-team }

Et anda kõigile projektis sama server, lisa projekti juurkausta `.mcp.json` fail. Ära kirjuta
võtit faili. Claude Code täidab `${DIGNA_API_KEY}` iga inimese enda keskkonnast:

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

Iga inimene määrab `DIGNA_API_KEY` väärtuseks oma võtme. Kui Claude Code faili esimest korda leiab,
küsib see, kas selles olevaid servereid kasutada.

### 3. Kontrolli ühendust {: #3-verify-the-connection }

Oma shellist:

```bash
claude mcp list
```

Server `digna` peab näitama `✔ Connected`. Claude Code'i seansis käivita `/mcp`, et näha serverit
ja selle tööriistu.

---

## Claude Desktop kohaliku sillaga {: #claude-desktop-with-a-local-bridge }

Claude Desktopi konfiguratsioonifail käivitab sinu masinas kohalikke MCP-servereid. Väike sild,
avatud lähtekoodiga pakett [`mcp-remote`](https://github.com/geelen/mcp-remote), töötab seal ja
edastab iga päringu koos sinu API võtmega *digna* lõpp-punkti. Kuna sild töötab sinu masinas,
toimib see *dignaga* sinu ettevõtte võrgu sees.

!!! note "Kogukonna pakett"

    `mcp-remote` paketti haldab selle avatud lähtekoodiga kogukond, mitte Anthropic ega digna.
    Enne kasutamist kontrolli, kas sinu organisatsioon seda lubab.

### 1. Paigalda Node.js {: #1-install-nodejs }

Sild vajab [Node.js](https://nodejs.org) versiooni 18 või uuemat. Claude Desktop kasutab sinu
süsteemi paigaldatud Node.js versiooni. Kontrolli seda käsuga:

```bash
node --version
```

### 2. Muuda konfiguratsioonifaili {: #2-edit-the-configuration-file }

Ava `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Lisa server `digna`. Kui failis on juba jaotis `mcpServers`, lisa kirje `digna` sinna:

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

!!! warning "Jäta päis täpselt nii, nagu näidatud"

    Kirjuta `Authorization:${AUTH_HEADER}` ilma tühikuteta ja pane `Bearer <api key>` jaotisse
    `env`. Claude Desktop Windowsis ei escape'i tühikuid `args` sees, seega rikub seal olev tühik
    päise.

### 3. Taaskäivita Claude Desktop {: #3-restart-claude-desktop }

Sulge Claude Desktop täielikult ja käivita see uuesti. Klõpsa uues vestluses **+** ja ava
**Connectors**: `digna` peab olema loendis ja sisse lülitatud.

---

## Custom connector {: #custom-connector }

Custom connector teeb *digna* kättesaadavaks claude.ai-s, Claude Desktopis ja Claude'i
mobiilirakendustes ilma kohaliku seadistuseta. Lõpp-punktiga ühendub Anthropicu pilv, seega töötab
see ainult siis, kui:

- *digna* lõpp-punkt on internetist HTTPS-i kaudu kättesaadav
- Sinu Claude'i organisatsioonil on dialoogis **Add custom connector** valik **Request headers**.
  Anthropic pakub seda beetana piiratud hulgale organisatsioonidele

!!! warning "Mitte sinu võrgu sees oleva digna jaoks"

    Claude'i MCP-tunnelid, mis jõuavad privaatvõrgu sees olevate serveriteni, nõuavad MCP-serverilt
    OAuthi. digna MCP Server autendib API võtmetega, seega tunnelit kasutada ei saa. Kasuta selle
    asemel [Claude Code'i](#claude-code) või
    [Claude Desktopi kohaliku sillaga](#claude-desktop-with-a-local-bridge).

### 1. Ava connectori seaded {: #1-open-the-connector-settings }

- **Free, Pro, Max ja Ultra paketid**: mine **Customize > Connectors** ja klõpsa
  **Add custom connector**.
- **Team ja Enterprise paketid**: Owner läheb **Organization settings > Connectors**, klõpsab
  **Add**, seejärel **Custom** ja valib **Web**, kui tüüpi küsitakse.

### 2. Sisesta connectori andmed {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: vali päise nimeks `authorization`, sisesta väärtuseks `Bearer <api key>`
   koos sõnaga `Bearer` ja tühikuga ning märgi see **Required**.
4. Klõpsa **Add**.

!!! warning "Kõik jagavad sama võtit"

    Iga liige, kes connectorit kasutab, töötab sama API võtmega ja seega sama *digna* kasutajaga.
    Loo connectori jaoks eraldi *digna* kasutaja ja anna sellele ainult need projektid ja rollid,
    mis võivad olla kõigil, nt lugeja roll.

Team ja Enterprise pakettide puhul ühenduvad liikmed seejärel jaotises **Customize > Connectors**,
kus connectoril on silt **Custom**.

Claude ei saa olemasoleva connectori päist muuta. Uue võtme kasutamiseks eemalda connector ja lisa
see uuesti.

---

## Claude'i tõrkeotsing {: #troubleshooting-claude }

### claude mcp list näitab Failed to connect

Käivita `claude mcp get digna`, et näha põhjust. `401` tähendab, et võti lükati tagasi; vaata
[401 Unauthorized](overview.md#troubleshooting). Claude Code hoiatab ka tühikute või reavahetuse
eest võtme alguses või lõpus, mis tulevad sageli kopeerimisel kaasa.

### digna ei ilmu Claude Desktopis

- Kontrolli, et Node.js 18 või uuem on paigaldatud: `node --version`.
- Kontrolli, et `claude_desktop_config.json` on kehtiv JSON. Puuduv koma takistab kõigi faili
  serverite laadimist.
- Sulge Claude Desktop täielikult, mitte ainult aken, ja käivita see uuesti.

### Custom connector ei jõua serverini

Anthropicu pilv ei jõua lõpp-punktini. Kontrolli, et see on internetist HTTPS-i kaudu kehtiva
sertifikaadiga kättesaadav, või ühenda selle asemel [Claude Code'i](#claude-code) kaudu.

---

## Vaata ka {: #see-also }

- [AI-agentide ülevaade](overview.md): lõpp-punkt, API võti, turvalisus ja üldine tõrkeotsing
- [Gemini](gemini_mcp_guide.md): ühenda Antigravity või Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): mida AI-agendid saavad *dignaga* teha
