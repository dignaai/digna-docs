---
title: Claude – Claude via MCP verbinden met digna | digna Documentatie
description: Verbind Claude met digna via de digna MCP Server — Claude Code vanaf de opdrachtregel of met een gedeeld .mcp.json, Claude Desktop met een lokale bridge, en custom connectors in claude.ai, met een API-key in de Authorization-header.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, claude.ai custom connector, digna MCP server, mcp-remote, Authorization Bearer, digna API-key
---

# Claude verbinden met digna

Deze gids verbindt Claude met de **digna MCP Server**. Je hebt het MCP-endpoint van je
*digna*-installatie en een API-key nodig, zoals beschreven in het [Overzicht AI-agents](overview.md).

De voorbeelden gebruiken `https://digna.example.com/mcp` als endpoint. Vervang het door dat van jou.

## Kiezen hoe je verbinding maakt {: #choose-how-to-connect }

| Claude-product | Verbindt vanaf | Werkt met *digna* binnen je netwerk |
|---|---|---|
| [Claude Code](#claude-code) | Je eigen machine | Ja |
| [Claude Desktop met een lokale bridge](#claude-desktop-with-a-local-bridge) | Je eigen machine | Ja |
| [Custom connector](#custom-connector) in claude.ai, Claude Desktop en Claude mobile | De cloud van Anthropic | Nee. Het endpoint moet vanaf het internet bereikbaar zijn |

Gebruik voor een *digna*-installatie die binnen je bedrijfsnetwerk draait Claude Code of Claude
Desktop met een lokale bridge.

---

## Claude Code {: #claude-code }

### 1. De server toevoegen {: #1-add-the-server }

Zet de API-key in een omgevingsvariabele en voeg dan de server toe:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Je shell vult `$DIGNA_API_KEY` in wanneer je de opdracht uitvoert, zodat Claude Code de key in zijn
eigen configuratie opslaat.

`--scope` bepaalt waar de server beschikbaar is:

| Scope | Beschikbaar |
|---|---|
| `local` (standaard) | Voor jou, alleen in het huidige project |
| `user` | Voor jou, in elk project |
| `project` | Voor iedereen die aan het project werkt, via een `.mcp.json`-bestand in het project |

### 2. De server met je team delen (optioneel) {: #2-share-the-server-with-your-team }

Om iedereen in een project dezelfde server te geven, voeg je een `.mcp.json`-bestand toe aan de
hoofdmap van het project. Schrijf de key niet in het bestand. Claude Code vult `${DIGNA_API_KEY}`
in vanuit de eigen omgeving van elke persoon:

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

Iedereen zet `DIGNA_API_KEY` op zijn eigen key. De eerste keer dat Claude Code het bestand vindt,
vraagt het of de servers erin gebruikt moeten worden.

### 3. De verbinding controleren {: #3-verify-the-connection }

Vanuit je shell:

```bash
claude mcp list
```

De server `digna` moet `✔ Connected` tonen. Voer binnen een Claude Code-sessie `/mcp` uit om de
server en zijn tools te zien.

---

## Claude Desktop met een lokale bridge {: #claude-desktop-with-a-local-bridge }

Het configuratiebestand van Claude Desktop start lokale MCP-servers op je machine. Een kleine bridge,
het open-sourcepakket [`mcp-remote`](https://github.com/geelen/mcp-remote), draait daar en stuurt
elk verzoek met je API-key door naar het *digna*-endpoint. Omdat de bridge op je eigen machine
draait, werkt dit met *digna* binnen je bedrijfsnetwerk.

!!! note "Een communitypakket"

    `mcp-remote` wordt onderhouden door de open-sourcecommunity, niet door Anthropic of digna.
    Controleer of je organisatie het toestaat voordat je het gebruikt.

### 1. Node.js installeren {: #1-install-nodejs }

De bridge heeft [Node.js](https://nodejs.org) 18 of later nodig. Claude Desktop gebruikt de
Node.js-versie die op je systeem is geïnstalleerd. Controleer die met:

```bash
node --version
```

### 2. Het configuratiebestand bewerken {: #2-edit-the-configuration-file }

Open `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Voeg de server `digna` toe. Heeft het bestand al een sectie `mcpServers`, voeg de vermelding
`digna` daar dan aan toe:

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

!!! warning "Houd de header precies zoals getoond"

    Schrijf `Authorization:${AUTH_HEADER}` zonder spaties en zet `Bearer <api key>` in `env`.
    Claude Desktop op Windows escapet geen spaties binnen `args`, dus een spatie daar breekt de
    header.

### 3. Claude Desktop opnieuw starten {: #3-restart-claude-desktop }

Sluit Claude Desktop volledig af en start het opnieuw. Klik in een nieuwe chat op **+** en open
**Connectors**: `digna` moet in de lijst staan en zijn ingeschakeld.

---

## Custom connector {: #custom-connector }

Een custom connector maakt *digna* beschikbaar in claude.ai, Claude Desktop en de mobiele apps van
Claude, zonder lokale installatie. De cloud van Anthropic maakt verbinding met het endpoint, dus dit
werkt alleen als:

- Het *digna*-endpoint via HTTPS vanaf het internet bereikbaar is
- Je Claude-organisatie de optie **Request headers** heeft in het dialoogvenster
  **Add custom connector**. Anthropic biedt die als bèta aan een beperkt aantal organisaties aan

!!! warning "Niet voor digna binnen je netwerk"

    De MCP-tunnels van Claude, die servers binnen een privénetwerk bereiken, vereisen OAuth op de
    MCP-server. De digna MCP Server authenticeert met API-keys, dus een tunnel kan niet worden
    gebruikt. Gebruik in plaats daarvan [Claude Code](#claude-code) of
    [Claude Desktop met een lokale bridge](#claude-desktop-with-a-local-bridge).

### 1. De connectorinstellingen openen {: #1-open-the-connector-settings }

- **Free-, Pro-, Max- en Ultra-abonnementen**: ga naar **Customize > Connectors** en klik op
  **Add custom connector**.
- **Team- en Enterprise-abonnementen**: een Owner gaat naar **Organization settings > Connectors**,
  klikt op **Add** en daarna op **Custom**, en kiest **Web** als om het type wordt gevraagd.

### 2. De connectorgegevens invoeren {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: kies `authorization` als headernaam, voer `Bearer <api key>` in als waarde,
   inclusief het woord `Bearer` en de spatie, en markeer de header als **Required**.
4. Klik op **Add**.

!!! warning "Iedereen deelt de key"

    Elk lid dat de connector gebruikt, werkt met dezelfde API-key en dus met dezelfde
    *digna*-gebruiker. Maak een aparte *digna*-gebruiker voor de connector aan en geef die alleen
    de projecten en rollen die iedereen mag hebben, bijv. de rol reader.

Bij Team- en Enterprise-abonnementen maken leden daarna verbinding onder **Customize > Connectors**,
waar de connector het label **Custom** draagt.

Claude kan de header van een bestaande connector niet wijzigen. Om een nieuwe key te gebruiken,
verwijder je de connector en voeg je hem opnieuw toe.

---

## Problemen oplossen met Claude {: #troubleshooting-claude }

### claude mcp list toont Failed to connect

Voer `claude mcp get digna` uit om de reden te zien. Een `401` betekent dat de key is geweigerd; zie
[401 Unauthorized](overview.md#troubleshooting). Claude Code waarschuwt ook voor spaties of een
regeleinde aan het begin of einde van de key, die vaak bij het kopiëren meekomen.

### digna verschijnt niet in Claude Desktop

- Controleer of Node.js 18 of later is geïnstalleerd: `node --version`.
- Controleer of `claude_desktop_config.json` geldige JSON is. Door een ontbrekende komma wordt geen
  enkele server in het bestand geladen.
- Sluit Claude Desktop volledig af, niet alleen het venster, en start het opnieuw.

### De custom connector kan de server niet bereiken

De cloud van Anthropic kan het endpoint niet bereiken. Controleer of het via HTTPS met een geldig
certificaat vanaf het internet bereikbaar is, of maak in plaats daarvan verbinding via
[Claude Code](#claude-code).

---

## Zie ook {: #see-also }

- [Overzicht AI-agents](overview.md): endpoint, API-key, beveiliging en algemene probleemoplossing
- [Gemini](gemini_mcp_guide.md): Antigravity of Gemini CLI verbinden
- [digna Agentic](../platform/agentic/Introduction.md): wat AI-agents met *digna* kunnen doen
