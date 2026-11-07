# Gemini verbinden met digna

Deze gids verbindt de Gemini-tools van Google met de **digna MCP Server**. Je hebt het MCP-endpoint
van je *digna*-installatie en een API-key nodig, zoals beschreven in het
[Overzicht AI-agents](overview.md).

De voorbeelden gebruiken `https://digna.example.com/mcp` als endpoint. Vervang het door dat van jou.

## Je tool kiezen {: #choose-your-tool }

| Tool | Voor | Configuratie |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE en app | De agenttools van Google. Antigravity CLI verving Gemini CLI in juni 2026 voor individuele Google-accounts | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard- en Enterprise-licenties, en betaalde Gemini API-keys | `settings.json` of `gemini mcp add` |
| Gemini Enterprise-app | — | Niet ondersteund. De custom MCP connector ervan logt in met OAuth of een Google Cloud-serviceaccount, terwijl de digna MCP Server authenticeert met API-keys |

Al deze tools maken verbinding vanaf de machine waarop ze draaien, dus ze werken met *digna* binnen
je bedrijfsnetwerk, zolang die machine het endpoint kan bereiken.

---

## Antigravity {: #antigravity }

Antigravity leest zijn MCP-servers uit `mcp_config.json`, dat wordt gedeeld door de CLI, de IDE en
de app.

### 1. mcp_config.json openen {: #1-open-mcp-config-json }

| Scope | Bestand |
|---|---|
| Al je projecten | `~/.gemini/config/mcp_config.json` |
| Eén workspace | `.agents/mcp_config.json` in de workspace |

Zo open je het bestand dat in gebruik is:

- **CLI**: typ `/mcp` en druk op ++enter++ om de MCP-manager te openen.
- **IDE**: open in het zijpaneel van de agent het menu **…**, kies **MCP Servers**, dan
  **Manage MCP Servers** en dan **View raw config**.
- **App**: ga naar **Customizations** > **Installed** > **MCP Servers** en gebruik
  **Copy Config File Path**.

### 2. De digna-server toevoegen {: #2-add-the-digna-server }

Voeg de vermelding `digna` toe. Heeft het bestand al een sectie `mcpServers`, voeg haar daar dan
aan toe:

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

Antigravity bereikt externe servers alleen via streamable HTTP, en dat is wat de digna MCP Server
gebruikt. Schrijf het endpoint als `serverUrl`; de sleutel `httpUrl` van Gemini CLI wordt niet
ondersteund.

### 3. De verbinding controleren {: #3-verify-the-connection }

Typ in de CLI `/mcp`: de MCP-manager toont de server `digna` met zijn status en tools, en kan de
configuratie opnieuw laden en verbindingslogs tonen. In de IDE verschijnt de server onder
**Manage MCP Servers**.

!!! warning "Bescherm het bestand"

    `mcp_config.json` bevat de API-key als platte tekst. Houd een workspace-bestand
    `.agents/mcp_config.json` buiten versiebeheer, en zorg dat alleen je eigen account het globale
    bestand kan lezen.

---

## Gemini CLI {: #gemini-cli }

### 1. De server toevoegen {: #1-add-the-server }

Zet de API-key in een omgevingsvariabele en voeg dan de server toe:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Je shell vult `$DIGNA_API_KEY` in wanneer je de opdracht uitvoert, zodat Gemini CLI de key in zijn
instellingen opslaat. Zonder `--scope user` wordt de server alleen aan het huidige project
toegevoegd.

### 2. Of settings.json bewerken {: #2-or-edit-settings-json }

De opdracht hierboven schrijft naar `settings.json`. Zo bewerk je het bestand zelf:

| Scope | Bestand |
|---|---|
| Al je projecten | `~/.gemini/settings.json` |
| Eén project | `.gemini/settings.json` in het project |

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

Gebruik `httpUrl`, de sleutel voor streamable HTTP. De vergelijkbare sleutel `url` kiest het oudere
SSE-transport, dat de digna MCP Server niet aanbiedt. Gebruik geen underscores in de servernaam.

!!! tip "Laat trust uit"

    Gemini CLI vraagt vóór elke tool call om bevestiging, tenzij de server `"trust": true` heeft.
    Laat `trust` uit voor *digna*, zodat je elke wijziging bevestigt die een agent in je
    configuratie aanbrengt.

### 3. De verbinding controleren {: #3-verify-the-connection-gemini-cli }

Vanuit je shell:

```bash
gemini mcp list
```

De server `digna` moet als verbonden worden getoond. Voer binnen een Gemini CLI-sessie `/mcp` uit
om de server en zijn tools te zien.

---

## Problemen oplossen met Gemini {: #troubleshooting-gemini }

### De server wordt als niet verbonden getoond

- Controleer of het endpoint op `/mcp` eindigt en vanaf je machine bereikbaar is.
- Controleer de sleutelnaam: `serverUrl` in Antigravity, `httpUrl` in Gemini CLI.
- Een `401` betekent dat de key is geweigerd; zie [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI start niet meer voor mijn account

Sinds juni 2026 gebruiken individuele Google-accounts Antigravity CLI in plaats van Gemini CLI.
Verplaats de vermelding `digna` naar `mcp_config.json` zoals beschreven onder
[Antigravity](#antigravity), en hernoem `httpUrl` naar `serverUrl`.

---

## Zie ook {: #see-also }

- [Overzicht AI-agents](overview.md): endpoint, API-key, beveiliging en algemene probleemoplossing
- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop of een custom connector verbinden
- [digna Agentic](../platform/agentic/Introduction.md): wat AI-agents met *digna* kunnen doen