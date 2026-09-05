# Data Schema Tracker – Monitoruj ewolucję schematu

---

## Cel

The **Data Schema Tracker** informuje o tym, jak ewoluują struktury Twojej bazy danych.  
Ciągłe monitoruje **schematy tabel, kolumny i typy danych**, aby wykryć **schema drift** — zamierzone lub niezamierzone zmiany strukturalne, które mogą zakłócić potoki danych, zadania ETL lub pulpity BI.

Zapewniając przejrzystość ewolucji schematów, digna pomaga organizacjom utrzymać **zaufanie do jakości danych**, zachować **obserwowalność systemów danych** i unikać kosztownych incydentów produkcyjnych spowodowanych niezauważonymi zmianami schematu.

---

## Przegląd techniczny

### Co monitoruje

- **Dodane lub usunięte kolumny** – wykrywa nowo wprowadzone, przemianowane lub usunięte kolumny.  
- **Modyfikacje typów danych** – identyfikuje zmiany takie jak `INT → VARCHAR` lub `DATE → TIMESTAMP`.  
- **Modyfikacje tabel i widoków** – śledzi tworzenie, zmianę nazwy lub usuwanie tabel i widoków.  
- **Różnice między środowiskami** – porównuje wersje schematów między środowiskami Dev, Test i Production.  

### Wykrywanie i alertowanie

- Skanuje **metadane bazy danych** lub **katalogi systemowe** bezpośrednio w Twojej platformie danych.  
- Porównuje każdą migawkę schematu z wcześniej znaną wersją przechowywaną w schemacie obserwowalności digna.  
- Generuje **alerty w czasie rzeczywistym** w dashboardzie, przez API lub zewnętrzne kanały powiadomień (email, Slack, webhook).  
- Loguje każdą wersję schematu w celu **śledzenia historycznego i gotowości do audytu**.

---

## Architektura i wykonanie

- **Wykonywanie w bazie danych:** digna działa w całości w Twoim środowisku, zapytując widoki metadanych bez ekstrakcji żadnych danych.  
- **Lekki skan:** uzyskuje dostęp wyłącznie do informacji strukturalnych — nigdy do danych użytkownika.  
- **Centralne przechowywanie:** metadane schematu i zapisy dryfu są przechowywane w schemacie obserwowalności digna do celów wizualizacji i analiz.  
- **Automatyzacja:** obsługuje zaplanowane lub zdarzeniowe skany za pomocą digna Core lub zewnętrznych narzędzi orkiestracji.  

---

## Przykładowe przypadki użycia

| Use Case | Description |
|-----------|--------------|
| **Monitorowanie stabilności ETL** | Wykrywaj zmiany struktury u źródła zanim pipeline'y zawiodą z powodu niezgodności schematów. |
| **Niezawodność Business Intelligence** | Zapobiegaj uszkodzonym dashboardom spowodowanym przemianowanymi lub brakującymi kolumnami. |
| **Zarządzanie magazynem danych** | Utrzymuj audytowalną historię ewolucji schematów dla zgodności i analizy wpływu zmian. |
| **Nadzór nad integracją** | Zapewnij synchronizację schematów między data lake a hurtownią danych po aktualizacjach strukturalnych. |

---

## Korzyści

| Obszar | Korzyść |
|------|----------|
| **Jakość danych** | Zapobiega niezauważonemu dryfowi schematu, który może uszkodzić lub unieważnić pipeline'y danych. |
| **Obserwowalność** | Dodaje monitoring strukturalny do ogólnej obserwowalności ekosystemów danych. |
| **Zgodność** | Utrzymuje wersjonowaną historię schematów dla audytu, śledzenia i kontroli zmian. |
| **Zapobieganie** | Wykrywa problemy strukturalne zanim przełożą się na błędy raportowania lub produkcji. |

---

## Jak to działa

1. **Zbieranie migawki** – digna przechwytuje bieżące metadane schematu.  
2. **Porównanie** – nowa migawka jest porównywana