# Dziennik zmian – Wydanie 2026.04  

W wydaniu 2026.04 digna znacząco rozszerza możliwości w zakresie analityki i walidacji danych.  
Ta wersja wprowadza zaawansowaną analizę szeregów czasowych, wielokrotnego użytku komponenty walidacyjne oraz scentralizowaną standaryzację wartości.

---

## Nowe funkcje  

### Analytics Chart – analiza szeregów czasowych bez Data Science  
- Nowy **Analytics Chart** do interaktywnej analizy szeregów czasowych  
- Wbudowane metody analityczne:
    - Regresja liniowa, kwadratowa i sześcienna  
    - Regresja kawałkami z konfigurowalnymi punktami łamania  
    - Techniki wygładzania  
    - Analiza kwantylowa  
- Automatyczne rozpoznawanie trendów, sezonowości i zmian wzorców  
- Analiza resztkowa dla głębszego wglądu w odchylenia  
- Szeregi czasowe są automatycznie obliczane dla każdego zestawu danych  

**Wpływ:** Umożliwia użytkownikom zrozumienie złożonego zachowania danych w czasie bez konieczności posiadania wiedzy z zakresu data science ani użycia narzędzi zewnętrznych.

---

### Enumerations – centralne definiowanie dozwolonych wartości  
- Definiowanie wielokrotnego użytku zestawów dozwolonych wartości (np. kraje, stany, kody statusu)  
- Walidacja wartości kolumn względem zdefiniowanych enumeracji w **digna Data Validation**  
- Ponowne użycie enumeracji w różnych projektach i źródłach danych  
- Korzystanie z enumeracji wszędzie za pomocą `#ENUM:MY_ENUM#`  
- Wszystkie kontrole są wykonywane **bezpośrednio w bazie danych źródłowej**  

**Wpływ:** Zapewnia spójność i standaryzację wartości danych w całej organizacji.

---

### Szablony reguł walidacji – wielokrotnego użytku logika jakości danych  
- Definiowanie wielokrotnego użytku reguł walidacji (np. sprawdzenia białych znaków, NOT NULL, kontrole formatów)  
- Zastosowanie szablonów w wielu zestawach danych  
- Zapewnienie spójnej logiki reguł w projektach  
- Redukcja duplikacji i ręcznej konfiguracji  
- Wszystkie kontrole są wykonywane **bezpośrednio w bazie danych źródłowej**  

**Wpływ:** Umożliwia skalowalną i wydajną walidację danych bez przemieszczania danych.

---

### Warunki istotności na poziomie statystyk  
- Definiowanie warunków istotności na **poziomie kolumny dla każdej statystyki**  
- Rozszerza koncepcję warunków relewantności anomalii  
- Kontroluj, kiedy dana statystyka powinna być uznana za istotną  
- Redukuj szum przez wyłączenie sytuacji niekrytycznych  

**Wpływ:** Poprawia jakość sygnałów przez skupienie się wyłącznie na istotnych odchyleniach.

---

## Rozszerzone możliwości Data Analytics i walidacji  

W tym wydaniu digna poszerza zarówno zakres **zrozumienia danych**, jak i **standaryzacji walidacji danych**:

- Zaawansowana **interpretacja szeregów czasowych** bez wiedzy z zakresu data science  
- Scentralizowane definiowanie **dozwolonych wartości za pomocą enumeracji**  
- Wielokrotnego użytku **logika walidacji za pomocą szablonów**  
- Drobnoziarnista kontrola nad **istotnością statystyk i alertów**  

Razem te możliwości umożliwiają organizacjom nie tylko wykrywanie problemów, ale także **zrozumienie, standaryzację i kontrolę jakości danych**.

---

## Kto skorzysta z tego wydania  

- **Inżynierowie danych:** wielokrotnego użytku logika walidacji i lepsza kontrola zachowania monitoringu  
- **Zespoły ds. jakości danych i governance:** znormalizowane reguły i spójna walidacja danych w systemach  
- **Zespoły analityczne i BI:** lepsze zrozumienie trendów i odchyleń  
- **Właściciele platformy:** zwiększona adopcja dzięki uproszczonej analizie i skalowalnej walidacji  

---

## Aktualizacje CLI  
- Brak zmian  

---