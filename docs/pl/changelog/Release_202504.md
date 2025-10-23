---
title: digna Wydanie 2025.04 | Inspection Hub, Wsparcie wielojęzyczne, Module Analytics
description: Dowiedz się, co nowego w wydaniu digna 2025.04. Ta wersja wprowadza Inspection Hub, obsługę wielu języków (angielski, niemiecki, polski), import/eksport źródeł danych za pomocą dignacli, pierwsze wydanie Module Analytics oraz usprawnione doświadczenie pulpitu.
keywords: digna Wydanie 2025.04, digna changelog, digna inspection hub, digna wsparcie wielojęzyczne, digna module analytics, digna import export, digna CLI, release notes, data observability, monitorowanie jakości danych
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Changelog – Wydanie 2025.04

W wydaniu 2025.04 digna robi duży krok naprzód, upraszczając zarządzanie jakością danych i obserwowalnością, zwiększając przejrzystość pracy zespołów oraz udostępniając narzędzie użytkownikom na całym świecie.  
To wydanie łączy w sobie **mocne, nowe funkcje**, **usprawnienia automatyzacji przepływów pracy** oraz **udoskonalenia doświadczenia użytkownika**.  

---

## Nowe funkcje

### Inspection Hub – nowe centrum dowodzenia
Do dyspozycji jest już **Inspection Hub** — centralne miejsce do zarządzania wszystkimi zadaniami inspekcji. Zamiast przeskakiwać między modułami czy polegać wyłącznie na uruchomieniach z linii poleceń, możesz teraz monitorować i kontrolować inspekcje z jednego, przejrzystego interfejsu.  

Kluczowe możliwości obejmują:  
- Inspekcje na żądanie: Uruchamiaj nowe zadania natychmiast, gdy potrzebujesz świeżych wyników.  
- Historia inspekcji: Zobacz oś czasu inspekcji — co zostało uruchomione, kto to wyzwolił i kiedy.  
- Śledzenie statusu: Zadania są wyraźnie oznaczone jako zakończone, w toku lub oczekujące.  
- Informacje o wyzwalaczu: Szybko sprawdź, czy inspekcja została uruchomiona przez użytkownika, scheduler czy CLI.  
- Narzędzia porządkowania: Usuń przestarzałe lub niepotrzebne zadania, aby utrzymać porządek w przestrzeni roboczej.  
- Szczegółowe logi: Przejdź do szczegółów każdego zadania, aby zobaczyć czas wykonania, uwzględnione źródła i zastosowane progi.  

Inspection Hub daje zespołom **pełną widoczność i kontrolę end-to-end**, ułatwiając zarządzanie inspekcjami w dużych projektach.  

---

### Wsparcie wielojęzyczne – digna mówi Twoim językiem
digna jest teraz przygotowana dla międzynarodowych zespołów dzięki wprowadzeniu **wsparcia wielojęzycznego**.  

W tym wydaniu możesz ustawić swój **preferowany język interfejsu** bezpośrednio w Preferencjach użytkownika. Obsługiwane języki to:  
- Angielski (UK, US, CA, AU)  
- Niemiecki (DE, AT, CH)  
- Polski (PL)  

Dzięki temu digna staje się łatwiejsza w użyciu dla organizacji wielojęzycznych i ułatwia adopcję w zespołach pracujących w różnych regionach. W kolejnych wydaniach dodamy kolejne języki.  

---

### Import i eksport źródeł danych – prosta konfiguracja
Spójność między środowiskami jest niezbędna w wdrożeniach korporacyjnych. W wydaniu 2025.04 digna wprowadza **import/eksport źródeł danych** za pomocą **dignacli**, narzędzia wiersza poleceń dla zaawansowanych użytkowników.  

Korzyści:  
- Wyeksportuj konfigurację źródła danych raz, a następnie użyj jej ponownie w środowiskach Development, Test i Production.  
- Wyeliminuj ręczne rekonfiguracje i uniknij kosztownych błędów.  
- Wspieraj zautomatyzowane przepływy pracy i pipeline’y CI/CD za pomocą prostych poleceń CLI (`export-ds` i `import-ds`).  
- Szybko kopiuj źródła danych między projektami, ułatwiając współpracę.  

Ta funkcjonalność zapewnia zespołom pewność wdrożeń, wiedząc, że konfiguracje są spójne w każdym środowisku.  

---

### Module Analytics (v1) – od wykrywania do zrozumienia
digna zaczynała jako platforma do wykrywania anomalii i monitorowania jakości danych. W wydaniu 2025.04 ewoluuje dalej z **pierwszą wersją Module Analytics**.  

Module Analytics pomaga użytkownikom **zrozumieć swoje dane**, a nie tylko reagować na problemy. W tym nowym module możesz:  
- Śledzić długoterminowe trendy w zbiorach danych.  
- Wykrywać i monitorować wolatility, aby zrozumieć wahania.  
- Analizować zachowanie danych w czasie, by uzyskać głębszy kontekst.  

Na przykład, digna może automatycznie wyróżnić, że „Liczba wierszy wzrosła o 15,8% od początku roku.”  
Bez zapytań SQL, bez ręcznych kontroli — po prostu **praktyczne wnioski na pierwszy rzut oka**.  

To fundament w drodze digna ku zaawansowanej analizie danych, umożliwiający zespołom danych przejście z monitorowania reaktywnego na monitoring proaktywny.  

---

### Ulepszenia pulpitu – płynniejsze doświadczenie użytkownika
Poza głównymi funkcjami, wydanie 2025.04 zawiera kilka **udoskonaleń pulpitu**, zaprojektowanych tak, aby digna była bardziej intuicyjna i przyjemna w użyciu:  
- Szybsza nawigacja między projektami i inspekcjami.  
- Czytelniejszy układ logów inspekcji i zgłoszeń zadań.  
- Subtelne korekty designu, które pomagają szybciej odnajdywać wnioski.  

Te usprawnienia są oparte bezpośrednio na opiniach klientów i potwierdzają nasze stałe zaangażowanie w tworzenie digna **platformy stworzonej do codziennego użytku**.  

---

## Ogólne ulepszenia
- Optymalizacje wydajności dla zadań inspekcji przy dużych zbiorach danych.  
- Ulepszone obsługi błędów w dignacli, zapewniające bardziej czytelne komunikaty.  
- Poprawa stabilności w projektach z wieloma równoczesnymi zadaniami.  
- Udoskonalenia interfejsu dla filtrowania logów zadań i zarządzania projektami.  

---

## Podsumowanie
Wydanie 2025.04 skupia się na **kontroli, dostępności i wglądzie**.  

- Nowy **Inspection Hub** daje użytkownikom pełną widoczność nad zadaniami inspekcji.  
- **Wsparcie wielojęzyczne** zapewnia, że digna może być używana w zespołach na całym świecie.  
- Funkcjonalność **import/eksport** upraszcza zarządzanie konfiguracją między środowiskami.  
- **Module Analytics (v1)** przesuwa fokus z wykrywania na zrozumienie, oferując śledzenie trendów i zmienności.  
- **Ulepszenia pulpitu** dopracowują ogólne doświadczenie użytkownika.  

Razem te aktualizacje czynią digna potężniejszą, bardziej przyjazną dla użytkownika i gotową na międzynarodowe wdrożenia niż kiedykolwiek wcześniej.