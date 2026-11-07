# A Claude csatlakoztatása a dignához

Ez az útmutató a Claude-ot a **digna MCP Serverhez** csatlakoztatja. Szüksége lesz a *digna*
telepítés MCP-végpontjára és egy API-kulcsra, az [AI-ágensek áttekintése](overview.md) oldalon
leírtak szerint.

A példák a `https://digna.example.com/mcp` végpontot használják. Cserélje le a sajátjára.

## A csatlakozás módjának kiválasztása {: #choose-how-to-connect }

| Claude-termék | Honnan csatlakozik | Működik a belső hálózaton futó *dignával* |
|---|---|---|
| [Claude Code](#claude-code) | Az Ön gépéről | Igen |
| [Claude Desktop helyi híddal](#claude-desktop-with-a-local-bridge) | Az Ön gépéről | Igen |
| [Egyéni connector](#custom-connector) a claude.ai-ban, a Claude Desktopban és a Claude mobile-ban | Az Anthropic felhőjéből | Nem. A végpontnak elérhetőnek kell lennie az internetről |

Ha a *digna* a vállalati hálózaton belül fut, használja a Claude Code-ot vagy a Claude Desktopot
helyi híddal.

---

## Claude Code {: #claude-code }

### 1. A szerver hozzáadása {: #1-add-the-server }

Tegye az API-kulcsot egy környezeti változóba, majd adja hozzá a szervert:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

A shell a parancs futtatásakor behelyettesíti a `$DIGNA_API_KEY` értékét, így a Claude Code a
kulcsot a saját konfigurációjában tárolja.

A `--scope` határozza meg, hol érhető el a szerver:

| Scope | Elérhető |
|---|---|
| `local` (alapértelmezett) | Önnek, csak az aktuális projektben |
| `user` | Önnek, minden projektben |
| `project` | Mindenkinek, aki a projekten dolgozik, a projektben lévő `.mcp.json` fájlon keresztül |

### 2. A szerver megosztása a csapattal (opcionális) {: #2-share-the-server-with-your-team }

Ha egy projektben mindenkinek ugyanazt a szervert szeretné biztosítani, helyezzen egy `.mcp.json`
fájlt a projekt gyökérkönyvtárába. A kulcsot ne írja bele a fájlba. A Claude Code a
`${DIGNA_API_KEY}` értékét mindenkinek a saját környezetéből tölti ki:

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

Mindenki a saját kulcsára állítja a `DIGNA_API_KEY` változót. Amikor a Claude Code először
megtalálja a fájlt, megkérdezi, hogy használja-e a benne lévő szervereket.

### 3. A kapcsolat ellenőrzése {: #3-verify-the-connection }

A shellből:

```bash
claude mcp list
```

A `digna` szervernél `✔ Connected` állapotnak kell megjelennie. Egy Claude Code munkameneten belül
futtassa a `/mcp` parancsot a szerver és az eszközei megtekintéséhez.

---

## Claude Desktop helyi híddal {: #claude-desktop-with-a-local-bridge }

A Claude Desktop konfigurációs fájlja helyi MCP-szervereket indít az Ön gépén. Egy kis híd, a nyílt
forráskódú [`mcp-remote`](https://github.com/geelen/mcp-remote) csomag fut ott, és minden kérést az
Ön API-kulcsával továbbít a *digna* végpontjára. Mivel a híd az Ön gépén fut, ez a módszer a
vállalati hálózaton belül futó *dignával* is működik.

!!! note "Közösségi csomag"

    Az `mcp-remote` csomagot a nyílt forráskódú közössége tartja karban, nem az Anthropic és nem a
    digna. Használat előtt ellenőrizze, hogy a szervezete engedélyezi-e.

### 1. A Node.js telepítése {: #1-install-nodejs }

A hídhoz [Node.js](https://nodejs.org) 18 vagy újabb szükséges. A Claude Desktop a rendszerére
telepített Node.js verziót használja. Ellenőrizze ezzel:

```bash
node --version
```

### 2. A konfigurációs fájl szerkesztése {: #2-edit-the-configuration-file }

Nyissa meg a `claude_desktop_config.json` fájlt:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Adja hozzá a `digna` szervert. Ha a fájlban már van `mcpServers` szakasz, abba vegye fel a `digna`
bejegyzést:

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

!!! warning "A fejlécet pontosan így adja meg"

    Az `Authorization:${AUTH_HEADER}` értéket szóközök nélkül írja, a `Bearer <api key>` pedig
    kerüljön az `env` részbe. A Windowson futó Claude Desktop nem escape-eli a szóközöket az
    `args` listában, így egy ott lévő szóköz elrontja a fejlécet.

### 3. A Claude Desktop újraindítása {: #3-restart-claude-desktop }

Lépjen ki teljesen a Claude Desktopból, és indítsa el újra. Egy új csevegésben kattintson a **+**
gombra, és nyissa meg a **Connectors** menüt: a `digna` elemnek szerepelnie kell a listában,
bekapcsolva.

---

## Egyéni connector {: #custom-connector }

Az egyéni connector helyi beállítás nélkül teszi elérhetővé a *dignát* a claude.ai-ban, a Claude
Desktopban és a Claude mobilalkalmazásokban. A végponthoz az Anthropic felhője csatlakozik, ezért
ez csak akkor működik, ha:

- A *digna* végpontja HTTPS-en elérhető az internetről
- A Claude-szervezetében az **Add custom connector** párbeszédablakban elérhető a
  **Request headers** beállítás. Az Anthropic ezt bétaként a szervezetek szűk körének kínálja

!!! warning "Nem a belső hálózaton futó dignához"

    A Claude MCP-tunneljei, amelyek privát hálózaton belüli szervereket érnek el, OAuth-ot
    igényelnek az MCP-szerveren. A digna MCP Server API-kulcsokkal hitelesít, így tunnel nem
    használható. Használja helyette a [Claude Code](#claude-code) vagy a
    [Claude Desktop helyi híddal](#claude-desktop-with-a-local-bridge) megoldást.

### 1. A connector-beállítások megnyitása {: #1-open-the-connector-settings }

- **Free, Pro, Max és Ultra előfizetés**: lépjen a **Customize > Connectors** oldalra, és kattintson
  az **Add custom connector** gombra.
- **Team és Enterprise előfizetés**: egy Owner a **Organization settings > Connectors** oldalon a
  **Add**, majd a **Custom** gombra kattint, és ha a rendszer rákérdez a típusra, a **Web**
  lehetőséget választja.

### 2. A connector adatainak megadása {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: fejlécnévként válassza az `authorization` értéket, értékként adja meg a
   `Bearer <api key>` szöveget, a `Bearer` szóval és a szóközzel együtt, és jelölje meg
   **Required** beállítással.
4. Kattintson az **Add** gombra.

!!! warning "Mindenki ugyanazt a kulcsot használja"

    A connectort használó minden tag ugyanazzal az API-kulccsal, és így ugyanazzal a *digna*
    felhasználóval dolgozik. Hozzon létre a connectorhoz egy külön *digna* felhasználót, és csak
    olyan projekteket és szerepköröket adjon neki, amelyek mindenkinek járnak, pl. a reader
    szerepkört.

Team és Enterprise előfizetésnél a tagok ezután a **Customize > Connectors** oldalon csatlakoznak,
ahol a connector a **Custom** címkét viseli.

A Claude nem tudja módosítani egy meglévő connector fejlécét. Új kulcs használatához távolítsa el a
connectort, és adja hozzá újra.

---

## Hibaelhárítás – Claude {: #troubleshooting-claude }

### A claude mcp list Failed to connect üzenetet mutat

Az ok megtekintéséhez futtassa a `claude mcp get digna` parancsot. A `401` azt jelenti, hogy a
kulcsot elutasították; lásd: [401 Unauthorized](overview.md#troubleshooting). A Claude Code
figyelmeztet a kulcs elején vagy végén lévő szóközökre és sortörésekre is, amelyek gyakran a
másoláskor kerülnek bele.

### A digna nem jelenik meg a Claude Desktopban

- Ellenőrizze, hogy telepítve van-e a Node.js 18 vagy újabb verziója: `node --version`.
- Ellenőrizze, hogy a `claude_desktop_config.json` érvényes JSON-e. Egy hiányzó vessző miatt a
  fájl egyik szervere sem töltődik be.
- Lépjen ki teljesen a Claude Desktopból, ne csak az ablakot zárja be, és indítsa el újra.

### Az egyéni connector nem éri el a szervert

Az Anthropic felhője nem éri el a végpontot. Ellenőrizze, hogy a végpont érvényes tanúsítvánnyal,
HTTPS-en elérhető-e az internetről, vagy csatlakozzon inkább a [Claude Code](#claude-code)
segítségével.

---

## Lásd még {: #see-also }

- [AI-ágensek áttekintése](overview.md): végpont, API-kulcs, biztonság és általános hibaelhárítás
- [Gemini](gemini_mcp_guide.md): az Antigravity vagy a Gemini CLI csatlakoztatása
- [digna Agentic](../platform/agentic/Introduction.md): mire képesek az AI-ágensek a *dignával*