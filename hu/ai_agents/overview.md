# AI-ágensek csatlakoztatása a dignához

A **digna MCP Server** lehetővé teszi, hogy az AI-ágensek a
[Model Context Protocolon](https://modelcontextprotocol.io) (MCP) keresztül dolgozzanak a
*dignával*. Az MCP nyílt szabvány, amelyet a Claude, a Gemini és sok más AI-eszköz támogat. A
*dignához* csatlakoztatott ágens kérdésekre válaszol az adataival kapcsolatban, kivizsgálja a
riasztásokat, és segít a *digna* konfigurálásában. Hogy mire képesek az ágensek, azt a
[digna Agentic](../platform/agentic/Introduction.md) oldal írja le.

Ez az oldal a *digna* oldali beállításokat tárgyalja, amelyek minden AI-kliensnél azonosak. A
kliensenkénti útmutatók ezután megmutatják, hová kell megadni a végpontot és a kulcsot:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop és egyéni connectorok
- [Gemini](gemini_mcp_guide.md): Antigravity és Gemini CLI

!!! info "Béta"

    A digna Agentic, és vele együtt a digna MCP Server, béta verzióként érhető el a
    [Release 2026.11](../changelog/Release_202611.md) kiadásban.

---

## Előfeltételek {: #before-you-start }

Szüksége lesz a következőkre:

- *digna* Release 2026.11 vagy újabb
- Olyan licenc, amely tartalmazza a **digna Agentic** funkciót. Enélkül az MCP-szerver minden
  kérést elutasít
- Egy *digna* felhasználói fiók. Az ágens minden projektben ennek a felhasználónak a jogosultságaival
  dolgozik, lásd: [Jogosultságok](../platform/agentic/how_it_works.md#permissions)
- Olyan AI-kliens, amely **streamable HTTP** protokollon csatlakozik távoli MCP-szerverekhez, és
  képes `Authorization` fejlécet küldeni

---

## 1. Az MCP-végpont megkeresése {: #1-find-the-mcp-endpoint }

Az MCP-szerver a *digna* backend része, így semmit sem kell külön telepíteni vagy elindítani. A
végpontja a backend címe, utána `/mcp`:

```text
https://digna.example.com/mcp
```

Ha a backend közvetlenül egy hoszton és porton fut, például a
`digna serve --address 0.0.0.0 --port 8082` parancs után, akkor a végpont ez a cím `/mcp`
végződéssel:

```text
http://digna-host:8082/mcp
```

Ha a backend előtt reverse proxy áll, annak a `/mcp` útvonalat az `Authorization` fejléccel együtt
kell továbbítania a backendnek.

!!! warning "Hálózaton használjon HTTPS-t"

    Minden kérés tartalmaz egy API-kulcsot. Használjon HTTPS-t, ha az AI-kliens és a *digna* nem
    ugyanazon a gépen fut.

### Honnan érkezik a kapcsolat {: #where-the-connection-comes-from }

A legtöbb AI-kliens arról a gépről csatlakozik, amelyen fut: a Claude Code, a Claude Desktop helyi
híddal, az Antigravity és a Gemini CLI. Ezeknél elég, ha a *digna* elérhető az adott gépről,
például a vállalati hálózaton belül.

A Claude **egyéni connectorai** (custom connectors) másképp működnek: az Anthropic felhője
csatlakozik a végponthoz. Csak akkor működnek, ha a végpont HTTPS-en elérhető az internetről. Ha a
*digna* telepítés csak a belső hálózatán érhető el, olyan klienst használjon, amely a saját gépén
fut.

---

## 2. API-kulcs létrehozása {: #2-create-an-api-key }

Az AI-kliens egy *digna* felhasználó API-kulcsával hitelesít.

1. Jelentkezzen be a *dignába*.
2. Nyissa meg a felhasználói profilját a bal alsó sarokban.
3. Kattintson az **API Keys**, majd az **Add API Key** elemre.
4. Adjon meg egy nevet, amelyből kiderül, mire szolgál a kulcs, pl. *Claude Code – Marcin*, és
   válassza ki, mikor járjon le.
5. Másolja ki a kulcsot. Csak egyszer jelenik meg.

Az MCP-szervernek küldött minden kérés ebben a fejlécben továbbítja a kulcsot:

```text
Authorization: Bearer <api key>
```

A `Bearer` szó és az utána következő szóköz a fejléc értékének része.

---

## 3. Az AI-kliens csatlakoztatása {: #3-connect-your-ai-client }

| AI-kliens | Honnan csatlakozik | Útmutató |
|---|---|---|
| Claude Code | Az Ön gépéről | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop helyi híddal | Az Ön gépéről | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Claude egyéni connector (claude.ai, Claude Desktop, Claude mobile) | Az Anthropic felhőjéből | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE és alkalmazás | Az Ön gépéről | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Az Ön gépéről | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Más MCP-kliensek is működnek, ha támogatják a távoli szervereket streamable HTTP-n, egyéni
fejléccel. A legtöbbjük az alábbihoz hasonló konfigurációt olvas be. A pontos fájl- és kulcsneveket
a kliens dokumentációjában találja:

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

## 4. Kipróbálás {: #4-try-it }

Kérdezzen az ágenstől olyasmit, amire csak a *digna* tud válaszolni:

- *„Sorold fel a digna-projektjeimet.”*
- *„Mely adatforrások nem zöldek ma az X projektben?”*
- *„Magyarázd el az Y adatforrás legutóbbi sikertelen ellenőrzését.”*

Ha az ágens felsorolja a projektjeit, a kapcsolat működik.

---

## Biztonság {: #security }

- **Személyenként és kliensenként egy kulcs.** Így egyetlen kulcsot visszavonhat a
  **Delete API Key** paranccsal anélkül, hogy ez bárki mást érintene.
- **Válassza meg tudatosan a felhasználót.** Az ágens mindent megtehet, amit a kulcs
  felhasználója. Ha csak adatokat vizsgál, olyan felhasználót használjon, akinek a projektekben
  reader szerepköre van.
- **Ne tegyen kulcsot megosztott fájlokba.** Ne commitoljon kulcsot tartalmazó konfigurációs fájlt.
  Ha a kliens támogatja, a kulcsot környezeti változóból olvassa be.
- **Állítson be lejáratot.** Hozzon létre új kulcsot, mielőtt a régi lejár, és frissítse a
  klienst.
- **Ellenőrizze az eszközhívásokat.** Hagyja bekapcsolva a kliensben az eszközhívások
  megerősítését, legalább a konfigurációt módosító hívásoknál.

---

## Hibaelhárítás {: #troubleshooting }

### 401 Unauthorized

A válasz megadja az okot:

| Üzenet | Ok |
|---|---|
| `Missing or malformed Authorization header` | Nem érkezett fejléc, vagy az érték nem `Bearer ` szöveggel kezdődik |
| `Invalid API key` | A kulcs hibás, vagy törölték |
| `API key expired` | A kulcs lejárt. Hozzon létre újat |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

A *digna* licencben nincs digna Agentic bejegyzés, vagy ez a bejegyzés lejárt. Kérjen a digna
csapatától olyan licencet, amely tartalmazza a digna Agentic funkciót, és telepítse az
operációs rendszeréhez tartozó telepítési útmutató szerint.

### Minden kérés érvénytelen licenc hibával meghiúsul

Maga a *digna* licenc járt le. Az MCP-szerver a dashboarddal együtt leáll a válaszadással, amíg új
licencet nem telepítenek.

### Az ágens olvasni tud, de a konfigurációt nem tudja módosítani

Az API-kulcs mögötti felhasználónak nincs editor szerepköre az adott projektben. Használja egy
editor szerepkörű felhasználó kulcsát, vagy kérje meg a projekt adminisztrátorát, hogy módosítsa a
szerepkört.

### A kliens egyáltalán nem tud csatlakozni

A csatlakozó gép nem éri el a végpontot. Nyissa meg a végpont címét erről a gépről, és ellenőrizze
a tűzfalakat, a proxykat és a tanúsítványt. Claude egyéni connector esetén ez a gép az Anthropic
felhőjében van, lásd: [Honnan érkezik a kapcsolat](#where-the-connection-comes-from).