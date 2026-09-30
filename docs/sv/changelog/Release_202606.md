---
title: digna Release 2026.06 | Python SDK, Docker-distribution & Förbättrad valideringshantering
description: Läs vad som är nytt i digna Release 2026.06. Denna version introducerar det nya digna Python SDK, officiellt Docker-stöd, en omdesignad dashboard-upplevelse och utökade import-/exportfunktioner för valideringsregler.
keywords: digna Release 2026.06, digna Python SDK, digna Docker-stöd, automatisering av datakvalitet, dataprofilering, import export av valideringsregler, digna dashboard, data observability-plattform, Python API, metadata-automatisering
image: /assets/logo_square.png
---

# Ändringslogg – Release 2026.06  

Med Release 2026.06 tar digna ett stort steg framåt inom automatisering, extensibilitet och plattformsanvändbarhet.  
Denna utgåva introducerar det nya **digna Python SDK**, officiellt **Docker-stöd**, en uppfräschad dashboard-upplevelse och förbättrad portabilitet för hantering av valideringsregler.

---

## Se releasen

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — en genomgång av den här releasen på dignas YouTube-kanal.*

---

## Nya funktioner  

### digna Python SDK – Automatisera allt med Python  
- Installera via:
  ```bash
  pip install digna-sdk
  ```
- Hantera och automatisera digna programmatisk med Python  
- Skapa och konfigurera projekt via kod  
- Trigga inspektioner och monitoreringsexekveringar  
- Hantera dataset, regler och konfigurationer programmatisk  
- Profilera tabeller och extrahera metadata-insikter  
- Exportera profilering och resultat för datakvalitet till externa repositoryn och system  
- Integrera med notebooks, orkestreringsverktyg och CI/CD-pipelines  

Påverkan: Möjliggör full infrastruktur-som-kod och djup automatisering av arbetsflöden för datakvalitet och observability med Python.

---

### Docker-stöd – Förenklad distribution och drift  
- Officiellt Docker-image-stöd för digna  
- Snabb och konsekvent uppsättning över miljöer  
- Förenklad onboarding för utveckling, test och produktion  
- Enkel integration med Kubernetes och containerplattformar  
- Förbättrad portabilitet och reproducerbarhet av distributioner  

Påverkan: Gör digna enklare att distribuera och drifta i moderna cloud-native arkitekturer.

---

### QueryMode – Flexibel strategi för SQL-exekvering

Konfigurera frågeexekveringsstrategi: **Single** eller **Combined**-läge

**Single Mode**: Varje statistik beräknas med en dedikerad SQL-fråga

  - Idealiskt för stora datakällor där minnesbegränsningar är ett problem
  - Förhindrar resursuttömning i kombinerade frågor (out of memory, spool-gränser)
  - Högre antal frågor men lägre minnesavtryck per fråga

**Combined Mode**: Alla statistiker beräknas inom en enda SQL-fråga

  - Minskar totalt antal frågor och nätverksöverhead
  - Optimerar prestanda när datakällor är hanterbara i minnet
  - Mer effektivt vid frekventa, parallella exekveringar

Påverkan: Ger användare finjusterad kontroll över frågeexekvering för att balansera prestanda, resursanvändning och minnessäkerhet baserat på deras datakällors egenskaper.

---

### Konfigurerbar prediktionsmodell

Modellen bakom avvikelsedetekteringen väger nu konkurrerande förklaringar av varje serie mot varandra – ett mönster kombinerat med en tolkning av de senaste observationerna – och blandar deras prognoser efter hur starkt stöd var och en har. Ett enskilt extremvärde kan inte längre läcka in i de efterföljande prediktionerna.

Två inställningar på datakällans nya flik **Model** styr den, var och en från `0.0` till `1.0` med `0.5` som standard:

- **Break Sensitivity** – hur snabbt ett hopp till en ny nivå eller en trend som vänder godtas i stället för att behandlas som extremvärden
- **Model Complexity** – hur mycket struktur modellen letar efter, från kalendereffekter och ett enskilt nivåskifte upp till okända cykler, effekter kopplade till dag i månaden och månatliga nollställningar

Båda kan när som helst återställas till sina standardvärden. Se [Modellinställningar](../platform/data_anomalies/how_it_works.md#model-settings) för hur var och en verkar.

Påverkan: Ger användare kontroll över själva prediktionsmodellen, vid sidan av de befintliga inställningarna Sensitivity och Memory för toleransbandet, som nu finns på fliken **Thresholds**.

---

### Styrning av avvikelsenotifieringar

- Ny flik **Notifications** i datakällans avvikelseinställningar:
  - **Minimum Alerts** – hur många misslyckade kontroller (inte osäkra) en inspektion behöver innan en notifiering skickas (standard `1`)
  - **Pause After Notification (Days)** – hur länge en prenumeration förblir tyst efter att ha notifierat om datakällan (standard `0`, ingen paus)
- Prenumeranter notifieras nu när en inspektion misslyckas helt (**Notify Inspection Errors**)
- Varje notifiering länkar direkt till sidan den gäller – inspektionens misslyckade kontroller, eller vyerna för Schema Tracker och Timeliness
- Tydligare prenumerationsreglage: **Notify on Passed Inspections**, **Notify Inspection Errors**, **Notify Data Volume Checks**

Så fungerar notifieringar: notifieringar skickas via **notifieringskanaler** – Email (via en SMTP-anslutning), Slack eller Jira – som administratörer konfigurerar och kan kontrollera med **Test Notification Channel**. En **prenumeration** kopplar en kanal till ett projekt: den omfattar alla datakällor eller utvalda, och dess reglage väljer vad den rapporterar – varje modul (Data Anomalies, Data Validation, Data Analytics, Timeliness, Schema Tracker och kontroller av datavolym), inspektioner som misslyckas helt och, om så önskas, även godkända inspektioner.

Påverkan: Färre och mer åtgärdbara notifieringar – enstaka avvikelser och kvarstående anomalier översvämmar inte längre kanalen.

---

### Omdesignad dashboard-upplevelse  
- Moderniserad och förbättrad UI/UX-design  
- Klarare navigation och struktur  
- Bättre synlighet av monitoreringsresultat och insikter om datakvalitet  
- Förbättrad läsbarhet för larm, statistik och dashboards  
- Snabbare åtkomst till viktig operationell information  

Påverkan: Förbättrar användbarheten och den dagliga produktiviteten för alla användare.

---

### Utökad import & export för valideringsregler  
- Förbättrad import/export-funktionalitet för valideringsregler  
- Enklare migrering mellan miljöer och projekt  
- Förbättrad återanvändning av standardiserade regelsamlingar  
- Bättre styrning av regler och livscykelhantering  
- Förenklad samarbete mellan team  

Påverkan: Möjliggör skalbar och konsekvent styrning av datakvalitet i hela organisationen.

---

## Plattformförbättringar  

- Full Python SDK-integration för automatisering  
- Containeriserad distribution via Docker  
- Förbättrad UX genom omdesignad dashboard  
- Utökad portabilitet för valideringslogik  

---

## Vem gynnas av denna release  

- Dataingenjörer: automatisering, SDK-användning, pipeline-integration  
- Plattformsteam: förenklad distribution via Docker  
- Data Governance-team: återanvändbar hantering av valideringsregler  
- Analysteam: förbättrad användbarhet och bättre synlighet av insikter  

---

## CLI-uppdateringar  
- Lagt till stöd för SDK-integration  
- Förbättrade import/export-arbetsflöden  
- Allmänna stabilitets- och prestandaförbättringar