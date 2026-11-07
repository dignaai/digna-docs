# Anslut Gemini till digna

Den här guiden ansluter Googles Gemini-verktyg till **digna MCP Server**. Du behöver MCP-endpointen
för din *digna*-installation och en API-nyckel, enligt beskrivningen i
[Översikt över AI-agenter](overview.md).

Exemplen använder `https://digna.example.com/mcp` som endpoint. Ersätt den med din egen.

## Välj ditt verktyg {: #choose-your-tool }

| Verktyg | För | Konfiguration |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE och app | Googles agentverktyg. Antigravity CLI ersatte Gemini CLI för individuella Google-konton i juni 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard- och Enterprise-licenser samt betalda Gemini API-nycklar | `settings.json` eller `gemini mcp add` |
| Gemini Enterprise-appen | — | Stöds inte. Dess anpassade MCP-connector loggar in med OAuth eller ett tjänstkonto i Google Cloud, medan digna MCP Server autentiserar med API-nycklar |

Alla dessa verktyg ansluter från den maskin de körs på, så de fungerar med *digna* inom ditt
företagsnätverk så länge den maskinen kan nå endpointen.

---

## Antigravity {: #antigravity }

Antigravity läser sina MCP-servrar från `mcp_config.json`, som delas av CLI, IDE och app.

### 1. Öppna mcp_config.json {: #1-open-mcp-config-json }

| Omfång | Fil |
|---|---|
| Alla dina projekt | `~/.gemini/config/mcp_config.json` |
| En workspace | `.agents/mcp_config.json` i workspacen |

Så här öppnar du filen som används:

- **CLI**: skriv `/mcp` och tryck på ++enter++ för att öppna MCP-hanteraren.
- **IDE**: i agentens sidopanel öppnar du menyn **…**, väljer **MCP Servers**, sedan
  **Manage MCP Servers** och därefter **View raw config**.
- **App**: gå till **Customizations** > **Installed** > **MCP Servers** och använd
  **Copy Config File Path**.

### 2. Lägg till digna-servern {: #2-add-the-digna-server }

Lägg till `digna`-posten. Om filen redan har ett `mcpServers`-avsnitt lägger du till den där:

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

Antigravity når fjärranslutna servrar bara via streamable HTTP, som digna MCP Server använder.
Skriv endpointen som `serverUrl`; nyckeln `httpUrl` från Gemini CLI stöds inte.

### 3. Verifiera anslutningen {: #3-verify-the-connection }

I CLI skriver du `/mcp`: MCP-hanteraren visar servern `digna` med dess status och verktyg, och kan
läsa in konfigurationen på nytt och visa anslutningsloggar. I IDE visas servern under
**Manage MCP Servers**.

!!! warning "Skydda filen"

    `mcp_config.json` innehåller API-nyckeln i klartext. Håll en workspace-fil
    `.agents/mcp_config.json` utanför versionshanteringen och låt bara ditt eget konto läsa den
    globala filen.

---

## Gemini CLI {: #gemini-cli }

### 1. Lägg till servern {: #1-add-the-server }

Lägg API-nyckeln i en miljövariabel och lägg sedan till servern:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Ditt skal fyller i `$DIGNA_API_KEY` när du kör kommandot, så Gemini CLI sparar nyckeln i sina
inställningar. Utan `--scope user` läggs servern bara till i det aktuella projektet.

### 2. Eller redigera settings.json {: #2-or-edit-settings-json }

Kommandot ovan skriver till `settings.json`. Så här redigerar du filen själv:

| Omfång | Fil |
|---|---|
| Alla dina projekt | `~/.gemini/settings.json` |
| Ett projekt | `.gemini/settings.json` i projektet |

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

Använd `httpUrl`, nyckeln för streamable HTTP. Den liknande nyckeln `url` väljer den äldre
SSE-transporten, som digna MCP Server inte erbjuder. Använd inte understreck i servernamnet.

!!! tip "Låt trust vara avstängt"

    Gemini CLI frågar före varje verktygsanrop om inte servern har `"trust": true`. Låt `trust` vara
    avstängt för *digna*, så att du bekräftar varje ändring som en agent gör i din konfiguration.

### 3. Verifiera anslutningen {: #3-verify-the-connection-gemini-cli }

I ditt skal:

```bash
gemini mcp list
```

Servern `digna` måste visas som ansluten. I en Gemini CLI-session kör du `/mcp` för att se servern
och dess verktyg.

---

## Felsökning av Gemini {: #troubleshooting-gemini }

### Servern visas som frånkopplad

- Kontrollera att endpointen slutar på `/mcp` och är nåbar från din maskin.
- Kontrollera nyckelnamnet: `serverUrl` i Antigravity, `httpUrl` i Gemini CLI.
- En `401` betyder att nyckeln avvisades; se [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI startar inte längre för mitt konto

Sedan juni 2026 använder individuella Google-konton Antigravity CLI i stället för Gemini CLI. Flytta
`digna`-posten till `mcp_config.json` enligt beskrivningen under [Antigravity](#antigravity), och
byt namn på `httpUrl` till `serverUrl`.

---

## Se även {: #see-also }

- [Översikt över AI-agenter](overview.md): endpoint, API-nyckel, säkerhet och allmän felsökning
- [Claude](claude_mcp_guide.md): anslut Claude Code, Claude Desktop eller en anpassad connector
- [digna Agentic](../platform/agentic/Introduction.md): vad AI-agenter kan göra med *digna*