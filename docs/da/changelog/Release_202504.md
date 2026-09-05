---
title: digna Release 2025.04 | Inspection Hub, Flersproget, Module Analytics
description: Læs hvad der er nyt i digna Release 2025.04. Denne version introducerer Inspection Hub, flersproget support (engelsk, tysk, polsk), import/eksport af datakilder via dignacli, den første udgave af Module Analytics og en forbedret dashboard-oplevelse.
keywords: digna Release 2025.04, digna ændringslog, digna Inspection Hub, digna flersproget support, digna Module Analytics, digna import eksport, digna CLI, udgivelsesnoter, dataobservabilitet, datakvalitetsovervågning
image: /assets/logo_square.png
---

# Ændringslog – Release 2025.04

Med Release 2025.04 tager digna et stort skridt fremad i at gøre datakvalitet og observabilitet nemmere at administrere, mere gennemsigtigt for teams og tilgængeligt for brugere verden over.  
Denne udgivelse kombinerer **kraftfulde nye funktioner**, **forbedringer i workflow-automation** og **forfinelser i brugeroplevelsen**.  

---

## Nye funktioner

### Inspection Hub – Et nyt kommandocenter
**Inspection Hub** er nu tilgængelig som det centrale sted til at administrere alle dine inspektionsjobs. I stedet for at hoppe mellem forskellige moduler eller udelukkende stole på kommandolinjekørsel, kan du nu overvåge og kontrollere dine inspektioner fra én strømlinet grænseflade.  

Vigtige funktioner inkluderer:  
- On-demand-inspektioner: Start nye jobs med det samme, når du har brug for friske resultater.  
- Inspektionshistorik: Se en tidslinje over inspektioner — hvad der blev kørt, hvem der udløste det, og hvornår.  
- Statussporing: Jobs er tydeligt markeret som fuldførte, i gang eller afventende.  
- Invoker-indblik: Tjek hurtigt, om en inspektion blev udløst af en bruger, en scheduler eller CLI’en.  
- Oprydningsværktøjer: Slet forældede eller unødvendige jobs for at holde dit arbejdsområde ryddeligt.  
- Detaljerede logs: Gå i dybden på hvert job for at se, hvor lang tid det tog, hvilke kilder der blev inkluderet, og hvordan thresholds blev anvendt.  

Inspection Hub giver teams **end-to-end synlighed og kontrol**, hvilket gør inspektioner nemmere at administrere i store projekter.  

---

### Flersproget support – digna taler dit sprog
digna er nu klar til internationale teams med introduktionen af **flersproget support**.  

I denne udgivelse kan du indstille dit **foretrukne grænsefladesprog** direkte i Brugerindstillinger. Understøttede sprog inkluderer:  
- Engelsk (UK, US, CA, AU)  
- Tysk (DE, AT, CH)  
- Polsk (PL)  

Dette gør digna nemmere at bruge for flersprogede organisationer og sikrer en mere smidig udrulning på tværs af teams i forskellige regioner. Flere sprog vil blive tilføjet i kommende udgivelser.  

---

### Import & eksport af datakilder – Konfiguration gjort enkel
Konsistens på tværs af miljøer er essentielt i enterprise-udrulninger. Med 2025.04 introducerer digna **import/eksport af datakilder** via **dignacli**, kommandolinjeværktøjet til avancerede brugere.  

Fordele:  
- Eksporter en datakildekonfiguration én gang, og genbrug den på tværs af Development, Test og Production.  
- Undgå manuel rekonfiguration og reducer dyre fejl.  
- Understøt automatiserede workflows og CI/CD-pipelines med simple CLI-kommandoer (`export-ds` og `import-ds`).  
- Kopiér hurtigt datakilder mellem projekter for lettere samarbejde.  

Denne funktionalitet sikrer, at teams kan udrulle med tillid, velvidende at konfigurationerne er ens i alle miljøer.  

---

### Module Analytics (v1) – Fra detektion til forståelse
digna startede som en platform for anomalidetektion og overvågning af datakvalitet. Med Release 2025.04 udvikler den sig videre med den **første udgave af Module Analytics**.  

Module Analytics hjælper brugere med at **forstå deres data** fremfor blot at reagere på problemer. Med dette nye modul kan du:  
- Spore langtids-trends i dine datamængder.  
- Detektere og overvåge volatilitet for at forstå udsving.  
- Udforske datadynamik over tid for dybere kontekst.  

For eksempel kan digna automatisk fremhæve, at *“Antal rækker er steget med 15,8 % siden årets begyndelse.”*  
Ingen SQL-forespørgsler, ingen manuelle tjek — bare **handlingsrettede indsigter med et øjekast**.  

Dette er fundamentet for dignas rejse mod avanceret dataanalyse, så data teams kan gå fra reaktiv til proaktiv overvågning.  

---

### Dashboard-forbedringer – En glattere brugeroplevelse
Udover de store funktioner indeholder Release 2025.04 flere **forfinelser af dashboardet**, designet til at gøre digna mere intuitiv og behagelig at bruge:  
- Hurtigere navigation mellem projekter og inspektioner.  
- Et renere layout for inspektionslogs og jobindsendelser.  
- Subtile designjusteringer, der hjælper dig med at finde indsigter hurtigere.  

Disse forbedringer er baseret direkte på kundefeedback og viser vores løbende engagement i at gøre digna **en platform bygget til daglig brug**.  

---

## Generelle forbedringer
- Ydeevneoptimeringer for inspektionsjobs på tværs af store datasæt.  
- Forbedret fejlbehandling i dignacli for at give klarere feedback.  
- Stabilitetsforbedringer for projekter med mange samtidige jobs.  
- UI-forbedringer til filtrering af joblogs og projektstyring.  

---

## Sammenfatning
Release 2025.04 handler om **kontrol, tilgængelighed og indsigt**.  

- Det nye **Inspection Hub** giver brugere fuld synlighed over inspektionsjobs.  
- **Flersproget support** sikrer, at digna kan bruges af globale teams.  
- **Import/eksport-funktionalitet** forenkler konfigurationsstyring på tværs af miljøer.  
- **Module Analytics (v1)** flytter fokus fra detektion til forståelse med trend- og volatilitetssporing.  
- **Dashboard-forbedringer** forfiner den samlede brugeroplevelse.  

Sammen gør disse opdateringer digna mere kraftfuld, brugervenlig og internationalt klar end nogensinde før.