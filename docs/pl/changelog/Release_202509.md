---
title: digna Wydanie 2025.09 | Architektura modułowa, pięć nowych modułów, MFA przez OIDC
description: Dowiedz się, co nowego w digna Wydanie 2025.09. Ta wersja wprowadza architekturę modułową, pięć nowych modułów, MFA przez OIDC oraz powiadomienia per moduł.
keywords: digna Release 2025.09, digna changelog, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modular design, digna OIDC MFA
image: /assets/logo_square.png
---

# Dziennik zmian – Wydanie 2025.09  

W Wydaniu 2025.09 digna wprowadza nową **architekturę modułową** i uruchamia **pięć wyspecjalizowanych modułów** dla jakości danych i obserwowalności.  
To wydanie wzmacnia również uwierzytelnianie oraz usprawnia obsługę powiadomień w całej platformie.  

---

## Nowości  

### Architektura modułowa  
- digna teraz korzysta z **architektury modułowej**.  
- Klienci mogą włączać tylko te moduły, których potrzebują, i dodawać kolejne w miarę rozwoju wymagań.  
- Poprzednia funkcjonalność jest teraz częścią **digna Data Anomalies**.  

### Nowe moduły  
- **digna Data Anomalies** – Wykrywanie anomalii w wolumenach danych, rozkładach i brakujących wartościach wspomagane przez AI.  
- **digna Data Analytics** – Analiza szeregów czasowych metryk obserwowalności w celu wykrywania długoterminowych trendów i zmienności.  
- **digna Data Timeliness** – Monitorowanie oczekiwanych czasów nadejścia danych, zarówno oparte na AI, jak i regułach.  
- **digna Data Validation** – Sprawdzanie rekordów na poziomie reguł, aby zapewnić zgodność z regułami biznesowymi.  
- **digna Data Schema Tracker** – Wykrywanie zmian schematu (modyfikacji DDL) w monitorowanych bazach danych.  

### MFA przez OIDC  
- Obsługa **Multi-Factor Authentication (MFA)** przy użyciu OIDC Single Sign-On.  
- Zapewnia zabezpieczenia klasy korporacyjnej dla wszystkich logowań użytkowników.  

### Powiadomienia e-mail per moduł  
- Powiadomienia są teraz wysyłane **per moduł**, co ułatwia rozdzielenie alertów z Data Anomalies, Data Analytics i innych modułów.  

---

## Aktualizacje CLI  

- **Nowa komenda: `inspect-cancel`** – Anuluje inspekcje według ID żądania lub kończy wszystkie aktywne żądania.  
- **Nowa komenda: `check-config`** – Waliduje pliki konfiguracyjne przed uruchomieniem.  
- **Nowa komenda: `remove-orphans`** – Czyści porzucone wpisy repository.  
- **Ulepszona komenda `inspect`** – Nowa opcja `--bypass-backend` (`-bb`) oraz znormalizowane kody zwrotu (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Dokumentacja  
- Nowe przewodniki:  
  - Przewodnik integracji Single Sign-On