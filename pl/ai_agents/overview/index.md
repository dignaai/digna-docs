# Połącz agentów AI z digna

**digna MCP Server** pozwala agentom AI pracować z *digna* przez
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), otwarty standard obsługiwany przez
Claude, Gemini i wiele innych narzędzi AI. Agent połączony z *digna* może odpowiadać na pytania o
Twoje dane, analizować alerty i pomagać w konfiguracji *digna*. Co potrafią agenci, opisuje strona
[digna Agentic](../platform/agentic/Introduction.md).

Ta strona opisuje stronę *digna*, która jest taka sama dla każdego klienta AI. Przewodniki dla
poszczególnych klientów pokazują, gdzie wprowadzić te dane:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop i niestandardowe konektory
- [Gemini](gemini_mcp_guide.md): Antigravity i Gemini CLI

!!! info "Beta"

    digna Agentic, a wraz z nim digna MCP Server, jest dostarczany jako wersja beta w
    [Release 2026.11](../changelog/Release_202611.md).

---

## Zanim zaczniesz {: #before-you-start }

Potrzebujesz:

- *digna* Release 2026.11 lub nowszej
- Licencji obejmującej **digna Agentic**. Bez niej serwer MCP odrzuca każde żądanie
- Konta użytkownika *digna*. Agent działa z uprawnieniami tego użytkownika w każdym projekcie, zobacz
  [Uprawnienia](../platform/agentic/how_it_works.md#permissions)
- Klienta AI, który łączy się ze zdalnymi serwerami MCP przez **streamable HTTP** i potrafi wysłać
  nagłówek `Authorization`

---

## 1. Znajdź endpoint MCP {: #1-find-the-mcp-endpoint }

Serwer MCP jest częścią backendu *digna*, więc nie trzeba niczego dodatkowo instalować ani
uruchamiać. Jego endpoint to adres backendu z dopisanym `/mcp`:

```text
https://digna.example.com/mcp
```

Jeśli backend działa bezpośrednio na hoście i porcie, na przykład po
`digna serve --address 0.0.0.0 --port 8082`, endpoint to ten adres z `/mcp`:

```text
http://digna-host:8082/mcp
```

Jeśli przed backendem stoi reverse proxy, musi ono przekazywać `/mcp` do backendu razem z
nagłówkiem `Authorization`.

!!! warning "Używaj HTTPS w sieci"

    Każde żądanie zawiera klucz API. Używaj HTTPS zawsze, gdy klient AI i *digna* nie działają na
    tej samej maszynie.

### Skąd pochodzi połączenie {: #where-the-connection-comes-from }

Większość klientów AI łączy się z maszyny, na której działa: Claude Code, Claude Desktop z lokalnym
mostkiem, Antigravity i Gemini CLI. Dla nich *digna* musi być osiągalna tylko z tej maszyny, na
przykład w sieci firmowej.

**Niestandardowe konektory** Claude działają inaczej: z endpointem łączy się chmura Anthropic.
Działają one tylko wtedy, gdy endpoint jest osiągalny z internetu przez HTTPS. Dla instalacji
*digna* dostępnej tylko w Twojej sieci użyj klienta działającego na Twojej maszynie.

---

## 2. Utwórz klucz API {: #2-create-an-api-key }

Klient AI uwierzytelnia się kluczem API użytkownika *digna*.

1. Zaloguj się do *digna*.
2. Otwórz swój profil użytkownika w lewym dolnym rogu.
3. Kliknij **Klucze API**, a następnie **Dodaj klucz API**.
4. Wpisz nazwę, która mówi, do czego służy klucz, np. *Claude Code – Marcin*, i wybierz, kiedy
   wygasa.
5. Skopiuj klucz. Jest wyświetlany tylko raz.

Każde żądanie do serwera MCP wysyła klucz w tym nagłówku:

```text
Authorization: Bearer <api key>
```

Słowo `Bearer` i spacja po nim są częścią wartości nagłówka.

---

## 3. Połącz swojego klienta AI {: #3-connect-your-ai-client }

| Klient AI | Łączy się z | Przewodnik |
|---|---|---|
| Claude Code | Twojej maszyny | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop z lokalnym mostkiem | Twojej maszyny | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Niestandardowy konektor Claude (claude.ai, Claude Desktop, Claude mobile) | Chmury Anthropic | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE i aplikacja | Twojej maszyny | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Twojej maszyny | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Inni klienci MCP również działają, jeśli obsługują zdalne serwery przez streamable HTTP z własnym
nagłówkiem. Większość z nich czyta konfigurację podobną do tej. Dokładne nazwy pliku i kluczy
znajdziesz w dokumentacji swojego klienta:

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

## 4. Wypróbuj {: #4-try-it }

Zadaj agentowi pytanie, na które odpowiedzieć może tylko *digna*:

- *„Wymień moje projekty w digna.”*
- *„Które źródła danych w projekcie X nie są dziś zielone?”*
- *„Wyjaśnij ostatnią nieudaną kontrolę źródła danych Y.”*

Jeśli agent wyświetli Twoje projekty, połączenie działa.

---

## Bezpieczeństwo {: #security }

- **Jeden klucz na osobę i klienta.** Wtedy możesz unieważnić pojedynczy klucz przyciskiem
  **Usuń klucz API**, nie wpływając na nikogo innego.
- **Świadomie wybierz użytkownika.** Agent może zrobić wszystko, co może użytkownik klucza. Do
  samej analizy danych użyj użytkownika z rolą Czytelnik w projektach.
- **Nie trzymaj kluczy we współdzielonych plikach.** Nie commituj pliku konfiguracyjnego
  zawierającego klucz. Jeśli klient to obsługuje, odczytuj klucz ze zmiennej środowiskowej.
- **Ustaw datę wygaśnięcia.** Utwórz nowy klucz, zanim stary wygaśnie, i zaktualizuj klienta.
- **Sprawdzaj wywołania narzędzi.** Pozostaw włączone potwierdzanie wywołań narzędzi w kliencie,
  przynajmniej dla wywołań, które zmieniają konfigurację.

---

## Rozwiązywanie problemów {: #troubleshooting }

### 401 Unauthorized

Odpowiedź podaje przyczynę:

| Komunikat | Przyczyna |
|---|---|
| `Missing or malformed Authorization header` | Nie wysłano nagłówka albo wartość nie zaczyna się od `Bearer ` |
| `Invalid API key` | Klucz jest błędny albo został usunięty |
| `API key expired` | Klucz wygasł. Utwórz nowy |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

Licencja *digna* nie ma wpisu digna Agentic albo ten wpis wygasł. Poproś zespół digna o licencję
obejmującą digna Agentic i zainstaluj ją zgodnie z przewodnikiem instalacji dla Twojego systemu
operacyjnego.

### Każde żądanie kończy się błędem nieprawidłowej licencji

Wygasła sama licencja *digna*. Serwer MCP przestaje odpowiadać razem z dashboardem, dopóki nie
zostanie zainstalowana nowa licencja.

### Agent może odczytywać, ale nie zmieniać konfiguracji

Użytkownik, do którego należy klucz API, nie ma w tym projekcie roli Edytor. Użyj klucza
użytkownika z rolą Edytor albo poproś administratora projektu o zmianę roli.

### Klient w ogóle nie może się połączyć

Maszyna, która się łączy, nie może dotrzeć do endpointu. Otwórz adres endpointu z tej maszyny i
sprawdź zapory sieciowe, serwery proxy oraz certyfikat. W przypadku niestandardowego konektora
Claude ta maszyna znajduje się w chmurze Anthropic, zobacz
[Skąd pochodzi połączenie](#where-the-connection-comes-from).