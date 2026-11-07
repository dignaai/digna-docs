# Koble AI-agenter til digna

Med **digna MCP Server** kan AI-agenter arbeide med *digna* via
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), en åpen standard som støttes av
Claude, Gemini og mange andre AI-verktøy. En agent som er koblet til *digna*, kan svare på spørsmål
om dataene dine, undersøke varsler og hjelpe til med å konfigurere *digna*. Se
[digna Agentic](../platform/agentic/Introduction.md) for hva agenter kan gjøre.

Denne siden dekker *digna*-siden, som er den samme for alle AI-klienter. Klientveiledningene viser
deretter hvor du legger den inn:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop og tilpassede connectorer
- [Gemini](gemini_mcp_guide.md): Antigravity og Gemini CLI

!!! info "Beta"

    digna Agentic, og dermed digna MCP Server, leveres som betaversjon i
    [Release 2026.11](../changelog/Release_202611.md).

---

## Før du begynner {: #before-you-start }

Du trenger:

- *digna* Release 2026.11 eller nyere
- En lisens som omfatter **digna Agentic**. Uten den avviser MCP-serveren alle forespørsler
- En brukerkonto i *digna*. Agenten handler med den brukerens tillatelser i hvert prosjekt, se
  [Tillatelser](../platform/agentic/how_it_works.md#permissions)
- En AI-klient som kobler til eksterne MCP-servere over **streamable HTTP** og kan sende en
  `Authorization`-header

---

## 1. Finn MCP-endepunktet {: #1-find-the-mcp-endpoint }

MCP-serveren er en del av *digna*-backenden, så det er ingenting ekstra å installere eller starte.
Endepunktet er backendens adresse etterfulgt av `/mcp`:

```text
https://digna.example.com/mcp
```

Hvis backenden kjører direkte på en vert og port, for eksempel etter
`digna serve --address 0.0.0.0 --port 8082`, er endepunktet den adressen med `/mcp`:

```text
http://digna-host:8082/mcp
```

Hvis en reverse proxy står foran backenden, må den videresende `/mcp` til backenden sammen med
`Authorization`-headeren.

!!! warning "Bruk HTTPS i et nettverk"

    Hver forespørsel inneholder en API-nøkkel. Bruk HTTPS når AI-klienten og *digna* ikke kjører på
    samme maskin.

### Hvor tilkoblingen kommer fra {: #where-the-connection-comes-from }

De fleste AI-klienter kobler til fra maskinen de kjører på: Claude Code, Claude Desktop med en
lokal bro, Antigravity og Gemini CLI. For dem trenger *digna* bare å være tilgjengelig fra den
maskinen, for eksempel innenfor bedriftsnettverket ditt.

Claudes **tilpassede connectorer** er annerledes: Det er Anthropics sky som kobler til endepunktet.
De fungerer bare når endepunktet er tilgjengelig fra internett over HTTPS. For en
*digna*-installasjon som bare er tilgjengelig innenfor nettverket ditt, bruker du en klient som
kjører på maskinen din.

---

## 2. Opprett en API-nøkkel {: #2-create-an-api-key }

En AI-klient autentiserer seg med API-nøkkelen til en *digna*-bruker.

1. Logg inn i *digna*.
2. Åpne brukerprofilen din nederst til venstre.
3. Klikk **API Keys** og deretter **Add API Key**.
4. Skriv inn et navn som sier hva nøkkelen er til, f.eks. *Claude Code – Marcin*, og velg når den
   utløper.
5. Kopier nøkkelen. Den vises bare én gang.

Hver forespørsel til MCP-serveren sender nøkkelen i denne headeren:

```text
Authorization: Bearer <api key>
```

Ordet `Bearer` og mellomrommet etter det er en del av headerverdien.

---

## 3. Koble til AI-klienten din {: #3-connect-your-ai-client }

| AI-klient | Kobler til fra | Veiledning |
|---|---|---|
| Claude Code | Maskinen din | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop med en lokal bro | Maskinen din | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Tilpasset connector i Claude (claude.ai, Claude Desktop, Claude mobile) | Anthropics sky | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE og app | Maskinen din | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Maskinen din | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Andre MCP-klienter fungerer også hvis de støtter eksterne servere over streamable HTTP med en
tilpasset header. De fleste av dem leser en konfigurasjon som denne. Se dokumentasjonen til klienten
din for de nøyaktige fil- og nøkkelnavnene:

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

## 4. Prøv det {: #4-try-it }

Spør agenten om noe bare *digna* kan svare på:

- *"List opp prosjektene mine i digna."*
- *"Hvilke datakilder i prosjekt X er ikke grønne i dag?"*
- *"Forklar den siste mislykkede kontrollen for datakilde Y."*

Hvis agenten lister opp prosjektene dine, fungerer tilkoblingen.

---

## Sikkerhet {: #security }

- **Én nøkkel per person og klient.** Da kan du tilbakekalle én enkelt nøkkel, med
  **Delete API Key**, uten å påvirke noen andre.
- **Velg brukeren med omhu.** Agenten kan gjøre alt som nøkkelens bruker kan gjøre. Hvis agenten
  bare skal undersøke data, bruker du en bruker med leserrollen i prosjektene.
- **Hold nøkler unna delte filer.** Ikke commit en konfigurasjonsfil som inneholder en nøkkel. Der
  klienten støtter det, leser du nøkkelen fra en miljøvariabel.
- **Angi en utløpsdato.** Opprett en ny nøkkel før den gamle utløper, og oppdater klienten.
- **Gå gjennom verktøykall.** La klientens bekreftelse av verktøykall være slått på, i hvert fall
  for kall som endrer konfigurasjonen.

---

## Feilsøking {: #troubleshooting }

### 401 Unauthorized

Svaret oppgir årsaken:

| Melding | Årsak |
|---|---|
| `Missing or malformed Authorization header` | Ingen header ble sendt, eller verdien begynner ikke med `Bearer ` |
| `Invalid API key` | Nøkkelen er feil, eller den er slettet |
| `API key expired` | Nøkkelen har utløpt. Opprett en ny |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

*digna*-lisensen har ingen oppføring for digna Agentic, eller den oppføringen har utløpt. Be
digna-teamet om en lisens som omfatter digna Agentic, og installer den slik installasjonsveiledningen
for operativsystemet ditt beskriver.

### Alle forespørsler feiler med en feil om ugyldig lisens

Selve *digna*-lisensen har utløpt. MCP-serveren slutter å svare sammen med dashbordet til en ny
lisens er installert.

### Agenten kan lese, men ikke endre konfigurasjonen

Brukeren bak API-nøkkelen har ikke redaktørrollen i det prosjektet. Bruk nøkkelen til en bruker med
redaktørrollen, eller be en prosjektadministrator om å endre rollen.

### Klienten kan ikke koble til i det hele tatt

Maskinen som kobler til, når ikke endepunktet. Åpne endepunktets adresse fra den maskinen, og sjekk
brannmurer, proxyer og sertifikatet. For en tilpasset connector i Claude står den maskinen i
Anthropics sky, se [Hvor tilkoblingen kommer fra](#where-the-connection-comes-from).