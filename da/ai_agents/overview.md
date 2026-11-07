# Forbind AI-agenter med digna

**digna MCP Server** lader AI-agenter arbejde med *digna* gennem
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), en åben standard, som Claude,
Gemini og mange andre AI-værktøjer understøtter. En agent, der er forbundet med *digna*, kan besvare
spørgsmål om dine data, undersøge alarmer og hjælpe med at konfigurere *digna*. Se
[digna Agentic](../platform/agentic/Introduction.md) for, hvad agenter kan.

Denne side dækker *digna*-delen, som er den samme for alle AI-klienter. Klientvejledningerne viser
derefter, hvor du indtaster den:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop og custom connectors
- [Gemini](gemini_mcp_guide.md): Antigravity og Gemini CLI

!!! info "Beta"

    digna Agentic, og dermed digna MCP Server, leveres som betaversion i
    [Release 2026.11](../changelog/Release_202611.md).

---

## Før du starter {: #before-you-start }

Du skal bruge:

- *digna* Release 2026.11 eller nyere
- En licens, der omfatter **digna Agentic**. Uden den afviser MCP-serveren alle forespørgsler
- En *digna*-brugerkonto. Agenten handler med denne brugers rettigheder i hvert projekt, se
  [Rettigheder](../platform/agentic/how_it_works.md#permissions)
- En AI-klient, der forbinder til eksterne MCP-servere over **streamable HTTP** og kan sende en
  `Authorization`-header

---

## 1. Find MCP-endpointet {: #1-find-the-mcp-endpoint }

MCP-serveren er en del af *digna*-backenden, så der er intet ekstra at installere eller starte.
Dens endpoint er backendens adresse efterfulgt af `/mcp`:

```text
https://digna.example.com/mcp
```

Hvis backenden kører direkte på en vært og en port, f.eks. efter
`digna serve --address 0.0.0.0 --port 8082`, er endpointet den adresse med `/mcp`:

```text
http://digna-host:8082/mcp
```

Hvis der står en reverse proxy foran backenden, skal den videresende `/mcp` til backenden sammen
med `Authorization`-headeren.

!!! warning "Brug HTTPS på et netværk"

    Hver forespørgsel indeholder en API-nøgle. Brug HTTPS, når AI-klienten og *digna* ikke kører på
    samme maskine.

### Hvor forbindelsen kommer fra {: #where-the-connection-comes-from }

De fleste AI-klienter forbinder fra den maskine, de kører på: Claude Code, Claude Desktop med en
lokal bro, Antigravity og Gemini CLI. For dem skal *digna* kun kunne nås fra den maskine, f.eks.
inden for jeres virksomhedsnetværk.

Claudes **custom connectors** er anderledes: Anthropics cloud forbinder til endpointet. De
virker kun, når endpointet kan nås fra internettet over HTTPS. Til en *digna*-installation, der kun
kan nås inden for jeres netværk, skal du bruge en klient, der kører på din maskine.

---

## 2. Opret en API-nøgle {: #2-create-an-api-key }

En AI-klient godkender sig med API-nøglen for en *digna*-bruger.

1. Log ind i *digna*.
2. Åbn din brugerprofil i nederste venstre hjørne.
3. Klik på **API Keys** og derefter **Add API Key**.
4. Indtast et navn, der siger, hvad nøglen bruges til, f.eks. *Claude Code – Marcin*, og vælg,
   hvornår den udløber.
5. Kopiér nøglen. Den vises kun én gang.

Hver forespørgsel til MCP-serveren sender nøglen i denne header:

```text
Authorization: Bearer <api key>
```

Ordet `Bearer` og mellemrummet efter det er en del af headerens værdi.

---

## 3. Forbind din AI-klient {: #3-connect-your-ai-client }

| AI-klient | Forbinder fra | Vejledning |
|---|---|---|
| Claude Code | Din maskine | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop med en lokal bro | Din maskine | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Claude custom connector (claude.ai, Claude Desktop, Claude mobil) | Anthropics cloud | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE og app | Din maskine | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Din maskine | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Andre MCP-klienter virker også, hvis de understøtter eksterne servere over streamable HTTP med en
brugerdefineret header. De fleste af dem læser en konfiguration som denne. Se din klients
dokumentation for de præcise fil- og nøglenavne:

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

Stil agenten et spørgsmål, som kun *digna* kan besvare:

- *"Vis mine digna-projekter."*
- *"Hvilke datakilder i projekt X er ikke grønne i dag?"*
- *"Forklar det seneste fejlede tjek for datakilde Y."*

Hvis agenten viser dine projekter, virker forbindelsen.

---

## Sikkerhed {: #security }

- **Én nøgle pr. person og klient.** Så kan du tilbagekalde en enkelt nøgle med **Delete API Key**
  uden at påvirke andre.
- **Vælg brugeren med omtanke.** Agenten kan alt, hvad nøglens bruger kan. Hvis der kun skal
  undersøges data, så brug en bruger med læserrollen i projekterne.
- **Hold nøgler ude af delte filer.** Commit ikke en konfigurationsfil, der indeholder en nøgle. Hvor
  klienten understøtter det, så læs nøglen fra en miljøvariabel.
- **Sæt en udløbsdato.** Opret en ny nøgle, før den gamle udløber, og opdatér klienten.
- **Gennemgå værktøjskald.** Lad klientens bekræftelse af værktøjskald være slået til, i hvert fald
  for kald, der ændrer konfigurationen.

---

## Fejlfinding {: #troubleshooting }

### 401 Unauthorized

Svaret siger hvorfor:

| Meddelelse | Årsag |
|---|---|
| `Missing or malformed Authorization header` | Der blev ikke sendt nogen header, eller værdien starter ikke med `Bearer ` |
| `Invalid API key` | Nøglen er forkert, eller den er slettet |
| `API key expired` | Nøglen er udløbet. Opret en ny |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

*digna*-licensen har ingen post for digna Agentic, eller posten er udløbet. Bed digna-teamet om en
licens, der omfatter digna Agentic, og installér den som beskrevet i installationsvejledningen for
dit styresystem.

### Alle forespørgsler fejler med en fejl om ugyldig licens

Selve *digna*-licensen er udløbet. MCP-serveren holder op med at svare sammen med dashboardet,
indtil en ny licens er installeret.

### Agenten kan læse, men ikke ændre konfigurationen

Brugeren bag API-nøglen har ikke editorrollen i det projekt. Brug nøglen for en bruger med
editorrollen, eller bed en projektadministrator om at ændre rollen.

### Klienten kan slet ikke forbinde

Den maskine, der forbinder, kan ikke nå endpointet. Åbn endpointets adresse fra den maskine, og
tjek firewalls, proxyer og certifikatet. For en Claude custom connector står den maskine i
Anthropics cloud, se [Hvor forbindelsen kommer fra](#where-the-connection-comes-from).