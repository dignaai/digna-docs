---
title: digna Release 2025.04 | Inspection Hub, Fler språk, Module Analytics
description: Ta reda på vad som är nytt i digna Release 2025.04. Den här versionen introducerar Inspection Hub, flerspråkigt stöd (engelska, tyska, polska), import/export av datakällor via dignacli, den första utgåvan av Module Analytics och en förbättrad instrumentpanel.
keywords: digna Release 2025.04, digna ändringslogg, digna inspection hub, digna flerspråkigt stöd, digna module analytics, digna import export, digna CLI, release notes, data observability, data quality monitoring
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Changelog – Release 2025.04

Med Release 2025.04 tar digna ett stort steg framåt för att göra datakvalitet och observability enklare att hantera, mer transparent för team och tillgängligt för användare världen över.  
Den här releasen kombinerar **kraftfulla nyheter**, **förbättringar av arbetsflödesautomatisering** och **förfiningar av användarupplevelsen**.  

---

## Nya funktioner

### Inspection Hub – Ett nytt kontrollcenter
**Inspection Hub** är nu tillgängligt som den centrala platsen för att hantera alla dina inspektionsjobb. Istället för att hoppa mellan olika moduler eller enbart förlita dig på kommandoradskörning kan du nu övervaka och styra dina inspektioner från ett enhetligt gränssnitt.  

Huvudfunktioner inkluderar:  
- Inspektioner vid behov: Starta nya jobb direkt när du behöver färska resultat.  
- Inspektionshistorik: Se en tidslinje över inspektioner — vad som kördes, vem som startade det och när.  
- Statusspårning: Jobb markeras tydligt som slutförda, pågående eller väntande.  
- Invoker-insikter: Kontrollera snabbt om en inspektion utlösts av en användare, schemaläggare eller CLI.  
- Rensningsverktyg: Ta bort inaktuella eller onödiga jobb för att hålla arbetsytan ren.  
- Detaljerade loggar: Borra ner i varje jobb för att se hur lång tid det tog, vilka källor som inkluderades och hur tröskelvärden tillämpades.  

Inspection Hub ger teamet **genomgående insyn och kontroll**, vilket gör inspektioner enklare att hantera i stora projekt.  

---

### Flerspråkigt stöd – digna talar ditt språk
digna är nu redo för internationella team med introduktionen av **flerspråkigt stöd**.  

I den här releasen kan du ställa in ditt **föredragna gränssnittsspråk** direkt i användarinställningarna. Stödda språk inkluderar:  
- Engelska (UK, US, CA, AU)  
- Tyska (DE, AT, CH)  
- Polska (PL)  

Detta gör digna enklare att använda för flerspråkiga organisationer och säkerställer smidigare införande i team som arbetar i olika regioner. Fler språk kommer att läggas till i kommande releaser.  

---

### Import & export av datakällor – Konfiguration förenklad
Konsistens mellan miljöer är avgörande i företagsdistributioner. Med 2025.04 introducerar digna **import/export av datakällor** via **dignacli**, kommandoradsverktyget för avancerade användare.  

Fördelar:  
- Exportera en datakällkonfiguration en gång och återanvänd den i Development, Test och Production.  
- Eliminera manuell omkonfiguration och undvik kostsamma fel.  
- Stöd automatiserade arbetsflöden och CI/CD-pipelines med enkla CLI-kommandon (`export-ds` och `import-ds`).  
- Kopiera snabbt datakällor mellan projekt för enklare samarbete.  

Denna funktionalitet säkerställer att team kan distribuera med förtroende, i vetskap om att konfigurationerna är konsekventa i varje miljö.  

---

### Module Analytics (v1) – Från upptäckt till förståelse
digna började som en plattform för anomalidetektion och övervakning av datakvalitet. Med Release 2025.04 utvecklas den vidare med den **första versionen av Module Analytics**.  

Module Analytics hjälper användare att **förstå sina data** istället för att bara reagera på problem. Med denna nya modul kan du:  
- Spåra långsiktiga trender i dina datamängder.  
- Upptäcka och övervaka volatilitet för att förstå fluktuationer.  
- Utforska data beteende över tid för djupare kontext.  

Till exempel kan digna automatiskt markera att *“Radantalet ökade med 15,8 % sedan årets början.”*  
Ingen SQL, inga manuella kontroller — bara **åtgärdsbara insikter vid en blick**.  

Detta är grunden för dignas resa mot avancerad dataanalys och gör det möjligt för datateam att gå från reaktiv till proaktiv övervakning.  

---

### Förbättringar av instrumentpanelen – En mjukare användarupplevelse
Utöver de stora funktionerna innehåller Release 2025.04 flera **förfiningar av instrumentpanelen** utformade för att göra digna mer intuitivt och trevligt att använda:  
- Snabbare navigation mellan projekt och inspektioner.  
- Ett renare upplägg för inspektionsloggar och jobbinsändningar.  
- Subtila designjusteringar som hjälper dig hitta insikter snabbare.  

Dessa förbättringar är baserade direkt på kundfeedback och visar vårt löpande engagemang för att göra digna **en plattform byggd för dagligt bruk**.  

---

## Allmänna förbättringar
- Prestandaoptimeringar för inspektionsjobb över stora datamängder.  
- Förbättrad felhantering i dignacli för att ge tydligare återkoppling.  
- Stabilitetsförbättringar för projekt med många samtidiga jobb.  
- UI-förbättringar för filtrering av jobbloggar och projektledning.  

---

## Sammanfattning
Release 2025.04 handlar om **kontroll, tillgänglighet och insikt**.  

- Det nya **Inspection Hub** ger användare full insyn i inspektionsjobb.  
- **Flerspråkigt stöd** säkerställer att digna kan användas i globala team.  
- **Import/export-funktionalitet** förenklar konfigurationshantering mellan miljöer.  
- **Module Analytics (v1)** flyttar fokus från upptäckt till förståelse, med trend- och volatilitetsspårning.  
- **Förbättringar av instrumentpanelen** förfinar den övergripande användarupplevelsen.  

Tillsammans gör dessa uppdateringar digna mer kraftfullt, användarvänligt och internationellt redo än någonsin tidigare.