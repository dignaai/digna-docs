---
title: digna Kiadás 2025.09 | Moduláris architektúra, öt új modul, MFA OIDC-en keresztül
description: Tudjon meg többet a digna 2025.09 kiadás újdonságairól. Ez a verzió bevezeti a moduláris architektúrát, öt új modult, MFA OIDC-en keresztül és modulonkénti értesítéseket.
keywords: digna Kiadás 2025.09, digna changelog, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna moduláris architektúra, digna OIDC MFA
image: /assets/logo_square.png
---

# Változásnapló – Kiadás 2025.09  

A 2025.09-es kiadásban a digna bemutatja az új **moduláris architektúrát**, és elindít **öt szakterületi modult** az adatok minősége és megfigyelhetősége érdekében.  
Ez a kiadás továbbá megerősíti a hitelesítést és javítja az értesítések kezelését az egész platformon.  

---

## 🚀 Új lehetőségek  

### Moduláris tervezés  
- A digna immár **moduláris architektúrát** használ.  
- Az ügyfelek csak azokat a modulokat kapcsolhatják be, amelyekre szükségük van, és továbbiakat adhatnak hozzá igényeik növekedésével.  
- A korábbi funkcionalitás most a **digna Data Anomalies** része.  

### Új modulok  
- **digna Data Anomalies** – AI által támogatott anomáliaészlelés az adatmennyiségekben, eloszlásokban és hiányzó értékekben.  
- **digna Data Analytics** – idősoros megfigyelési mutatók elemzése hosszú távú trendek és volatilitás feltárásához.  
- **digna Data Timeliness** – az adatok várható érkezési idejének monitorozása, AI és szabályalapú megközelítéssel egyaránt.  
- **digna Data Validation** – rekordszintű szabályalapú ellenőrzések az üzleti szabályok betartásához.  
- **digna Data Schema Tracker** – sémaváltozások (DDL módosítások) észlelése a monitorozott adatbázisokban.  

### MFA OIDC-en keresztül  
- Támogatás a **többfaktoros hitelesítés (MFA)** számára OIDC Single Sign-On-on keresztül.  
- Vállalati szintű biztonságot nyújt minden felhasználói belépéshez.  

### Modulonkénti e-mail értesítések  
- Az értesítések most **modulonként** érkeznek, megkönnyítve a Data Anomalies, Data Analytics és más modulok riasztásainak elkülönítését.  

---

## 🛠 CLI frissítések  

- **Új parancs: `inspect-cancel`** – Inspekciók törlése kérésazonosító alapján vagy az összes aktív kérés leállítása.  
- **Új parancs: `check-config`** – Konfigurációs fájlok ellenőrzése a rendszer indítása előtt.  
- **Új parancs: `remove-orphans`** – Árva tárolóbejegyzések eltakarítása.  
- **Fokozott `inspect` parancs** – Új opció `--bypass-backend` (`-bb`) és standardizált visszatérési kódok (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokumentáció  
- Új útmutatók:  
  - Útmutató a Single Sign-On integrációhoz