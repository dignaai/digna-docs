---
title: Data Schema Tracker – Monitoruj ewolucję schematu | dokumentacja digna
description: Dowiedz się, jak digna Data Schema Tracker monitoruje zmiany kolumn, aktualizacje typów danych i schema drift. Wykrywaj i otrzymuj alerty zarówno przy celowych, jak i niezamierzonych zmianach schematu, aby zapobiec awariom ETL, uszkodzonym dashboardom i utracie obserwowalności danych.
canonical_url: https://docs.digna.ai/platform/data_schema_tracker/
image: /assets/logo_square.png
keywords:
  - data schema tracker
  - schema drift detection
  - schema evolution monitoring
  - metadata observability
  - data observability
  - quality of data
  - data structure monitoring
  - database metadata
  - etl pipeline stability
  - digna data schema tracker
lang: pl
robots: index, follow
og_title: Data Schema Tracker – Monitoruj ewolucję schematu | dokumentacja digna
og_description: digna Data Schema Tracker monitoruje schema drift, zmiany typów danych oraz aktualizacje kolumn. Otrzymuj alerty zanim pipeline’y ETL lub dashboardy przestaną działać z powodu niespodziewanych zmian struktury.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Monitoruj ewolucję schematu
<h1 style="display:none;">Moduł oparty na AI do obserwowalności metadanych i jakości danych – digna Data Schema Tracker</h1>

---

## Cel

The **Data Schema Tracker** informuje o tym, jak ewoluują struktury Twojej bazy danych.  
Ciągle monitoruje **schematy tabel, kolumny i typy danych**, aby wykrywać **schema drift** — celowe lub niezamierzone zmiany strukturalne, które mogą zakłócić działanie pipeline’ów, zadań ETL lub dashboardów BI.

Zapewniając przejrzystość ewolucji schematu, digna pomaga organizacjom utrzymać **zaufanie do jakości danych**, zachować **obserwowalność systemów danych** i unikać kosztownych incydentów produkcyjnych wywołanych niezauważonymi zmianami schematu.

---

## Przegląd techniczny

### Co monitoruje

- **Dodane lub usunięte kolumny** – Wykrywa nowo wprowadzone, zmienione nazwy lub usunięte kolumny.  
- **Modyfikacje typów danych** – Identyfikuje zmiany takie jak `INT → VARCHAR` lub `DATE → TIMESTAMP`.  
- **Modyfikacje tabel i widoków** – Śledzi tworzenie, zmiany nazw lub usunięcie tabel i widoków.  
- **Różnice między środowiskami** – Porównuje wersje schematów między środowiskami Dev, Test i Production.  

### Wykrywanie i alertowanie

- Skanuje **metadane bazy danych** lub **katalogi systemowe** bezpośrednio w Twojej platformie danych.  
- Porównuje każdy zrzut schematu z poprzednio znaną wersją przechowywaną w schemacie obserwowalności digna.  
- Generuje **alerty w czasie rzeczywistym** na pulpicie, przez API lub zewnętrzne kanały powiadomień (e-mail, Slack, webhook).  
- Loguje każdą wersję schematu dla **śledzenia historycznego i gotowości audytowej**.

---

## Architektura i wykonanie

- **Wykonywanie w bazie (In-Database Execution):** digna działa w całości w Twoim środowisku, odpytywując widoki metadanych bez ekstrakcji jakichkolwiek danych.  
- **Lekki skan (Lightweight Scanning):** uzyskuje dostęp wyłącznie do informacji strukturalnych — nigdy do danych użytkowników.  
- **Centralne przechowywanie (Centralized Storage):** metadane schematu i rekordy driftu są przechowywane w schemacie obserwowalności digna do wizualizacji i analiz.  
- **Automatyzacja (Automation):** obsługuje zaplanowane lub zdarzeniowe skany za pomocą digna Core lub zewnętrznych narzędzi orkiestracyjnych.  

---

## Przykładowe scenariusze użycia

| Use Case | Description |
|-----------|--------------|
| **ETL Stability Monitoring** | Wykrywaj zmiany w strukturze u źródła zanim pipeline’y zawiodą z powodu niezgodności schematu. |
| **Business Intelligence Reliability** | Zapobiegaj uszkodzonym dashboardom spowodowanym zmianą nazwy lub brakiem kolumn. |
| **Data Warehouse Governance** | Utrzymuj audytowalną historię ewolucji schematu dla zgodności i analizy wpływu. |
| **Integration Oversight** | Zapewnij synchronizację schematów data lake i hurtowni po aktualizacjach strukturalnych. |

---

## Korzyści

| Area | Benefit |
|------|----------|
| **Data Quality** | Zapobiega niezauważonemu schema drift, który może uszkodzić lub unieważnić pipeline’y danych. |
| **Observability** | Dodaje monitorowanie strukturalne do ogólnej obserwowalności ekosystemów danych. |
| **Compliance** | Utrzymuje wersjonowaną historię schematu dla audytu, śledzenia i kontroli zmian. |
| **Prevention** | Wykrywa problemy strukturalne zanim rozprzestrzenią się na raportowanie lub środowisko produkcyjne. |

---

## Jak to działa

1. **Zbieranie zrzutów (Snapshot Collection)** – digna przechwytuje aktualne metadane schematu.  
2. **Porównanie (Comparison)** – nowy zrzut jest porównywany