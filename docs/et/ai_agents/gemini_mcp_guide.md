---
title: Gemini – ühenda Antigravity ja Gemini CLI MCP kaudu dignaga | digna dokumentatsioon
description: Ühenda Google'i Gemini tööriistad dignaga digna MCP Serveri kaudu — Antigravity CLI, IDE ja rakendus mcp_config.json failiga ning Gemini CLI settings.json failiga või käsuga gemini mcp add, API võti Authorization päises.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, digna API võti
---

# Ühenda Gemini dignaga

See juhend ühendab Google'i Gemini tööriistad **digna MCP Serveriga**. Sul on vaja oma *digna*
paigalduse MCP lõpp-punkti ja API võtit, nagu on kirjeldatud [AI-agentide ülevaates](overview.md).

Näidetes on lõpp-punktiks `https://digna.example.com/mcp`. Asenda see enda omaga.

## Vali tööriist {: #choose-your-tool }

| Tööriist | Kellele | Konfiguratsioon |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE ja rakendus | Google'i agenditööriistad. Antigravity CLI asendas 2026. aasta juunis isiklike Google'i kontode jaoks Gemini CLI | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard ja Enterprise litsentsid ning tasulised Gemini API võtmed | `settings.json` või `gemini mcp add` |
| Gemini Enterprise rakendus | — | Ei ole toetatud. Selle kohandatud MCP-connector logib sisse OAuthi või Google Cloudi teenusekontoga, digna MCP Server aga autendib API võtmetega |

Kõik need tööriistad ühenduvad masinast, milles nad töötavad, seega toimivad need *dignaga* sinu
ettevõtte võrgu sees, kui see masin jõuab lõpp-punktini.

---

## Antigravity {: #antigravity }

Antigravity loeb oma MCP-servereid failist `mcp_config.json`, mida jagavad CLI, IDE ja rakendus.

### 1. Ava mcp_config.json {: #1-open-mcp-config-json }

| Scope | Fail |
|---|---|
| Kõik sinu projektid | `~/.gemini/config/mcp_config.json` |
| Üks tööruum | `.agents/mcp_config.json` tööruumis |

Kasutusel oleva faili avamiseks:

- **CLI**: kirjuta `/mcp` ja vajuta ++enter++, et avada MCP haldur.
- **IDE**: ava agendi külgpaneelis menüü **…**, vali **MCP Servers**, seejärel
  **Manage MCP Servers** ja siis **View raw config**.
- **Rakendus**: mine **Customizations** > **Installed** > **MCP Servers** ja kasuta
  **Copy Config File Path**.

### 2. Lisa digna server {: #2-add-the-digna-server }

Lisa kirje `digna`. Kui failis on juba jaotis `mcpServers`, lisa see sinna:

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

Antigravity jõuab kaugserveriteni ainult streamable HTTP kaudu, mida digna MCP Server kasutab.
Kirjuta lõpp-punkt võtmega `serverUrl`; Gemini CLI võtit `httpUrl` ei toetata.

### 3. Kontrolli ühendust {: #3-verify-the-connection }

Kirjuta CLI-s `/mcp`: MCP haldur näitab serverit `digna` koos oleku ja tööriistadega ning saab
konfiguratsiooni uuesti laadida ja ühenduse logisid näidata. IDE-s ilmub server jaotisse
**Manage MCP Servers**.

!!! warning "Kaitse faili"

    `mcp_config.json` sisaldab API võtit lihttekstina. Hoia tööruumi `.agents/mcp_config.json`
    versioonihaldusest väljas ja luba globaalset faili lugeda ainult oma kontol.

---

## Gemini CLI {: #gemini-cli }

### 1. Lisa server {: #1-add-the-server }

Pane API võti keskkonnamuutujasse ja lisa seejärel server:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Sinu shell asendab käsu käivitamisel `$DIGNA_API_KEY` väärtusega, seega salvestab Gemini CLI võtme
oma seadetesse. Ilma `--scope user` lisatakse server ainult praegusesse projekti.

### 2. Või muuda settings.json faili {: #2-or-edit-settings-json }

Ülaltoodud käsk kirjutab faili `settings.json`. Faili ise muutmiseks:

| Scope | Fail |
|---|---|
| Kõik sinu projektid | `~/.gemini/settings.json` |
| Üks projekt | `.gemini/settings.json` projektis |

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

Kasuta võtit `httpUrl`, mis on streamable HTTP võti. Sarnane võti `url` valib vanema SSE-transpordi,
mida digna MCP Server ei paku. Ära kasuta serveri nimes allkriipse.

!!! tip "Jäta trust välja lülitatuks"

    Gemini CLI küsib enne iga tööriistakutset kinnitust, välja arvatud juhul, kui serveril on
    `"trust": true`. Jäta `trust` *digna* puhul välja lülitatuks, et kinnitaksid iga muudatuse, mille
    agent sinu konfiguratsioonis teeb.

### 3. Kontrolli ühendust {: #3-verify-the-connection-gemini-cli }

Oma shellist:

```bash
gemini mcp list
```

Server `digna` peab olema näidatud ühendatuna. Gemini CLI seansis käivita `/mcp`, et näha serverit
ja selle tööriistu.

---

## Gemini tõrkeotsing {: #troubleshooting-gemini }

### Server on näidatud lahtiühendatuna

- Kontrolli, et lõpp-punkt lõpeb `/mcp`-ga ja on sinu masinast kättesaadav.
- Kontrolli võtme nime: Antigravitys `serverUrl`, Gemini CLI-s `httpUrl`.
- `401` tähendab, et võti lükati tagasi; vaata [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI ei käivitu enam minu kontoga

Alates 2026. aasta juunist kasutavad isiklikud Google'i kontod Gemini CLI asemel Antigravity CLI-d.
Teisalda kirje `digna` faili `mcp_config.json`, nagu on kirjeldatud jaotises
[Antigravity](#antigravity), ja nimeta `httpUrl` ümber `serverUrl`-iks.

---

## Vaata ka {: #see-also }

- [AI-agentide ülevaade](overview.md): lõpp-punkt, API võti, turvalisus ja üldine tõrkeotsing
- [Claude](claude_mcp_guide.md): ühenda Claude Code, Claude Desktop või custom connector
- [digna Agentic](../platform/agentic/Introduction.md): mida AI-agendid saavad *dignaga* teha
