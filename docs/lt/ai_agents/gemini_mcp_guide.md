---
title: Gemini – Antigravity ir Gemini CLI prijungimas prie digna per MCP | digna dokumentacija
description: Prijunkite Google Gemini įrankius prie digna per digna MCP Server — Antigravity CLI, IDE ir programą su mcp_config.json bei Gemini CLI su settings.json arba gemini mcp add, su API raktu Authorization antraštėje.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, digna API raktas
---

# Gemini prijungimas prie digna

Šiame vadove Google Gemini įrankiai prijungiami prie **digna MCP Server**. Jums reikės savo *digna*
diegimo MCP galinio taško ir API rakto, kaip aprašyta [AI agentų apžvalgoje](overview.md).

Pavyzdžiuose galinis taškas yra `https://digna.example.com/mcp`. Pakeiskite jį savuoju.

## Pasirinkite įrankį {: #choose-your-tool }

| Įrankis | Kam | Konfigūracija |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE ir programa | Google agentų įrankiai. 2026 m. birželį Antigravity CLI pakeitė Gemini CLI asmeninėms Google paskyroms | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard ir Enterprise licencijos bei mokami Gemini API raktai | `settings.json` arba `gemini mcp add` |
| Gemini Enterprise programa | — | Nepalaikoma. Jos pasirinktinis MCP connector prisijungia su OAuth arba Google Cloud paslaugos paskyra, o digna MCP Server autentifikuoja API raktais |

Visi šie įrankiai jungiasi iš kompiuterio, kuriame veikia, todėl jie veikia su *digna* jūsų įmonės
tinkle, jei tas kompiuteris pasiekia galinį tašką.

---

## Antigravity {: #antigravity }

Antigravity skaito savo MCP serverius iš `mcp_config.json`, kurį bendrai naudoja CLI, IDE ir
programa.

### 1. Atidarykite mcp_config.json {: #1-open-mcp-config-json }

| Scope | Failas |
|---|---|
| Visi jūsų projektai | `~/.gemini/config/mcp_config.json` |
| Viena darbo sritis | `.agents/mcp_config.json` darbo srityje |

Kaip atidaryti naudojamą failą:

- **CLI**: įveskite `/mcp` ir paspauskite ++enter++, kad atidarytumėte MCP tvarkyklę.
- **IDE**: agento šoniniame skydelyje atidarykite meniu **…**, pasirinkite **MCP Servers**, tada
  **Manage MCP Servers**, tada **View raw config**.
- **Programa**: eikite į **Customizations** > **Installed** > **MCP Servers** ir naudokite
  **Copy Config File Path**.

### 2. Pridėkite digna serverį {: #2-add-the-digna-server }

Pridėkite `digna` įrašą. Jei faile jau yra `mcpServers` skyrius, pridėkite jį ten:

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

Antigravity pasiekia nuotolinius serverius tik per streamable HTTP, kurį naudoja digna MCP Server.
Galinį tašką rašykite kaip `serverUrl`; Gemini CLI raktas `httpUrl` nepalaikomas.

### 3. Patikrinkite ryšį {: #3-verify-the-connection }

CLI įveskite `/mcp`: MCP tvarkyklė rodo serverį `digna` su jo būsena ir įrankiais, gali iš naujo
įkelti konfigūraciją ir parodyti ryšio žurnalus. IDE serveris rodomas skiltyje
**Manage MCP Servers**.

!!! warning "Apsaugokite failą"

    `mcp_config.json` saugo API raktą atviru tekstu. Darbo srities `.agents/mcp_config.json`
    nelaikykite versijų valdymo sistemoje, o globalų failą leiskite skaityti tik savo paskyrai.

---

## Gemini CLI {: #gemini-cli }

### 1. Pridėkite serverį {: #1-add-the-server }

Įrašykite API raktą į aplinkos kintamąjį, tada pridėkite serverį:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Paleidus komandą jūsų shell įrašo `$DIGNA_API_KEY` reikšmę, todėl Gemini CLI išsaugo raktą savo
nustatymuose. Be `--scope user` serveris pridedamas tik prie dabartinio projekto.

### 2. Arba redaguokite settings.json {: #2-or-edit-settings-json }

Aukščiau pateikta komanda rašo į `settings.json`. Norėdami failą redaguoti patys:

| Scope | Failas |
|---|---|
| Visi jūsų projektai | `~/.gemini/settings.json` |
| Vienas projektas | `.gemini/settings.json` projekte |

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

Naudokite `httpUrl` – streamable HTTP raktą. Panašus raktas `url` pasirenka senesnį SSE perdavimą,
kurio digna MCP Server nesiūlo. Serverio pavadinime nenaudokite pabraukimo brūkšnių.

!!! tip "Palikite trust išjungtą"

    Gemini CLI prieš kiekvieną įrankio iškvietimą klausia patvirtinimo, nebent serveris turi
    `"trust": true`. *digna* atveju palikite `trust` išjungtą, kad patvirtintumėte kiekvieną
    pakeitimą, kurį agentas atlieka jūsų konfigūracijoje.

### 3. Patikrinkite ryšį {: #3-verify-the-connection-gemini-cli }

Iš savo shell:

```bash
gemini mcp list
```

Serveris `digna` turi būti rodomas kaip prijungtas. Gemini CLI sesijoje paleiskite `/mcp`, kad
pamatytumėte serverį ir jo įrankius.

---

## Gemini trikčių šalinimas {: #troubleshooting-gemini }

### Serveris rodomas kaip atjungtas

- Patikrinkite, ar galinis taškas baigiasi `/mcp` ir yra pasiekiamas iš jūsų kompiuterio.
- Patikrinkite rakto pavadinimą: `serverUrl` Antigravity, `httpUrl` Gemini CLI.
- `401` reiškia, kad raktas buvo atmestas; žr. [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI nebepasileidžia su mano paskyra

Nuo 2026 m. birželio asmeninės Google paskyros vietoj Gemini CLI naudoja Antigravity CLI. Perkelkite
`digna` įrašą į `mcp_config.json`, kaip aprašyta skyriuje [Antigravity](#antigravity), ir pervadinkite
`httpUrl` į `serverUrl`.

---

## Taip pat žr. {: #see-also }

- [AI agentų apžvalga](overview.md): galinis taškas, API raktas, saugumas ir bendrasis trikčių šalinimas
- [Claude](claude_mcp_guide.md): prijunkite Claude Code, Claude Desktop arba custom connector
- [digna Agentic](../platform/agentic/Introduction.md): ką AI agentai gali daryti su *digna*
