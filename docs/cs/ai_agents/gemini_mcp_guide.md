---
title: Gemini – Připojení Antigravity a Gemini CLI k digna přes MCP | Dokumentace digna
description: Připojte nástroje Gemini od Googlu k digna prostřednictvím digna MCP Server — Antigravity CLI, IDE a aplikaci pomocí mcp_config.json a Gemini CLI pomocí settings.json nebo gemini mcp add, s klíčem API v hlavičce Authorization.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, klíč API digna
---

# Připojení Gemini k digna

Tento průvodce připojí nástroje Gemini od Googlu k **digna MCP Server**. Potřebujete endpoint MCP
vaší instalace *digna* a klíč API, jak je popsáno v [Přehledu AI agentů](overview.md).

Příklady používají jako endpoint `https://digna.example.com/mcp`. Nahraďte ho svým.

## Výběr nástroje {: #choose-your-tool }

| Nástroj | Pro | Konfigurace |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE a aplikace | Agentní nástroje Googlu. Antigravity CLI v červnu 2026 nahradil Gemini CLI pro individuální účty Google | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Licence Gemini Code Assist Standard a Enterprise a placené klíče Gemini API | `settings.json` nebo `gemini mcp add` |
| Aplikace Gemini Enterprise | — | Nepodporováno. Její vlastní konektor MCP se přihlašuje přes OAuth nebo servisní účet Google Cloud, zatímco digna MCP Server se ověřuje klíči API |

Všechny tyto nástroje se připojují z počítače, na kterém běží, takže fungují s *digna* uvnitř vaší
firemní sítě, pokud tento počítač dosáhne na endpoint.

---

## Antigravity {: #antigravity }

Antigravity načítá své MCP servery ze souboru `mcp_config.json`, který sdílí CLI, IDE i aplikace.

### 1. Otevření mcp_config.json {: #1-open-mcp-config-json }

| Scope | Soubor |
|---|---|
| Všechny vaše projekty | `~/.gemini/config/mcp_config.json` |
| Jeden workspace | `.agents/mcp_config.json` ve workspace |

Jak otevřít používaný soubor:

- **CLI**: napište `/mcp` a stiskněte ++enter++, čímž otevřete správce MCP.
- **IDE**: v postranním panelu agenta otevřete nabídku **…**, vyberte **MCP Servers**, pak
  **Manage MCP Servers** a pak **View raw config**.
- **Aplikace**: přejděte na **Customizations** > **Installed** > **MCP Servers** a použijte
  **Copy Config File Path**.

### 2. Přidání serveru digna {: #2-add-the-digna-server }

Přidejte položku `digna`. Pokud soubor již obsahuje sekci `mcpServers`, přidejte ji do ní:

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

Antigravity se ke vzdáleným serverům připojuje jen přes streamable HTTP, který digna MCP Server
používá. Endpoint zapište jako `serverUrl`; klíč `httpUrl` z Gemini CLI není podporován.

### 3. Ověření připojení {: #3-verify-the-connection }

V CLI napište `/mcp`: správce MCP zobrazí server `digna` s jeho stavem a nástroji a umí znovu
načíst konfiguraci a zobrazit protokoly připojení. V IDE se server objeví v
**Manage MCP Servers**.

!!! warning "Chraňte soubor"

    `mcp_config.json` obsahuje klíč API jako prostý text. Soubor `.agents/mcp_config.json` ve
    workspace nedávejte do správy verzí a globální soubor nechte číst jen svůj vlastní účet.

---

## Gemini CLI {: #gemini-cli }

### 1. Přidání serveru {: #1-add-the-server }

Uložte klíč API do proměnné prostředí a pak přidejte server:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Shell dosadí `$DIGNA_API_KEY` při spuštění příkazu, takže Gemini CLI uloží klíč do svého
nastavení. Bez `--scope user` se server přidá jen do aktuálního projektu.

### 2. Nebo úprava settings.json {: #2-or-edit-settings-json }

Výše uvedený příkaz zapisuje do `settings.json`. Chcete-li soubor upravit sami:

| Scope | Soubor |
|---|---|
| Všechny vaše projekty | `~/.gemini/settings.json` |
| Jeden projekt | `.gemini/settings.json` v projektu |

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

Použijte `httpUrl`, klíč pro streamable HTTP. Podobný klíč `url` volí starší transport SSE, který
digna MCP Server nenabízí. V názvu serveru nepoužívejte podtržítka.

!!! tip "Nechte trust vypnutý"

    Gemini CLI se před každým voláním nástroje zeptá, pokud server nemá `"trust": true`. Pro
    *digna* nechte `trust` vypnutý, abyste potvrzovali každou změnu, kterou agent ve vaší
    konfiguraci provede.

### 3. Ověření připojení {: #3-verify-the-connection-gemini-cli }

Ze shellu:

```bash
gemini mcp list
```

Server `digna` musí být zobrazen jako připojený. V relaci Gemini CLI spusťte `/mcp`, abyste viděli
server a jeho nástroje.

---

## Řešení problémů s Gemini {: #troubleshooting-gemini }

### Server se zobrazuje jako odpojený

- Zkontrolujte, že endpoint končí na `/mcp` a je dostupný z vašeho počítače.
- Zkontrolujte název klíče: `serverUrl` v Antigravity, `httpUrl` v Gemini CLI.
- `401` znamená, že klíč byl odmítnut; viz [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI se pro můj účet už nespustí

Od června 2026 používají individuální účty Google místo Gemini CLI Antigravity CLI. Přesuňte
položku `digna` do `mcp_config.json`, jak je popsáno v části [Antigravity](#antigravity), a
přejmenujte `httpUrl` na `serverUrl`.

---

## Viz také {: #see-also }

- [Přehled AI agentů](overview.md): endpoint, klíč API, zabezpečení a obecné řešení problémů
- [Claude](claude_mcp_guide.md): připojení Claude Code, Claude Desktop nebo vlastního konektoru
- [digna Agentic](../platform/agentic/Introduction.md): co mohou AI agenti s *digna* dělat
