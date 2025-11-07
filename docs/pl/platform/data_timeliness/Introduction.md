---
title: Data Timeliness – Monitorowanie terminowych dostaw | Dokumentacja digna
description: Dowiedz się, jak Data Timeliness od digna zapewnia, że dane docierają na czas. Wykrywaj opóźnione lub brakujące dostawy, monitoruj SLA i chroń procesy biznesowe przed ukrytymi opóźnieniami. Wykrywanie wspomagane AI dla lepszej jakości danych i obserwowalności potoków danych.
canonical_url: https://docs.digna.ai/platform/data_timeliness/
image: /assets/logo_square.png
keywords:
  - terminowość danych
  - monitorowanie dostaw
  - jakość danych
  - jakość informacji
  - obserwowalność danych
  - wykrywanie opóźnionych danych
  - alerty o brakujących danych
  - monitorowanie SLA
  - analiza dostaw AI
  - digna data timeliness
lang: pl
robots: index, follow
og_title: Data Timeliness – Monitorowanie terminowych dostaw | Dokumentacja digna
og_description: Data Timeliness od digna automatycznie wykrywa opóźnione lub brakujące dostawy danych przy użyciu AI. Chroń procesy biznesowe, monitoruj SLA i zapewnij terminowe oraz wiarygodne dane we wszystkich potokach.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – On-Time Delivery Monitoring
<h1 style="display:none;">AI-Driven Data Timeliness Module for Data Quality and Observability – digna</h1>

---

## Cel

Moduł **Data Timeliness** zapewnia, że **dane docierają na czas** — za każdym razem.  
Ciągle monitoruje harmonogramy dostaw i automatycznie wykrywa, gdy zbiory danych, tabele lub pliki są **opóźnione, brakujące lub niekompletne**.  

Łącząc uczenie AI z harmonogramami definiowanymi przez użytkownika, *digna* pozwala organizacjom zapobiegać błędom downstream i utrzymywać rygorystyczne cele **SLA (Service Level Agreement)** zarówno dla **jakości danych**, jak i **obserwowalności potoków danych**.

---

## Przegląd techniczny

### Podwójne tryby monitorowania
- **AI-Learned Arrival Patterns**  
  digna automatycznie uczy się naturalnego rytmu dostaw danych — codziennie, co godzinę lub sterowanych zdarzeniami — analizując historyczne znaczniki czasu i czasy zakończenia.  
  Dostosowuje się do zmian w kalendarzach biznesowych, weekendów czy szczytów na koniec miesiąca.

- **User-Defined Schedules**  
  Użytkownicy mogą jawnie określić oczekiwane czasy dostaw (np. *w każdy dzień powszedni przed 07:30*).  
  digna porównuje rzeczywisty czas przybycia z zaplanowanym harmonogramem i generuje alerty, gdy dane są opóźnione lub brakujące.

### Mechanizm wykrywania
- Ocena **znaczników czasu w metadanych**, **liczby rekordów** i **świeżości tabel**  
- Wykrywa **zawieszone zadania ETL**, **nieudane ekstrakcje** i **częściowe przybycie plików**  
- Integruje się z *Data Anomalies* oraz *Data Validation* dla skonsolidowanych wglądów

---

## Scenariusze wykrywania

| Scenariusz | Opis |
|-----------|--------------|
| **Late data arrival** | Codzienny strumień danych rynkowych opóźniony o dwie godziny, powodujący niedotrzymanie SLA w raportach |
| **Missing load** | Zaplanowana tabela lub partycja nie została zaktualizowana dla bieżącej daty |
| **Chained dependency delay** | Opóźnienie zadania upstream wpływa na odświeżenie potoku downstream |
| **Weekend pattern shift** | Model AI automatycznie dostosowuje się, gdy w niedziele nie oczekuje się danych |

---

## Architektura i wykonanie

- **Wykonanie w bazie danych:** digna uruchamia kontrole terminowości bezpośrednio w Twojej bazie danych lub hurtowni danych.  
- **Lekki dostęp do metadanych:** odczytuje znaczniki czasu z zadań, liczbę rekordów i informacje o partycjach — bez konieczności ekstrakcji danych.  
- **Konfigurowalna częstotliwość:** planuj monitorowanie per zbiór danych, schemat lub potok.  
- **Alerty między modułami:** wyniki mogą wywoływać wizualne ostrzeżenia w *Inspection Hub* lub powiadomienia przez e-mail, Slack lub API.  

---

## Przykładowe zastosowania

- **Dane rynków finansowych:** wykrywanie opóźnień w aktualizacjach cen lub danych transakcyjnych.  
- **Ładowania do hurtowni danych:** monitorowanie, kiedy nocne zadania ETL kończą się później niż oczekiwano.  
- **Udostępnianie danych między zespołami:** zapewnienie, że dostawy działowe następują przed dziennymi cutoffami.  
- **Raportowanie regulacyjne:** potwierdzenie, że zgłoszenia zawierają najnowszy dostępny zrzut danych.  

---

## Korzyści

| Obszar | Korzyść |
|------|----------|
| **Ciągłość biznesowa** | Zapobiega przerwom operacyjnym spowodowanym opóźnionymi lub brakującymi danymi |
| **Jakość danych** | Poprawia wiarygodność i spójność potoków danych |
| **Zgodność** | Zapewnia przestrzeganie SLA i przejrzystość audytową |
| **Automatyzacja** | AI eliminuje ręczne śledzenie harmonogramów |
| **Integracja** | Działa bezproblemowo z *Data Analytics* do wizualizacji trendów terminowości w czasie |

---

## Jak digna uczy się oczekiwanych czasów dostaw

1. **Analiza historyczna:** digna obserwuje wcześniejsze czasy ładowania i ich trwania.  
2. **Modelowanie AI:** uczenie maszynowe tworzy dynamiczną bazę odniesienia dla oczekiwanego czasu przybycia.  
3. **Monitorowanie:** Każda nowa dostawa jest porównywana z bazą odniesienia.  
4. **Alertowanie:** Odchylenia wywołują alerty z kontekstowymi metrykami i wskaźnikami pewności.

To ciągłe uczenie się dostosowuje się do ewoluujących procesów przy jednoczesnym utrzymaniu niskiego poziomu fałszywych alarmów.

---

## Najczęściej zadawane pytania

**Czy mogę zdefiniować własne czasy dostaw?**  
Tak. digna obsługuje zarówno stałe harmonogramy definiowane przez użytkownika, jak i wzorce wyuczone przez AI.

**Czy można zintegrować to z moim narzędziem ETL lub orkiestracyjnym?**  
Tak. digna integruje się z narzędziami takimi jak Airflow, dbt, Informatica czy niestandardowe schedulery.

**Gdzie odbywają się obliczenia?**  
Wszystkie analizy uruchamiane są w Twojej bazie danych lub hurtowni w chmurze — bez użycia zewnętrznych usług.

**Co się dzieje, gdy dane są opóźnione?**  
digna generuje alerty w panelu, Inspection Hub oraz poprzez API/webhooki, aby natychmiast powiadomić zespoły operacyjne.

---


**digna Data Timeliness** pomaga zapewnić **zaufanie do danych**, łącząc **wykrywanie oparte na AI**, **lokalne wykonanie (on-premises)** oraz **obserwowalność danych** — wszystko w Twoim kontrolowanym środowisku.