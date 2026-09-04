---
title: digna Wydanie 2026.06 | Python SDK, wdrożenie w Dockerze i ulepszone zarządzanie walidacją
description: Poznaj nowości w wydaniu digna 2026.06. Ta wersja wprowadza nowy digna Python SDK, wsparcie dla wdrożeń w Dockerze, odświeżony pulpit nawigacyjny oraz rozszerzoną przenośność zarządzania regułami walidacji.
keywords: digna Wydanie 2026.06, digna Python SDK, digna Docker support, automatyzacja jakości danych, profilowanie danych, import eksport reguł walidacji, digna dashboard, platforma obserwowalności danych, Python API, automatyzacja metadanych
image: /assets/logo_square.png
---

# Changelog – Wydanie 2026.06  

W wydaniu 2026.06 digna robi duży krok naprzód w zakresie automatyzacji, rozszerzalności i użyteczności platformy.  
W tej wersji wprowadzono nowy **digna Python SDK**, oficjalne wsparcie dla wdrożeń w **Docker**, odświeżone doświadczenie pulpitu oraz lepszą przenośność w zarządzaniu regułami walidacji.

---

## Nowe funkcje  

### digna Python SDK – Automatyzuj wszystko za pomocą Pythona  
- Instalacja:
  ```bash
  pip install digna-sdk
  ```
- Programowe zarządzanie i automatyzacja digna przy użyciu Pythona  
- Tworzenie i konfigurowanie projektów przez kod  
- Wywoływanie inspekcji i uruchomień monitoringu  
- Programowe zarządzanie zestawami danych, regułami i konfiguracjami  
- Profilowanie tabel i wydobywanie informacji o metadanych  
- Eksport wyników profilowania i jakości danych do zewnętrznych repozytoriów i systemów  
- Integracja z notebookami, narzędziami orkiestracji i pipeline’ami CI/CD  

**Wpływ:** Umożliwia pełne podejście infrastructure-as-code oraz głęboką automatyzację procesów jakości danych i obserwowalności przy użyciu Pythona.

---

### Wsparcie Docker – Uproszczone wdrożenia i operacje  
- Oficjalne wsparcie obrazu Docker dla digna  
- Szybka i spójna konfiguracja w różnych środowiskach  
- Uproszczone onboardowanie dla środowisk deweloperskich, testowych i produkcyjnych  
- Łatwa integracja z Kubernetes i platformami kontenerowymi  
- Lepsza przenośność i powtarzalność wdrożeń  

**Wpływ:** Ułatwia wdrażanie i eksploatację digna w nowoczesnych architekturach cloud-native.

---

### QueryMode – Elastyczna strategia wykonywania zapytań SQL

Skonfiguruj strategię wykonywania zapytań: tryb **Single** lub **Combined**

**Single Mode**: Każda statystyka jest obliczana za pomocą jednego dedykowanego zapytania SQL

  - Idealne dla dużych źródeł danych, gdzie istotne są ograniczenia pamięci
  - Zapobiega wyczerpaniu zasobów przy zapytaniach łączonych (brak pamięci, limity spool)
  - Większa liczba zapytań, lecz mniejsze zużycie pamięci na zapytanie

**Combined Mode**: Wszystkie statystyki obliczane są w pojedynczym zapytaniu SQL

  - Zmniejsza łączną liczbę zapytań i narzut sieciowy
  - Optymalizuje wydajność, gdy źródła danych mieszczą się w pamięci
  - Bardziej efektywne przy częstych, równoległych uruchomieniach

**Wpływ:** Daje użytkownikom precyzyjną kontrolę nad wykonywaniem zapytań, pozwalając wyważyć wydajność, wykorzystanie zasobów i bezpieczeństwo pamięci w zależności od charakterystyki źródła danych.


---

### Przeprojektowane doświadczenie pulpitu  
- Zmodernizowany i ulepszony design UI/UX  
- Czytelniejsza nawigacja i struktura  
- Lepsza widoczność wyników monitoringu i insightów dotyczących jakości danych  
- Poprawiona czytelność alertów, statystyk i dashboardów  
- Szybszy dostęp do kluczowych informacji operacyjnych  

**Wpływ:** Zwiększa użyteczność i produktywność użytkowników w codziennej pracy.

---

### Rozszerzony import i eksport reguł walidacji  
- Ulepszona funkcjonalność importu/eksportu reguł walidacji  
- Łatwiejsza migracja między środowiskami i projektami  
- Lepsze ponowne wykorzystanie standaryzowanych zestawów reguł  
- Udoskonalone zarządzanie cyklem życia reguł i governance  
- Uproszczona współpraca między zespołami  

**Wpływ:** Umożliwia skalowalne i spójne zarządzanie jakością danych w całej organizacji.

---

## Ulepszenia platformy  

- Pełna integracja Python SDK dla automatyzacji  
- Konteneryzacja i wdrożenia za pomocą Dockera  
- Poprawiony UX dzięki przeprojektowanemu pulpitowi  
- Zwiększona przenośność logiki walidacyjnej  

---

## Kto skorzysta z tego wydania  

- Inżynierowie danych: automatyzacja, użycie SDK, integracja z pipeline’ami  
- Zespoły platformowe: uproszczone wdrożenia przez Docker  
- Zespoły ds. zarządzania danymi: zarządzanie wielokrotnego użytku reguł walidacji  
- Zespoły analityczne: lepsza użyteczność i widoczność insightów  

---

## Aktualizacje CLI  
- Dodane wsparcie integracji SDK  
- Ulepszone workflowy import/eksport  
- Ogólne poprawki stabilności i wydajności