---
title: Claude – forbind Claude med digna via MCP | digna-dokumentation
description: Forbind Claude med digna gennem digna MCP Server — Claude Code fra kommandolinjen eller en delt .mcp.json, Claude Desktop med en lokal bro og custom connectors i claude.ai, med en API-nøgle i Authorization-headeren.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, claude.ai custom connector, digna MCP server, mcp-remote, Authorization Bearer, digna API-nøgle
---

# Forbind Claude med digna

Denne vejledning forbinder Claude med **digna MCP Server**. Du skal bruge MCP-endpointet for din
*digna*-installation og en API-nøgle, som beskrevet i [Oversigt over AI-agenter](overview.md).

Eksemplerne bruger `https://digna.example.com/mcp` som endpoint. Erstat det med dit eget.

## Vælg, hvordan du forbinder {: #choose-how-to-connect }

| Claude-produkt | Forbinder fra | Virker med *digna* inden for jeres netværk |
|---|---|---|
| [Claude Code](#claude-code) | Din maskine | Ja |
| [Claude Desktop med en lokal bro](#claude-desktop-with-a-local-bridge) | Din maskine | Ja |
| [Custom connector](#custom-connector) i claude.ai, Claude Desktop og Claude mobil | Anthropics cloud | Nej. Endpointet skal kunne nås fra internettet |

Til en *digna*-installation, der kører inden for jeres virksomhedsnetværk, skal du bruge Claude Code
eller Claude Desktop med en lokal bro.

---

## Claude Code {: #claude-code }

### 1. Tilføj serveren {: #1-add-the-server }

Læg API-nøglen i en miljøvariabel, og tilføj derefter serveren:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Din shell indsætter `$DIGNA_API_KEY`, når du kører kommandoen, så Claude Code gemmer nøglen i sin
egen konfiguration.

`--scope` bestemmer, hvor serveren er tilgængelig:

| Scope | Tilgængelig |
|---|---|
| `local` (standard) | For dig, kun i det aktuelle projekt |
| `user` | For dig, i alle projekter |
| `project` | For alle, der arbejder i projektet, gennem en `.mcp.json`-fil i projektet |

### 2. Del serveren med dit team (valgfrit) {: #2-share-the-server-with-your-team }

For at give alle i et projekt den samme server skal du tilføje en `.mcp.json`-fil i projektets rod.
Skriv ikke nøglen i filen. Claude Code indsætter `${DIGNA_API_KEY}` fra hver persons eget miljø:

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

Hver person sætter `DIGNA_API_KEY` til sin egen nøgle. Første gang Claude Code finder filen, spørger
den, om serverne i den skal bruges.

### 3. Bekræft forbindelsen {: #3-verify-the-connection }

Fra din shell:

```bash
claude mcp list
```

Serveren `digna` skal vise `✔ Connected`. I en Claude Code-session kan du køre `/mcp` for at se
serveren og dens værktøjer.

---

## Claude Desktop med en lokal bro {: #claude-desktop-with-a-local-bridge }

Claude Desktops konfigurationsfil starter lokale MCP-servere på din maskine. En lille bro, den
open source-baserede pakke [`mcp-remote`](https://github.com/geelen/mcp-remote), kører der og
videresender hver forespørgsel til *digna*-endpointet med din API-nøgle. Fordi broen kører på din
maskine, virker dette med *digna* inden for jeres virksomhedsnetværk.

!!! note "En community-pakke"

    `mcp-remote` vedligeholdes af sit open source-community, ikke af Anthropic eller digna. Tjek, at
    din organisation tillader den, før du bruger den.

### 1. Installér Node.js {: #1-install-nodejs }

Broen kræver [Node.js](https://nodejs.org) 18 eller nyere. Claude Desktop bruger den Node.js-version,
der er installeret på dit system. Tjek den med:

```bash
node --version
```

### 2. Redigér konfigurationsfilen {: #2-edit-the-configuration-file }

Åbn `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Tilføj serveren `digna`. Hvis filen allerede har en `mcpServers`-sektion, så tilføj `digna`-posten
i den:

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

!!! warning "Behold headeren præcis som vist"

    Skriv `Authorization:${AUTH_HEADER}` uden mellemrum, og læg `Bearer <api key>` i `env`.
    Claude Desktop på Windows escaper ikke mellemrum i `args`, så et mellemrum dér ødelægger
    headeren.

### 3. Genstart Claude Desktop {: #3-restart-claude-desktop }

Afslut Claude Desktop helt, og start det igen. Klik på **+** i en ny chat, og åbn
**Connectors**: `digna` skal stå på listen og være slået til.

---

## Custom connector {: #custom-connector }

En custom connector gør *digna* tilgængelig i claude.ai, Claude Desktop og Claudes mobilapps uden
nogen lokal opsætning. Anthropics cloud forbinder til endpointet, så det virker kun, når:

- *digna*-endpointet kan nås fra internettet over HTTPS
- Din Claude-organisation har indstillingen **Request headers** i dialogen
  **Add custom connector**. Anthropic tilbyder den som beta til et begrænset antal organisationer

!!! warning "Ikke til digna inden for jeres netværk"

    Claudes MCP-tunneler, som når servere inden for et privat netværk, kræver OAuth på
    MCP-serveren. digna MCP Server godkender med API-nøgler, så en tunnel kan ikke bruges. Brug
    [Claude Code](#claude-code) eller [Claude Desktop med en lokal bro](#claude-desktop-with-a-local-bridge)
    i stedet.

### 1. Åbn connector-indstillingerne {: #1-open-the-connector-settings }

- **Free-, Pro-, Max- og Ultra-abonnementer**: gå til **Customize > Connectors**, og klik på
  **Add custom connector**.
- **Team- og Enterprise-abonnementer**: en Owner går til **Organization settings > Connectors**,
  klikker på **Add** og derefter **Custom** og vælger **Web**, hvis der spørges om typen.

### 2. Indtast connectorens oplysninger {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: vælg `authorization` som headernavn, indtast `Bearer <api key>` som
   værdi, inklusive ordet `Bearer` og mellemrummet, og markér den som **Required**.
4. Klik på **Add**.

!!! warning "Alle deler nøglen"

    Alle medlemmer, der bruger connectoren, arbejder med den samme API-nøgle og dermed med den samme
    *digna*-bruger. Opret en dedikeret *digna*-bruger til connectoren, og giv den kun de projekter
    og roller, som alle må have, f.eks. læserrollen.

På Team- og Enterprise-abonnementer forbinder medlemmerne derefter under **Customize > Connectors**,
hvor connectoren har mærket **Custom**.

Claude kan ikke ændre headeren på en eksisterende connector. For at bruge en ny nøgle skal du
fjerne connectoren og tilføje den igen.

---

## Fejlfinding i Claude {: #troubleshooting-claude }

### claude mcp list viser Failed to connect

Kør `claude mcp get digna` for at se årsagen. En `401` betyder, at nøglen blev afvist; se
[401 Unauthorized](overview.md#troubleshooting). Claude Code advarer også om mellemrum eller et
linjeskift i starten eller slutningen af nøglen, som ofte kommer med, når den kopieres.

### digna vises ikke i Claude Desktop

- Tjek, at Node.js 18 eller nyere er installeret: `node --version`.
- Tjek, at `claude_desktop_config.json` er gyldig JSON. Et manglende komma forhindrer alle servere i
  filen i at blive indlæst.
- Afslut Claude Desktop helt, ikke kun vinduet, og start det igen.

### Custom connectoren kan ikke nå serveren

Anthropics cloud kan ikke nå endpointet. Tjek, at det kan nås fra internettet over HTTPS med et
gyldigt certifikat, eller forbind i stedet gennem [Claude Code](#claude-code).

---

## Se også {: #see-also }

- [Oversigt over AI-agenter](overview.md): endpoint, API-nøgle, sikkerhed og generel fejlfinding
- [Gemini](gemini_mcp_guide.md): forbind Antigravity eller Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): hvad AI-agenter kan gøre med *digna*
