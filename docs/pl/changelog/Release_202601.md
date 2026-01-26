---
title: digna Wydanie 2026.01 | Logiczne źródła danych, Globalne połączenia & Zaawansowana Data Validation
description: Dowiedz się, co nowego w wydaniu digna 2026.01. Ta wersja wprowadza globalne połączenia z bazami danych, logiczne źródła danych, warunki relewancji anomalii, eksporty CSV oraz zaawansowaną Data Validation obejmującą sprawdzenia integralności referencyjnej.
keywords: digna Release 2026.01, digna changelog, digna datasource, digna database connections, digna Data Anomalies, digna Data Validation, referential integrity validation, data quality rules, data observability, digna CSV export
image: /assets/logo_square.png
---

# Dziennik zmian – Wydanie 2026.01  

W wydaniu 2026.01 digna wprowadza istotne udoskonalenia w modelowaniu źródeł danych, zarządzaniu połączeniami oraz użyteczności inspekcji.  
To wydanie zwiększa elastyczność we wszystkich modułach i znacząco rozszerza zakres **jakości danych i walidacji**.

---

## 🚀 Nowości  

### Globalne połączenia z bazami danych  
- Połączenia z bazami danych są teraz konfigurowane na **poziomie globalnym**.  
- Globalne połączenia można ponownie wykorzystać we **wszystkich projektach**, upraszczając konfigurację i konserwację.  
- **Wpływ:** Zmniejsza obciążenie operacyjne i zapewnia spójne łączenie z różnymi środowiskami.

### Możliwość wielu połączeń źródłowych na projekt  
- Projekty mogą teraz odwoływać się do **wielu konfiguracji połączeń źródłowych**.  
- Umożliwia bardziej elastyczne ustawienia dla skomplikowanych krajobrazów danych w projektach.  
- **Wpływ:** Wspiera realistyczne architektury korporacyjne z heterogenicznymi źródłami danych.

### Logiczne źródła danych  
- Źródła danych reprezentują teraz **warstwę logiczną** w ramach projektu.  
- Każde źródło danych może być oparte na:
    - tabeli bazy danych
    - widoku bazy danych
    - niestandardowym zapytaniu SQL  
- To rozdzielenie poprawia ponowne użycie, przejrzystość i modelowanie inspekcji we wszystkich modułach.  
- **Wpływ:** Oddziela inspekcje i reguły jakości danych od fizycznego przechowywania, poprawiając utrzymanie i ponowne użycie.

### Warunek relewancji anomalii  
- Można teraz zdefiniować **Warunek relewancji anomalii**, który kontroluje ocenę statusu anomalii na poziomie zestawu danych.  
- Statystyki są obliczane niezależnie od tego, czy warunek został ustawiony lub spełniony.  
- Jeśli warunek **nie jest spełniony**, **digna Data Anomalies** nie przydziela statusu anomalii (zielony / żółty / czerwony).  
- **Przykład:** Wyklucz zestaw danych z oceny anomalii, gdy liczba rekordów jest mniejsza niż 10.  
- **Wpływ:** Zapewnia ocenę anomalii tylko w istotnych kontekstach biznesowych.

### Konfiguracja powiadomień dla poszczególnych modułów  
- Powiadomienia można teraz konfigurować **dla każdego modułu osobno** bezpośrednio w digna.  
- Umożliwia niezależne zarządzanie alertami dla **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** i innych modułów.  
- **Wpływ:** Pozwala na precyzyjne strategie alertowania dostosowane do odpowiedzialności zespołów i krytyczności.

### Eksport wyników inspekcji (CSV)  
- Użytkownicy mogą teraz **pobrać wyniki inspekcji jako pliki CSV**.  
- Umożliwia analizę offline, raportowanie i integrację z zewnętrznymi narzędziami.  
- **Wpływ:** Upraszcza audyty, raportowanie i dalszą analizę jakości danych.

---

## 🧪 Rozszerzone możliwości Data Validation  

W tym wydaniu **digna Data Validation** obsługuje teraz kompleksowy zestaw reguł jakości danych:

- **Reguły walidacji na poziomie wiersza**  
- **Sprawdzenia unikalności obejmujące wiele kolumn**  
- **Weryfikacja integralności referencyjnej między źródłami danych**

Te kontrole umożliwiają egzekwowanie **strukturalnych i relacyjnych reguł jakości danych** w złożonych środowiskach danych.

### Sprawdzenia unikalności dla wielu kolumn
- Wprowadzono **Sprawdzenia unikalności** dla konfigurowalnego **zbioru kolumn**.  
- Umożliwia walidację kluczy złożonych i biznesowych ograniczeń unikalności.  
- **Wpływ:** Wykrywa zduplikowane byty biznesowe, których nie da się zidentyfikować za pomocą sprawdzeń pojedynczej kolumny.

### Sprawdzenia integralności referencyjnej
- Wprowadzono **Sprawdzenia integralności referencyjnej** do weryfikacji relacji między źródłami danych.  
- Zapewnia, że wartości kluczy obcych w źródłowym źródle danych istnieją w referencyjnym źródle docelowym.  
- Pomaga wykrywać osierocone rekordy, uszkodzone relacje i problemy ze spójnością danych na wczesnym etapie.  
- Zaprojektowane tak, aby działać z **logicznymi źródłami danych**, w tym z widokami i niestandardowym SQL.  
- **Przykłady użycia:** integralność hurtowni danych, raportowanie regulacyjne, spójność danych głównych i niezawodne analizy downstream.

---

## 🎯 Kto skorzysta z tego wydania  

- **Inżynierowie danych:** Bardziej elastyczne modelowanie źródeł danych i wielokrotnego użytku połączenia z bazami danych  
- **Zespoły ds. jakości danych i governance:** Rozszerzony zakres walidacji, w tym reguły integralności relacyjnej  
- **Zespoły analiz i BI:** Czystsze wejścia i możliwość eksportu wyników inspekcji  
- **Właściciele platformy:** Mniejsza złożoność konfiguracji i lepsze utrzymanie operacyjne

---

## 🛠 Aktualizacje CLI  
- Brak zmian

---