# Changelog – Wydanie 2026.11  

Wydanie 2026.11 koncentruje się na trzech głównych nowościach:

- **digna Data Reconciliation**: sprawdza, czy dane pozostają spójne podczas przepływu między systemami  
- **digna Agentic**: otwiera digna na agentów AI za pośrednictwem digna MCP Server  
- **digna Engine**: opcjonalnie profiluje dane wewnątrz digna i umożliwia kontrole integralności referencyjnej między różnymi technologiami baz danych  

---

## Nowe funkcje  

### digna Data Reconciliation (Beta) – Spójność od źródła do celu  
Dane często przechodzą przez kilka systemów, zanim trafią do raportu. digna Data Reconciliation porównuje **docelowe** źródło danych ze **źródłami**, z których zostało zbudowane, i alarmuje, gdy przestają się one zgadzać.

- Konfigurowane jako nazwane reguły na nowej karcie **Data Reconciliation** docelowego źródła danych  
- Źródłem może być każde źródło danych projektu z włączonym modułem Data Reconciliation  
- Zastosowania obejmują standardowe procedury uzgadniania oraz walidację wyników procesów ETL  
- Dwa typy reguł: **Dokładne** i **AI**  

**Reguły Dokładne – Uzgadnianie jako reguła jakości danych**: Dokładnie określasz, co musi się zgadzać między jednym źródłem a jednym celem, tak jak w regule jakości danych.

  - Porównanie jednego źródłowego źródła danych z jednym docelowym źródłem danych  
  - Parowanie kontroli docelowej z kontrolą źródłową według statystyki i atrybutu, np. liczby wierszy lub sumy kolumny z kwotami  
  - Dopuszczenie różnicy z tolerancją typu **Bezwzględna** (np. ± 10) lub **Względna** (np. ± 0,5% wartości źródłowej)  
  - Oś czasu pokazuje różnicę z każdego dnia na tle tolerancji  

**Reguły AI – Uzgadnianie jako obserwowalność danych**: digna uczy się, jak cel podąża za swoimi źródłami – w taki sam sposób, w jaki digna obserwuje dane w innych modułach – i alarmuje, gdy ta zależność zostaje zerwana.

  - Łączenie kontroli z kilku źródłowych źródeł danych z kontrolami jednego celu  
  - Nie trzeba znać ani spisywać logiki, która je łączy (złączenia, filtry, agregacje)  
  - Model uczy się z historii, jak cel podąża za swoimi źródłami tego samego dnia  
  - Każda kontrola docelowa jest przewidywana na podstawie wartości źródłowych z danego dnia, a digna alarmuje, gdy cel wyjdzie poza pasmo wyznaczone przez wcześniejsze błędy samej reguły  
  - Każda reguła ma własne **Ustawienia modelu**: **Czułość**, **Pamięć** i **Złożoność modelu**  

Kontrole uzgadniania pojawiają się na pulpicie z osią czasu dla każdej reguły. Są wliczane do ogólnego statusu inspekcji i wyzwalają powiadomienia.

**Wpływ:** Obejmuje obie strony uzgadniania. Reguły Dokładne egzekwują znane kontrole między źródłem a celem, a reguły AI monitorują złożone przepływy, takie jak procesy ETL, dzięki czemu dane utracone lub zmienione po drodze są wychwytywane bez ręcznie pisanego SQL do uzgadniania.

---

### digna Agentic (Beta) – digna dla agentów AI  
Pierwsza wersja digna Agentic. Agenci AI mogą teraz pracować z digna, odpowiadać na pytania biznesowe dotyczące Twoich danych i pomagać w ulepszaniu Twojej konfiguracji.

**digna MCP Server**: Umożliwia Claude i innym agentom AI pracę z digna za pośrednictwem Model Context Protocol.

  - Zarządzanie projektami, źródłami danych, regułami, harmonogramami inspekcji i subskrypcjami  
  - Odczyt statusów inspekcji aż do pojedynczej kontroli, aby badać alerty  

**Opisy źródeł danych i atrybutów**: Opisz prostym językiem, co zawiera źródło danych lub atrybut.

  - Agenci AI wykorzystują opisy do interpretowania Twoich danych  
  - Zadawaj pytania biznesowe dotyczące Twoich danych, a agenci AI odpowiedzą na nie na podstawie tego, co monitoruje digna  
  - Jeśli bieżąca konfiguracja digna nie pozwala odpowiedzieć na pytanie, agent AI w miarę możliwości proponuje zmiany w źródle danych i jego atrybutach, np. dodanie nowego zbioru danych  

**Wpływ:** Pozwala zadawać pytania biznesowe dotyczące danych prostym językiem, a agentom AI pomagać w konfigurowaniu digna i badaniu problemów z jakością danych.

---

### digna Engine – Profilowanie tam, gdzie chcesz  
Domyślnie digna profiluje dane tam, gdzie się znajdują, czyli w źródłowej bazie danych. digna Engine dodaje nową możliwość: digna eksportuje dane ze źródła i profiluje je wewnątrz digna Engine.

- Opcjonalnie, nie obowiązkowo: profilowanie w źródłowej bazie danych pozostaje dostępne  
- Wybierane dla każdego połączenia z bazą danych jako **Lokalizacja profilowania**: **Źródłowa baza danych** lub **digna Engine**  
- Dostępne dla każdej obsługiwanej technologii źródłowej  

**Integralność referencyjna między połączeniami**: Niektóre kontrole wymagają eksportu danych. digna Engine rozszerza **digna Data Validation** o obsługę takich przypadków.

  - **Kontrole integralności referencyjnej** między źródłami danych na **różnych połączeniach z bazami danych**, także w różnych technologiach baz danych (np. Oracle i PostgreSQL)  
  - Działa z obiema lokalizacjami profilowania: w przypadku źródłowej bazy danych do digna Engine eksportowane są tylko kolumny kluczowe  
  - Pulpit pokazuje, kiedy kontrola obejmuje dwa połączenia  

**Wpływ:** Pozwala wybrać, gdzie dane są profilowane, i egzekwuje zależności między systemami działającymi na różnych technologiach baz danych.

---

## Ulepszenia profilowania  

To wydanie daje też użytkownikom większą kontrolę nad tym, co i jak jest profilowane.

### Atrybuty zapytań – Kolumny definiowane przez użytkownika  
- Definiowanie sztucznych kolumn: wyrażenie SQL na jednej lub kilku kolumnach źródła danych  
- Każdy atrybut zapytania ma własną nazwę  
- Profilowany i sprawdzany jak każdy inny atrybut  

### Kategoria kolumn DATE  
- Nowa kategoria **Data** dla atrybutów  
- Metryki liczone względem badanej daty  

### Profilowanie na żądanie  
- Profilowanie dowolnego atrybutu na pełnym zrzucie danych z jednej daty, bez uruchamiania inspekcji  
- Pomaga ustawić typ kolumny atrybutu: **Liczbowy**, **Kategoryczny**, **Data** lub **Inny**  

---

## Kto skorzysta z tego wydania  

- **Inżynierowie danych:** walidacja wyników ETL z digna Data Reconciliation  
- **Zespoły finansów, ryzyka i controllingu:** standardowe procedury uzgadniania jako reguły Dokładne w digna Data Reconciliation  
- **Zespoły ds. jakości danych i governance:** integralność referencyjna między technologiami baz danych dzięki digna Engine  
- **Użytkownicy biznesowi:** odpowiedzi agentów AI na pytania biznesowe o dane dzięki digna Agentic  
- **Zespoły AI i automatyzacji:** agenci AI pracujący z digna za pośrednictwem digna Agentic  

---

## Aktualizacje CLI  
- Brak zmian  