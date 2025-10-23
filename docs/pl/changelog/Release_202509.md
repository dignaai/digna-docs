---
title: digna Wydanie 2025.09 | Architektura modułowa, pięć nowych modułów, MFA przez OIDC
description: Dowiedz się, co nowego w digna Wydanie 2025.09. Ta wersja wprowadza architekturę modułową, pięć nowych modułów, MFA przez OIDC oraz powiadomienia przypisane do poszczególnych modułów.
keywords: digna Wydanie 2025.09, digna dziennik zmian, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna architektura modułowa, digna OIDC MFA
image: /assets/logo_square.png
---

# Changelog – Release 2025.09  

W wydaniu 2025.09 digna wprowadza nową **architekturę modułową** i uruchamia **pięć wyspecjalizowanych modułów** do jakości danych i obserwowalności.  
To wydanie wzmacnia także mechanizmy uwierzytelniania i usprawnia obsługę powiadomień w całej platformie.  

---

## 🚀 Nowości  

### Architektura modułowa  
- digna teraz stosuje **architekturę modułową**.  
- Klienci mogą włączyć tylko te moduły, których potrzebują, i dodawać kolejne wraz z rozwojem wymagań.  
- Poprzednia funkcjonalność jest teraz częścią **digna Data Anomalies**.  

### Nowe moduły  
- **digna Data Anomalies** – Wykrywanie anomalii zasilane AI w zakresie wolumenów danych, rozkładów i brakujących wartości.  
- **digna Data Analytics** – Analiza szeregów czasowych metryk obserwowalności w celu wykrywania długoterminowych trendów i zmienności.  
- **digna Data Timeliness** – Monitorowanie oczekiwanych czasów napływu danych, zarówno oparte na AI, jak i regułach.  
- **digna Data Validation** – Kontrole oparte na regułach na poziomie rekordów, zapewniające zgodność z regułami biznesowymi.  
- **digna Data Schema Tracker** – Wykrywanie zmian schematu (modyfikacje DDL) w monitorowanych bazach danych.  

### MFA przez OIDC  
- Obsługa uwierzytelniania wieloskładnikowego (MFA) z OIDC Single Sign-On.  
- Zapewnia zabezpieczenia klasy korporacyjnej dla wszystkich logowań użytkowników.  

### Powiadomienia e-mail przypisane do poszczególnych modułów  
- Powiadomienia są teraz wysyłane **per moduł**, co ułatwia rozdzielenie alertów pochodzących z Data Anomalies, Data Analytics i innych modułów.  

---

## 🛠 Aktualizacje CLI  

- **Nowa komenda: `inspect-cancel`** – Anuluj inspekcje według ID żądania lub zakończ wszystkie aktywne żądania.  
- **Nowa komenda: `check-config`** – Waliduj pliki konfiguracyjne przed uruchomieniem.  
- **Nowa komenda: `remove-orphans`** – Posprzątaj porzucone wpisy repozytorium.  
- **Ulepszona komenda `inspect`** – Nowa opcja `--bypass-backend` (`-bb`) oraz ustandaryzowane kody zwrotne (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokumentacja  
- Nowe przewodniki:  
  - Przewodnik integracji Single Sign-On