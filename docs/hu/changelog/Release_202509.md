---
title: digna Kiadás 2025.09 | Moduláris felépítés, öt új modul, MFA OIDC-en keresztül
description: Ismerje meg, mi az újdonság a digna Kiadás 2025.09-ben. Ez a verzió moduláris architektúrát, öt új modult, MFA-t OIDC-en keresztül és modulonkénti értesítéseket vezet be.
keywords: digna Kiadás 2025.09, digna változásnapló, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna moduláris felépítés, digna OIDC MFA
image: /assets/logo_square.png
---

# Változásnapló – Kiadás 2025.09  

A 2025.09-es kiadással a digna új **moduláris architektúrát** vezet be és elindít **öt specializált modult** az Adatminőség és Observability területén.  
Ez a kiadás továbbá megerősíti a hitelesítést és javítja az értesítések kezelését a platformon.  

---

## 🚀 Új funkciók  

### Moduláris felépítés  
- A digna mostantól **moduláris architektúrát** követ.  
- Az ügyfelek csak azokat a modulokat engedélyezhetik, amelyekre szükségük van, és később továbbiakat adhatnak hozzá.  
- A korábbi funkcionalitás mostantól a **digna Data Anomalies** része.  

### Új modulok  
- **digna Data Anomalies** – AI-alapú anomáliaészlelés az adatmennyiségekben, eloszlásokban és hiányzó értékekben.  
- **digna Data Analytics** – Idősoros értékelés az observability-mutatók vizsgálatára hosszú távú trendek és ingadozások felderítéséhez.  
- **digna Data Timeliness** – A várt adatok érkezési idejének monitorozása, AI-alapú és szabályalapú megközelítéssel.  
- **digna Data Validation** – Szabályalapú, rekordszintű ellenőrzések az üzleti szabályoknak való megfelelés biztosítására.  
- **digna Data Schema Tracker** – Sémaváltozások (DDL-módosítások) észlelése a felügyelt adatbázisokban.  

### MFA OIDC-n keresztül  
- Támogatás a **Multi-Factor Authentication (MFA)** számára OIDC Single Sign-On integrációval.  
- Vállalati szintű biztonságot nyújt minden felhasználói bejelentkezéshez.  

### Modulonkénti értesítő e-mailek  
- Az értesítések mostantól **modulonként** érkeznek, így könnyebb elkülöníteni a riasztásokat a Data Anomalies, Data Analytics és más modulok esetében.  

---

## 🛠 CLI frissítések  

- **Új parancs: `inspect-cancel`** – Törli a vizsgálatokat kérésazonosító alapján, vagy leállítja az összes aktív kérést.  
- **Új parancs: `check-config`** – Konfigurációs fájlok érvényesítése indítás előtt.  
- **Új parancs: `remove-orphans`** – Árván maradt repository bejegyzések takarítása.  
- **Kibővített `inspect` parancs** – Új opció `--bypass-backend` (`-bb`) és szabványosított visszatérési kódok (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokumentáció  
- Új útmutatók:  
  - Single Sign-On integrációs útmutató