---
title: digna Release 2024.12 | Endringslogg og nye funksjoner
description: Oppdag hva som er nytt i digna Release 2024.12. Denne versjonen introduserer en innebygd scheduler, PDF-rapportering, fleksible egendefinerte kolonner, dynamiske plassholdere i snapshot-forespørsler og smartere terskeloptimalisering for å forbedre anomalideteksjon og overvåking av datakvalitet.
keywords: digna Release 2024.12, digna endringslogg, utgivelsesnotater, innebygd scheduler, PDF-rapporter, egendefinert kolonne-type, snapshot-spørringsplassholdere, terskeloptimalisering, data observability, datakvalitetsovervåking, anomalideteksjon
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Endringslogg – Release 2024.12

Release 2024.12 inneholder en ny serie funksjoner og forbedringer som gjør digna mer automatisert, fleksibel og klar for forretningen.  
Denne versjonen forbedrer planlegging, rapportering, forespørselshåndtering og nøyaktigheten i anomalideteksjon.  

---

## Nye funksjoner

### Innebygd Scheduler
Inspeksjoner er ikke lenger avhengige kun av kommandolinje eller API-kall.  
Med den **nye digna Scheduler** kan inspeksjoner kjøres automatisk på definerte tidspunkter.  

- Støtter **Cron-uttrykk** for tilbakevendende planlegging (daglig, ukentlig eller tilpassede intervaller).  
- Gir presis kontroll gjennom **offsets**, **startdatoer** og **sluttdatoer**.  
- Gjør det mulig for team å sikre at alle kritiske datakilder blir inspisert konsekvent uten manuelt arbeid.  

---

### Rapporter i PDF-format
Team kan nå enkelt dele resultater med interessenter via **PDF-eksporter**.  

- Diagrammer, måleverdier og anomalieresultater kan eksporteres i et profesjonelt PDF-format.  
- Rapporter kombinerer **visualiseringer** og **underliggende data** for å betjene både tekniske og forretningsmessige brukere.  
- Fjerner behovet for eksterne verktøy for rapportgenerering.  

---

### Ny kolonnetype: `CUSTOM`
For å gi mer fleksibilitet introduserer digna en ny kolonnetype: **`CUSTOM`**.  

- Brukere kan definere nøyaktig hvilke **statistikker og metrikker** som anvendes på spesifikke attributter.  
- Perfekt for spesialtilfeller som ikke passer inn i standardkategorier som NUMERICAL eller CATEGORICAL.  
- Hjelper med å holde analyser fokuserte og resultater relevante for forretningskonteksten.  

---

### Nye plassholdere i snapshot-forespørsler
Snapshot-forespørsler blir enklere og mindre feilutsatte med **dynamiske plassholdere**.  

- Token som `#date+n#` eller `#date-n#` justerer automatisk datoer i forespørsler.  
- Eksempel:  
  - `#date+1#` → i morgen  
  - `#date-2#` → to dager siden  
- Eliminerer manuelle datoberegninger og sikrer konsistens på tvers av team.  

---

### Terskeloptimalisering
Anomaliterskler er nå mer intelligente og kontekstbevisste.  

- For metrikker som **NULL COUNT** blir nedre terskler automatisk begrenset til **0**.  
- Forhindrer ugyldige eller meningsløse terskler.  
- Gir færre falske positiver og mer pålitelig anomalideteksjon.  

---

## Generelle forbedringer
- Forbedrede **UI-komponenter** i prosjekt- og attributtkonfigurasjonsvisninger.  
- Forbedret **dashbordytelse** for store datavolumer.  
- Bedre **logging og feilmeldinger** for feilsøking.  

---

## Sammendrag
Release 2024.12 styrker digna som en plattform for **datakvalitet, anomalideteksjon og data observability**.  
Med automatisering gjennom planlegging, delbare PDF-rapporter, tilpassbare kolonner, forenklede snapshot-forespørsler og smartere terskler blir digna enda mer verdifull for både tekniske brukere og forretningsinteressenter.