---
title: digna Release 2026.06 | Python SDK, Docker-implementatie & Verbeterd beheer van validatieregels
description: Lees wat er nieuw is in digna Release 2026.06. Deze versie introduceert de nieuwe digna Python SDK, Docker-implementatieondersteuning, een vernieuwde dashboardervaring en uitgebreide import/exportmogelijkheden voor validatieregels.
keywords: digna Release 2026.06, digna Python SDK, digna Docker-ondersteuning, automatisering van datakwaliteit, data profiling, import/export van validatieregels, digna-dashboard, data observability platform, Python API, metadata-automatisering
image: /assets/logo_square.png
---

# Wijzigingslog – Release 2026.06  

Met Release 2026.06 zet digna een grote stap vooruit op het gebied van automatisering, uitbreidbaarheid en platformbruikbaarheid.  
Deze release introduceert de nieuwe **digna Python SDK**, officiële **Docker-implementatieondersteuning**, een vernieuwde dashboardervaring en verbeterde draagbaarheid voor het beheer van validatieregels.

---

## 🚀 Nieuwe functies  

### digna Python SDK – Automatiseer alles met Python  
- Installatie via:
  ```bash
  pip install digna-sdk
  ```
- Programmeerbaar beheer en automatisering van digna met Python  
- Maak projecten aan en configureer ze via code  
- Trigger inspecties en monitoring-executies  
- Beheer datasets, regels en configuraties programmeerbaar  
- Profileer tabellen en extraheer metadata-inzichten  
- Exporteer profiling- en datakwaliteitsresultaten naar externe repositories en systemen  
- Integreer met notebooks, orchestration tools en CI/CD-pijplijnen  

**Impact:** Maakt volledig infrastructure-as-code mogelijk en biedt diepe automatisering van datakwaliteits- en observability-workflows met Python.

---

### Docker-ondersteuning – Vereenvoudigde deployment & operatie  
- Officiële Docker-image-ondersteuning voor digna  
- Snelle en consistente setup in verschillende omgevingen  
- Vereenvoudigde onboarding voor development, test en productie  
- Eenvoudige integratie met Kubernetes en containerplatforms  
- Verbeterde draagbaarheid en reproduceerbaarheid van deployments  

**Impact:** Maakt digna eenvoudiger te deployen en te beheren in moderne cloud-native architecturen.

---

### QueryMode – Flexibele SQL-uitvoeringsstrategie

Stel de query-uitvoeringsstrategie in: **Single** of **Combined** modus

**Single Mode**: Elke statistiek wordt berekend met één dedicated SQL-query

  - Ideaal voor grote datasources waar geheugenbeperkingen een rol spelen
  - Voorkomt resource-uitputting bij gecombineerde queries (out of memory, spool-limieten)
  - Hoger aantal queries maar lagere geheugendruk per query

**Combined Mode**: Alle statistieken worden berekend binnen één enkele SQL-query

  - Vermindert het totale aantal queries en netwerkoverhead
  - Optimaliseert prestaties wanneer datasources in het geheugen beheersbaar zijn
  - Efficiënter voor frequente, parallelle uitvoeringen

**Impact:** Geeft gebruikers fijnmazige controle over query-executie om prestaties, resourcegebruik en geheugenzekerheid af te stemmen op de kenmerken van hun datasource.

---

### Herontworpen dashboardervaring  
- Gemoderniseerd en verbeterd UI/UX-ontwerp  
- Duidelijkere navigatie en structuur  
- Betere zichtbaarheid van monitoringresultaten en datakwaliteitsinzichten  
- Verbeterde leesbaarheid van alerts, statistieken en dashboards  
- Snellere toegang tot cruciale operationele informatie  

**Impact:** Verhoogt de gebruiksvriendelijkheid en dagelijkse productiviteit voor alle gebruikers.

---

### Uitgebreide import & export voor validatieregels  
- Verbeterde import/exportfunctionaliteit voor validatieregels  
- Eenvoudigere migratie tussen omgevingen en projecten  
- Betere herbruikbaarheid van gestandaardiseerde regelsets  
- Verbeterde governance en lifecycle-management van regels  
- Vereenvoudigde samenwerking tussen teams  

**Impact:** Maakt schaalbaar en consistent beheer van datakwaliteit across de organisatie mogelijk.

---

## 🧪 Platformverbeteringen  

- Volledige Python SDK-integratie voor automatisering  
- Gefcontaineriseerde deployment via Docker  
- Verbeterde UX door het herontworpen dashboard  
- Uitgebreide draagbaarheid van validatielogica  

---

## 🎯 Wie profiteert van deze release  

- Data Engineers: automatisering, SDK-gebruik, pipeline-integratie  
- Platformteams: vereenvoudigde deployment via Docker  
- Data Governance Teams: herbruikbaar beheer van validatieregels  
- Analytics Teams: verbeterde gebruiksvriendelijkheid en zichtbaarheid van inzichten  

---

## 🛠 CLI-updates  
- Toegevoegde SDK-integratiesteun  
- Verbeterde import/export-workflows  
- Algemeen stabielheids- en prestatieverbeteringen