---
title: Gemini – Az Antigravity és a Gemini CLI csatlakoztatása a dignához MCP-n keresztül | digna dokumentáció
description: Csatlakoztassa a Google Gemini-eszközeit a dignához a digna MCP Serveren keresztül — Antigravity CLI, IDE és alkalmazás az mcp_config.json fájllal, valamint Gemini CLI a settings.json fájllal vagy a gemini mcp add paranccsal, API-kulccsal az Authorization fejlécben.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, digna API-kulcs
---

# A Gemini csatlakoztatása a dignához

Ez az útmutató a Google Gemini-eszközeit a **digna MCP Serverhez** csatlakoztatja. Szüksége lesz a
*digna* telepítés MCP-végpontjára és egy API-kulcsra, az
[AI-ágensek áttekintése](overview.md) oldalon leírtak szerint.

A példák a `https://digna.example.com/mcp` végpontot használják. Cserélje le a sajátjára.

## Az eszköz kiválasztása {: #choose-your-tool }

| Eszköz | Kinek | Konfiguráció |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE és alkalmazás | A Google ágenseszközei. Az Antigravity CLI 2026 júniusában váltotta fel a Gemini CLI-t az egyéni Google-fiókoknál | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard és Enterprise licencek, valamint fizetős Gemini API-kulcsok | `settings.json` vagy `gemini mcp add` |
| Gemini Enterprise alkalmazás | — | Nem támogatott. Egyéni MCP-connectora OAuth-tal vagy Google Cloud szolgáltatásfiókkal jelentkezik be, a digna MCP Server viszont API-kulcsokkal hitelesít |

Mindegyik eszköz arról a gépről csatlakozik, amelyen fut, így a vállalati hálózaton belül futó
*dignával* is működik, amíg az adott gép eléri a végpontot.

---

## Antigravity {: #antigravity }

Az Antigravity az MCP-szervereit az `mcp_config.json` fájlból olvassa be, amelyen a CLI, az IDE és
az alkalmazás osztozik.

### 1. Az mcp_config.json megnyitása {: #1-open-mcp-config-json }

| Scope | Fájl |
|---|---|
| Minden projektje | `~/.gemini/config/mcp_config.json` |
| Egy workspace | `.agents/mcp_config.json` a workspace-ben |

A használatban lévő fájl megnyitása:

- **CLI**: írja be a `/mcp` parancsot, és nyomja meg az ++enter++ billentyűt az MCP-kezelő
  megnyitásához.
- **IDE**: az ágens oldalpaneljén nyissa meg a **…** menüt, válassza az **MCP Servers**, majd a
  **Manage MCP Servers**, végül a **View raw config** elemet.
- **Alkalmazás**: lépjen a **Customizations** > **Installed** > **MCP Servers** oldalra, és
  használja a **Copy Config File Path** parancsot.

### 2. A digna szerver hozzáadása {: #2-add-the-digna-server }

Adja hozzá a `digna` bejegyzést. Ha a fájlban már van `mcpServers` szakasz, oda vegye fel:

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

Az Antigravity a távoli szervereket csak streamable HTTP-n éri el, és a digna MCP Server ezt
használja. A végpontot `serverUrl` kulccsal adja meg; a Gemini CLI `httpUrl` kulcsa nem
támogatott.

### 3. A kapcsolat ellenőrzése {: #3-verify-the-connection }

A CLI-ben írja be a `/mcp` parancsot: az MCP-kezelő megmutatja a `digna` szervert az állapotával és
az eszközeivel, és újra tudja tölteni a konfigurációt, valamint meg tudja jeleníteni a kapcsolati
naplókat. Az IDE-ben a szerver a **Manage MCP Servers** alatt jelenik meg.

!!! warning "Védje a fájlt"

    Az `mcp_config.json` egyszerű szövegként tartalmazza az API-kulcsot. A workspace
    `.agents/mcp_config.json` fájlját tartsa távol a verziókezeléstől, a globális fájlt pedig
    csak a saját fiókja olvashassa.

---

## Gemini CLI {: #gemini-cli }

### 1. A szerver hozzáadása {: #1-add-the-server }

Tegye az API-kulcsot egy környezeti változóba, majd adja hozzá a szervert:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

A shell a parancs futtatásakor behelyettesíti a `$DIGNA_API_KEY` értékét, így a Gemini CLI a
kulcsot a saját beállításaiban tárolja. A `--scope user` nélkül a szerver csak az aktuális
projekthez adódik hozzá.

### 2. Vagy a settings.json szerkesztése {: #2-or-edit-settings-json }

A fenti parancs a `settings.json` fájlba ír. Ha a fájlt saját maga szeretné szerkeszteni:

| Scope | Fájl |
|---|---|
| Minden projektje | `~/.gemini/settings.json` |
| Egy projekt | `.gemini/settings.json` a projektben |

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

Használja a `httpUrl` kulcsot, ez a streamable HTTP kulcsa. A hasonló `url` kulcs a régebbi SSE
transzportot választja, amelyet a digna MCP Server nem kínál. A szerver nevében ne használjon
aláhúzásjelet.

!!! tip "Hagyja kikapcsolva a trust beállítást"

    A Gemini CLI minden eszközhívás előtt rákérdez, kivéve, ha a szervernél `"trust": true` van
    beállítva. A *digna* esetében hagyja kikapcsolva a `trust` beállítást, hogy minden módosítást
    megerősíthessen, amelyet egy ágens a konfigurációjában végez.

### 3. A kapcsolat ellenőrzése {: #3-verify-the-connection-gemini-cli }

A shellből:

```bash
gemini mcp list
```

A `digna` szervernek csatlakoztatottként kell megjelennie. Egy Gemini CLI munkameneten belül
futtassa a `/mcp` parancsot a szerver és az eszközei megtekintéséhez.

---

## Hibaelhárítás – Gemini {: #troubleshooting-gemini }

### A szerver leválasztottként jelenik meg

- Ellenőrizze, hogy a végpont `/mcp` végződésű-e, és elérhető-e a gépéről.
- Ellenőrizze a kulcs nevét: `serverUrl` az Antigravityben, `httpUrl` a Gemini CLI-ben.
- A `401` azt jelenti, hogy a kulcsot elutasították; lásd: [401 Unauthorized](overview.md#troubleshooting).

### A Gemini CLI már nem indul el a fiókommal

2026 júniusa óta az egyéni Google-fiókok a Gemini CLI helyett az Antigravity CLI-t használják.
Helyezze át a `digna` bejegyzést az `mcp_config.json` fájlba az [Antigravity](#antigravity)
részben leírtak szerint, és nevezze át a `httpUrl` kulcsot `serverUrl` névre.

---

## Lásd még {: #see-also }

- [AI-ágensek áttekintése](overview.md): végpont, API-kulcs, biztonság és általános hibaelhárítás
- [Claude](claude_mcp_guide.md): a Claude Code, a Claude Desktop vagy egy egyéni connector csatlakoztatása
- [digna Agentic](../platform/agentic/Introduction.md): mire képesek az AI-ágensek a *dignával*
