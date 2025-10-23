---
title: digna Wydanie 2024.12 | Rejestr zmian i nowe funkcje
description: Odkryj nowości w digna Wydanie 2024.12. Ta wersja wprowadza wbudowany scheduler, raportowanie do PDF, elastyczne kolumny niestandardowe, dynamiczne placeholdery w zapytaniach snapshot oraz inteligentniejszą optymalizację progów, poprawiając wykrywanie anomalii i monitorowanie jakości danych.
keywords: digna Wydanie 2024.12, digna rejestr zmian, informacje o wydaniu, wbudowany scheduler, raporty PDF, typ kolumny CUSTOM, placeholdery w zapytaniach snapshot, optymalizacja progów, obserwowalność danych, monitorowanie jakości danych, wykrywanie anomalii
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Rejestr zmian – Wydanie 2024.12

Wydanie 2024.12 dostarcza nowy zestaw funkcji i usprawnień, które sprawiają, że digna jest bardziej zautomatyzowana, elastyczna i gotowa do użytku biznesowego.  
Ta wersja usprawnia harmonogramowanie, raportowanie, obsługę zapytań oraz dokładność wykrywania anomalii.  

---

## Nowe funkcje

### Wbudowany Scheduler
Inspekcje nie muszą już polegać wyłącznie na wierszu poleceń lub wywołaniach API.  
Dzięki **nowemu digna Scheduler** inspekcje mogą być wykonywane automatycznie w określonych godzinach.  

- Obsługa **wyrażeń Cron** dla cyklicznych harmonogramów (codziennie, co tydzień lub niestandardowe interwały).  
- Precyzyjna kontrola dzięki **offsetom**, **datom rozpoczęcia** i **datom zakończenia**.  
- Umożliwia zespołom zapewnienie, że wszystkie krytyczne źródła danych są inspekcjonowane konsekwentnie i bez ręcznej pracy.  

---

### Raporty w formacie PDF
Zespoły mogą teraz łatwo dzielić się wynikami ze stronami zainteresowanymi za pomocą **eksportów do PDF**.  

- Wykresy, metryki i wyniki anomalii można eksportować w profesjonalnym formacie PDF.  
- Raporty łączą **wizualizacje** i **dane źródłowe**, służąc zarówno użytkownikom technicznym, jak i biznesowym.  
- Eliminacja konieczności korzystania z zewnętrznych narzędzi do tworzenia raportów.  

---

### Nowy typ kolumny: `CUSTOM`
Aby zapewnić większą elastyczność, digna wprowadza nowy typ kolumny **`CUSTOM`**.  

- Użytkownicy mogą precyzyjnie określać, które **statystyki i metryki** są stosowane do konkretnych atrybutów.  
- Idealne dla szczególnych przypadków, które nie mieszczą się w standardowych kategoriach takich jak NUMERICAL czy CATEGORICAL.  
- Pomaga utrzymać analizy skoncentrowane i wyniki istotne z punktu widzenia biznesu.  

---

### Nowe placeholdery w zapytaniach snapshot
Zapytania snapshot są teraz prostsze i mniej podatne na błędy dzięki **dynamicznym placeholderom**.  

- Tokeny takie jak `#date+n#` lub `#date-n#` automatycznie dostosowują daty w zapytaniach.  
- Przykład:  
  - `#date+1#` → jutro  
  - `#date-2#` → dwa dni temu  
- Eliminacja ręcznych obliczeń dat i zapewnienie spójności w całych zespołach.  

---

### Optymalizacja progów
Progi anomalii są teraz bardziej inteligentne i świadome kontekstu.  

- Dla metryk takich jak **NULL COUNT** dolne progi są automatycznie ograniczane do **0**.  
- Zapobiega to ustawianiu nieprawidłowych lub pozbawionych sensu progów.  
- Skutkuje mniejszą liczbą fałszywych alarmów i bardziej wiarygodnym wykrywaniem anomalii.  

---

## Ogólne usprawnienia
- Udoskonalone **komponenty UI** w widokach konfiguracji projektu i atrybutów.  
- Poprawiona wydajność **dashboardu** przy dużych wolumenach danych.  
- Rozszerzone logowanie i komunikaty o błędach ułatwiające rozwiązywanie problemów.  

---

## Podsumowanie
Wydanie 2024.12 wzmacnia digna jako platformę do **jakości danych, wykrywania anomalii i obserwowalności**.  
Dzięki automatyzacji przez harmonogramowanie, udostępnianym raportom PDF, konfigurowalnym kolumnom, uproszczonym zapytaniom snapshot i inteligentniejszym progom, digna staje się jeszcze bardziej wartościowa zarówno dla użytkowników technicznych, jak i interesariuszy biznesowych.