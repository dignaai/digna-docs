---
title: AI-agenter – översikt över MCP-integrationen | digna Dokumentation
description: Anslut Claude, Gemini och andra AI-agenter till digna via digna MCP Server. Hitta MCP-endpointen, skapa en API-nyckel, kontrollera licens- och nätverkskraven och välj guiden för din AI-klient.
image: /assets/logo_square.png
keywords: digna MCP server, Model Context Protocol, ansluta AI-agent, Claude MCP, Gemini MCP, Antigravity MCP, digna API-nyckel, digna Agentic
---

# Anslut AI-agenter till digna

Med **digna MCP Server** kan AI-agenter arbeta med *digna* via
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), en öppen standard som stöds av
Claude, Gemini och många andra AI-verktyg. En agent som är ansluten till *digna* kan svara på frågor
om dina data, utreda larm och hjälpa till att konfigurera *digna*. Se
[digna Agentic](../platform/agentic/Introduction.md) för vad agenter kan göra.

Den här sidan beskriver *digna*-sidan, som är densamma för alla AI-klienter. Klientguiderna visar
sedan var du anger uppgifterna:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop och anpassade connectorer
- [Gemini](gemini_mcp_guide.md): Antigravity och Gemini CLI

!!! info "Beta"

    digna Agentic, och därmed digna MCP Server, levereras som betaversion i
    [Release 2026.11](../changelog/Release_202611.md).

---

## Innan du börjar {: #before-you-start }

Du behöver:

- *digna* Release 2026.11 eller senare
- En licens som omfattar **digna Agentic**. Utan den avvisar MCP-servern varje förfrågan
- Ett användarkonto i *digna*. Agenten agerar med den användarens behörigheter i varje projekt, se
  [Behörigheter](../platform/agentic/how_it_works.md#permissions)
- En AI-klient som ansluter till fjärranslutna MCP-servrar via **streamable HTTP** och kan skicka
  en `Authorization`-header

---

## 1. Hitta MCP-endpointen {: #1-find-the-mcp-endpoint }

MCP-servern är en del av *digna*-backenden, så det finns inget extra att installera eller starta.
Dess endpoint är backendens adress följd av `/mcp`:

```text
https://digna.example.com/mcp
```

Om backenden körs direkt på en värd och port, till exempel efter
`digna serve --address 0.0.0.0 --port 8082`, är endpointen den adressen med `/mcp`:

```text
http://digna-host:8082/mcp
```

Om en reverse proxy står framför backenden måste den vidarebefordra `/mcp` till backenden
tillsammans med `Authorization`-headern.

!!! warning "Använd HTTPS i ett nätverk"

    Varje förfrågan innehåller en API-nyckel. Använd HTTPS så snart AI-klienten och *digna* inte
    körs på samma maskin.

### Varifrån anslutningen kommer {: #where-the-connection-comes-from }

De flesta AI-klienter ansluter från den maskin de körs på: Claude Code, Claude Desktop med en
lokal brygga, Antigravity och Gemini CLI. För dem behöver *digna* bara vara nåbar från den
maskinen, till exempel inom ditt företagsnätverk.

Claudes **anpassade connectorer** fungerar annorlunda: det är Anthropics moln som ansluter till
endpointen. De fungerar bara när endpointen är nåbar från internet via HTTPS. För en
*digna*-installation som bara är nåbar inom ditt nätverk, använd en klient som körs på din maskin.

---

## 2. Skapa en API-nyckel {: #2-create-an-api-key }

En AI-klient autentiserar sig med API-nyckeln för en *digna*-användare.

1. Logga in i *digna*.
2. Öppna din användarprofil i nedre vänstra hörnet.
3. Klicka på **API Keys** och sedan på **Add API Key**.
4. Ange ett namn som säger vad nyckeln är till för, t.ex. *Claude Code – Marcin*, och välj när den
   ska upphöra att gälla.
5. Kopiera nyckeln. Den visas bara en gång.

Varje förfrågan till MCP-servern skickar nyckeln i den här headern:

```text
Authorization: Bearer <api key>
```

Ordet `Bearer` och mellanslaget efter det är en del av headerns värde.

---

## 3. Anslut din AI-klient {: #3-connect-your-ai-client }

| AI-klient | Ansluter från | Guide |
|---|---|---|
| Claude Code | Din maskin | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop med en lokal brygga | Din maskin | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Anpassad connector i Claude (claude.ai, Claude Desktop, Claude mobile) | Anthropics moln | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE och app | Din maskin | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Din maskin | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Andra MCP-klienter fungerar också om de stöder fjärranslutna servrar via streamable HTTP med en
anpassad header. De flesta läser en konfiguration som den här. Se klientens dokumentation för de
exakta fil- och nyckelnamnen:

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

## 4. Prova {: #4-try-it }

Fråga agenten något som bara *digna* kan svara på:

- *"Lista mina projekt i digna."*
- *"Vilka datakällor i projekt X är inte gröna i dag?"*
- *"Förklara den senaste misslyckade kontrollen för datakälla Y."*

Om agenten listar dina projekt fungerar anslutningen.

---

## Säkerhet {: #security }

- **En nyckel per person och klient.** Då kan du återkalla en enskild nyckel, med
  **Delete API Key**, utan att påverka någon annan.
- **Välj användaren medvetet.** Agenten kan göra allt som nyckelns användare kan göra. Om agenten
  bara ska utreda data, använd en användare med läsarrollen i projekten.
- **Håll nycklar borta från delade filer.** Checka inte in en konfigurationsfil som innehåller en
  nyckel. Om klienten stöder det, läs nyckeln från en miljövariabel.
- **Ange ett utgångsdatum.** Skapa en ny nyckel innan den gamla upphör att gälla och uppdatera
  klienten.
- **Granska verktygsanrop.** Låt klientens bekräftelse av verktygsanrop vara påslagen, åtminstone
  för anrop som ändrar konfigurationen.

---

## Felsökning {: #troubleshooting }

### 401 Unauthorized

Svaret anger orsaken:

| Meddelande | Orsak |
|---|---|
| `Missing or malformed Authorization header` | Ingen header skickades, eller värdet börjar inte med `Bearer ` |
| `Invalid API key` | Nyckeln är fel eller har tagits bort |
| `API key expired` | Nyckeln har gått ut. Skapa en ny |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

*digna*-licensen saknar en post för digna Agentic, eller så har den posten gått ut. Be digna-teamet
om en licens som omfattar digna Agentic och installera den enligt installationsguiden för ditt
operativsystem.

### Varje förfrågan misslyckas med ett fel om ogiltig licens

Själva *digna*-licensen har gått ut. MCP-servern slutar svara tillsammans med dashboarden tills en
ny licens har installerats.

### Agenten kan läsa men inte ändra konfigurationen

Användaren bakom API-nyckeln har inte redaktörsrollen i det projektet. Använd nyckeln för
en användare med redaktörsrollen, eller be en projektadministratör att ändra rollen.

### Klienten kan inte ansluta alls

Maskinen som ansluter når inte endpointen. Öppna endpointens adress från den maskinen och
kontrollera brandväggar, proxyservrar och certifikatet. För en anpassad connector i Claude finns
den maskinen i Anthropics moln, se [Varifrån anslutningen kommer](#where-the-connection-comes-from).
