---
title: digna Izdaja 2025.09 | Modularna zasnova, pet novih modulov, OIDC z MFA
description: Odkrijte novosti v izdaji digna 2025.09. Ta izdaja uvaja modularno arhitekturo, pet novih modulov, OIDC z MFA in obvestila po modulih.
keywords: digna Izdaja 2025.09, digna dnevnik sprememb, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modularna zasnova, digna OIDC MFA
image: /assets/logo_square.png
---

# Dnevnik sprememb – Izdaja 2025.09  

Z izdajo 2025.09 digna predstavlja novo **modularno arhitekturo** in ponuja **pet specializiranih modulov** za kakovost podatkov in opazljivost.  
Ta izdaja tudi krepi preverjanje identitete in izboljšuje upravljanje obvestil po celotni platformi.  

---

## 🚀 Nove funkcije  

### Modularna zasnova  
- digna zdaj uporablja **modularno arhitekturo**.  
- Stranke lahko omogočijo samo module, ki jih potrebujejo, in dodajo dodatne module, ko se potrebe povečajo.  
- Prejšnja funkcionalnost je zdaj del **digna Data Anomalies**.  

### Novi moduli  
- **digna Data Anomalies** – zaznavanje anomalij, podprto z umetno inteligenco, v obsegu podatkov, porazdelitvah in manjkajočih vrednostih.  
- **digna Data Analytics** – analiza časovnih vrst za odkrivanje dolgoročnih trendov in volatilnosti metrik opazljivosti.  
- **digna Data Timeliness** – spremljanje pričakovanih časov prihoda podatkov; tako AI-podprto kot na pravilih temelječe.  
- **digna Data Validation** – preverjanja na ravni zapisov, na osnovi pravil, za zagotavljanje skladnosti s poslovnimi pravili.  
- **digna Data Schema Tracker** – zaznavanje sprememb sheme (DDL spremembe) v spremljanih bazah podatkov.  

### OIDC z MFA  
- Podpora za **večfaktorsko preverjanje pristnosti (MFA)** z OIDC Single Sign-On.  
- Nudi varnost na podjetniški ravni za vse uporabniške prijave.  

### E-poštna obvestila po modulih  
- Obvestila se zdaj pošiljajo **po modulih**; tako je lažje ločiti opozorila iz Data Anomalies, Data Analytics in drugih modulov.  

---

## 🛠 Posodobitve CLI  

- **Nov ukaz: `inspect-cancel`** – prekličite preglede glede na ID zahteve ali končajte vse aktivne zahteve.  
- **Nov ukaz: `check-config`** – preverite datoteke konfiguracije pred zagonom.  
- **Nov ukaz: `remove-orphans`** – počistite sirote vnose repozitorijev.  
- **Izboljšan ukaz `inspect`** – nova možnost `--bypass-backend` (`-bb`) in standardizirane izhodne kode (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokumentacija  
- Novi vodiči:  
  - Priročnik za integracijo Single Sign-On