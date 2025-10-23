---
title: digna Wydanie 2024.12 | Lista zmian i nowe funkcje
description: Dowiedz się, co nowego w wydaniu digna 2024.12. Ta wersja wprowadza wbudowany scheduler, raportowanie do PDF, elastyczne niestandardowe kolumny, dynamiczne placeholdery w zapytaniach snapshot oraz inteligentniejszą optymalizację progów, aby poprawić wykrywanie anomalii i monitorowanie jakości danych.
keywords: digna Wydanie 2024.12, digna lista zmian, release notes, wbudowany scheduler, raporty PDF, typ kolumny CUSTOM, placeholdery zapytań snapshot, optymalizacja progów, obserwowalność danych, monitorowanie jakości danych, wykrywanie anomalii
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Lista zmian – Wydanie 2024.12

Wydanie 2024.12 dostarcza nowy zestaw funkcji i ulepszeń, które czynią digna bardziej zautomatyzowaną, elastyczną i gotową dla biznesu.  
Ta wersja usprawnia harmonogramowanie, raportowanie, obsługę zapytań oraz dokładność wykrywania anomalii.  

---

## Nowe funkcje

### Wbudowany Scheduler
Inspekcje nie są już zależne wyłącznie od wiersza poleceń lub wywołań API.  
Dzięki **nowemu digna Scheduler** inspekcje mogą być wykonywane automatycznie w zaplanowanych terminach.  

- Obsługuje **wyrażenia Cron** dla cyklicznych harmonogramów (codziennie, co tydzień lub niestandardowe interwały).  
- Umożliwia precyzyjną kontrolę przez **offsety**, **daty rozpoczęcia** i **daty zakończenia**.  
- Pozwala zespołom zapewnić, że wszystkie krytyczne źródła danych są inspekcjonowane konsekwentnie i bez ręcznej pracy.  

---

### Raporty w formacie PDF
Zespoły mogą teraz łatwo udostępniać wyniki interesariuszom poprzez **eksporty do PDF**.  

- Wykresy, metryki i wyniki detekcji anomalii można eksportować do profesjonalnego pliku PDF.  
- Raporty łączą **wizualizacje** i **dane źródłowe**, by służyć zarówno użytkownikom technicznym, jak i biznesowym.  
- Eliminują potrzebę używania zewnętrznych narzędzi do tworzenia raportów.  

---

### Nowy typ kolumny: `CUSTOM`
Aby zapewnić większą elastyczność, digna wprowadza nowy typ kolumny **`CUSTOM`**.  

- Użytkownicy mogą dokładnie zdefiniować, które **statystyki i metryki** mają być stosowane do konkretnych atrybutów.  
- Idealne dla specjalnych przypadków, które nie pasują do standardowych kategorii, takich jak NUMERICAL czy CATEGORICAL.  
- Pomaga utrzymać analizy ukierunkowane i wyniki istotne w kontekście biznesowym.  

---

### Nowe placeholdery w zapytaniach snapshot
Zapytania snapshot są teraz prostsze i mniej podatne na błędy dzięki **dynamicznym placeholderom**.  

- Tokeny takie jak `#date+n#` lub `#date-n#` automatycznie dopasowują daty w zapytaniach.  
- Przykład:  
  - `#date+1#` → jutro  
  - `#date-2#` → dwa dni temu  
- Eliminują ręczne obliczanie dat i zapewniają spójność w zespołach.  

---

### Optymalizacja progów
Progi anomalii są teraz bardziej inteligentne i świadome kontekstu.  

- Dla metryk takich jak **NULL COUNT**, dolne progi są automatycznie ograniczane do **0**.  
- Zapobiega ustawianiu nieprawidłowych lub bezsensownych progów.  
- Skutkuje mniejszą liczbą fałszywych alarmów i bardziej niezawodnym wykrywaniem anomalii.  

---

## Ogólne usprawnienia
- Udoskonalone **komponenty UI** w widokach konfiguracji projektu i atrybutów.  
- Poprawiona wydajność **dashboardu** przy dużych wolumenach danych.  
- Ulepszone **logowanie i komunikaty o błędach** ułatwiające rozwiązywanie problemów.  

---

## Podsumowanie
Wydanie 2024.12 wzmacnia digna jako platformę do **jakości danych, wykrywania anomalii i obserwowalności**.  
Dzięki automatyzacji poprzez harmonogramowanie, możliwością udostępniania raportów w PDF, konfigurowalnym kolumnom, uproszczonym zapytaniom snapshot oraz inteligentniejszym progom, digna staje się jeszcze cenniejsza zarówno dla użytkowników technicznych, jak i interesariuszy biznesowych.