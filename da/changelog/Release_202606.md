# Changelog – Release 2026.06  

Med Release 2026.06 tager digna et stort skridt fremad inden for automation, extensibilitet og platformbrugervenlighed.  
Denne udgivelse introducerer den nye **digna Python SDK**, officiel **Docker**-implementeringssupport, en opdateret dashboard-oplevelse og forbedret portabilitet til håndtering af valideringsregler.

---

## Nye funktioner  

### digna Python SDK – Automatiser alt med Python  
- Installer via:
  ```bash
  pip install digna-sdk
  ```
- Programmatisk administration og automatisering af digna med Python  
- Opret og konfigurer projekter via kode  
- Trigger inspektioner og overvågningskørsler  
- Administrer datasæt, regler og konfigurationer programmatisk  
- Profilér tabeller og udtræk metadataindsigter  
- Eksporter profiling- og datakvalitetsresultater til eksterne repositories og systemer  
- Integrer med notebooks, orkestreringsværktøjer og CI/CD-pipelines  

**Indvirkning:** Muliggør fuld infrastructure-as-code og dyb automatisering af datakvalitets- og observability-workflows ved hjælp af Python.

---

### Docker Support – Forenklet implementering og drift  
- Officiel Docker-image-support for digna  
- Hurtig og ensartet opsætning på tværs af miljøer  
- Forenklet onboarding til udvikling, test og produktion  
- Nem integration med Kubernetes og containerplatforme  
- Forbedret portabilitet og reproducerbarhed af deployment  

**Indvirkning:** Gør digna lettere at deployere og drive i moderne cloud-native arkitekturer.

---

### QueryMode – Fleksibel SQL-udførelsesstrategi

Konfigurer forespørgselsudførelsesstrategi: **Single** eller **Combined** mode

**Single Mode**: Hver statistik beregnes med en dedikeret SQL-forespørgsel

  - Ideel til store datakilder, hvor hukommelsesbegrænsninger er en bekymring  
  - Forhindrer ressourcemæssig udmattelse ved kombinerede forespørgsler (out of memory, spool-grænser)  
  - Højere antal forespørgsler, men lavere hukommelsesforbrug per forespørgsel

**Combined Mode**: Alle statistikker beregnes i én samlet SQL-forespørgsel

  - Reducerer det samlede antal forespørgsler og netværksoverhead  
  - Optimerer ydeevnen når datakilder er håndterbare i hukommelsen  
  - Mere effektivt ved hyppige, parallelle kørsler

**Indvirkning:** Giver brugerne finmasket kontrol over forespørgselsudførelse for at balancere ydeevne, ressourceforbrug og hukommelsessikkerhed baseret på deres datakilders karakteristika.

---

### Omdesignet dashboardoplevelse  
- Moderniseret og forbedret UI/UX-design  
- Klarere navigation og struktur  
- Bedre synlighed af overvågningsresultater og indsigter i datakvalitet  
- Forbedret læsbarhed af alerts, statistikker og dashboards  
- Hurtigere adgang til vigtig operationel information  

**Indvirkning:** Forbedrer brugervenlighed og daglig produktivitet for alle brugere.

---

### Udvidet import & eksport af valideringsregler  
- Forbedret import-/eksportfunktionalitet for valideringsregler  
- Nemmere migration mellem miljøer og projekter  
- Forbedret genbrug af standardiserede regelsæt  
- Bedre governance og lifecycle-styring af regler  
- Forenklet samarbejde på tværs af teams  

**Indvirkning:** Muliggør skalerbar og konsistent datakvalitetsgovernance i hele organisationen.

---

## Platformforbedringer  

- Fuldt Python SDK-integreret for automation  
- Containeriseret deployment via Docker  
- Forbedret UX gennem omdesignet dashboard  
- Udvidet portabilitet af valideringslogik  

---

## Hvem får gavn af denne udgivelse  

- Data Engineers: automation, SDK-brug, pipeline-integration  
- Platformteams: forenklet deployment via Docker  
- Data Governance-teams: genbrugelig håndtering af valideringsregler  
- Analytics-teams: forbedret brugbarhed og synlighed af indsigter  

---

## CLI-opdateringer  
- Tilføjet SDK-integrationssupport  
- Forbedrede import/eksport-workflows  
- Generelle stabilitets- og ydeevneforbedringer