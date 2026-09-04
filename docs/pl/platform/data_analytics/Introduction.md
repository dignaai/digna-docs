---
title: Data Analytics – Trendy, stabilność i długoterminowe wnioski | Dokumentacja digna
description: Dowiedz się, jak Data Analytics w digna ujawnia długoterminowe trendy, zmienność i stabilność danych w odniesieniu do KPI. Wykrywaj zmiany w jakości i obserwowalności danych, odkrywaj ukryte anomalie i przekształcaj statystyki w praktyczne wnioski.
canonical_url: https://docs.digna.ai/platform/data_analytics/
image: /assets/logo_square.png
keywords:
  - data analytics
  - data stability
  - data trends
  - volatility detection
  - data observability
  - quality of data
  - data monitoring
  - time-series analysis
  - digna data analytics
  - kpi stability
lang: pl
robots: index, follow
og_title: Data Analytics – Trendy, stabilność i długoterminowe wnioski | Dokumentacja digna
og_description: Data Analytics w digna wykrywa długoterminowe trendy, zmienność i stabilność danych. Odkryj, jak monitorować KPI, wykrywać dryf i przekształcać statystyki danych w praktyczne wnioski biznesowe.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Analytics – Trendy i stabilność

---

## Cel

Moduł **Data Analytics** ujawnia **długoterminowe wzorce, stabilność i zmienność** w Twoich zbiorach danych — przekształcając surowe metryki w istotne wnioski.  
Zapewnia warstwę analityczną wyższego poziomu ponad wynikami *Data Anomalies*, umożliwiając zespołom **zrozumienie zmian w czasie** i poprawę zarówno **jakości danych**, jak i **obserwowalności pipeline'ów danych**.

Poprzez identyfikację przerwań trendów, powtarzających się wzorców i zmian w zmienności, Data Analytics pomaga odróżnić **oczekiwane zachowania sezonowe** od **rzeczywistych problemów z jakością danych**.

---

## Przegląd techniczny

### Statystyki pochodne
*Data Analytics* oblicza właściwości statystyczne takie jak:

- **Trend** – długoterminowy kierunek metryki (rosnący, malejący, stabilny)  
- **Volatility** – jak bardzo metryka fluktuuje w danym oknie czasowym  
- **Seasonality** – powtarzające się wzorce czasowe (dobowe, tygodniowe, miesięczne)  
- **Change Points** – statystycznie istotne przesunięcia w zachowaniu  

### Obsługiwane metryki
Moduł może analizować dowolną metrykę generowaną przez inne moduły digna, w tym:

- Liczba rekordów  
- Wskaźniki brakujących wartości  
- Statystyki rozkładu (min, max, średnia, wariancja)  
- Agregacje KPI (np. przychody, transakcje, roszczenia)  
- Odchylenia timeliness lub częstość występowania anomalii  

### Analiza szeregów czasowych
Data Analytics ocenia **stabilność w przekroju okresów** — porównując jeden tydzień, miesiąc czy kwartał z innym — wykorzystując zaufanie statystyczne i wizualne miary stabilności trendu.

---

## Jak to działa

1. **Dane wejściowe** – digna zbiera metryki szeregów czasowych z innych modułów (np. liczba anomalii).  
2. **Modelowanie statystyczne** – funkcje AI i statystyczne identyfikują ukryte trendy i poziomy zmienności.  
3. **Porównanie między okresami** – digna porównuje historyczną i aktualną wydajność KPI lub wskaźników jakości.  
4. **Generowanie wniosków** – pulpity pokazują wykryte trendy, stabilne okresy i punkty zmian w *Inspection Hub* oraz widokach analitycznych.  

Dzięki temu możliwe jest proaktywne wykrywanie *powolnych dryfów* lub *stopniowej degradacji* jakości danych, zanim staną się krytyczne.

---

## Przykładowe przypadki użycia

| Use Case | Description |
|-----------|--------------|
| **Monitoring stabilności KPI** | Śledź sprzedaż, transakcje lub roszczenia w czasie i wykrywaj nietypową zmienność. |
| **Wykrywanie ukrytego dryfu danych** | Obserwuj powolne przesunięcia w rozkładach danych lub wskaźnikach brakujących wartości, które typowe reguły pomijają. |
| **Analiza punktów zmiany** | Zidentyfikuj momenty, w których metryka zmienia swoje zachowanie (np. nagły wzrost liczby anomalii). |
| **Niezawodność operacyjna** | Oceń okresy wysokiej i niskiej stabilności danych w systemach lub działach. |
| **Wnioski biznesowe** | Wyróżnij najlepiej działające kategorie lub produkty w okresach kroczących. |

---

## Korzyści

| Area | Benefit |
|------|----------|
| **Widoczność** | Zapewnia długoterminowy wgląd w trendy i wzorce jakości danych. |
| **Wczesne ostrzeganie** | Wykrywa powolne dryfy, zanim wywołają anomalie lub naruszenia SLA. |
| **Optymalizacja** | Pomaga zidentyfikować niestabilne źródła danych lub systemy wymagające dostrojenia procesów. |
| **Analiza między modułami** | Łączy dane z Data Anomalies, Data Validation i Data Timeliness, aby uzyskać holistyczne wnioski. |
| **Działania praktyczne** | Wspiera zarówno zespoły techniczne, jak i użytkowników biznesowych w zrozumieniu danych i podejmowaniu działań.