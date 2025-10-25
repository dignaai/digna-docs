---
title: digna Release 2025.09 | Modulär design, fem nya moduler, MFA via OIDC
description: Lär dig vad som är nytt i digna Release 2025.09. Denna version inför en modulär arkitektur, fem nya moduler, MFA via OIDC och notifieringar per modul.
keywords: digna Release 2025.09, digna ändringslogg, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modulär design, digna OIDC MFA
image: /assets/logo_square.png
---

# Ändringslogg – Release 2025.09  

Med Release 2025.09 introducerar digna en ny **modulär arkitektur** och lanserar **fem specialiserade moduler** för datakvalitet och observability.  
Denna release stärker också autentisering och förbättrar hanteringen av notifieringar i hela plattformen.  

---

## 🚀 Nya funktioner  

### Modulär design  
- digna använder nu en **modulär arkitektur**.  
- Kunder kan aktivera endast de moduler de behöver och lägga till fler efterhand som kraven växer.  
- Tidigare funktionalitet ingår nu i **digna Data Anomalies**.  

### Nya moduler  
- **digna Data Anomalies** – AI-drivna upptäckter av anomalier i datavolymer, fördelningar och saknade värden.  
- **digna Data Analytics** – Tidsserieanalys av observability-mått för att upptäcka långsiktiga trender och volatilitet.  
- **digna Data Timeliness** – Övervakning av förväntade ankomsttider för data, både AI-baserad och regelbaserad.  
- **digna Data Validation** – Regelbaserade kontroller på postnivå för att säkerställa efterlevnad av affärsregler.  
- **digna Data Schema Tracker** – Upptäckt av schemaändringar (DDL-ändringar) i övervakade databaser.  

### MFA via OIDC  
- Stöd för **Multi-Factor Authentication (MFA)** med OIDC Single Sign-On.  
- Ger företagsklassad säkerhet för alla användarinloggningar.  

### Notifieringar per modul  
- Notifieringar skickas nu **per modul**, vilket gör det enklare att separera larm från Data Anomalies, Data Analytics och andra moduler.  

---

## 🛠 CLI-uppdateringar  

- **Nytt kommando: `inspect-cancel`** – Avbryt inspektioner via begärans-ID eller terminera alla aktiva förfrågningar.  
- **Nytt kommando: `check-config`** – Validera konfigurationsfiler före uppstart.  
- **Nytt kommando: `remove-orphans`** – Rensa upp föräldralösa repositoryposter.  
- **Förbättrat `inspect`-kommando** – Nytt alternativ `--bypass-backend` (`-bb`) och standardiserade returkoder (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokumentation  
- Nya guider:  
  - Guide för integration av Single Sign-On