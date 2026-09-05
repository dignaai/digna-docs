# Ændringslog – Udgivelse 2024.12

Udgivelsen 2024.12 bringer et nyt sæt funktioner og forbedringer, der gør digna mere automatiseret, fleksibel og klar til forretningsbrug.  
Denne version forbedrer planlægning, rapportering, forespørgselsbehandling og nøjagtigheden af anomalidetektion.  

---

## Nye funktioner

### Indbygget Scheduler
Inspektioner er ikke længere afhængige udelukkende af kommandolinjen eller API-kald.  
Med den **nye digna Scheduler** kan inspektioner udføres automatisk på definerede tidspunkter.  

- Understøtter **Cron-udtryk** for tilbagevendende skemaer (dagligt, ugentligt eller brugerdefinerede intervaller).  
- Tilbyder præcis kontrol via **offsets**, **startdatoer** og **slutdatoer**.  
- Gør det muligt for teams at sikre, at alle kritiske datakilder inspiceres konsekvent og uden manuel indsats.  

---

### Rapporter i PDF-format
Teams kan nu nemt dele resultater med interessenter via **PDF-eksport**.  

- Grafer, metrikker og anomalieresultater kan eksporteres i et professionelt PDF-format.  
- Rapporter kombinerer **visualiseringer** og **underliggende data** for at dække både tekniske og forretningsmæssige brugere.  
- Fjerner behovet for eksterne værktøjer til rapportgenerering.  

---

### Ny kolonnetype: `CUSTOM`
For at give mere fleksibilitet introducerer digna en ny **`CUSTOM` kolonnetype**.  

- Brugere kan præcist definere, hvilke **statistikker og metrikker** der anvendes på specifikke attributter.  
- Perfekt til specialtilfælde, der ikke passer ind i standardkategorier som NUMERICAL eller CATEGORICAL.  
- Hjælper med at holde analyser fokuserede og resultater relevante for forretningskonteksten.  

---

### Nye pladsholdere i snapshot-forespørgsler
Snapshot-forespørgsler er nu enklere og mindre fejlbehæftede med **dynamiske pladsholdere**.  

- Tokens som `#date+n#` eller `#date-n#` justerer automatisk datoer i forespørgsler.  
- Eksempel:  
  - `#date+1#` → i morgen  
  - `#date-2#` → for to dage siden  
- Fjerner manuelle datoberegninger og sikrer konsistens på tværs af teams.  

---

### Tærskeloptimering
Anomali-tærskler er nu mere intelligente og kontekstbevidste.  

- For metrikker som **NULL COUNT** bliver lavere tærskler automatisk begrænset til **0**.  
- Forhindrer ugyldige eller meningsløse tærskler.  
- Resulterer i færre falske positiver og mere pålidelig anomalidetektion.  

---

## Generelle forbedringer
- Forfinede **UI-komponenter** i projekt- og attributkonfigurationsvisninger.  
- Forbedret **dashboard-ydeevne** ved store datavolumener.  
- Udvidet **logning og fejlmeddelelser** til fejlfinding.  

---

## Sammenfatning
Udgivelse 2024.12 styrker digna som en platform for **datakvalitet, anomalidetektion og observabilitet**.  
Med automatisering via planlægning, delbare PDF-rapporter, tilpasselige kolonner, forenklede snapshot-forespørgsler og smartere tærskler bliver digna endnu mere værdifuld for både tekniske brugere og forretningsinteressenter.