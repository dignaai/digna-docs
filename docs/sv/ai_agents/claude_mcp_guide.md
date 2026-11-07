---
title: Claude – anslut Claude till digna via MCP | digna Dokumentation
description: Anslut Claude till digna via digna MCP Server — Claude Code från kommandoraden eller med en delad .mcp.json, Claude Desktop med en lokal brygga och anpassade connectorer i claude.ai, med en API-nyckel i Authorization-headern.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, anpassad connector claude.ai, digna MCP server, mcp-remote, Authorization Bearer, digna API-nyckel
---

# Anslut Claude till digna

Den här guiden ansluter Claude till **digna MCP Server**. Du behöver MCP-endpointen för din
*digna*-installation och en API-nyckel, enligt beskrivningen i [Översikt över AI-agenter](overview.md).

Exemplen använder `https://digna.example.com/mcp` som endpoint. Ersätt den med din egen.

## Välj hur du ansluter {: #choose-how-to-connect }

| Claude-produkt | Ansluter från | Fungerar med *digna* inom ditt nätverk |
|---|---|---|
| [Claude Code](#claude-code) | Din maskin | Ja |
| [Claude Desktop med en lokal brygga](#claude-desktop-with-a-local-bridge) | Din maskin | Ja |
| [Anpassad connector](#custom-connector) i claude.ai, Claude Desktop och Claude mobile | Anthropics moln | Nej. Endpointen måste vara nåbar från internet |

För en *digna*-installation som körs inom ditt företagsnätverk, använd Claude Code eller Claude
Desktop med en lokal brygga.

---

## Claude Code {: #claude-code }

### 1. Lägg till servern {: #1-add-the-server }

Lägg API-nyckeln i en miljövariabel och lägg sedan till servern:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Ditt skal fyller i `$DIGNA_API_KEY` när du kör kommandot, så Claude Code sparar nyckeln i sin egen
konfiguration.

`--scope` avgör var servern är tillgänglig:

| Omfång | Tillgänglig |
|---|---|
| `local` (standard) | För dig, bara i det aktuella projektet |
| `user` | För dig, i alla projekt |
| `project` | För alla som arbetar i projektet, via en `.mcp.json`-fil i projektet |

### 2. Dela servern med ditt team (valfritt) {: #2-share-the-server-with-your-team }

För att ge alla i ett projekt samma server, lägg till en `.mcp.json`-fil i projektets rotkatalog.
Skriv inte in nyckeln i filen. Claude Code fyller i `${DIGNA_API_KEY}` från varje persons egen
miljö:

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

Var och en sätter `DIGNA_API_KEY` till sin egen nyckel. Första gången Claude Code hittar filen
frågar det om servrarna i den ska användas.

### 3. Verifiera anslutningen {: #3-verify-the-connection }

I ditt skal:

```bash
claude mcp list
```

Servern `digna` måste visa `✔ Connected`. I en Claude Code-session kör du `/mcp` för att se
servern och dess verktyg.

---

## Claude Desktop med en lokal brygga {: #claude-desktop-with-a-local-bridge }

Claude Desktops konfigurationsfil startar lokala MCP-servrar på din maskin. En liten brygga,
open source-paketet [`mcp-remote`](https://github.com/geelen/mcp-remote), körs där och
vidarebefordrar varje förfrågan till *digna*-endpointen med din API-nyckel. Eftersom bryggan körs
på din maskin fungerar det här med *digna* inom ditt företagsnätverk.

!!! note "Ett communitypaket"

    `mcp-remote` underhålls av sin open source-community, inte av Anthropic eller digna. Kontrollera
    att din organisation tillåter det innan du använder det.

### 1. Installera Node.js {: #1-install-nodejs }

Bryggan kräver [Node.js](https://nodejs.org) 18 eller senare. Claude Desktop använder den
Node.js-version som är installerad på ditt system. Kontrollera den med:

```bash
node --version
```

### 2. Redigera konfigurationsfilen {: #2-edit-the-configuration-file }

Öppna `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Lägg till servern `digna`. Om filen redan har ett `mcpServers`-avsnitt lägger du till
`digna`-posten där:

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

!!! warning "Behåll headern exakt som den visas"

    Skriv `Authorization:${AUTH_HEADER}` utan mellanslag och lägg `Bearer <api key>` i `env`.
    Claude Desktop på Windows escapar inte mellanslag i `args`, så ett mellanslag där förstör
    headern.

### 3. Starta om Claude Desktop {: #3-restart-claude-desktop }

Avsluta Claude Desktop helt och starta det igen. I en ny chatt klickar du på **+** och öppnar
**Connectors**: `digna` måste finnas i listan och vara påslagen.

---

## Anpassad connector {: #custom-connector }

En anpassad connector gör *digna* tillgänglig i claude.ai, Claude Desktop och Claudes mobilappar
utan någon lokal installation. Det är Anthropics moln som ansluter till endpointen, så det här
fungerar bara när:

- *digna*-endpointen är nåbar från internet via HTTPS
- Din Claude-organisation har alternativet **Request headers** i dialogrutan
  **Add custom connector**. Anthropic erbjuder det som beta till ett begränsat antal organisationer

!!! warning "Inte för digna inom ditt nätverk"

    Claudes MCP-tunnlar, som når servrar i ett privat nätverk, kräver OAuth på MCP-servern. digna
    MCP Server autentiserar med API-nycklar, så en tunnel kan inte användas. Använd
    [Claude Code](#claude-code) eller [Claude Desktop med en lokal brygga](#claude-desktop-with-a-local-bridge)
    i stället.

### 1. Öppna inställningarna för connectorer {: #1-open-the-connector-settings }

- **Planerna Free, Pro, Max och Ultra**: gå till **Customize > Connectors** och klicka på
  **Add custom connector**.
- **Planerna Team och Enterprise**: en Owner går till **Organization settings > Connectors**,
  klickar på **Add** och sedan **Custom**, och väljer **Web** om typen efterfrågas.

### 2. Ange uppgifterna för connectorn {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: välj `authorization` som headernamn, ange `Bearer <api key>` som värde,
   inklusive ordet `Bearer` och mellanslaget, och markera den som **Required**.
4. Klicka på **Add**.

!!! warning "Alla delar nyckeln"

    Varje medlem som använder connectorn arbetar med samma API-nyckel och därmed med samma
    *digna*-användare. Skapa en dedikerad *digna*-användare för connectorn och ge den bara de
    projekt och roller som alla får ha, t.ex. läsarrollen.

I planerna Team och Enterprise ansluter medlemmarna sedan under **Customize > Connectors**, där
connectorn har etiketten **Custom**.

Claude kan inte ändra headern för en befintlig connector. För att använda en ny nyckel tar du bort
connectorn och lägger till den igen.

---

## Felsökning av Claude {: #troubleshooting-claude }

### claude mcp list visar Failed to connect

Kör `claude mcp get digna` för att se orsaken. En `401` betyder att nyckeln avvisades; se
[401 Unauthorized](overview.md#troubleshooting). Claude Code varnar också för mellanslag eller en
radbrytning i början eller slutet av nyckeln, som ofta följer med när man kopierar den.

### digna visas inte i Claude Desktop

- Kontrollera att Node.js 18 eller senare är installerat: `node --version`.
- Kontrollera att `claude_desktop_config.json` är giltig JSON. Ett saknat kommatecken gör att ingen
  server i filen laddas.
- Avsluta Claude Desktop helt, inte bara fönstret, och starta det igen.

### Den anpassade connectorn når inte servern

Anthropics moln når inte endpointen. Kontrollera att den är nåbar från internet via HTTPS med ett
giltigt certifikat, eller anslut via [Claude Code](#claude-code) i stället.

---

## Se även {: #see-also }

- [Översikt över AI-agenter](overview.md): endpoint, API-nyckel, säkerhet och allmän felsökning
- [Gemini](gemini_mcp_guide.md): anslut Antigravity eller Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): vad AI-agenter kan göra med *digna*
