# Připojení Claude k digna

Tento průvodce připojí Claude k **digna MCP Server**. Potřebujete endpoint MCP vaší instalace
*digna* a klíč API, jak je popsáno v [Přehledu AI agentů](overview.md).

Příklady používají jako endpoint `https://digna.example.com/mcp`. Nahraďte ho svým.

## Výběr způsobu připojení {: #choose-how-to-connect }

| Produkt Claude | Připojuje se z | Funguje s *digna* uvnitř vaší sítě |
|---|---|---|
| [Claude Code](#claude-code) | Váš počítač | Ano |
| [Claude Desktop s lokálním mostem](#claude-desktop-with-a-local-bridge) | Váš počítač | Ano |
| [Vlastní konektor](#custom-connector) v claude.ai, Claude Desktop a Claude mobile | Cloud společnosti Anthropic | Ne. Endpoint musí být dostupný z internetu |

Pro instalaci *digna*, která běží uvnitř vaší firemní sítě, použijte Claude Code nebo Claude
Desktop s lokálním mostem.

---

## Claude Code {: #claude-code }

### 1. Přidání serveru {: #1-add-the-server }

Uložte klíč API do proměnné prostředí a pak přidejte server:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Shell dosadí `$DIGNA_API_KEY` při spuštění příkazu, takže Claude Code uloží klíč do své vlastní
konfigurace.

`--scope` určuje, kde je server dostupný:

| Scope | Dostupný |
|---|---|
| `local` (výchozí) | Pro vás, pouze v aktuálním projektu |
| `user` | Pro vás, v každém projektu |
| `project` | Pro každého, kdo na projektu pracuje, prostřednictvím souboru `.mcp.json` v projektu |

### 2. Sdílení serveru s týmem (volitelné) {: #2-share-the-server-with-your-team }

Chcete-li všem v projektu nastavit stejný server, přidejte do kořenového adresáře projektu soubor
`.mcp.json`. Klíč do souboru nezapisujte. Claude Code dosadí `${DIGNA_API_KEY}` z vlastního
prostředí každého uživatele:

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

Každý si nastaví `DIGNA_API_KEY` na svůj vlastní klíč. Když Claude Code soubor poprvé najde, zeptá
se, zda má servery v něm používat.

### 3. Ověření připojení {: #3-verify-the-connection }

Ze shellu:

```bash
claude mcp list
```

Server `digna` musí zobrazovat `✔ Connected`. V relaci Claude Code spusťte `/mcp`, abyste viděli
server a jeho nástroje.

---

## Claude Desktop s lokálním mostem {: #claude-desktop-with-a-local-bridge }

Konfigurační soubor Claude Desktop spouští lokální MCP servery na vašem počítači. Malý most,
open-source balíček [`mcp-remote`](https://github.com/geelen/mcp-remote), běží na něm a přeposílá
každý požadavek na endpoint *digna* s vaším klíčem API. Protože most běží na vašem počítači, funguje
to s *digna* uvnitř vaší firemní sítě.

!!! note "Komunitní balíček"

    `mcp-remote` spravuje jeho open-source komunita, nikoli Anthropic ani digna. Než ho použijete,
    ověřte, že ho vaše organizace povoluje.

### 1. Instalace Node.js {: #1-install-nodejs }

Most potřebuje [Node.js](https://nodejs.org) 18 nebo novější. Claude Desktop používá verzi Node.js
nainstalovanou ve vašem systému. Zkontrolujte ji příkazem:

```bash
node --version
```

### 2. Úprava konfiguračního souboru {: #2-edit-the-configuration-file }

Otevřete `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Přidejte server `digna`. Pokud soubor již obsahuje sekci `mcpServers`, přidejte do ní položku
`digna`:

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

!!! warning "Ponechte hlavičku přesně tak, jak je uvedena"

    Zapište `Authorization:${AUTH_HEADER}` bez mezer a `Bearer <api key>` vložte do `env`.
    Claude Desktop ve Windows neescapuje mezery uvnitř `args`, takže mezera na tomto místě hlavičku
    rozbije.

### 3. Restart Claude Desktop {: #3-restart-claude-desktop }

Úplně ukončete Claude Desktop a znovu ho spusťte. V novém chatu klikněte na **+** a otevřete
**Connectors**: `digna` musí být v seznamu a zapnutá.

---

## Vlastní konektor {: #custom-connector }

Vlastní konektor zpřístupní *digna* v claude.ai, Claude Desktop a mobilních aplikacích Claude bez
jakéhokoli lokálního nastavení. K endpointu se připojuje cloud společnosti Anthropic, takže to
funguje jen tehdy, když:

- Endpoint *digna* je dostupný z internetu přes HTTPS
- Vaše organizace v Claude má v dialogu **Add custom connector** volbu **Request headers**.
  Anthropic ji nabízí jako betu omezenému okruhu organizací

!!! warning "Není pro digna uvnitř vaší sítě"

    Tunely MCP v Claude, které dosáhnou na servery v privátní síti, vyžadují na MCP serveru OAuth.
    digna MCP Server se ověřuje klíči API, takže tunel použít nelze. Použijte místo toho
    [Claude Code](#claude-code) nebo [Claude Desktop s lokálním mostem](#claude-desktop-with-a-local-bridge).

### 1. Otevření nastavení konektorů {: #1-open-the-connector-settings }

- **Tarify Free, Pro, Max a Ultra**: přejděte na **Customize > Connectors** a klikněte na
  **Add custom connector**.
- **Tarify Team a Enterprise**: Owner přejde na **Organization settings > Connectors**, klikne na
  **Add**, pak na **Custom**, a pokud je dotázán na typ, zvolí **Web**.

### 2. Zadání údajů konektoru {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: jako název hlavičky zvolte `authorization`, jako hodnotu zadejte
   `Bearer <api key>` včetně slova `Bearer` a mezery a označte ji jako **Required**.
4. Klikněte na **Add**.

!!! warning "Všichni sdílejí klíč"

    Každý člen, který konektor používá, pracuje se stejným klíčem API, a tedy se stejným
    uživatelem *digna*. Vytvořte pro konektor vyhrazeného uživatele *digna* a přidělte mu jen ty
    projekty a role, které smí mít každý, např. roli reader.

V tarifech Team a Enterprise se pak členové připojují v **Customize > Connectors**, kde má konektor
štítek **Custom**.

Claude nedokáže změnit hlavičku existujícího konektoru. Chcete-li použít nový klíč, konektor
odeberte a přidejte znovu.

---

## Řešení problémů s Claude {: #troubleshooting-claude }

### claude mcp list zobrazuje Failed to connect

Spusťte `claude mcp get digna` a zjistěte důvod. `401` znamená, že klíč byl odmítnut; viz
[401 Unauthorized](overview.md#troubleshooting). Claude Code také upozorní na mezery nebo zalomení
řádku na začátku či konci klíče, které často vzniknou při kopírování.

### digna se v Claude Desktop nezobrazuje

- Zkontrolujte, že je nainstalován Node.js 18 nebo novější: `node --version`.
- Zkontrolujte, že `claude_desktop_config.json` je platný JSON. Chybějící čárka zabrání načtení
  všech serverů v souboru.
- Ukončete Claude Desktop úplně, nejen okno, a znovu ho spusťte.

### Vlastní konektor nedosáhne na server

Cloud společnosti Anthropic nedosáhne na endpoint. Zkontrolujte, že je dostupný z internetu přes
HTTPS s platným certifikátem, nebo se místo toho připojte přes [Claude Code](#claude-code).

---

## Viz také {: #see-also }

- [Přehled AI agentů](overview.md): endpoint, klíč API, zabezpečení a obecné řešení problémů
- [Gemini](gemini_mcp_guide.md): připojení Antigravity nebo Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): co mohou AI agenti s *digna* dělat