---
title: digna Release 2025.04 | Inspection Hub, Wielojęzyczność, Module Analytics
description: Dowiedz się, co nowego w digna Release 2025.04. Ta wersja wprowadza Inspection Hub, wsparcie wielojęzyczne (angielski, niemiecki, polski), import/eksport źródeł danych za pomocą dignacli, pierwsze wydanie Module Analytics oraz ulepszone doświadczenie na pulpicie nawigacyjnym.
keywords: digna Release 2025.04, digna changelog, digna inspection hub, digna multi-language support, digna module analytics, digna import export, digna CLI, release notes, data observability, data quality monitoring
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Changelog – Release 2025.04

W wydaniu Release 2025.04 digna robi istotny krok naprzód, ułatwiając zarządzanie jakością danych i obserwowalnością, zwiększając przejrzystość dla zespołów oraz udostępniając narzędzie użytkownikom na całym świecie.  
To wydanie łączy w sobie **mocne nowe funkcje**, **ulepszenia automatyzacji przepływów pracy** oraz **dopracowanie doświadczenia użytkownika**.  

---

## Nowości

### Inspection Hub – nowe centrum dowodzenia
**Inspection Hub** jest teraz dostępny jako centralne miejsce do zarządzania wszystkimi zadaniami inspekcji. Zamiast przeskakiwać między różnymi modułami czy polegać wyłącznie na uruchamianiu z wiersza poleceń, możesz teraz monitorować i kontrolować inspekcje z jednego, uporządkowanego interfejsu.  

Główne możliwości obejmują:  
- Inspekcje na żądanie: Uruchamiaj nowe zadania natychmiast, gdy potrzebujesz świeżych rezultatów.  
- Historia inspekcji: Zobacz linię czasu inspekcji — co zostało uruchomione, kto to wywołał i kiedy.  
- Śledzenie statusu: Zadania są wyraźnie oznaczone jako zakończone, w toku lub oczekujące.  
- Informacje o inicjatorze: Szybko sprawdź, czy inspekcja została uruchomiona przez użytkownika, scheduler czy CLI.  
- Narzędzia do porządkowania: Usuń przestarzałe lub niepotrzebne zadania, aby utrzymać porządek w przestrzeni pracy.  
- Szczegółowe logi: Przejdź do każdego zadania, aby zobaczyć, ile trwało, które źródła zostały uwzględnione oraz jak zastosowano progi.  

Inspection Hub daje zespołom **pełną widoczność i kontrolę**, ułatwiając zarządzanie inspekcjami w dużych projektach.  

---

### Wielojęzyczność – digna mówi Twoim językiem
digna jest teraz gotowa dla międzynarodowych zespołów dzięki wprowadzeniu **wsparcia wielojęzycznego**.  

W tym wydaniu możesz ustawić **preferowany język interfejsu** bezpośrednio w Ustawieniach użytkownika. Obsługiwane języki to:  
- English (UK, US, CA, AU)  
- German (DE, AT, CH)  
- Polish (PL)  

Dzięki temu digna staje się łatwiejsza w użyciu dla wielojęzycznych organizacji i zapewnia płynniejsze wdrożenie w zespołach działających w różnych regionach. W kolejnych wydaniach zostaną dodane kolejne języki.  

---

### Import i eksport źródeł danych – prosta konfiguracja
Spójność między środowiskami jest kluczowa w wdrożeniach korporacyjnych. W wydaniu 2025.04 digna wprowadza **import/eksport źródeł danych** za pomocą **dignacli**, narzędzia wiersza poleceń dla zaawansowanych użytkowników.  

Korzyści:  
- Wyeksportuj konfigurację źródła danych raz, a następnie wykorzystaj ją ponownie w środowiskach Development, Test i Production.  
- Eliminiuj ręczną rekonfigurację i unikaj kosztownych błędów.  
- Wspieraj zautomatyzowane workflow i CI/CD za pomocą prostych poleceń CLI (`export-ds` i `import-ds`).  
- Szybko kopiuj źródła danych między projektami dla łatwiejszej współpracy.  

Ta funkcjonalność zapewnia zespołom pewność wdrożeń, wiedząc że konfiguracje są spójne w każdym środowisku.  

---

### Module Analytics (v1) – od wykrywania do zrozumienia
digna zaczynała jako platforma do wykrywania anomalii i monitorowania jakości danych. W wydaniu Release 2025.04 rozwija się dalej dzięki **pierwszej wersji Module Analytics**.  

Module Analytics pomaga użytkownikom **zrozumieć swoje dane** zamiast jedynie reagować na problemy. W tym nowym module możesz:  
- Śledzić długoterminowe trendy w zestawach danych.  
- Wykrywać i monitorować zmienność, aby zrozumieć wahania.  
- Eksplorować zachowanie danych w czasie dla głębszego kontekstu.  

Na przykład digna może automatycznie wyróżnić, że „liczba wierszy zwiększyła się o 15,8% od początku roku.”  
Bez zapytań SQL, bez ręcznych kontroli — po prostu **praktyczne wnioski na pierwszy rzut oka**.  

To podstawa drogi digna w kierunku zaawansowanej analityki danych, pozwalająca zespołom danych przejść z monitorowania reaktywnego do proaktywnego.  

---

### Ulepszenia pulpitu nawigacyjnego – płynniejsze doświadczenie użytkownika
Poza głównymi funkcjami, Release 2025.04 zawiera kilka **usprawnień pulpitu nawigacyjnego**, zaprojektowanych, by uczynić digna bardziej intuicyjną i przyjemną:  
- Szybsza nawigacja między projektami i inspekcjami.  
- Czytelniejszy układ logów inspekcji i zgłoszeń zadań.  
- Subtelne poprawki w projekcie, które pomagają szybciej odnajdywać wnioski.  

Te ulepszenia bazują bezpośrednio na opinii klientów i pokazują nasze ciągłe zaangażowanie w tworzenie digna **platformy do codziennego użytku**.  

---

## Ogólne ulepszenia
- Optymalizacje wydajności dla zadań inspekcyjnych na dużych zestawach danych.  
- Ulepszone obsługi błędów w dignacli, zapewniające czytelniejszy feedback.  
- Poprawa stabilności dla projektów z wieloma równoczesnymi zadaniami.  
- Dopracowania UI dla filtrowania logów zadań i zarządzania projektami.  

---

## Podsumowanie
Release 2025.04 to przede wszystkim **kontrola, dostępność i wgląd**.  

- Nowy **Inspection Hub** daje użytkownikom pełną widoczność nad zadaniami inspekcji.  
- **Wielojęzyczność** sprawia, że digna może być używana przez międzynarodowe zespoły.  
- Funkcjonalność **import/eksport** upraszcza zarządzanie konfiguracją między środowiskami.  
- **Module Analytics (v1)** przesuwa fokus z wykrywania na zrozumienie, oferując śledzenie trendów i zmienności.  
- **Ulepszenia pulpitu nawigacyjnego** poprawiają ogólne doświadczenie użytkownika.  

Razem te aktualizacje czynią digna bardziej wydajną, przyjazną dla użytkownika i gotową na rynki międzynarodowe niż kiedykolwiek wcześniej.