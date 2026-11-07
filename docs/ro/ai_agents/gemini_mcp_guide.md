---
title: Gemini – Conectarea Antigravity și Gemini CLI la digna prin MCP | Documentația digna
description: Conectați instrumentele Gemini ale Google la digna prin digna MCP Server — Antigravity CLI, IDE și aplicația cu mcp_config.json, și Gemini CLI cu settings.json sau gemini mcp add, folosind o cheie API în header-ul Authorization.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, cheie API digna
---

# Conectați Gemini la digna

Acest ghid conectează instrumentele Gemini ale Google la **digna MCP Server**. Aveți nevoie de
endpoint-ul MCP al instalării dvs. *digna* și de o cheie API, așa cum este descris în
[Prezentarea agenților AI](overview.md).

Exemplele folosesc `https://digna.example.com/mcp` ca endpoint. Înlocuiți-l cu al dvs.

## Alegeți instrumentul {: #choose-your-tool }

| Instrument | Pentru | Configurare |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE și aplicație | Instrumentele de agenți ale Google. Antigravity CLI a înlocuit Gemini CLI pentru conturile Google individuale în iunie 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Licențele Gemini Code Assist Standard și Enterprise și cheile Gemini API plătite | `settings.json` sau `gemini mcp add` |
| Aplicația Gemini Enterprise | — | Nu este acceptată. Conectorul său MCP personalizat se autentifică prin OAuth sau cu un cont de serviciu Google Cloud, în timp ce digna MCP Server se autentifică cu chei API |

Toate aceste instrumente se conectează de pe mașina pe care rulează, deci funcționează cu *digna*
în rețeaua companiei dvs., atâta timp cât acea mașină poate ajunge la endpoint.

---

## Antigravity {: #antigravity }

Antigravity își citește serverele MCP din `mcp_config.json`, fișier partajat de CLI, IDE și
aplicație.

### 1. Deschideți mcp_config.json {: #1-open-mcp-config-json }

| Domeniu | Fișier |
|---|---|
| Toate proiectele dvs. | `~/.gemini/config/mcp_config.json` |
| Un singur workspace | `.agents/mcp_config.json` în workspace |

Pentru a deschide fișierul folosit:

- **CLI**: tastați `/mcp` și apăsați ++enter++ pentru a deschide managerul MCP.
- **IDE**: în panoul lateral al agentului, deschideți meniul **…**, selectați **MCP Servers**, apoi
  **Manage MCP Servers**, apoi **View raw config**.
- **Aplicație**: accesați **Customizations** > **Installed** > **MCP Servers** și folosiți
  **Copy Config File Path**.

### 2. Adăugați serverul digna {: #2-add-the-digna-server }

Adăugați intrarea `digna`. Dacă fișierul are deja o secțiune `mcpServers`, adăugați-o acolo:

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

Antigravity ajunge la serverele la distanță doar prin streamable HTTP, pe care îl folosește digna
MCP Server. Scrieți endpoint-ul ca `serverUrl`; cheia `httpUrl` din Gemini CLI nu este acceptată.

### 3. Verificați conexiunea {: #3-verify-the-connection }

În CLI, tastați `/mcp`: managerul MCP afișează serverul `digna` cu starea și instrumentele sale și
poate reîncărca configurația și afișa jurnalele de conexiune. În IDE, serverul apare sub
**Manage MCP Servers**.

!!! warning "Protejați fișierul"

    `mcp_config.json` conține cheia API în text simplu. Păstrați un `.agents/mcp_config.json` de
    workspace în afara controlului versiunilor și permiteți doar contului dvs. să citească fișierul
    global.

---

## Gemini CLI {: #gemini-cli }

### 1. Adăugați serverul {: #1-add-the-server }

Puneți cheia API într-o variabilă de mediu, apoi adăugați serverul:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Shell-ul dvs. completează `$DIGNA_API_KEY` atunci când rulați comanda, astfel încât Gemini CLI
stochează cheia în setările sale. Fără `--scope user`, serverul este adăugat doar în proiectul
curent.

### 2. Sau editați settings.json {: #2-or-edit-settings-json }

Comanda de mai sus scrie în `settings.json`. Pentru a edita fișierul manual:

| Domeniu | Fișier |
|---|---|
| Toate proiectele dvs. | `~/.gemini/settings.json` |
| Un singur proiect | `.gemini/settings.json` în proiect |

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

Folosiți `httpUrl`, cheia pentru streamable HTTP. Cheia similară `url` selectează transportul SSE
mai vechi, pe care digna MCP Server nu îl oferă. Nu folosiți underscore în numele serverului.

!!! tip "Lăsați trust dezactivat"

    Gemini CLI cere confirmare înainte de fiecare apel de instrument, cu excepția cazului în care
    serverul are `"trust": true`. Lăsați `trust` dezactivat pentru *digna*, astfel încât să
    confirmați fiecare modificare pe care un agent o face în configurația dvs.

### 3. Verificați conexiunea {: #3-verify-the-connection-gemini-cli }

Din shell:

```bash
gemini mcp list
```

Serverul `digna` trebuie să apară ca fiind conectat. Într-o sesiune Gemini CLI, rulați `/mcp`
pentru a vedea serverul și instrumentele sale.

---

## Depanarea Gemini {: #troubleshooting-gemini }

### Serverul apare ca deconectat

- Verificați că endpoint-ul se termină cu `/mcp` și este accesibil de pe mașina dvs.
- Verificați numele cheii: `serverUrl` în Antigravity, `httpUrl` în Gemini CLI.
- Un `401` înseamnă că cheia a fost respinsă; consultați [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI nu mai pornește pentru contul meu

Din iunie 2026, conturile Google individuale folosesc Antigravity CLI în loc de Gemini CLI.
Mutați intrarea `digna` în `mcp_config.json` așa cum este descris la
[Antigravity](#antigravity) și redenumiți `httpUrl` în `serverUrl`.

---

## Vezi și {: #see-also }

- [Prezentarea agenților AI](overview.md): endpoint, cheie API, securitate și depanare generală
- [Claude](claude_mcp_guide.md): conectați Claude Code, Claude Desktop sau un conector personalizat
- [digna Agentic](../platform/agentic/Introduction.md): ce pot face agenții AI cu *digna*
