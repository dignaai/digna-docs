---
title: Gemini – koble Antigravity og Gemini CLI til digna via MCP | digna-dokumentasjon
description: Koble Googles Gemini-verktøy til digna via digna MCP Server — Antigravity CLI, IDE og app med mcp_config.json, og Gemini CLI med settings.json eller gemini mcp add, med en API-nøkkel i Authorization-headeren.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, digna API-nøkkel
---

# Koble Gemini til digna

Denne veiledningen kobler Googles Gemini-verktøy til **digna MCP Server**. Du trenger MCP-endepunktet
til *digna*-installasjonen din og en API-nøkkel, som beskrevet i
[Oversikt over AI-agenter](overview.md).

Eksemplene bruker `https://digna.example.com/mcp` som endepunkt. Erstatt det med ditt eget.

## Velg verktøyet ditt {: #choose-your-tool }

| Verktøy | For | Konfigurasjon |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE og app | Googles agentverktøy. Antigravity CLI erstattet Gemini CLI for individuelle Google-kontoer i juni 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard- og Enterprise-lisenser samt betalte Gemini API-nøkler | `settings.json` eller `gemini mcp add` |
| Gemini Enterprise-appen | — | Støttes ikke. Den tilpassede MCP-connectoren dens logger inn med OAuth eller en tjenestekonto i Google Cloud, mens digna MCP Server autentiserer med API-nøkler |

Alle disse verktøyene kobler til fra maskinen de kjører på, så de fungerer med *digna* innenfor
bedriftsnettverket ditt så lenge den maskinen når endepunktet.

---

## Antigravity {: #antigravity }

Antigravity leser MCP-serverne sine fra `mcp_config.json`, som deles av CLI, IDE og app.

### 1. Åpne mcp_config.json {: #1-open-mcp-config-json }

| Omfang | Fil |
|---|---|
| Alle prosjektene dine | `~/.gemini/config/mcp_config.json` |
| Ett workspace | `.agents/mcp_config.json` i workspacet |

Slik åpner du filen som er i bruk:

- **CLI**: skriv `/mcp` og trykk ++enter++ for å åpne MCP-behandleren.
- **IDE**: i agentens sidepanel åpner du menyen **…**, velger **MCP Servers**, deretter
  **Manage MCP Servers** og så **View raw config**.
- **App**: gå til **Customizations** > **Installed** > **MCP Servers** og bruk
  **Copy Config File Path**.

### 2. Legg til digna-serveren {: #2-add-the-digna-server }

Legg til `digna`-oppføringen. Hvis filen allerede har en `mcpServers`-seksjon, legger du den til der:

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

Antigravity når eksterne servere bare over streamable HTTP, som digna MCP Server bruker. Skriv
endepunktet som `serverUrl`; nøkkelen `httpUrl` fra Gemini CLI støttes ikke.

### 3. Bekreft tilkoblingen {: #3-verify-the-connection }

I CLI skriver du `/mcp`: MCP-behandleren viser serveren `digna` med status og verktøy, og kan laste
inn konfigurasjonen på nytt og vise tilkoblingslogger. I IDE vises serveren under
**Manage MCP Servers**.

!!! warning "Beskytt filen"

    `mcp_config.json` inneholder API-nøkkelen i klartekst. Hold en workspace-fil
    `.agents/mcp_config.json` utenfor versjonskontroll, og la bare din egen konto lese den globale
    filen.

---

## Gemini CLI {: #gemini-cli }

### 1. Legg til serveren {: #1-add-the-server }

Legg API-nøkkelen i en miljøvariabel, og legg deretter til serveren:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Skallet ditt fyller inn `$DIGNA_API_KEY` når du kjører kommandoen, så Gemini CLI lagrer nøkkelen i
innstillingene sine. Uten `--scope user` legges serveren bare til i det gjeldende prosjektet.

### 2. Eller rediger settings.json {: #2-or-edit-settings-json }

Kommandoen ovenfor skriver til `settings.json`. Slik redigerer du filen selv:

| Omfang | Fil |
|---|---|
| Alle prosjektene dine | `~/.gemini/settings.json` |
| Ett prosjekt | `.gemini/settings.json` i prosjektet |

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

Bruk `httpUrl`, nøkkelen for streamable HTTP. Den lignende nøkkelen `url` velger den eldre
SSE-transporten, som digna MCP Server ikke tilbyr. Ikke bruk understrek i servernavnet.

!!! tip "La trust være slått av"

    Gemini CLI spør før hvert verktøykall med mindre serveren har `"trust": true`. La `trust` være
    slått av for *digna*, slik at du bekrefter hver endring en agent gjør i konfigurasjonen din.

### 3. Bekreft tilkoblingen {: #3-verify-the-connection-gemini-cli }

Fra skallet ditt:

```bash
gemini mcp list
```

Serveren `digna` må vises som tilkoblet. I en Gemini CLI-økt kjører du `/mcp` for å se serveren og
verktøyene dens.

---

## Feilsøking av Gemini {: #troubleshooting-gemini }

### Serveren vises som frakoblet

- Sjekk at endepunktet slutter på `/mcp` og er tilgjengelig fra maskinen din.
- Sjekk nøkkelnavnet: `serverUrl` i Antigravity, `httpUrl` i Gemini CLI.
- En `401` betyr at nøkkelen ble avvist; se [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI starter ikke lenger for kontoen min

Siden juni 2026 bruker individuelle Google-kontoer Antigravity CLI i stedet for Gemini CLI. Flytt
`digna`-oppføringen til `mcp_config.json` som beskrevet under [Antigravity](#antigravity), og gi
`httpUrl` nytt navn til `serverUrl`.

---

## Se også {: #see-also }

- [Oversikt over AI-agenter](overview.md): endepunkt, API-nøkkel, sikkerhet og generell feilsøking
- [Claude](claude_mcp_guide.md): koble til Claude Code, Claude Desktop eller en tilpasset connector
- [digna Agentic](../platform/agentic/Introduction.md): hva AI-agenter kan gjøre med *digna*
