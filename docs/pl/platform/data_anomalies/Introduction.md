---
title: Data Anomalies – Automatyczne wykrywanie | Dokumentacja digna
description: Dowiedz się, jak digna Data Anomalies automatycznie wykrywa spadki wolumenu, brakujące wartości, przesunięcia rozkładów i nieoczekiwane wzorce bez ręcznych reguł. Popraw jakość danych dzięki wykrywaniu anomalii opartemu na AI.
---

# Data Anomalies – Automatyczne wykrywanie

## Cel
Wykrywanie anomalii bez pisania reguł.

## Funkcje techniczne
### Analizowane metryki
- Liczba rekordów  
- Brakujące wartości  
- Rozkłady i histogramy  
- Zakresy wartości  
- Unikalność  

### Inteligentne wykrywanie
- Wykorzystuje **uczenie na podstawie danych historycznych** do dynamicznego definiowania oczekiwanych zakresów  
- Oznacza anomalie, gdy rzeczywiste dane znajdują się poza oczekiwanymi granicami  

## Scenariusze wykrywania
- **Spadki/wzrosty wolumenu** → np. brak połowy dziennych transakcji  
- **Zamiana kolumn** → kolumny z imieniem i nazwiskiem zamienione miejscami  
- **Niespodziewane wartości** → „Zurich” pojawiający się wśród austriackich miast  

## Wartość
Automatyzuje to, co normalnie wymagałoby setek ręcznych reguł.