---
title: AI-agents – Overzicht MCP-integratie | digna Documentatie
description: Verbind Claude, Gemini en andere AI-agents met digna via de digna MCP Server. Vind het MCP-endpoint, maak een API-key aan, controleer de licentie- en netwerkvereisten en kies de gids voor je AI-client.
image: /assets/logo_square.png
keywords: digna MCP server, Model Context Protocol, AI-agent verbinden, Claude MCP, Gemini MCP, Antigravity MCP, digna API-key, digna Agentic
---

# AI-agents verbinden met digna

Met de **digna MCP Server** kunnen AI-agents met *digna* werken via het
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), een open standaard die wordt
ondersteund door Claude, Gemini en veel andere AI-tools. Een agent die met *digna* is verbonden,
kan vragen over je data beantwoorden, meldingen onderzoeken en helpen *digna* te configureren. Zie
[digna Agentic](../platform/agentic/Introduction.md) voor wat agents kunnen doen.

Deze pagina behandelt de *digna*-kant, die voor elke AI-client hetzelfde is. De gidsen per client
laten daarna zien waar je het endpoint en de key invoert:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop en custom connectors
- [Gemini](gemini_mcp_guide.md): Antigravity en Gemini CLI

!!! info "Bèta"

    digna Agentic, en daarmee de digna MCP Server, wordt als bètaversie geleverd in
    [Release 2026.11](../changelog/Release_202611.md).

---

## Voordat je begint {: #before-you-start }

Je hebt nodig:

- *digna* Release 2026.11 of later
- Een licentie die **digna Agentic** omvat. Zonder die licentie weigert de MCP-server elk verzoek
- Een *digna*-gebruikersaccount. De agent handelt in elk project met de rechten van die gebruiker, zie
  [Rechten](../platform/agentic/how_it_works.md#permissions)
- Een AI-client die verbinding maakt met externe MCP-servers via **streamable HTTP** en een
  `Authorization`-header kan meesturen

---

## 1. Het MCP-endpoint vinden {: #1-find-the-mcp-endpoint }

De MCP-server maakt deel uit van de *digna*-backend, dus je hoeft niets extra's te installeren of te
starten. Het endpoint is het adres van de backend gevolgd door `/mcp`:

```text
https://digna.example.com/mcp
```

Als de backend direct op een host en poort draait, bijvoorbeeld na
`digna serve --address 0.0.0.0 --port 8082`, is het endpoint dat adres met `/mcp`:

```text
http://digna-host:8082/mcp
```

Staat er een reverse proxy voor de backend, dan moet die `/mcp` samen met de
`Authorization`-header doorsturen naar de backend.

!!! warning "Gebruik HTTPS in een netwerk"

    Elk verzoek bevat een API-key. Gebruik HTTPS zodra de AI-client en *digna* niet op dezelfde
    machine draaien.

### Waar de verbinding vandaan komt {: #where-the-connection-comes-from }

De meeste AI-clients maken verbinding vanaf de machine waarop ze draaien: Claude Code, Claude Desktop
met een lokale bridge, Antigravity en Gemini CLI. Voor deze clients hoeft *digna* alleen bereikbaar
te zijn vanaf die machine, bijvoorbeeld binnen je bedrijfsnetwerk.

Claude's **custom connectors** werken anders: de cloud van Anthropic maakt verbinding met het
endpoint. Ze werken alleen als het endpoint via HTTPS vanaf het internet bereikbaar is. Gebruik voor
een *digna*-installatie die alleen binnen je netwerk bereikbaar is een client die op je eigen machine
draait.

---

## 2. Een API-key aanmaken {: #2-create-an-api-key }

Een AI-client authenticeert zich met de API-key van een *digna*-gebruiker.

1. Log in bij *digna*.
2. Open je gebruikersprofiel linksonder.
3. Klik op **API Keys** en daarna op **Add API Key**.
4. Voer een naam in die zegt waarvoor de key dient, bijv. *Claude Code – Marcin*, en kies wanneer
   de key verloopt.
5. Kopieer de key. Hij wordt maar één keer getoond.

Elk verzoek aan de MCP-server stuurt de key mee in deze header:

```text
Authorization: Bearer <api key>
```

Het woord `Bearer` en de spatie erna horen bij de waarde van de header.

---

## 3. Je AI-client verbinden {: #3-connect-your-ai-client }

| AI-client | Verbindt vanaf | Gids |
|---|---|---|
| Claude Code | Je eigen machine | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop met een lokale bridge | Je eigen machine | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Claude custom connector (claude.ai, Claude Desktop, Claude mobile) | De cloud van Anthropic | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE en app | Je eigen machine | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Je eigen machine | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Andere MCP-clients werken ook, als ze externe servers via streamable HTTP met een eigen header
ondersteunen. De meeste lezen een configuratie zoals deze. Raadpleeg de documentatie van je client
voor de exacte bestands- en sleutelnamen:

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

## 4. Uitproberen {: #4-try-it }

Stel de agent een vraag die alleen *digna* kan beantwoorden:

- *"Toon mijn digna-projecten."*
- *"Welke databronnen in project X zijn vandaag niet groen?"*
- *"Leg de laatste mislukte controle van databron Y uit."*

Als de agent je projecten opsomt, werkt de verbinding.

---

## Beveiliging {: #security }

- **Eén key per persoon en client.** Dan kun je één key intrekken, met **Delete API Key**,
  zonder dat iemand anders daar last van heeft.
- **Kies de gebruiker bewust.** De agent kan alles wat de gebruiker van de key kan. Gebruik voor
  alleen het onderzoeken van data een gebruiker met de rol reader in de projecten.
- **Houd keys uit gedeelde bestanden.** Commit geen configuratiebestand dat een key bevat. Laat de
  client de key uit een omgevingsvariabele lezen als hij dat ondersteunt.
- **Stel een vervaldatum in.** Maak een nieuwe key aan voordat de oude verloopt, en werk de client
  bij.
- **Controleer tool calls.** Laat de bevestiging van tool calls in de client ingeschakeld, in elk
  geval voor calls die de configuratie wijzigen.

---

## Problemen oplossen {: #troubleshooting }

### 401 Unauthorized

Het antwoord vermeldt de reden:

| Melding | Oorzaak |
|---|---|
| `Missing or malformed Authorization header` | Er is geen header meegestuurd, of de waarde begint niet met `Bearer ` |
| `Invalid API key` | De key is onjuist of is verwijderd |
| `API key expired` | De key is verlopen. Maak een nieuwe aan |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

De *digna*-licentie heeft geen vermelding voor digna Agentic, of die vermelding is verlopen. Vraag
het digna-team om een licentie die digna Agentic omvat, en installeer die zoals de
installatiegids voor je besturingssysteem beschrijft.

### Elk verzoek mislukt met een fout over een ongeldige licentie

De *digna*-licentie zelf is verlopen. De MCP-server stopt dan samen met het dashboard met
antwoorden, totdat er een nieuwe licentie is geïnstalleerd.

### De agent kan lezen, maar de configuratie niet wijzigen

De gebruiker achter de API-key heeft in dat project niet de rol editor. Gebruik de key van een
gebruiker met de rol editor, of vraag een projectbeheerder om de rol te wijzigen.

### De client kan helemaal geen verbinding maken

De machine die verbinding maakt, kan het endpoint niet bereiken. Open het adres van het endpoint
vanaf die machine en controleer firewalls, proxy's en het certificaat. Bij een Claude custom
connector staat die machine in de cloud van Anthropic, zie
[Waar de verbinding vandaan komt](#where-the-connection-comes-from).
