---
title: digna Release 2025.09 | Modularna arhitektura, pet novih modulov, MFA via OIDC
description: Preberite, kaj je novega v digna Release 2025.09. Ta različica uvaja modularno arhitekturo, pet novih modulov, MFA via OIDC in opozorila po modulih.
keywords: digna Release 2025.09, opombe k izdaji, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modularna arhitektura, digna OIDC MFA
image: /assets/logo_square.png
---

# Izdajne opombe – 2025.09  

Z izdajo 2025.09 digna uvaja novo **modularno arhitekturo** in predstavlja **pet specializiranih modulov** za kakovost podatkov in observability.  
Ta izdaja prav tako krepi avtentikacijo in izboljšuje upravljanje opozoril po celotni platformi.  

---

## 🚀 Nove funkcije  

### Modularna arhitektura  
- digna zdaj sledi **modularni arhitekturi**.  
- Stranke lahko omogočijo le tiste module, ki jih potrebujejo, in dodajo več pozneje, ko se zahteve povečajo.  
- Prejšnja funkcionalnost je zdaj del **digna Data Anomalies**.  

### Novi moduli  
- **digna Data Anomalies** – AI-pogojena detekcija anomalij v količinah podatkov, porazdelitvah in manjkajočih vrednostih.  
- **digna Data Analytics** – Analiza časovnih vrst metrik observability za odkrivanje dolgoročnih trendov in volatilnosti.  
- **digna Data Timeliness** – Nadzor pričakovanih časov prihoda podatkov, tako AI-podprto kot na pravilih temelječe.  
- **digna Data Validation** – Na pravilih temelječe kontrole na ravni zapisov za zagotavljanje skladnosti s poslovnimi pravili.  
- **digna Data Schema Tracker** – Odkritje sprememb sheme (DDL-modifikacij) v nadzorovanih bazah podatkov.  

### MFA via OIDC  
- Podpora za **Multi-Factor Authentication (MFA)** z OIDC Single Sign-On.  
- Nudi varnost na ravni podjetja za vse uporabniške prijave.  

### Opozorila po modulih  
- Opozorila se zdaj pošiljajo **po modulih**, kar olajša razlikovanje opozoril iz Data Anomalies, Data Analytics in drugih modulov.  

---

## 🛠 Posodobitve CLI  

- **Nov ukaz: `inspect-cancel`** – Prekliči inšpekcije po ID zahteve ali konča vse aktivne zahteve.  
- **Nov ukaz: `check-config`** – Preveri veljavnost konfiguracijskih datotek pred zagonom.  
- **Nov ukaz: `remove-orphans`** – Počisti sirotične vnose v repozitoriju.  
- **Izboljšan ukaz `inspect`** – Nova možnost `--bypass-backend` (`-bb`) in standardizirane izhodne kode (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokumentacija  
- Novi vodiči:  
  - Vodnik za integracijo Single Sign-On