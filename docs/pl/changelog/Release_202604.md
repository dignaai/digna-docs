---
title: digna Wydanie 2026.04 | Analytics Chart, Enumerations & Szablony reguł walidacji
description: Dowiedz się, co nowego w wydaniu digna 2026.04. Ta wersja wprowadza zaawansowaną analizę szeregów czasowych z Analytics Chart, wielokrotnego użytku szablony reguł walidacji, enumeracje do scentralizowanej standaryzacji wartości oraz warunki relewancji na poziomie kolumn.
keywords: digna Wydanie 2026.04, digna changelog, digna Data Analytics, time series analysis, regression, data validation templates, enumerations, allowed values validation, data quality rules, data observability
image: /assets/logo_square.png
---

# Changelog – Wydanie 2026.04  

W wydaniu 2026.04 digna znacząco rozszerza swoje możliwości w obszarze analityki i walidacji danych.  
W tej wersji wprowadzono zaawansowaną analizę szeregów czasowych, wielokrotnego użytku komponenty walidacyjne oraz scentralizowaną standaryzację wartości.

---

## 🚀 Nowości  

### Analytics Chart – analiza szeregów czasowych bez potrzeby data science  
- Nowy **Analytics Chart** do interaktywnej analizy szeregów czasowych  
- Wbudowane metody analityczne:
    - Regresja liniowa, kwadratowa i sześcienna  
    - Regresja kawałkami (piecewise) z konfigurowalnymi punktami łamania  
    - Techniki wygładzania  
    - Analiza kwantylowa  
- Automatyczna identyfikacja trendów, sezonowości i zmian wzorców  
- Analiza reszt dla głębszego wglądu w odchylenia  
- Szeregi czasowe są automatycznie obliczane dla każdego zestawu danych  

**Wpływ:** Umożliwia użytkownikom zrozumienie złożonego zachowania danych w czasie bez konieczności posiadania wiedzy z zakresu data science lub używania zewnętrznych narzędzi.

---

### Enumerations – centralna definicja dozwolonych wartości  
- Definiuj wielokrotnego użytku zbiory dozwolonych wartości (np. kraje, stany, kody statusów)  
- Waliduj wartości kolumn względem predefiniowanych enumeracji w **Data Validation**  
- Reużywaj enumeracji w wielu projektach i źródłach danych  
- Używaj enumeracji wszędzie za pomocą `#ENUM:MY_ENUM#`  
- Wszystkie sprawdzenia są wykonywane **bezpośrednio w bazie danych źródłowej**  

**Wpływ:** Zapewnia spójne i znormalizowane wartości danych w całej organizacji.

---

### Szablony reguł walidacji – wielokrotnego użytku logika jakości danych  
- Definiuj wielokrotnego użytku reguły walidacji (np. sprawdzenia białych znaków, NOT NULL, sprawdzenia formatu)  
- Stosuj szablony w wielu zestawach danych  
- Zapewniaj spójną logikę reguł w różnych projektach  
- Ogranicz powielanie konfiguracji i ręczną pracę  
- Wszystkie sprawdzenia są wykonywane **bezpośrednio w bazie danych źródłowej**  

**Wpływ:** Umożliwia skalowalną i wydajną walidację danych bez konieczności przenoszenia danych.

---

### Warunki relewancji na poziomie statystyki  
- Zdefiniuj warunki relewancji na **poziomie kolumny dla każdej statystyki**  
- Rozszerza koncepcję warunków relewancji dla anomalii  
- Kontroluj, kiedy dana statystyka powinna być uznana za istotną  
- Zmniejszaj szum przez wykluczanie sytuacji niekrytycznych  

**Wpływ:** Poprawia jakość sygnałów, koncentrując się wyłącznie na istotnych odchyleniach.

---

## 🧪 Rozszerzone możliwości Data Analytics i walidacji  

W tym wydaniu digna rozwija zarówno aspekty związane ze zrozumieniem danych, jak i standaryzacją walidacji danych:

- Zaawansowana interpretacja **szeregów czasowych** bez konieczności posiadania wiedzy data science  
- Scentralizowana definicja **dozwolonych wartości za pomocą enumeracji**  
- Wielokrotnego użytku **logika walidacji poprzez szablony**  
- Drobnoziarnista kontrola nad **relewancją statystyk i alertów**  

Razem te możliwości pozwalają organizacjom nie tylko wykrywać problemy, ale także **rozumieć, standaryzować i kontrolować jakość danych**.

---

## 🎯 Kto skorzysta z tego wydania  

- Inżynierowie danych: wielokrotnego użytku logika walidacji i lepsza kontrola nad zachowaniem monitoringu  
- Zespoły ds. jakości danych i governance: znormalizowane reguły i spójna walidacja danych w różnych systemach  
- Zespoły Analytics i BI: lepsze zrozumienie trendów i odchyleń  
- Właściciele platformy: zwiększona adopcja dzięki uproszczonej analizie i skalowalnej walidacji  

---

## 🛠 Aktualizacje CLI  
- Brak zmian  

---