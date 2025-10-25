---
title: digna Izdaja 2025.09 | Modularna arhitektura, pet novih modulov, MFA prek OIDC
description: Izvedite, kaj je novega v izdaji digna 2025.09. Ta različica uvaja modularno arhitekturo, pet novih modulov, MFA prek OIDC in obvestila po modulih.
keywords: digna Release 2025.09, digna changelog, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modularna arhitektura, digna OIDC MFA
image: /assets/logo_square.png
---

# Žurnale sprememb – Izdaja 2025.09  

V izdaji 2025.09 digna predstavlja novo **modularno arhitekturo** in zažene **pet specializiranih modulov** za kakovost podatkov in opazljivost.  
Ta izdaja prav tako krepi overjanje in izboljšuje obdelavo obvestil po celotni platformi.  

---

## 🚀 Novosti  

### Modularna zasnova  
- digna zdaj uporablja **modularno arhitekturo**.  
- Stranke lahko vklopijo samo tiste module, ki jih potrebujejo, in dodajajo ostale z rastjo zahtev.  
- Prejšnja funkcionalnost je zdaj del **digna Data Anomalies**.  

### Novi moduli  
- **digna Data Anomalies** – AI-podprto zaznavanje anomalij v količinah podatkov, porazdelitvah in manjkajočih vrednostih.  
- **digna Data Analytics** – ocena časovnih vrst opazovalnih meritev za odkrivanje dolgoročnih trendov in volatilnosti.  
- **digna Data Timeliness** – spremljanje pričakovanih časov prihoda podatkov, tako na podlagi AI kot po pravilih.  
- **digna Data Validation** – preverjanja na ravni zapisov, temelječa na pravilih, za zagotavljanje skladnosti s poslovnimi pravili.  
- **digna Data Schema Tracker** – zaznavanje sprememb shem (DDL spremembe) v spremljanih podatkovnih bazah.  

### MFA prek OIDC  
- Podpora za **večfaktorsko overjanje (MFA)** prek OIDC Single Sign-On.  
- Zagotavlja korporativno raven varnosti za vse prijave uporabnikov.  

### E-poštna obvestila po modulu  
- Obvestila so zdaj poslana **po modulu**, kar olajša ločevanje alarmov iz Data Anomalies, Data Analytics in drugih modulov.  

---

## 🛠 Posodobitve CLI  

- **Nov ukaz: `inspect-cancel`** – prekliči inšpekcije po identifikatorju zahteve ali zaključi vse aktivne zahteve.  
- **Nov ukaz: `check-config`** – preveri konfiguracijske datoteke pred zagonu.  
- **Nov ukaz: `remove-orphans`** – počisti sirotiške vnose v repozitorijih.  
- **Izboljšan ukaz `inspect`** – nova možnost `--bypass-backend` (`-bb`) in standardizirane izhodne kode (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokumentacija  
- Novi vodniki:  
  - Vodnik za integracijo Single Sign-On