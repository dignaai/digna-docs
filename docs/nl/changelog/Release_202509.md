---
title: digna Release 2025.09 | Modulair ontwerp, vijf nieuwe modules, MFA via OIDC
description: Lees wat nieuw is in digna Release 2025.09. Deze versie introduceert een modulaire architectuur, vijf nieuwe modules, MFA via OIDC en per-module meldingen.
keywords: digna Release 2025.09, digna changelog, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modular design, digna OIDC MFA
image: /assets/logo_square.png
---

# Changelog – Release 2025.09  

Met Release 2025.09 introduceert digna een nieuwe **modulaire architectuur** en lanceert het **vijf gespecialiseerde modules** voor Data Quality en Observability.  
Deze release versterkt ook de authenticatie en verbetert de afhandeling van notificaties over het platform.  

---

## 🚀 Nieuwe functies  

### Modulair ontwerp  
- digna volgt nu een **modulaire architectuur**.  
- Klanten kunnen alleen de modules inschakelen die ze nodig hebben en later extra modules toevoegen naarmate de eisen groeien.  
- Vorige functionaliteit maakt nu deel uit van **digna Data Anomalies**.  

### Nieuwe modules  
- **digna Data Anomalies** – AI-gestuurde detectie van anomalieën in datavolumes, verdelingen en ontbrekende waarden.  
- **digna Data Analytics** – Tijdreeksanalyse van observability-metrics om langetermijntrends en volatiliteit te detecteren.  
- **digna Data Timeliness** – Monitoring van verwachte aankomsttijden van data, zowel AI-gebaseerd als regelsgewijs.  
- **digna Data Validation** – Regels gebaseerde recordniveau-controles om naleving van bedrijfsregels te waarborgen.  
- **digna Data Schema Tracker** – Detectie van schemawijzigingen (DDL-aanpassingen) in gemonitorde databases.  

### MFA via OIDC  
- Ondersteuning voor **Multi-Factor Authentication (MFA)** met OIDC Single Sign-On.  
- Biedt enterprise-grade beveiliging voor alle gebruikersaanmeldingen.  

### Per-module notificatie-e-mails  
- Notificaties worden nu **per module** verzonden, waardoor het eenvoudiger wordt om waarschuwingen van Data Anomalies, Data Analytics en andere modules te scheiden.  

---

## 🛠 CLI-updates  

- **Nieuwe opdracht: `inspect-cancel`** – Annuleer inspecties op aanvraag-ID of beëindig alle actieve verzoeken.  
- **Nieuwe opdracht: `check-config`** – Valideer configuratiebestanden vóór opstart.  
- **Nieuwe opdracht: `remove-orphans`** – Ruim verweesde repository-vermeldingen op.  
- **Verbeterde `inspect`-opdracht** – Nieuwe optie `--bypass-backend` (`-bb`) en gestandaardiseerde returncodes (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Documentatie  
- Nieuwe gidsen:  
  - Single Sign-On integratiegids