# Koble Claude til digna

Denne veiledningen kobler Claude til **digna MCP Server**. Du trenger MCP-endepunktet til
*digna*-installasjonen din og en API-nøkkel, som beskrevet i [Oversikt over AI-agenter](overview.md).

Eksemplene bruker `https://digna.example.com/mcp` som endepunkt. Erstatt det med ditt eget.

## Velg hvordan du kobler til {: #choose-how-to-connect }

| Claude-produkt | Kobler til fra | Fungerer med *digna* innenfor nettverket ditt |
|---|---|---|
| [Claude Code](#claude-code) | Maskinen din | Ja |
| [Claude Desktop med en lokal bro](#claude-desktop-with-a-local-bridge) | Maskinen din | Ja |
| [Tilpasset connector](#custom-connector) i claude.ai, Claude Desktop og Claude mobile | Anthropics sky | Nei. Endepunktet må være tilgjengelig fra internett |

For en *digna*-installasjon som kjører innenfor bedriftsnettverket ditt, bruker du Claude Code eller
Claude Desktop med en lokal bro.

---

## Claude Code {: #claude-code }

### 1. Legg til serveren {: #1-add-the-server }

Legg API-nøkkelen i en miljøvariabel, og legg deretter til serveren:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Skallet ditt fyller inn `$DIGNA_API_KEY` når du kjører kommandoen, så Claude Code lagrer nøkkelen i
sin egen konfigurasjon.

`--scope` bestemmer hvor serveren er tilgjengelig:

| Omfang | Tilgjengelig |
|---|---|
| `local` (standard) | For deg, bare i det gjeldende prosjektet |
| `user` | For deg, i alle prosjekter |
| `project` | For alle som jobber i prosjektet, via en `.mcp.json`-fil i prosjektet |

### 2. Del serveren med teamet ditt (valgfritt) {: #2-share-the-server-with-your-team }

For å gi alle i et prosjekt den samme serveren legger du til en `.mcp.json`-fil i prosjektets
rotmappe. Ikke skriv nøkkelen inn i filen. Claude Code fyller inn `${DIGNA_API_KEY}` fra hver persons
eget miljø:

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

Hver person setter `DIGNA_API_KEY` til sin egen nøkkel. Første gang Claude Code finner filen, spør
det om serverne i den skal brukes.

### 3. Bekreft tilkoblingen {: #3-verify-the-connection }

Fra skallet ditt:

```bash
claude mcp list
```

Serveren `digna` må vise `✔ Connected`. I en Claude Code-økt kjører du `/mcp` for å se serveren og
verktøyene dens.

---

## Claude Desktop med en lokal bro {: #claude-desktop-with-a-local-bridge }

Konfigurasjonsfilen til Claude Desktop starter lokale MCP-servere på maskinen din. En liten bro,
open source-pakken [`mcp-remote`](https://github.com/geelen/mcp-remote), kjører der og videresender
hver forespørsel til *digna*-endepunktet med API-nøkkelen din. Fordi broen kjører på maskinen din,
fungerer dette med *digna* innenfor bedriftsnettverket ditt.

!!! note "En community-pakke"

    `mcp-remote` vedlikeholdes av sitt open source-fellesskap, ikke av Anthropic eller digna. Sjekk
    at organisasjonen din tillater den før du bruker den.

### 1. Installer Node.js {: #1-install-nodejs }

Broen trenger [Node.js](https://nodejs.org) 18 eller nyere. Claude Desktop bruker Node.js-versjonen
som er installert på systemet ditt. Sjekk den med:

```bash
node --version
```

### 2. Rediger konfigurasjonsfilen {: #2-edit-the-configuration-file }

Åpne `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Legg til serveren `digna`. Hvis filen allerede har en `mcpServers`-seksjon, legger du til
`digna`-oppføringen i den:

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

!!! warning "Behold headeren nøyaktig som vist"

    Skriv `Authorization:${AUTH_HEADER}` uten mellomrom, og legg `Bearer <api key>` i `env`.
    Claude Desktop på Windows escaper ikke mellomrom i `args`, så et mellomrom der ødelegger
    headeren.

### 3. Start Claude Desktop på nytt {: #3-restart-claude-desktop }

Avslutt Claude Desktop helt og start det igjen. I en ny chat klikker du **+** og åpner
**Connectors**: `digna` må stå i listen og være slått på.

---

## Tilpasset connector {: #custom-connector }

En tilpasset connector gjør *digna* tilgjengelig i claude.ai, Claude Desktop og Claudes mobilapper
uten noe lokalt oppsett. Det er Anthropics sky som kobler til endepunktet, så dette fungerer bare
når:

- *digna*-endepunktet er tilgjengelig fra internett over HTTPS
- Claude-organisasjonen din har alternativet **Request headers** i dialogboksen
  **Add custom connector**. Anthropic tilbyr det som beta til et begrenset utvalg organisasjoner

!!! warning "Ikke for digna innenfor nettverket ditt"

    Claudes MCP-tunneler, som når servere i et privat nettverk, krever OAuth på MCP-serveren. digna
    MCP Server autentiserer med API-nøkler, så en tunnel kan ikke brukes. Bruk
    [Claude Code](#claude-code) eller [Claude Desktop med en lokal bro](#claude-desktop-with-a-local-bridge)
    i stedet.

### 1. Åpne connector-innstillingene {: #1-open-the-connector-settings }

- **Planene Free, Pro, Max og Ultra**: gå til **Customize > Connectors** og klikk
  **Add custom connector**.
- **Planene Team og Enterprise**: en Owner går til **Organization settings > Connectors**, klikker
  **Add** og deretter **Custom**, og velger **Web** hvis det blir spurt om typen.

### 2. Legg inn connector-detaljene {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: velg `authorization` som headernavn, skriv inn `Bearer <api key>` som verdi,
   inkludert ordet `Bearer` og mellomrommet, og merk den som **Required**.
4. Klikk **Add**.

!!! warning "Alle deler nøkkelen"

    Hvert medlem som bruker connectoren, arbeider med den samme API-nøkkelen og dermed med den samme
    *digna*-brukeren. Opprett en egen *digna*-bruker for connectoren, og gi den bare de prosjektene
    og rollene alle kan ha, f.eks. leserrollen.

På planene Team og Enterprise kobler medlemmene seg deretter til under **Customize > Connectors**,
der connectoren har etiketten **Custom**.

Claude kan ikke endre headeren til en eksisterende connector. For å bruke en ny nøkkel fjerner du
connectoren og legger den til på nytt.

---

## Feilsøking av Claude {: #troubleshooting-claude }

### claude mcp list viser Failed to connect

Kjør `claude mcp get digna` for å se årsaken. En `401` betyr at nøkkelen ble avvist; se
[401 Unauthorized](overview.md#troubleshooting). Claude Code advarer også om mellomrom eller et
linjeskift i starten eller slutten av nøkkelen, som ofte følger med når man kopierer den.

### digna vises ikke i Claude Desktop

- Sjekk at Node.js 18 eller nyere er installert: `node --version`.
- Sjekk at `claude_desktop_config.json` er gyldig JSON. Et manglende komma gjør at ingen av serverne
  i filen lastes inn.
- Avslutt Claude Desktop helt, ikke bare vinduet, og start det igjen.

### Den tilpassede connectoren når ikke serveren

Anthropics sky når ikke endepunktet. Sjekk at det er tilgjengelig fra internett over HTTPS med et
gyldig sertifikat, eller koble til via [Claude Code](#claude-code) i stedet.

---

## Se også {: #see-also }

- [Oversikt over AI-agenter](overview.md): endepunkt, API-nøkkel, sikkerhet og generell feilsøking
- [Gemini](gemini_mcp_guide.md): koble til Antigravity eller Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): hva AI-agenter kan gjøre med *digna*