---
title: Referencja SDK Python digna 2026.06 | Dokumentacja digna
description: Pełna dokumentacja referencyjna SDK Python digna w wersji 2026.06
image: /assets/logo_square.png
---

# Referencja SDK Python digna 2026.06

Ta sekcja dokumentuje SDK Python dla ***digna***. Została przygotowana jako referencja złożona z kilku stron: ta strona przeglądowa wprowadza w działanie klienta, a dalsze informacje znajdziesz na osobnych stronach poświęconych szybkiemu startowi, zasobom, modelom, błędom oraz wygenerowanej dokumentacji API.

SDK jest publikowane jako pakiet `digna-sdk` i udostępnia stabilnego, wersjonowanego klienta interfejsu REST API ***digna***.

---

## Podstawy SDK

---

### Przegląd

SDK opiera się na projekcie klienta zorientowanym na zasoby. Każdy obszar API jest udostępniany jako pełnoprawny klient w nadrzędnym obiekcie `DignaClient`, z typowanymi modelami żądań i odpowiedzi oraz spójną obsługą błędów.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Najważniejsze funkcje

- **Typowane modele** — każde żądanie i każda odpowiedź są walidowane przez pydantic, dzięki czemu edytor i kontroler typów wychwytują błędy, zanim dojdzie do wywołania sieciowego.
- **Orientacja na zasoby** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` oraz `client.inspection_statuses` udostępniają proste metody `list` / `get` / `create` / `update` / `delete`.
- **Czytelne błędy** — błędy API zgłaszają wyjątek `DignaAPIError` (lub bardziej szczegółową podklasę, taką jak `DignaAuthenticationError`, `DignaAuthorizationError` czy `DignaNotFoundError`) zamiast po cichu zwracać `None`.

### Instalacja

```bash
pip install digna-sdk
```

---

## Strony referencyjne

To wydanie zostało podzielone na następujące strony:

- [Szybki start](quickstart.md) — połączenie i pierwsze wywołania.
- [Zasoby](resources.md) — pełna lista dostępnych klientów zasobów.
- [Modele](models.md) — modele pydantic używane na wejściu i wyjściu.
- [Błędy](errors.md) — hierarchia wyjątków.
- [Referencja API](reference.md) — automatycznie generowana dokumentacja referencyjna.
