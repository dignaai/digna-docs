---
title: digna Izdaja 2025.09 | Modularna zasnova, pet novih modulov, MFA prek OIDC
description: Izvedite, kaj je novega v digna izdaji 2025.09. Ta različica uvaja modularno arhitekturo, pet novih modulov, MFA prek OIDC in obvestila po modulih.
keywords: digna Izdaja 2025.09, digna zapis sprememb, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modularna zasnova, digna OIDC MFA
image: /assets/logo_square.png
---

# Zapis sprememb – Izdaja 2025.09  

S izdajo 2025.09 digna uvaja novo **modularno arhitekturo** in predstavlja **pet specializiranih modulov** za kakovost podatkov in opazovanje.  
Ta izdaja prav tako krepi overjanje in izboljšuje upravljanje obvestil po celotni platformi.  

---

## Nove funkcije  

### Modularna zasnova  
- digna zdaj sledi **modularni arhitekturi**.  
- Stranke lahko omogočijo le module, ki jih potrebujejo, in jih dodajajo po rasti zahtev.  
- Prejšnja funkcionalnost je zdaj del **digna Data Anomalies**.  

### Novi moduli  
- **digna Data Anomalies** – AI-poganjeno zaznavanje anomalij v količinah podatkov, porazdelitvah in manjkajočih vrednostih.  
- **digna Data Analytics** – Časovno-serijska ocena metrik opazovanja za zaznavanje dolgoročnih trendov in volatilnosti.  
- **digna Data Timeliness** – Spremljanje pričakovanih časov prihoda podatkov, tako AI-podprto kot pravilo-podprto.  
- **digna Data Validation** – Preverjanja na nivoju zapisov na osnovi pravil za zagotavljanje skladnosti s poslovnimi pravili.  
- **digna Data Schema Tracker** – Zaznavanje sprememb sheme (DDL sprememb) v nadzorovanih bazah podatkov.  

### MFA prek OIDC  
- Podpora za **večfaktorsko avtentikacijo (MFA)** z OIDC Single Sign-On.  
- Zagotavlja varnost na ravni podjetja za vse prijave uporabnikov.  

### Obvestila po modulih  
- Obvestila se zdaj pošiljajo **po modulih**, kar olajša ločevanje opozoril iz Data Anomalies, Data Analytics in drugih modulov.  

---

## Posodobitve CLI  

- **Nova ukaz: `inspect-cancel`** – Prekliči inšpekcije po ID zahteve ali prekine vse aktivne zahtevke.  
- **Nova ukaz: `check-config`** – Validira konfiguracijske datoteke pred zagonom.  
- **Nova ukaz: `remove-orphans`** – Očisti sirote vpisov repozitorija.  
- **Izboljšan ukaz `inspect`** – Nova možnost `--bypass-backend` (`-bb`) in standardizirane povratne kode (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Dokumentacija  
- Novi vodniki:  
  - Vodnik za integracijo Single Sign-On