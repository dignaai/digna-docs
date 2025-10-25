---
title: digna Release 2025.09 | Moduláris architektúra, öt nye moduler, MFA via OIDC
description: Tudja meg, mi újdonság a digna Release 2025.09-ben. Ez a kiadás moduláris architektúrát, öt új modult, MFA via OIDC-t és modulonkénti értesítéseket vezet be.
keywords: digna Release 2025.09, digna kiadási megjegyzések, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna moduláris architektúra, digna OIDC MFA
image: /assets/logo_square.png
---

# Kiadási megjegyzések – 2025.09  

A Release 2025.09-nél a digna egy új **moduláris architektúrát** vezet be, és elindít **öt specializált modult** az adatok minősége és observability területén.  
Ez a kiadás tovább erősíti az autentikációt és javítja az értesítések kezelését a platformon.  

---

## 🚀 Új funkciók  

### Moduláris architektúra  
- digna mostantól egy **moduláris architektúrát** követ.  
- Az ügyfelek csak azokat a modulokat aktiválhatják, amelyekre szükségük van, és továbbiakat adhatnak hozzá, ahogy a követelmények növekednek.  
- A korábbi funkciók mostantól a **digna Data Anomalies** részei.  

### Új modulok  
- **digna Data Anomalies** – AI-vezérelt anomáliafelismerés adattömegekben, eloszlásokban és hiányzó értékeknél.  
- **digna Data Analytics** – Idősorelemzés az observability-mutatókon a hosszú távú trendek és volatilitás észlelésére.  
- **digna Data Timeliness** – A várható adatérkezési idők felügyelete, mind AI-alapú, mind szabályalapú megközelítéssel.  
- **digna Data Validation** – Szabályalapú ellenőrzések rekordszinten az üzleti szabályoknak való megfelelés biztosítására.  
- **digna Data Schema Tracker** – Sémaváltozások (DDL-módosítások) feltárása a felügyelt adatbázisokban.  

### MFA via OIDC  
- Támogatás a **Multi-Factor Authentication (MFA)** számára OIDC Single Sign-On használatával.  
- Vállalati szintű biztonságot nyújt minden felhasználói bejelentkezéshez.  

### Értesítések modulonként  
- Az értesítések mostantól **modulonként** kerülnek kiküldésre, így könnyebb megkülönböztetni a Data Anomalies, Data Analytics és egyéb modulok értesítéseit.  

---

## 🛠 CLI-frissítések  

- **Új parancs: `inspect-cancel`** – Inspekciók megszakítása kérésazonosító alapján vagy az összes aktív kérés leállítása.  
- **Új parancs: `check-config`** – Konfigurációs fájlok érvényesítése indítás előtt.  
- **Új parancs: `remove-orphans`** – Árva repository-bejegyzések eltakarítása.  
- **Fejlesztett `inspect` parancs** – Új `--bypass-backend` (`-bb`) opció és standardizált visszatérési kódok (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokumentáció  
- Új útmutatók:  
  - Single Sign-On integrációs útmutató