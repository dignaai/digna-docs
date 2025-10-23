---
title: digna Wydanie 2025.09 | Architektura modułowa, pięć nowych modułów, MFA przez OIDC
description: Dowiedz się, co nowego w digna Wydanie 2025.09. Ta wersja wprowadza architekturę modułową, pięć nowych modułów, MFA przez OIDC oraz powiadomienia per moduł.
keywords: digna Wydanie 2025.09, digna lista zmian, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna architektura modułowa, digna OIDC MFA
image: /assets/logo_square.png
---

# Lista zmian – Wydanie 2025.09  

W wydaniu 2025.09 digna wprowadza nową **architekturę modułową** i uruchamia **pięć wyspecjalizowanych modułów** do kontroli jakości danych i obserwowalności.  
To wydanie wzmacnia również uwierzytelnianie i poprawia obsługę powiadomień w całej platformie.  

---

## 🚀 Nowe funkcje  

### Architektura modułowa  
- digna teraz korzysta z **architektury modułowej**.  
- Klienci mogą włączać tylko te moduły, których potrzebują, i dodawać kolejne w miarę rozwoju wymagań.  
- Poprzednia funkcjonalność jest teraz częścią **digna Data Anomalies**.  

### Nowe moduły  
- **digna Data Anomalies** – detekcja anomalii zasilana AI w zakresie wolumenów danych, rozkładów i brakujących wartości.  
- **digna Data Analytics** – ocena metryk obserwowalności w szeregach czasowych w celu wykrywania długoterminowych trendów i zmienności.  
- **digna Data Timeliness** – monitorowanie oczekiwanych czasów przybycia danych, zarówno oparte na AI, jak i regułach.  
- **digna Data Validation** – regułowe kontrole na poziomie rekordów, zapewniające zgodność z regułami biznesowymi.  
- **digna Data Schema Tracker** – wykrywanie zmian schematu (modyfikacje DDL) w monitorowanych bazach danych.  

### MFA przez OIDC  
- Wsparcie dla **uwierzytelniania wieloskładnikowego (MFA)** z OIDC Single Sign-On.  
- Zapewnia zabezpieczenia klasy korporacyjnej dla wszystkich logowań użytkowników.  

### Powiadomienia e-mail per moduł  
- Powiadomienia są teraz wysyłane **na poziomie modułu**, co ułatwia rozdzielenie alertów z Data Anomalies, Data Analytics i innych modułów.  

---

## 🛠 Aktualizacje CLI  

- **Nowa komenda: `inspect-cancel`** – anuluj inspekcje według ID żądania lub zakończ wszystkie aktywne żądania.  
- **Nowa komenda: `check-config`** – waliduj pliki konfiguracyjne przed uruchomieniem.  
- **Nowa komenda: `remove-orphans`** – oczyszczanie osieroconych wpisów repozytorium.  
- **Ulepszona komenda `inspect`** – nowa opcja `--bypass-backend` (`-bb`) i ustandaryzowane kody zwrotu (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokumentacja  
- Nowe przewodniki:  
  - Przewodnik integracji Single Sign-On