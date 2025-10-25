---
title: digna Kiadás 2025.09 | Moduláris felépítés, öt új modul, OIDC-vel MFA
description: Ismerje meg a digna 2025.09 kiadás újdonságait. Ez a kiadás moduláris architektúrát, öt új modult, OIDC-s MFA-t és modulonkénti értesítéseket tartalmaz.
keywords: digna Kiadás 2025.09, digna változásnapló, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna moduláris felépítés, digna OIDC MFA
image: /assets/logo_square.png
---

# Változásnapló – Kiadás 2025.09  

A 2025.09-es kiadásban a digna bemutat egy új **moduláris architektúrát**, és az adatminőség és megfigyelhetőség számára **öt szakosodott modult** kínál.  
Ez a kiadás továbbá megerősíti a hitelesítést és javítja az értesítési működést a platformon.  

---

## 🚀 Új funkciók  

### Moduláris felépítés  
- A digna mostantól **moduláris architektúrát** alkalmaz.  
- Az ügyfelek csak az általuk szükséges modulokat aktiválhatják, és igény szerint további modulokat adhatnak hozzá.  
- A korábbi funkcionalitás mostantól a **digna Data Anomalies** része.  

### Új modulok  
- **digna Data Anomalies** – Mesterséges intelligencia alapú anomáliadetektálás adatmennyiségekben, eloszlásokban és hiányzó értékekben.  
- **digna Data Analytics** – Idősoros elemzés a megfigyelhetőségi metrikák hosszú távú trendjeinek és volatilitásának azonosítására.  
- **digna Data Timeliness** – A várt adatok érkezési idejének nyomon követése; mind mesterséges intelligencia-alapú, mind szabályalapú megközelítésekkel.  
- **digna Data Validation** – Szabályalapú rekordszintű ellenőrzések az üzleti szabályoknak való megfelelés biztosítására.  
- **digna Data Schema Tracker** – A felügyelt adatbázisokban bekövetkező séma változások (DDL változások) észlelése.  

### OIDC-vel többtényezős hitelesítés (MFA)  
- OIDC Single Sign-On segítségével **többtényezős hitelesítés (MFA)** támogatása.  
- Minden felhasználói bejelentkezéshez vállalati szintű biztonságot nyújt.  

### Modulonkénti értesítő e-mailek  
- Az értesítések mostantól **modulonként** érkeznek; így könnyebb elkülöníteni a Data Anomalies, Data Analytics és a többi modul figyelmeztetéseit.  

---

## 🛠 CLI frissítések  

- **Új parancs: `inspect-cancel`** – Törölje a vizsgálatokat kérésazonosító alapján, vagy állítsa le az összes aktív kérést.  
- **Új parancs: `check-config`** – Ellenőrizze a konfigurációs fájlokat indítás előtt.  
- **Új parancs: `remove-orphans`** – Tisztítsa meg az árva tárolóbejegyzéseket.  
- **Fejlesztett `inspect` parancs** – Új opció `--bypass-backend` (`-bb`) és szabványosított kilépési kódok (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokumentáció  
- Új útmutatók:  
  - Single Sign-On integrációs útmutató