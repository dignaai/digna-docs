# Changelog – Release 2025.04

W wydaniu 2025.04 digna robi duży krok naprzód, upraszczając zarządzanie jakością danych i obserwowalnością, zwiększając przejrzystość dla zespołów oraz udostępniając narzędzie użytkownikom na całym świecie.  
To wydanie łączy w sobie **mocne nowe funkcje**, **usprawnienia automatyzacji pracy** oraz **ulepszenia doświadczenia użytkownika**.  

---

## Nowości

### Inspection Hub – nowe centrum zarządzania
**Inspection Hub** jest teraz dostępny jako centralne miejsce do zarządzania wszystkimi jobami inspekcji. Zamiast przeskakiwać między różnymi modułami lub polegać wyłącznie na uruchamianiu z linii poleceń, możesz teraz monitorować i kontrolować inspekcje z jednego, uporządkowanego interfejsu.  

Główne możliwości obejmują:  
- Inspekcje na żądanie: Uruchamiaj nowe joby natychmiast, kiedy potrzebujesz świeżych wyników.  
- Historia inspekcji: Zobacz oś czasu inspekcji — co zostało uruchomione, kto to wywołał i kiedy.  
- Śledzenie statusu: Joby są wyraźnie oznaczone jako zakończone, w trakcie lub oczekujące.  
- Informacje o wywołującym: Szybko sprawdź, czy inspekcja została wyzwolona przez użytkownika, scheduler czy CLI.  
- Narzędzia porządkowania: Usuwaj przestarzałe lub niepotrzebne joby, aby utrzymać porządek w workspace.  
- Szczegółowe logi: Zajrzyj w każdy job, aby zobaczyć czas trwania, uwzględnione źródła i sposób zastosowania progów.  

Inspection Hub daje zespołom **pełną widoczność i kontrolę**, ułatwiając zarządzanie inspekcjami w dużych projektach.  

---

### Wielojęzyczność – digna mówi Twoim językiem
digna jest teraz gotowa dla międzynarodowych zespołów dzięki wprowadzeniu **obsługi wielu języków**.  

W tym wydaniu możesz ustawić swój **preferowany język interfejsu** bezpośrednio w Preferencjach użytkownika. Obsługiwane języki to:  
- Angielski (UK, US, CA, AU)  
- Niemiecki (DE, AT, CH)  
- Polski (PL)  

Dzięki temu digna jest łatwiejsza w użyciu dla wielojęzycznych organizacji i gwarantuje płynniejsze wdrożenie w zespołach pracujących w różnych regionach. W nadchodzących wydaniach dodamy więcej języków.  

---

### Import i eksport źródeł danych – prosta konfiguracja
Spójność między środowiskami jest kluczowa w wdrożeniach korporacyjnych. W wersji 2025.04 digna wprowadza **import/eksport źródeł danych** przez **dignacli**, narzędzie wiersza poleceń dla zaawansowanych użytkowników.  

Korzyści:  
- Wyeksportuj konfigurację źródła danych raz, a następnie wykorzystaj ją ponownie w Development, Test i Production.  
- Wyeliminuj ręczne rekonfiguracje i uniknij kosztownych błędów.  
- Wspieraj zautomatyzowane workflowy i pipeline’y CI/CD za pomocą prostych poleceń CLI (`export-ds` i `import-ds`).  
- Szybko kopiuj źródła danych między projektami, ułatwiając współpracę.  

Ta funkcjonalność zapewnia zespołom pewność wdrożeń, wiedząc, że konfiguracje są spójne w każdym środowisku.  

---

### Module Analytics (v1) – od wykrywania do rozumienia
digna rozpoczęła jako platforma do wykrywania anomalii i monitoringu jakości danych. W wydaniu 2025.04 ewoluuje dalej dzięki **pierwszej wersji Module Analytics**.  

Module Analytics pomaga użytkownikom **zrozumieć swoje dane**, a nie tylko reagować na problemy. Dzięki temu nowemu modułowi możesz:  
- Śledzić długoterminowe trendy w zbiorach danych.  
- Wykrywać i monitorować zmienność, aby zrozumieć wahania.  
- Eksplorować zachowanie danych w czasie, uzyskując głębszy kontekst.  

Na przykład digna może automatycznie wyróżnić, że *“Liczba wierszy wzrosła o 15,8% od początku roku.”*  
Bez zapytań SQL, bez ręcznych kontroli — po prostu **praktyczne wnioski na pierwszy rzut oka**.  

To podstawa wędrówki digna w kierunku zaawansowanej analityki danych, pozwalająca zespołom danych przejść od monitoringu reaktywnego do proaktywnego.  

---

### Ulepszenia dashboardu – płynniejsze doświadczenie użytkownika
Poza głównymi funkcjami, wydanie 2025.04 zawiera kilka **udoskonaleń dashboardu**, zaprojektowanych, by uczynić digna bardziej intuicyjną i przyjemną w użyciu:  
- Szybsza nawigacja między projektami i inspekcjami.  
- Czytelniejszy układ logów inspekcji i zgłoszeń jobów.  
- Subtelne poprawki designu, które pomagają szybciej znaleźć wnioski.  

Te ulepszenia są oparte bezpośrednio na opinii klientów i pokazują nasze stałe zobowiązanie do budowania digna **jako platformy do codziennego użytku**.  

---

## Ogólne ulepszenia
- Optymalizacje wydajności jobów inspekcyjnych dla dużych zbiorów danych.  
- Ulepszone obsługiwanie błędów w dignacli, zapewniające jaśniejszy feedback.  
- Poprawa stabilności dla projektów z wieloma równoczesnymi jobami.  
- Ulepszenia UI w filtrowaniu logów jobów i zarządzaniu projektami.  

---

## Podsumowanie
Wydanie 2025.04 to przede wszystkim **kontrola, dostępność i wgląd**.  

- Nowy **Inspection Hub** daje użytkownikom pełną widoczność nad jobami inspekcji.  
- **Wielojęzyczność** zapewnia, że digna może być używana w zespołach globalnych.  
- Funkcjonalność **import/eksport** upraszcza zarządzanie konfiguracjami między środowiskami.  
- **Module Analytics (v1)** przesuwa fokus z wykrywania na rozumienie, oferując śledzenie trendów i zmienności.  
- **Ulepszenia dashboardu** udoskonalają ogólne doświadczenie użytkownika.  

Razem te aktualizacje czynią digna bardziej wydajną, przyjazną dla użytkownika i gotową na międzynarodowe wdrożenia niż kiedykolwiek wcześniej.