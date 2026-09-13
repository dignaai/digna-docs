# Changelog – Wydanie 2026.06  

W wydaniu 2026.06 digna robi duży krok naprzód w zakresie automatyzacji, rozszerzalności i użyteczności platformy.  
W tej wersji wprowadzono nowy **digna Python SDK**, oficjalne wsparcie dla wdrożeń w **Docker**, odświeżone doświadczenie pulpitu oraz lepszą przenośność w zarządzaniu regułami walidacji.

---

## Obejrzyj prezentację wydania

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — przegląd tego wydania na kanale YouTube digna.*

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

### Konfigurowalny model predykcji

Model stojący za wykrywaniem anomalii jest teraz konfigurowalny. Siedem parametrów steruje sposobem dopasowania predykcji:

- Break Sensitivity
- Outlier Sensitivity
- Memory
- Ridge Strength
- Gap Tolerance
- Outlier Correction
- Plausible Range Tightness

Wartości domyślne odpowiadają zdecydowanej większości szeregów, a każdy parametr można w dowolnej chwili przywrócić do wartości domyślnej.

**Wpływ:** Daje użytkownikom kontrolę nad samym modelem predykcji, obok istniejących ustawień Sensitivity i Memory dla pasma tolerancji. Po wskazówki, kiedy sięgnąć po dany parametr i jak go ustawić, skontaktuj się z digna.

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