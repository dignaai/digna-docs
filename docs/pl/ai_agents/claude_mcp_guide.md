---
title: Claude – połącz Claude z digna przez MCP | Dokumentacja digna
description: Połącz Claude z digna przez digna MCP Server — Claude Code z wiersza poleceń lub przez współdzielony plik .mcp.json, Claude Desktop z lokalnym mostkiem oraz niestandardowe konektory w claude.ai, z kluczem API w nagłówku Authorization.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, niestandardowy konektor claude.ai, digna MCP server, mcp-remote, Authorization Bearer, klucz API digna
---

# Połącz Claude z digna

Ten przewodnik łączy Claude z **digna MCP Server**. Potrzebujesz endpointu MCP swojej instalacji
*digna* i klucza API, jak opisano w [Przeglądzie agentów AI](overview.md).

Przykłady używają `https://digna.example.com/mcp` jako endpointu. Zastąp go swoim.

## Wybierz sposób połączenia {: #choose-how-to-connect }

| Produkt Claude | Łączy się z | Działa z *digna* w Twojej sieci |
|---|---|---|
| [Claude Code](#claude-code) | Twojej maszyny | Tak |
| [Claude Desktop z lokalnym mostkiem](#claude-desktop-with-a-local-bridge) | Twojej maszyny | Tak |
| [Niestandardowy konektor](#custom-connector) w claude.ai, Claude Desktop i Claude mobile | Chmury Anthropic | Nie. Endpoint musi być osiągalny z internetu |

Dla instalacji *digna* działającej w sieci firmowej użyj Claude Code lub Claude Desktop z
lokalnym mostkiem.

---

## Claude Code {: #claude-code }

### 1. Dodaj serwer {: #1-add-the-server }

Umieść klucz API w zmiennej środowiskowej, a następnie dodaj serwer:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Powłoka podstawia `$DIGNA_API_KEY` w chwili uruchomienia polecenia, więc Claude Code zapisuje
klucz we własnej konfiguracji.

`--scope` decyduje, gdzie serwer jest dostępny:

| Zakres | Dostępny |
|---|---|
| `local` (domyślnie) | Dla Ciebie, tylko w bieżącym projekcie |
| `user` | Dla Ciebie, w każdym projekcie |
| `project` | Dla każdego, kto pracuje w projekcie, przez plik `.mcp.json` w projekcie |

### 2. Udostępnij serwer zespołowi (opcjonalnie) {: #2-share-the-server-with-your-team }

Aby wszyscy w projekcie mieli ten sam serwer, dodaj plik `.mcp.json` w katalogu głównym projektu.
Nie wpisuj do pliku klucza. Claude Code podstawia `${DIGNA_API_KEY}` ze środowiska każdej osoby:

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

Każda osoba ustawia `DIGNA_API_KEY` na własny klucz. Gdy Claude Code po raz pierwszy znajdzie
ten plik, zapyta, czy używać zdefiniowanych w nim serwerów.

### 3. Sprawdź połączenie {: #3-verify-the-connection }

W powłoce:

```bash
claude mcp list
```

Serwer `digna` musi pokazywać `✔ Connected`. W sesji Claude Code uruchom `/mcp`, aby zobaczyć
serwer i jego narzędzia.

---

## Claude Desktop z lokalnym mostkiem {: #claude-desktop-with-a-local-bridge }

Plik konfiguracyjny Claude Desktop uruchamia lokalne serwery MCP na Twojej maszynie. Mały mostek,
pakiet open source [`mcp-remote`](https://github.com/geelen/mcp-remote), działa na niej i
przekazuje każde żądanie do endpointu *digna* razem z Twoim kluczem API. Ponieważ mostek działa na
Twojej maszynie, ten sposób działa z *digna* w sieci firmowej.

!!! note "Pakiet społecznościowy"

    `mcp-remote` jest utrzymywany przez społeczność open source, a nie przez Anthropic czy digna.
    Zanim go użyjesz, sprawdź, czy Twoja organizacja na to pozwala.

### 1. Zainstaluj Node.js {: #1-install-nodejs }

Mostek wymaga [Node.js](https://nodejs.org) w wersji 18 lub nowszej. Claude Desktop używa wersji
Node.js zainstalowanej w systemie. Sprawdź ją poleceniem:

```bash
node --version
```

### 2. Edytuj plik konfiguracyjny {: #2-edit-the-configuration-file }

Otwórz `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Dodaj serwer `digna`. Jeśli plik ma już sekcję `mcpServers`, dodaj do niej wpis `digna`:

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

!!! warning "Zachowaj nagłówek dokładnie w tej postaci"

    Wpisz `Authorization:${AUTH_HEADER}` bez spacji, a `Bearer <api key>` umieść w `env`.
    Claude Desktop w systemie Windows nie escapuje spacji w `args`, więc spacja w tym miejscu
    psuje nagłówek.

### 3. Uruchom ponownie Claude Desktop {: #3-restart-claude-desktop }

Całkowicie zamknij Claude Desktop i uruchom go ponownie. W nowym czacie kliknij **+** i otwórz
**Connectors**: `digna` musi być na liście i być włączona.

---

## Niestandardowy konektor {: #custom-connector }

Niestandardowy konektor udostępnia *digna* w claude.ai, Claude Desktop i aplikacjach mobilnych
Claude bez żadnej lokalnej konfiguracji. Z endpointem łączy się chmura Anthropic, więc działa to
tylko wtedy, gdy:

- Endpoint *digna* jest osiągalny z internetu przez HTTPS
- Twoja organizacja Claude ma opcję **Request headers** w oknie **Add custom connector**.
  Anthropic udostępnia ją w wersji beta ograniczonej grupie organizacji

!!! warning "Nie dla digna w Twojej sieci"

    Tunele MCP Claude, które docierają do serwerów w sieci prywatnej, wymagają OAuth na serwerze
    MCP. digna MCP Server uwierzytelnia się kluczami API, więc tunelu nie można użyć. Zamiast tego
    użyj [Claude Code](#claude-code) lub [Claude Desktop z lokalnym mostkiem](#claude-desktop-with-a-local-bridge).

### 1. Otwórz ustawienia konektorów {: #1-open-the-connector-settings }

- **Plany Free, Pro, Max i Ultra**: przejdź do **Customize > Connectors** i kliknij
  **Add custom connector**.
- **Plany Team i Enterprise**: Owner przechodzi do **Organization settings > Connectors**, klika
  **Add**, a następnie **Custom**, i wybiera **Web**, jeśli pojawi się pytanie o typ.

### 2. Wprowadź dane konektora {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: wybierz `authorization` jako nazwę nagłówka, wpisz `Bearer <api key>` jako
   wartość, łącznie ze słowem `Bearer` i spacją, i oznacz go jako **Required**.
4. Kliknij **Add**.

!!! warning "Wszyscy współdzielą klucz"

    Każdy członek, który korzysta z konektora, pracuje z tym samym kluczem API, a więc z tym samym
    użytkownikiem *digna*. Utwórz dla konektora osobnego użytkownika *digna* i nadaj mu tylko te
    projekty i role, które może mieć każdy, np. rolę Czytelnik.

W planach Team i Enterprise członkowie łączą się następnie w **Customize > Connectors**, gdzie
konektor ma etykietę **Custom**.

Claude nie pozwala zmienić nagłówka istniejącego konektora. Aby użyć nowego klucza, usuń konektor
i dodaj go ponownie.

---

## Rozwiązywanie problemów z Claude {: #troubleshooting-claude }

### claude mcp list pokazuje Failed to connect

Uruchom `claude mcp get digna`, aby zobaczyć przyczynę. `401` oznacza, że klucz został odrzucony;
zobacz [401 Unauthorized](overview.md#troubleshooting). Claude Code ostrzega też przed spacjami
lub znakiem nowej linii na początku albo końcu klucza, które często pojawiają się przy kopiowaniu.

### digna nie pojawia się w Claude Desktop

- Sprawdź, czy zainstalowany jest Node.js 18 lub nowszy: `node --version`.
- Sprawdź, czy `claude_desktop_config.json` jest poprawnym plikiem JSON. Brakujący przecinek
  powoduje, że żaden serwer z pliku się nie ładuje.
- Zamknij Claude Desktop całkowicie, nie tylko okno, i uruchom go ponownie.

### Niestandardowy konektor nie może połączyć się z serwerem

Chmura Anthropic nie może dotrzeć do endpointu. Sprawdź, czy jest on osiągalny z internetu przez
HTTPS z ważnym certyfikatem, albo połącz się przez [Claude Code](#claude-code).

---

## Zobacz także {: #see-also }

- [Przegląd agentów AI](overview.md): endpoint, klucz API, bezpieczeństwo i ogólne rozwiązywanie
  problemów
- [Gemini](gemini_mcp_guide.md): połącz Antigravity lub Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): co agenci AI mogą robić z *digna*
