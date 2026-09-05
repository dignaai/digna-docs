# Lista zmian – Wydanie 2026.01  

W wydaniu 2026.01 digna wprowadza istotne ulepszenia w modelowaniu źródeł danych, zarządzaniu połączeniami i użyteczności inspekcji.  
To wydanie zwiększa elastyczność we wszystkich modułach i znacząco rozszerza zakres **jakości danych i walidacji**.

---

## Nowe funkcje  

### Globalne połączenia z bazą danych  
- Połączenia z bazami danych są teraz konfigurowane na **poziomie globalnym**.  
- Globalne połączenia można ponownie wykorzystywać we **wszystkich projektach**, co upraszcza konfigurację i utrzymanie.  
- **Wpływ:** Zmniejsza nakład operacyjny i zapewnia spójność połączeń w różnych środowiskach.

### Możliwość wielu konfiguracji źródeł połączeń na projekt  
- Projekty mogą teraz odwoływać się do **wielu konfiguracji połączeń źródłowych**.  
- Umożliwia bardziej elastyczne ustawienia w złożonych krajobrazach danych.  
- **Wpływ:** Wspiera realistyczne architektury korporacyjne z heterogenicznymi źródłami danych.

### Logiczne źródła danych  
- Źródła danych teraz reprezentują **warstwę logiczną** w obrębie projektu.  
- Każde źródło danych może być oparte na:
   - **tabeli bazodanowej**
   - **widoku bazodanowym**
   - **własnym zapytaniu SQL**  
- To rozdzielenie poprawia ponowne użycie, przejrzystość i modelowanie inspekcji we wszystkich modułach.  
- **Wpływ:** Rozdziela inspekcje i reguły jakości danych od fizycznego przechowywania, poprawiając konserwowalność i ponowne użycie.

### Warunek istotności anomalii  
- Można teraz zdefiniować **Warunek istotności anomalii**, aby kontrolować ocenę statusu anomalii na poziomie zestawu danych.  
- Statystyki są obliczane niezależnie od tego, czy warunek jest ustawiony lub spełniony.  
- Jeśli warunek **nie jest spełniony**, **digna Data Anomalies** nie przypisuje statusu anomalii (zielony / żółty / czerwony).  
- **Przykład:** Wyklucz zestaw danych z oceny anomalii, gdy liczba rekordów jest mniejsza niż 10.  
- **Wpływ:** Zapewnia, że anomalie są oceniane tylko w istotnych kontekstach biznesowych.

### Konfiguracja powiadomień dla poszczególnych modułów  
- Powiadomienia można teraz konfigurować **dla poszczególnych modułów** bezpośrednio w digna.  
- Umożliwia niezależną kontrolę zachowania alertów dla **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** i innych modułów.  
- **Wpływ:** Pozwala na precyzyjne strategie powiadamiania zgodne z obowiązkami zespołów i krytycznością.

### Eksport wyników inspekcji (CSV)  
- Użytkownicy mogą teraz **pobrać wyniki inspekcji jako pliki CSV**.  
- Umożliwia analizę offline, raportowanie i integrację z narzędziami zewnętrznymi.  
- **Wpływ:** Upraszcza audyty, raportowanie i dalszą analizę jakości danych.

---

## Rozszerzone możliwości walidacji danych  

W tym wydaniu **digna Data Validation** obsługuje teraz kompleksowy zestaw reguł jakości danych:

- **Reguły walidacji na poziomie wiersza**  
- **Sprawdzenia unikalności dla wielu kolumn**  
- **Walidacja integralności referencyjnej między źródłami danych**

Te sprawdzenia razem umożliwiają egzekwowanie **strukturalnych i relacyjnych reguł jakości danych** w złożonych środowiskach danych.

### Sprawdzenia unikalności dla wielu kolumn
- Wprowadzono **sprawdzenia unikalności** dla konfigurowalnego **zbioru kolumn**.  
- Umożliwia walidację kluczy złożonych i biznesowych ograniczeń unikalności.  
- **Wpływ:** Wykrywa duplikaty encji biznesowych, których nie da się zidentyfikować za pomocą pojedynczych kolumn.

### Sprawdzenia integralności referencyjnej
- Wprowadzono **sprawdzenia integralności referencyjnej** do walidacji relacji między źródłami danych.  
- Zapewnia, że **wartości kluczy obcych** w źródłowym źródle danych istnieją w referencyjnym docelowym źródle danych.  
- Obsługuje walidację pomiędzy:
  - różnymi tabelami lub widokami  
  - różnymi schematami  
  - różnymi połączeniami bazodanowymi w ramach tego samego projektu  
- Pomaga wykrywać osierocone rekordy, przerwane relacje i problemy ze spójnością danych we wczesnej fazie.  
- Zaprojektowane do pracy z **logicznymi źródłami danych**, w tym widokami i własnymi zapytaniami SQL.  
- **Zastosowania:** integralność hurtowni danych, raportowanie regulacyjne, spójność danych głównych i niezawodne analizy downstream.

---

## Kto skorzysta z tego wydania  

- **Inżynierowie danych:** Bardziej elastyczne modelowanie źródeł danych i wielokrotnego użytku połączenia z bazami danych  
- **Zespoły ds. jakości danych i governance:** Rozszerzony zakres walidacji, w tym reguły integralności relacyjnej  
- **Zespoły analityczne i BI:** Czystsze dane wejściowe i eksportowalne wyniki inspekcji  
- **Właściciele platformy:** Zmniejszona złożoność konfiguracji i lepsza konserwowalność operacyjna

---

## Aktualizacje CLI  
- Brak zmian

---