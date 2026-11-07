---
title: Gemini – forbind Antigravity og Gemini CLI med digna via MCP | digna-dokumentation
description: Forbind Googles Gemini-værktøjer med digna gennem digna MCP Server — Antigravity CLI, IDE og app med mcp_config.json og Gemini CLI med settings.json eller gemini mcp add, med en API-nøgle i Authorization-headeren.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, digna API-nøgle
---

# Forbind Gemini med digna

Denne vejledning forbinder Googles Gemini-værktøjer med **digna MCP Server**. Du skal bruge
MCP-endpointet for din *digna*-installation og en API-nøgle, som beskrevet i
[Oversigt over AI-agenter](overview.md).

Eksemplerne bruger `https://digna.example.com/mcp` som endpoint. Erstat det med dit eget.

## Vælg dit værktøj {: #choose-your-tool }

| Værktøj | Til | Konfiguration |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE og app | Googles agentværktøjer. Antigravity CLI erstattede Gemini CLI for personlige Google-konti i juni 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard- og Enterprise-licenser samt betalte Gemini API-nøgler | `settings.json` eller `gemini mcp add` |
| Gemini Enterprise-appen | — | Understøttes ikke. Dens custom MCP connector logger ind med OAuth eller en Google Cloud-tjenestekonto, mens digna MCP Server godkender med API-nøgler |

Alle disse værktøjer forbinder fra den maskine, de kører på, så de virker med *digna* inden for
jeres virksomhedsnetværk, så længe den maskine kan nå endpointet.

---

## Antigravity {: #antigravity }

Antigravity læser sine MCP-servere fra `mcp_config.json`, som deles af CLI'en, IDE'en og appen.

### 1. Åbn mcp_config.json {: #1-open-mcp-config-json }

| Scope | Fil |
|---|---|
| Alle dine projekter | `~/.gemini/config/mcp_config.json` |
| Ét workspace | `.agents/mcp_config.json` i workspacet |

Sådan åbner du den fil, der er i brug:

- **CLI**: skriv `/mcp`, og tryk på ++enter++ for at åbne MCP-manageren.
- **IDE**: i agentens sidepanel skal du åbne menuen **…**, vælge **MCP Servers**, derefter
  **Manage MCP Servers** og så **View raw config**.
- **App**: gå til **Customizations** > **Installed** > **MCP Servers**, og brug
  **Copy Config File Path**.

### 2. Tilføj digna-serveren {: #2-add-the-digna-server }

Tilføj `digna`-posten. Hvis filen allerede har en `mcpServers`-sektion, så tilføj den dér:

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

Antigravity når kun eksterne servere over streamable HTTP, som digna MCP Server bruger. Skriv
endpointet som `serverUrl`; nøglen `httpUrl` fra Gemini CLI understøttes ikke.

### 3. Bekræft forbindelsen {: #3-verify-the-connection }

Skriv `/mcp` i CLI'en: MCP-manageren viser serveren `digna` med dens status og værktøjer og kan
genindlæse konfigurationen og vise forbindelseslogs. I IDE'en vises serveren under
**Manage MCP Servers**.

!!! warning "Beskyt filen"

    `mcp_config.json` indeholder API-nøglen i klartekst. Hold en workspace-fil
    `.agents/mcp_config.json` ude af versionsstyring, og lad kun din egen konto læse den globale fil.

---

## Gemini CLI {: #gemini-cli }

### 1. Tilføj serveren {: #1-add-the-server }

Læg API-nøglen i en miljøvariabel, og tilføj derefter serveren:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Din shell indsætter `$DIGNA_API_KEY`, når du kører kommandoen, så Gemini CLI gemmer nøglen i sine
indstillinger. Uden `--scope user` tilføjes serveren kun til det aktuelle projekt.

### 2. Eller redigér settings.json {: #2-or-edit-settings-json }

Kommandoen ovenfor skriver til `settings.json`. Sådan redigerer du filen selv:

| Scope | Fil |
|---|---|
| Alle dine projekter | `~/.gemini/settings.json` |
| Ét projekt | `.gemini/settings.json` i projektet |

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

Brug `httpUrl`, nøglen til streamable HTTP. Den lignende nøgle `url` vælger den ældre SSE-transport,
som digna MCP Server ikke tilbyder. Brug ikke understregninger i servernavnet.

!!! tip "Lad trust være slået fra"

    Gemini CLI spørger før hvert værktøjskald, medmindre serveren har `"trust": true`. Lad `trust`
    være slået fra for *digna*, så du bekræfter hver ændring, en agent foretager i din konfiguration.

### 3. Bekræft forbindelsen {: #3-verify-the-connection-gemini-cli }

Fra din shell:

```bash
gemini mcp list
```

Serveren `digna` skal vises som forbundet. I en Gemini CLI-session kan du køre `/mcp` for at se
serveren og dens værktøjer.

---

## Fejlfinding i Gemini {: #troubleshooting-gemini }

### Serveren vises som afbrudt

- Tjek, at endpointet ender på `/mcp` og kan nås fra din maskine.
- Tjek nøglens navn: `serverUrl` i Antigravity, `httpUrl` i Gemini CLI.
- En `401` betyder, at nøglen blev afvist; se [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI starter ikke længere for min konto

Siden juni 2026 bruger personlige Google-konti Antigravity CLI i stedet for Gemini CLI. Flyt
`digna`-posten til `mcp_config.json` som beskrevet under [Antigravity](#antigravity), og omdøb
`httpUrl` til `serverUrl`.

---

## Se også {: #see-also }

- [Oversigt over AI-agenter](overview.md): endpoint, API-nøgle, sikkerhed og generel fejlfinding
- [Claude](claude_mcp_guide.md): forbind Claude Code, Claude Desktop eller en custom connector
- [digna Agentic](../platform/agentic/Introduction.md): hvad AI-agenter kan gøre med *digna*
