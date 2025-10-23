---
title: digna Lansare 2025.09 | Arhitectură modulară, cinci module noi, MFA prin OIDC
description: Aflați noutățile din lansarea digna 2025.09. Această versiune introduce o arhitectură modulară, cinci module noi, MFA prin OIDC și notificări per modul.
keywords: digna Lansare 2025.09, digna jurnal de modificări, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna design modular, digna OIDC MFA
image: /assets/logo_square.png
---

# Jurnal de modificări – Versiunea 2025.09  

Odată cu lansarea versiunii 2025.09, digna introduce o nouă **arhitectură modulară** și lansează **cinci module specializate** pentru calitatea datelor și observabilitate.  
Această versiune întărește autentificarea și îmbunătățește gestionarea notificărilor în întreaga platformă.  

---

## 🚀 Funcționalități noi  

### Arhitectură modulară  
- digna urmează acum o **arhitectură modulară**.  
- Clienții pot activa doar modulele de care au nevoie și pot adăuga altele pe măsură ce cerințele cresc.  
- Funcționalitatea anterioară face acum parte din **digna Data Anomalies**.  

### Module noi  
- **digna Data Anomalies** – Detectare bazată pe AI a anomaliilor în volumele de date, distribuții și valori lipsă.  
- **digna Data Analytics** – Evaluare în serie temporală a metricilor de observabilitate pentru detectarea trendurilor pe termen lung și a volatilității.  
- **digna Data Timeliness** – Monitorizarea momentelor așteptate de apariție a datelor, atât bazată pe AI, cât și pe reguli.  
- **digna Data Validation** – Verificări la nivel de înregistrare, bazate pe reguli, pentru a asigura conformitatea cu regulile de business.  
- **digna Data Schema Tracker** – Detectarea schimbărilor de schemă (modificări DDL) în bazele de date monitorizate.  

### MFA prin OIDC  
- Suport pentru **Autentificare Multi-Factor (MFA)** cu OIDC Single Sign-On.  
- Oferă securitate la nivel enterprise pentru toate autentificările utilizatorilor.  

### Notificări prin email per modul  
- Notificările sunt acum trimise **per modul**, facilitând separarea alertelor din Data Anomalies, Data Analytics și celelalte module.  

---

## 🛠 Actualizări CLI  

- **Comandă nouă: `inspect-cancel`** – Anulează inspectările după ID-ul cererii sau oprește toate cererile active.  
- **Comandă nouă: `check-config`** – Validează fișierele de configurare înainte de pornire.  
- **Comandă nouă: `remove-orphans`** – Curăță intrările orfane din repository.  
- **Comanda `inspect` îmbunătățită** – Opțiune nouă `--bypass-backend` (`-bb`) și coduri de retur standardizate (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Documentație  
- Ghiduri noi:  
  - Ghid de integrare Single Sign-On