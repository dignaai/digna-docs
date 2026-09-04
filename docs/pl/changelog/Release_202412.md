---
title: digna Wydanie 2024.12 | Zmiany i nowe funkcje
description: Odkryj nowości w digna Wydanie 2024.12. W tej wersji wprowadzono wbudowany scheduler, raportowanie do PDF, elastyczne niestandardowe kolumny, dynamiczne placeholdery w zapytaniach snapshot oraz inteligentniejszą optymalizację progów, aby poprawić wykrywanie anomalii i monitorowanie jakości danych.
keywords: digna Wydanie 2024.12, digna dziennik zmian, informacje o wydaniu, wbudowany scheduler, raporty PDF, typ kolumny CUSTOM, placeholdery w zapytaniach snapshot, optymalizacja progów, obserwowalność danych, monitorowanie jakości danych, wykrywanie anomalii
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Dziennik zmian – Wydanie 2024.12

Wydanie 2024.12 wprowadza zestaw funkcji i usprawnień, które sprawiają, że digna jest bardziej zautomatyzowana, elastyczna i gotowa do użycia biznesowego.  
Ta wersja ulepsza harmonogramowanie, raportowanie, obsługę zapytań oraz dokładność wykrywania anomalii.  

---

## Nowe funkcje

### Wbudowany Scheduler
Inspekcje nie zależą już wyłącznie od wiersza poleceń ani wywołań API.  
Dzięki **nowemu Schedulerowi digna** inspekcje mogą być uruchamiane automatycznie w zdefiniowanych momentach.  

- Obsługuje **Cron expressions** dla powtarzalnych harmonogramów (codziennie, co tydzień lub niestandardowe interwały).  
- Oferuje precyzyjną kontrolę przez **offsety**, **daty rozpoczęcia** i **daty zakończenia**.  
- Pozwala zespołom zapewnić konsekwentną i bezobsługową kontrolę wszystkich krytycznych źródeł danych.  

---

### Raporty w formacie PDF
Zespoły mogą teraz łatwo udostępniać wyniki interesariuszom za pomocą **eksportów do PDF**.  

- Wykresy, metryki i wyniki anomalii można eksportować w profesjonalnym formacie PDF.  
- Raporty łączą **wizualizacje** i **dane źródłowe**, aby służyć zarówno użytkownikom technicznym, jak i biznesowym.  
- Eliminuje konieczność korzystania z narzędzi zewnętrznych do tworzenia raportów.  

---

### Nowy typ kolumny: `CUSTOM`
Aby zapewnić większą elastyczność, digna wprowadza nowy typ kolumny **`CUSTOM`**.  

- Użytkownicy mogą dokładnie zdefiniować, które **statystyki i metryki** są stosowane do konkretnych atrybutów.  
- Idealne do specjalnych przypadków, które nie mieszczą się w standardowych kategoriach takich jak NUMERICAL czy CATEGORICAL.  
- Pomaga utrzymać analizy ukierunkowane i wyniki istotne dla kontekstu biznesowego.  

---

### Nowe placeholdery w zapytaniach snapshot
Zapytania snapshot są teraz prostsze i mniej podatne na błędy dzięki **dynamicznym placeholderom**.  

- Tokeny takie jak `#date+n#` lub `#date-n#` automatycznie dopasowują daty w zapytaniach.  
- Przykład:  
  - `#date+1#` → jutro  
  - `#date-2#` → dwa dni temu  
- Eliminuje ręczne obliczenia dat i zapewnia spójność w zespołach.  

---

### Optymalizacja progów
Progi anomalii są teraz bardziej inteligentne i uwzględniają kontekst.  

- Dla metryk takich jak **NULL COUNT**, dolne progi są automatycznie ograniczane do **0**.  
- Zapobiega ustawianiu nieprawidłowych lub bezsensownych progów.  
- Skutkuje mniejszą liczbą fałszywych alarmów i bardziej niezawodnym wykrywaniem anomalii.  

---

## Ogólne usprawnienia
- Udoskonalone **komponenty UI** w widokach konfiguracji projektów i atrybutów.  
- Poprawiona **wydajność dashboardu** dla dużych wolumenów danych.  
- Rozszerzone **logowanie i komunikaty o błędach** ułatwiające rozwiązywanie problemów.  

---

## Podsumowanie
Wydanie 2024.12 wzmacnia digna jako platformę do **jakości danych, wykrywania anomalii i obserwowalności**.  
Dzięki automatyzacji przez harmonogramowanie, udostępnianym raportom PDF, konfigurowalnym kolumnom, uproszczonym zapytaniom snapshot i inteligentniejszym progom, digna staje się jeszcze bardziej wartościowa zarówno dla użytkowników technicznych, jak i interesariuszy biznesowych.