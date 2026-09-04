---
title: Data Validation – Kontrole oparte na regułach dla zgodności i audytowalności | Dokumentacja digna
description: Dowiedz się, jak digna Data Validation egzekwuje deterministyczne kontrole oparte na regułach z progami, zakresami i listami referencyjnymi. Zapewnij zgodność, audytowalność i raportowanie regulacyjne w finansach, ochronie zdrowia i innych branżach wrażliwych na dane.
image: /assets/logo_square.png
keywords:
  - walidacja danych
  - kontrole danych oparte na regułach
  - jakość danych
  - jakość danych
  - obserwowalność danych
  - progi i zakresy
  - walidacja względem list referencyjnych
  - audytowalność
  - monitorowanie zgodności
  - digna Data Validation
lang: pl
robots: index, follow
og_title: Data Validation – Kontrole oparte na regułach dla zgodności i audytowalności | Dokumentacja digna
og_description: digna Data Validation egzekwuje deterministyczne kontrole oparte na regułach z progami, zakresami i listami referencyjnymi. Zaprojektowany dla branż regulowanych, zapewnia zgodność, przejrzystość i audytowalność.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Kontrole oparte na regułach

---

## Purpose

Moduł **Data Validation** zapewnia **jakość danych** poprzez precyzyjne kontrole oparte na regułach.  
Umożliwia organizacjom zdefiniowanie deterministycznej logiki walidacji biznesowej i technicznej, zapewniając, że dane spełniają standardy zgodności, umowne SLA oraz wymagania regulacyjne.

Łącząc *wykonywanie reguł w bazie danych*, *pełne ścieżki audytu* oraz *integrację z innymi modułami digna*, **Data Validation** gwarantuje spójną i możliwą do śledzenia **jakość danych i obserwowalność** w złożonych środowiskach korporacyjnych.

---

## Technical Overview

### Supported Validation Types

- **Kontrole równości**  
  Sprawdzają, czy wartości odpowiadają oczekiwanym wynikom (np. kody referencyjne, flagi logiczne, mapowania kategorii).

- **Progi i zakresy**  
  Weryfikują miary numeryczne lub KPI względem zdefiniowanych limitów — statycznych lub dynamicznie wyprowadzanych.

- **Listy referencyjne i wyszukiwania**  
  Sprawdzają, czy wartości pól znajdują się w zatwierdzonych zestawach danych podstawowych (np. kody VAT, listy krajów ISO, katalogi produktów).

- **Spójność między kolumnami**  
  Zapewniają poprawność relacyjną (np. waluta zgodna z regionem, kategoria ryzyka dopasowana do typu aktywa).

- **Zasady obsługi wartości null**  
  Wykrywają nieoczekiwane wartości null lub puste w krytycznych kolumnach.

### Execution and Logging

- **Przetwarzanie w bazie danych** – Wszystkie reguły walidacyjne wykonywane są bezpośrednio w Twojej bazie danych (Teradata, Snowflake, Databricks, PostgreSQL itp.).  
- **Brak ekstrakcji danych** – digna nigdy nie przesyła surowych danych poza Twoje środowisko.  
- **Pełna śledzalność** – Wynik każdej reguły jest logowany z sygnaturą czasową, odpowiedzialnym zbiorem danych, liczbą rekordów oraz wynikiem zaliczenia/niezaliczenia.  
- **Audyt**
