# Gemini savienošana ar digna

Šajā rokasgrāmatā Google Gemini rīki tiek savienoti ar **digna MCP Server**. Jums nepieciešams jūsu
*digna* instalācijas MCP galapunkts un API atslēga, kā aprakstīts [AI aģentu pārskatā](overview.md).

Piemēros kā galapunkts izmantots `https://digna.example.com/mcp`. Aizstājiet to ar savu.

## Rīka izvēle {: #choose-your-tool }

| Rīks | Kam | Konfigurācija |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE un lietotne | Google aģentu rīki. Antigravity CLI 2026. gada jūnijā aizstāja Gemini CLI individuālajiem Google kontiem | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard un Enterprise licences, kā arī maksas Gemini API atslēgas | `settings.json` vai `gemini mcp add` |
| Gemini Enterprise lietotne | — | Netiek atbalstīta. Tās pielāgotais MCP savienotājs piesakās ar OAuth vai Google Cloud pakalpojuma kontu, savukārt digna MCP Server autentificē ar API atslēgām |

Visi šie rīki savienojas no datora, kurā tie darbojas, tāpēc tie darbojas ar *digna* jūsu uzņēmuma
tīklā, ja vien šis dators var sasniegt galapunktu.

---

## Antigravity {: #antigravity }

Antigravity nolasa savus MCP serverus no `mcp_config.json`, ko koplieto CLI, IDE un lietotne.

### 1. mcp_config.json atvēršana {: #1-open-mcp-config-json }

| Scope | Fails |
|---|---|
| Visi jūsu projekti | `~/.gemini/config/mcp_config.json` |
| Viena darbvieta (workspace) | `.agents/mcp_config.json` darbvietā |

Lai atvērtu izmantoto failu:

- **CLI**: ierakstiet `/mcp` un nospiediet ++enter++, lai atvērtu MCP pārvaldnieku.
- **IDE**: aģenta sānu panelī atveriet izvēlni **…**, atlasiet **MCP Servers**, pēc tam
  **Manage MCP Servers** un tad **View raw config**.
- **Lietotne**: dodieties uz **Customizations** > **Installed** > **MCP Servers** un izmantojiet
  **Copy Config File Path**.

### 2. digna servera pievienošana {: #2-add-the-digna-server }

Pievienojiet ierakstu `digna`. Ja failā jau ir sadaļa `mcpServers`, pievienojiet to tur:

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

Antigravity sasniedz attālos serverus tikai, izmantojot streamable HTTP, ko izmanto digna MCP
Server. Norādiet galapunktu kā `serverUrl`; Gemini CLI atslēga `httpUrl` netiek atbalstīta.

### 3. Savienojuma pārbaude {: #3-verify-the-connection }

CLI ierakstiet `/mcp`: MCP pārvaldnieks parāda serveri `digna` ar tā statusu un rīkiem, un tas var
atkārtoti ielādēt konfigurāciju un parādīt savienojuma žurnālus. IDE serveris parādās sadaļā
**Manage MCP Servers**.

!!! warning "Aizsargājiet failu"

    `mcp_config.json` satur API atslēgu atklātā tekstā. Neiekļaujiet darbvietas
    `.agents/mcp_config.json` versiju kontrolē un ļaujiet globālo failu lasīt tikai savam kontam.

---

## Gemini CLI {: #gemini-cli }

### 1. Servera pievienošana {: #1-add-the-server }

Ievietojiet API atslēgu vides mainīgajā un pēc tam pievienojiet serveri:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Jūsu čaula (shell) aizpilda `$DIGNA_API_KEY`, kad izpildāt komandu, tāpēc Gemini CLI saglabā
atslēgu savos iestatījumos. Bez `--scope user` serveris tiek pievienots tikai pašreizējam
projektam.

### 2. Vai settings.json rediģēšana {: #2-or-edit-settings-json }

Iepriekš minētā komanda raksta failā `settings.json`. Lai rediģētu failu patstāvīgi:

| Scope | Fails |
|---|---|
| Visi jūsu projekti | `~/.gemini/settings.json` |
| Viens projekts | `.gemini/settings.json` projektā |

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

Izmantojiet `httpUrl` — atslēgu streamable HTTP. Līdzīgā atslēga `url` izvēlas vecāko SSE
transportu, ko digna MCP Server nepiedāvā. Servera nosaukumā neizmantojiet pasvītras.

!!! tip "Atstājiet trust izslēgtu"

    Gemini CLI jautā pirms katra rīka izsaukuma, ja vien serverim nav `"trust": true`. Atstājiet
    `trust` izslēgtu *digna* serverim, lai jūs apstiprinātu katras izmaiņas, ko aģents veic jūsu
    konfigurācijā.

### 3. Savienojuma pārbaude {: #3-verify-the-connection-gemini-cli }

No čaulas:

```bash
gemini mcp list
```

Serverim `digna` jābūt redzamam kā savienotam. Gemini CLI sesijā izpildiet `/mcp`, lai redzētu
serveri un tā rīkus.

---

## Gemini problēmu novēršana {: #troubleshooting-gemini }

### Serveris tiek rādīts kā atvienots

- Pārbaudiet, vai galapunkts beidzas ar `/mcp` un ir sasniedzams no jūsu datora.
- Pārbaudiet atslēgas nosaukumu: `serverUrl` Antigravity, `httpUrl` Gemini CLI.
- `401` nozīmē, ka atslēga tika noraidīta; skatiet [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI vairs nestartē manam kontam

Kopš 2026. gada jūnija individuālie Google konti Gemini CLI vietā izmanto Antigravity CLI.
Pārvietojiet ierakstu `digna` uz `mcp_config.json`, kā aprakstīts sadaļā [Antigravity](#antigravity),
un pārdēvējiet `httpUrl` par `serverUrl`.

---

## Skatīt arī {: #see-also }

- [AI aģentu pārskats](overview.md): galapunkts, API atslēga, drošība un vispārīga problēmu novēršana
- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop vai pielāgotā savienotāja savienošana
- [digna Agentic](../platform/agentic/Introduction.md): ko AI aģenti var paveikt ar *digna*