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

Modellen bakom avvikelsedetekteringen är nu konfigurerbar. Sju parametrar styr hur prediktionen anpassas:

- Break Sensitivity
- Outlier Sensitivity
- Memory
- Ridge Strength
- Gap Tolerance
- Outlier Correction
- Plausible Range Tightness

Standardvärdena passar den absoluta merparten av serierna, och varje parameter kan när som helst återställas till sitt standardvärde.

Påverkan: Ger användare kontroll över själva prediktionsmodellen, vid sidan av de befintliga inställningarna Sensitivity och Memory för toleransbandet. Kontakta digna för vägledning om när en parameter bör ändras och hur den ska sättas.

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