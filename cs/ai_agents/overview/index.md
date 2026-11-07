# Připojení AI agentů k digna

**digna MCP Server** umožňuje AI agentům pracovat s *digna* prostřednictvím
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), otevřeného standardu, který
podporují Claude, Gemini a mnoho dalších AI nástrojů. Agent připojený k *digna* může odpovídat na
otázky o vašich datech, prošetřovat upozornění a pomáhat s konfigurací *digna*. Co agenti dokážou,
popisuje [digna Agentic](../platform/agentic/Introduction.md).

Tato stránka popisuje stranu *digna*, která je pro každého AI klienta stejná. Průvodce pro
jednotlivé klienty pak ukazují, kam zadat endpoint a klíč:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop a vlastní konektory
- [Gemini](gemini_mcp_guide.md): Antigravity a Gemini CLI

!!! info "Beta"

    digna Agentic, a s ním i digna MCP Server, se dodává jako beta verze v
    [Release 2026.11](../changelog/Release_202611.md).

---

## Než začnete {: #before-you-start }

Potřebujete:

- *digna* Release 2026.11 nebo novější
- Licenci, která zahrnuje **digna Agentic**. Bez ní MCP server odmítne každý požadavek
- Uživatelský účet *digna*. Agent jedná v každém projektu s oprávněními tohoto uživatele, viz
  [Oprávnění](../platform/agentic/how_it_works.md#permissions)
- AI klienta, který se připojuje ke vzdáleným MCP serverům přes **streamable HTTP** a umí posílat
  hlavičku `Authorization`

---

## 1. Zjištění endpointu MCP {: #1-find-the-mcp-endpoint }

MCP server je součástí backendu *digna*, takže není nic navíc k instalaci ani ke spuštění. Jeho
endpoint je adresa backendu následovaná `/mcp`:

```text
https://digna.example.com/mcp
```

Pokud backend běží přímo na hostiteli a portu, například po
`digna serve --address 0.0.0.0 --port 8082`, je endpointem tato adresa s `/mcp`:

```text
http://digna-host:8082/mcp
```

Pokud je před backendem reverzní proxy, musí přeposílat `/mcp` na backend spolu s hlavičkou
`Authorization`.

!!! warning "V síti používejte HTTPS"

    Každý požadavek nese klíč API. Používejte HTTPS vždy, když AI klient a *digna* neběží na
    stejném počítači.

### Odkud přichází připojení {: #where-the-connection-comes-from }

Většina AI klientů se připojuje z počítače, na kterém běží: Claude Code, Claude Desktop s lokálním
mostem, Antigravity a Gemini CLI. Pro ně stačí, aby byla *digna* dostupná z tohoto počítače,
například uvnitř vaší firemní sítě.

**Vlastní konektory** (custom connectors) Claude jsou jiné: k endpointu se připojuje cloud
společnosti Anthropic. Fungují jen tehdy, když je endpoint dostupný z internetu přes HTTPS. Pro
instalaci *digna*, která je dostupná pouze uvnitř vaší sítě, použijte klienta, který běží na vašem
počítači.

---

## 2. Vytvoření klíče API {: #2-create-an-api-key }

AI klient se ověřuje klíčem API uživatele *digna*.

1. Přihlaste se do *digna*.
2. Otevřete svůj uživatelský profil v levém dolním rohu.
3. Klikněte na **API Keys** a poté na **Add API Key**.
4. Zadejte název, který vystihuje, k čemu klíč slouží, např. *Claude Code – Marcin*, a zvolte, kdy
   vyprší jeho platnost.
5. Zkopírujte klíč. Zobrazí se pouze jednou.

Každý požadavek na MCP server posílá klíč v této hlavičce:

```text
Authorization: Bearer <api key>
```

Slovo `Bearer` a mezera za ním jsou součástí hodnoty hlavičky.

---

## 3. Připojení AI klienta {: #3-connect-your-ai-client }

| AI klient | Připojuje se z | Průvodce |
|---|---|---|
| Claude Code | Váš počítač | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop s lokálním mostem | Váš počítač | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Vlastní konektor Claude (claude.ai, Claude Desktop, Claude mobile) | Cloud společnosti Anthropic | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE a aplikace | Váš počítač | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Váš počítač | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Fungují i další MCP klienti, pokud podporují vzdálené servery přes streamable HTTP s vlastní
hlavičkou. Většina z nich čte konfiguraci podobnou této. Přesné názvy souborů a klíčů najdete v
dokumentaci svého klienta:

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

## 4. Vyzkoušení {: #4-try-it }

Zeptejte se agenta na něco, na co umí odpovědět jen *digna*:

- *„Vypiš moje projekty v digna.“*
- *„Které datové zdroje v projektu X dnes nejsou zelené?“*
- *„Vysvětli poslední neúspěšnou kontrolu datového zdroje Y.“*

Pokud agent vypíše vaše projekty, připojení funguje.

---

## Zabezpečení {: #security }

- **Jeden klíč na osobu a klienta.** Pak můžete jediný klíč odvolat pomocí **Delete API Key**,
  aniž byste ovlivnili kohokoli jiného.
- **Uživatele vybírejte uvážlivě.** Agent může dělat vše, co může uživatel, jemuž klíč patří. Pouze
  pro zkoumání dat použijte uživatele s rolí reader v daných projektech.
- **Nedávejte klíče do sdílených souborů.** Necommitujte konfigurační soubor, který obsahuje klíč.
  Pokud to klient podporuje, načítejte klíč z proměnné prostředí.
- **Nastavte vypršení platnosti.** Vytvořte nový klíč dříve, než starý vyprší, a aktualizujte
  klienta.
- **Kontrolujte volání nástrojů.** Ponechte v klientovi zapnuté potvrzování volání nástrojů,
  alespoň u volání, která mění konfiguraci.

---

## Řešení problémů {: #troubleshooting }

### 401 Unauthorized

Odpověď uvádí důvod:

| Zpráva | Příčina |
|---|---|
| `Missing or malformed Authorization header` | Nebyla odeslána žádná hlavička, nebo hodnota nezačíná na `Bearer ` |
| `Invalid API key` | Klíč je chybný, nebo byl smazán |
| `API key expired` | Platnost klíče vypršela. Vytvořte nový |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

Licence *digna* neobsahuje položku digna Agentic, nebo platnost této položky vypršela. Požádejte
tým digna o licenci, která zahrnuje digna Agentic, a nainstalujte ji podle instalačního průvodce
pro váš operační systém.

### Každý požadavek selže s chybou neplatné licence

Vypršela platnost samotné licence *digna*. MCP server přestane odpovídat spolu s dashboardem, dokud
nebude nainstalována nová licence.

### Agent umí číst, ale ne měnit konfiguraci

Uživatel, kterému patří klíč API, nemá v daném projektu roli editor. Použijte klíč uživatele s rolí
editor, nebo požádejte správce projektu o změnu role.

### Klient se vůbec nemůže připojit

Počítač, který se připojuje, nedosáhne na endpoint. Otevřete adresu endpointu z tohoto počítače a
zkontrolujte firewally, proxy a certifikát. U vlastního konektoru Claude je tento počítač v cloudu
společnosti Anthropic, viz [Odkud přichází připojení](#where-the-connection-comes-from).