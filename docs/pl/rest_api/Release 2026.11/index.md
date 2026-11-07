---
title: Przegląd REST API 2026.11 | Dokumentacja digna
description: Za pomocą REST API v1 digna odczytasz projekty i wyniki inspekcji, zarządzisz źródłami danych, zbiorami danych i atrybutami oraz uruchomisz inspekcje — bazowy URL, uwierzytelnianie kluczem API, paginacja, błędy i dokument OpenAPI.
image: /assets/logo_square.png
keywords: REST API digna, API digna, OpenAPI digna, klucz API digna, API żądań inspekcji, API jakości danych, Swagger UI
---

# REST API digna 2026.11

REST API *digna* pozwala Twoim własnym narzędziom i pipeline'om pracować z *digna* przez HTTP i JSON:
odczytywać projekty i wyniki inspekcji, zarządzać źródłami danych, zbiorami danych i atrybutami oraz
uruchamiać inspekcje, na przykład na koniec ładowania danych. [Python SDK](../../sdk/Release%202026.11/index.md)
korzysta z tego samego API.

Ta strona opisuje to, co jest wspólne dla wszystkich żądań. Strony zasobów opisują każdy endpoint wraz
z parametrami, treścią żądania, odpowiedziami i schematami:

| Zasób | Endpointy |
|---|---|
| [Projects](projects.md) | Odczyt projektów |
| [DB Connections](db_connections.md) | Odczyt połączeń z bazą danych |
| [Data Sources](data_sources.md) | Tworzenie, odczyt, aktualizacja i usuwanie źródeł danych |
| [Data Sets](data_sets.md) | Tworzenie, odczyt, aktualizacja i usuwanie zbiorów danych |
| [Attributes](attributes.md) | Tworzenie, odczyt, aktualizacja i usuwanie atrybutów |
| [Check Definitions](check_definitions.md) | Odczyt definicji kontroli |
| [Inspection Requests](inspection_requests.md) | Uruchamianie inspekcji i śledzenie ich postępu |
| [Inspection Statuses](inspection_statuses.md) | Odczyt wyników inspekcji według projektu, źródła danych i zbioru danych |

---

## Bazowy URL {: #base-url }

API jest częścią backendu *digna*. Każda ścieżka zaczyna się od `/v1` po adresie backendu:

```text
https://digna.example.com/v1/projects
```

Adres backendu to ten sam adres, którego używa dashboard: `baseUrl` w sekcji `[api]` pliku
`dashboard/dashboard_config.toml`. Używaj HTTPS zawsze, gdy wywołujący i *digna* nie działają na tej
samej maszynie, ponieważ każde żądanie przenosi klucz API.

---

## Uwierzytelnianie {: #authentication }

Każde żądanie wysyła klucz API użytkownika *digna* w nagłówku `Authorization`:

```text
Authorization: Bearer <api key>
```

Aby utworzyć klucz, otwórz swój profil użytkownika w lewym dolnym rogu dashboardu, kliknij
**Klucze API**, a następnie **Dodaj klucz API** i skopiuj klucz. Jest wyświetlany tylko raz. Te same
klucze działają w [digna MCP Server](../../ai_agents/overview.md).

Żądanie jest wykonywane z uprawnieniami użytkownika, do którego należy klucz. Tworzenie, zmienianie
i usuwanie wymaga roli Edytor w projekcie; w przeciwnym razie żądanie zostaje odrzucone z kodem `403`
i komunikatem `You don't have permission to edit this project`.

!!! tip "Do automatyzacji używaj osobnego użytkownika"

    Utwórz osobnego użytkownika *digna* dla każdej integracji, nadaj mu tylko te projekty i role,
    których potrzebuje, i utwórz jego klucz z datą wygaśnięcia. Wtedy możesz odebrać dostęp jednej
    integracji, usuwając jej klucz, bez wpływu na nikogo innego.

---

## Wysyłanie żądania {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Odpowiedzi są w formacie JSON. Listy są zwracane jako tablica JSON. Treść żądań również jest w formacie
JSON i jest wysyłana z nagłówkiem `Content-Type: application/json`.

---

## Limity i filtry {: #limits-and-filters }

Endpointy list zwracają co najwyżej `limit` elementów: domyślnie 200, maksymalnie 5000. Wartość spoza
tego zakresu jest odrzucana z kodem `400`. Nie ma offsetu ani tokenu strony, więc zawężaj listę jej
filtrami, na przykład `project_id`, `data_source_id` albo `start_date` i `end_date` w przypadku
statusów inspekcji.

Żądanie trwające dłużej niż 60 sekund zostaje anulowane z kodem `408 Request Timeout`.

---

## Błędy {: #errors }

Odpowiedź z błędem ma treść JSON z kodem i komunikatem:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Status | Kod | Znaczenie |
|---|---|---|
| `400` | `BAD_REQUEST` | Żądanie jest nieprawidłowe, na przykład `limit` jest poza zakresem |
| `401` | `NOT_AUTHENTICATED` | Brak klucza API albo klucz jest źle sformatowany, nieznany lub wygasł |
| `403` | `NOT_AUTHORIZED` | Użytkownik klucza nie ma roli wymaganej przez to żądanie |
| `403` | `INVALID_LICENSE` | Licencja *digna* wygasła |
| `404` | `NOT_FOUND` | Projekt, źródło danych lub inny element nie istnieje |
| `500` | `INTERNAL_ERROR` | Nieoczekiwany błąd w *digna*. Szczegóły znajdziesz w logu backendu |

Pole `message` odpowiedzi `401` mówi, co jest nie tak z kluczem:

| Komunikat | Przyczyna |
|---|---|
| `Missing Authorization header` | Nie wysłano nagłówka `Authorization` |
| `Invalid Authorization header format` | Wartość nie zaczyna się od `Bearer ` |
| `Invalid API key` | Klucz jest błędny albo został usunięty |
| `API key expired` | Klucz wygasł. Utwórz nowy |

---

## Uruchamianie inspekcji {: #running-an-inspection }

Typowa integracja uruchamia inspekcję po zakończeniu ładowania danych, czeka na jej zakończenie
i odczytuje wynik:

1. **Uruchom inspekcję** za pomocą [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Odpowiedź zawiera `id` żądania.
2. **Śledź jej postęp** za pomocą [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Jej `status` zmienia się z `PENDING` przez `RUNNING` na `COMPLETED` albo kończy się jako `FAILED`,
   `ABORTED` lub `CANCELLED`. Odpytuj ponownie co kilka sekund, aż przestanie się zmieniać.
3. **Odczytaj wynik** za pomocą [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   dla sprawdzonych dat. Każdy element ma ogólny `status`: `0` (OK), `1` (ostrzeżenie),
   `2` (krytyczny) lub `-1` (brak statusu), oraz status dla każdego modułu z liczbą zaliczonych,
   niepewnych i niezaliczonych kontroli.

```bash
curl -X POST https://digna.example.com/v1/inspection-requests \
  -H "Authorization: Bearer $DIGNA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "project_id": 1,
    "include_all_data_sources": true,
    "data_source_ids": [],
    "start_date": "2026-11-06",
    "end_date": "2026-11-06",
    "mode": "DAILY",
    "weekly_mode_weekdays": [],
    "monthly_mode_days": [],
    "use_notification": true
  }'
```

---

## Dokument OpenAPI {: #openapi-document }

Każda instalacja *digna* opisuje to API w dokumencie OpenAPI 3.1 i udostępnia interaktywny Swagger UI,
w którym możesz wypróbować żądania:

| Co | Adres |
|---|---|
| Dokument OpenAPI | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Dokument z Release 2026.11 jest też dostępny tutaj: [openapi.json](openapi.json). Użyj go, aby
wygenerować klienta w innym języku.

!!! note "Obejmuje tylko endpointy /v1"

    Dashboard komunikuje się z backendem także przez inne, wewnętrzne endpointy. Nie są one częścią
    tego API i mogą się zmienić w każdym wydaniu, dlatego buduj integracje wyłącznie na endpointach
    `/v1`.
