---
title: Wydanie digna 2026.06 | Python SDK, wdrożenie w Dockerze i rozszerzone zarządzanie walidacją
description: Dowiedz się, co nowego w wydaniu digna 2026.06. Ta wersja wprowadza nowe digna Python SDK, oficjalne wsparcie dla Dockera, odświeżony interfejs dashboardu oraz rozszerzoną możliwość importu/eksportu reguł walidacji danych.
keywords: digna Wydanie 2026.06, digna Python SDK, wsparcie Docker dla digna, automatyzacja jakości danych, profilowanie danych, import eksport reguł walidacji, dashboard digna, platforma obserwowalności danych, Python API, automatyzacja metadanych
image: /assets/logo_square.png
---

# Rejestr zmian – Wydanie 2026.06  

W wydaniu 2026.06 digna stawia istotny krok naprzód w zakresie automatyzacji, rozszerzalności i użyteczności platformy.  
W tej wersji wprowadzamy nowe **digna Python SDK**, oficjalne **wsparcie dla wdrożeń w Dockerze**, odświeżony interfejs dashboardu oraz zwiększoną przenośność zarządzania regułami walidacji.

---

## 🚀 Nowe funkcje  

### digna Python SDK – Automatyzuj wszystko przy użyciu Pythona  
- Instalacja:
  ```bash
  pip install digna-sdk
  ```
- Zarządzaj i automatyzuj digna programowo przy użyciu Pythona  
- Twórz i konfiguruj projekty w kodzie  
- Wyzwalaj inspekcje i uruchomienia monitoringu  
- Zarządzaj zbiorami danych, regułami i konfiguracjami programowo  
- Profiluj tabele i wydobywaj informacje o metadanych  
- Eksportuj wyniki profilowania i jakości danych do zewnętrznych repozytoriów i systemów  
- Integruj z notebookami, narzędziami orkiestracyjnymi i pipeline'ami CI/CD  

**Wpływ:** Umożliwia pełne podejście Infrastructure-as-Code oraz głęboką automatyzację przepływów pracy związanych z jakością danych i obserwowalnością przy użyciu Pythona.

---

### Wsparcie dla Dockera – Uproszczone wdrożenia i operacje  
- Oficjalny obraz Docker dla digna  
- Szybkie i spójne uruchomienie w różnych środowiskach  
- Uproszczone wdrożenie dla środowisk deweloperskich, testowych i produkcyjnych  
- Łatwa integracja z Kubernetes i platformami kontenerowymi  
- Lepsza przenośność i powtarzalność wdrożeń  

**Wpływ:** Ułatwia wdrażanie i eksploatację digna w nowoczesnych architekturach cloud-native.

---

### QueryMode – Elastyczna strategia wykonywania zapytań SQL

Skonfiguruj strategię wykonywania zapytań: tryb **Single** lub **Combined**

**Tryb Single**: Każda statystyka jest obliczana za pomocą osobnego zapytania SQL

  - Idealny dla dużych źródeł danych, gdzie ograniczenia pamięci są istotne
  - Zapobiega wyczerpaniu zasobów przy zapytaniach łączonych (brak pamięci, limity spool)
  - Większa liczba zapytań, ale niższe zużycie pamięci na zapytanie

**Tryb Combined**: Wszystkie statystyki obliczane są w jednym zapytaniu SQL

  - Zmniejsza całkowitą liczbę zapytań i narzut sieciowy
  - Optymalizuje wydajność, gdy źródła danych mieszczą się w pamięci
  - Bardziej efektywny przy częstych, równoległych uruchomieniach

**Wpływ:** Daje użytkownikom precyzyjną kontrolę nad wykonywaniem zapytań, umożliwiając balansowanie między wydajnością, zużyciem zasobów i bezpieczeństwem pamięci w zależności od charakterystyki źródła danych.


---

### Przeprojektowany interfejs dashboardu  
- Zmodernizowany i ulepszony design UI/UX  
- Czytelniejsza nawigacja i struktura  
- Lepsza widoczność wyników monitoringu i insightów dotyczących jakości danych  
- Lepsza czytelność alertów, statystyk i dashboardów  
- Szybszy dostęp do kluczowych informacji operacyjnych  

**Wpływ:** Poprawia użyteczność i codzienną produktywność wszystkich użytkowników.

---

### Rozszerzony import i eksport reguł walidacji  
- Rozszerzona funkcjonalność importu/eksportu reguł walidacji  
- Ułatwiona migracja między środowiskami i projektami  
- Lepsze ponowne wykorzystanie standaryzowanych zestawów reguł  
- Lepsze zarządzanie i kontrola cyklu życia reguł  
- Uproszczona współpraca między zespołami  

**Wpływ:** Umożliwia skalowalne i spójne zarządzanie jakością danych w całej organizacji.

---

## 🧪 Ulepszenia platformy  

- Pełna integracja Python SDK w celach automatyzacji  
- Konteneryzowane wdrożenia za pomocą Dockera  
- Poprawiony UX dzięki przeprojektowanemu dashboardowi  
- Zwiększona przenośność logiki walidacji  

---

## 🎯 Kto skorzysta z tego wydania  

- Inżynierowie danych: automatyzacja, użycie SDK, integracja z pipeline'ami  
- Zespoły platformowe: uproszczone wdrożenia przy użyciu Dockera  
- Zespoły ds. zarządzania danymi: zarządzanie wielokrotnego użytku reguł walidacji  
- Zespoły analityczne: lepsza użyteczność i widoczność insightów  

---

## 🛠 Aktualizacje CLI  
- Dodano wsparcie integracji ze SDK  
- Usprawnione procesy importu/eksportu  
- Ogólne poprawki stabilności i wydajności