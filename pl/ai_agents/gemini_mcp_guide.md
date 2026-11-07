# Połącz Gemini z digna

Ten przewodnik łączy narzędzia Gemini od Google z **digna MCP Server**. Potrzebujesz endpointu MCP
swojej instalacji *digna* i klucza API, jak opisano w [Przeglądzie agentów AI](overview.md).

Przykłady używają `https://digna.example.com/mcp` jako endpointu. Zastąp go swoim.

## Wybierz narzędzie {: #choose-your-tool }

| Narzędzie | Dla | Konfiguracja |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE i aplikacja | Narzędzia agentowe Google. Antigravity CLI zastąpiło Gemini CLI dla indywidualnych kont Google w czerwcu 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Licencje Gemini Code Assist Standard i Enterprise oraz płatne klucze Gemini API | `settings.json` lub `gemini mcp add` |
| Aplikacja Gemini Enterprise | — | Nieobsługiwana. Jej niestandardowy konektor MCP loguje się przez OAuth lub konto usługi Google Cloud, a digna MCP Server uwierzytelnia się kluczami API |

Wszystkie te narzędzia łączą się z maszyny, na której działają, więc współpracują z *digna* w sieci
firmowej, o ile ta maszyna może dotrzeć do endpointu.

---

## Antigravity {: #antigravity }

Antigravity odczytuje swoje serwery MCP z pliku `mcp_config.json`, wspólnego dla CLI, IDE i
aplikacji.

### 1. Otwórz mcp_config.json {: #1-open-mcp-config-json }

| Zakres | Plik |
|---|---|
| Wszystkie Twoje projekty | `~/.gemini/config/mcp_config.json` |
| Jeden workspace | `.agents/mcp_config.json` w workspace |

Aby otworzyć używany plik:

- **CLI**: wpisz `/mcp` i naciśnij ++enter++, aby otworzyć menedżera MCP.
- **IDE**: w panelu bocznym agenta otwórz menu **…**, wybierz **MCP Servers**, następnie
  **Manage MCP Servers**, a potem **View raw config**.
- **Aplikacja**: przejdź do **Customizations** > **Installed** > **MCP Servers** i użyj
  **Copy Config File Path**.

### 2. Dodaj serwer digna {: #2-add-the-digna-server }

Dodaj wpis `digna`. Jeśli plik ma już sekcję `mcpServers`, dodaj go tam:

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

Antigravity łączy się ze zdalnymi serwerami tylko przez streamable HTTP, którego używa digna MCP
Server. Wpisz endpoint jako `serverUrl`; klucz `httpUrl` z Gemini CLI nie jest obsługiwany.

### 3. Sprawdź połączenie {: #3-verify-the-connection }

W CLI wpisz `/mcp`: menedżer MCP pokazuje serwer `digna` z jego statusem i narzędziami, potrafi
ponownie wczytać konfigurację i wyświetlić logi połączenia. W IDE serwer pojawia się w
**Manage MCP Servers**.

!!! warning "Chroń plik"

    `mcp_config.json` przechowuje klucz API jako zwykły tekst. Nie umieszczaj pliku
    `.agents/mcp_config.json` z workspace w systemie kontroli wersji, a plik globalny udostępnij do
    odczytu tylko własnemu kontu.

---

## Gemini CLI {: #gemini-cli }

### 1. Dodaj serwer {: #1-add-the-server }

Umieść klucz API w zmiennej środowiskowej, a następnie dodaj serwer:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Powłoka podstawia `$DIGNA_API_KEY` w chwili uruchomienia polecenia, więc Gemini CLI zapisuje klucz
w swoich ustawieniach. Bez `--scope user` serwer zostaje dodany tylko do bieżącego projektu.

### 2. Lub edytuj settings.json {: #2-or-edit-settings-json }

Powyższe polecenie zapisuje do `settings.json`. Aby samodzielnie edytować plik:

| Zakres | Plik |
|---|---|
| Wszystkie Twoje projekty | `~/.gemini/settings.json` |
| Jeden projekt | `.gemini/settings.json` w projekcie |

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

Użyj `httpUrl`, klucza dla streamable HTTP. Podobny klucz `url` wybiera starszy transport SSE,
którego digna MCP Server nie oferuje. Nie używaj podkreśleń w nazwie serwera.

!!! tip "Pozostaw trust wyłączone"

    Gemini CLI pyta przed każdym wywołaniem narzędzia, chyba że serwer ma `"trust": true`. Dla
    *digna* pozostaw `trust` wyłączone, aby potwierdzać każdą zmianę, jaką agent wprowadza w Twojej
    konfiguracji.

### 3. Sprawdź połączenie {: #3-verify-the-connection-gemini-cli }

W powłoce:

```bash
gemini mcp list
```

Serwer `digna` musi być pokazany jako połączony. W sesji Gemini CLI uruchom `/mcp`, aby zobaczyć
serwer i jego narzędzia.

---

## Rozwiązywanie problemów z Gemini {: #troubleshooting-gemini }

### Serwer jest pokazany jako rozłączony

- Sprawdź, czy endpoint kończy się na `/mcp` i jest osiągalny z Twojej maszyny.
- Sprawdź nazwę klucza: `serverUrl` w Antigravity, `httpUrl` w Gemini CLI.
- `401` oznacza, że klucz został odrzucony; zobacz [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI nie uruchamia się już na moim koncie

Od czerwca 2026 indywidualne konta Google używają Antigravity CLI zamiast Gemini CLI. Przenieś wpis
`digna` do `mcp_config.json`, jak opisano w sekcji [Antigravity](#antigravity), i zmień nazwę
`httpUrl` na `serverUrl`.

---

## Zobacz także {: #see-also }

- [Przegląd agentów AI](overview.md): endpoint, klucz API, bezpieczeństwo i ogólne rozwiązywanie
  problemów
- [Claude](claude_mcp_guide.md): połącz Claude Code, Claude Desktop lub niestandardowy konektor
- [digna Agentic](../platform/agentic/Introduction.md): co agenci AI mogą robić z *digna*