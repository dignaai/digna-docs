---
title: digna Data Anomalies | KI-drevet observerbarhet for data
description: digna Data Anomalies er en del av digna Data Observability Platform. Modulen lærer automatisk mønstrene i dataene dine og oppdager avvik for å forbedre datakvaliteten og observerbarheten på tvers av databaser, datasjøer og datavarehus.
tags:
  - datakvalitet
  - dataobserverbarhet
  - kvalitet på data
  - observerbarhet for data
  - KI-drevet overvåking
  - avviksdeteksjon
  - digna
  - digna-plattformen
hide:
  - toc                # valgfritt: skjul den lille innholdsfortegnelsen på øverste nivå hvis du bruker innebygd navigasjon
  - navigation         # valgfritt: skjul sidenavigasjonen for frittstående sider
image: /assets/logo_square.png
---


# digna Data Anomalies – KI-basert oppdagelse av datakvalitetsproblemer

**KI-drevet observerbarhet for kontinuerlig tillit til data**

digna Data Anomalies er en del av **digna Data Observability Platform** — en modulær løsning som forbedrer **datakvaliteten** ved kontinuerlig å analysere hvordan datasett oppfører seg over tid.

Modulen lærer automatisk hva som er «normalt» for dataene dine, og varsler deg når atferden endrer seg — uten at du definerer statiske terskler eller skriver en eneste regel.  
Modulen kjører direkte i databasen din, så dataene forlater aldri ditt eget miljø.

---

## Formålet med digna Data Anomalies

Modulen **digna Data Anomalies** gir kontinuerlig **observerbarhet for data** ved å beregne og følge forhåndsdefinerte statistiske måltall, for eksempel:

- Datavolum og antall rader  
- Andel manglende verdier  
- Verdifordelinger og histogrammer  
- Numeriske intervaller og gjennomsnitt  
- Unikhet i kolonner og tekstlengde  

Disse måltallene samles inn automatisk for hvert datasett.  
Ut fra dem bygger digna modeller som representerer den typiske atferden til hvert måltall — og lærer daglige, ukentlige eller sesongbaserte mønstre.  
Når modellene er trent, forutsier modulen forventede verdier for nye data og oppdager avvik som kan tyde på kvalitetsproblemer, prosessfeil eller endringer lenger opp i kjeden.

---

## Sentrale egenskaper

- Lærer forventet dataatferd automatisk ved hjelp av KI — uten konfigurasjon av terskler.  
- Oppdager plutselige fall, topper eller drift i datavolum og fordelinger.  
- Identifiserer ombyttede kolonner eller feil kobling mellom attributter.  
- Fremhever uventede kategoriske verdier (for eksempel nye regioner eller koder).  
- Støtter alle kolonnetyper: numeriske, kategoriske eller uspesifiserte.  
- Kjører i sin helhet i kundens miljø — ingen flytting av data.  
- Integreres med **digna Data Analytics** for langsiktig trendanalyse.

---

## Slik fungerer det

### Trinn 1 – Beregning av måltall
digna beregner et sett med profilmåltall for hver tabell og kolonne.  
Disse måltallene beskriver strukturen og den statistiske atferden i dataene dine og lagres for videre analyse.

### Trinn 2 – Modelltrening
Med utgangspunkt i historiske måltallsverdier trener digna kompakte maskinlæringsmodeller (signaturmodeller) som fanger opp det normale intervallet for hvert måltall.

### Trinn 3 – Automatiske terskler
Ved hjelp av *konform inferens* beregner digna adaptive konfidensintervaller (automatiske terskler) som utvikler seg sammen med dataene dine.  
Faller nye måltallsverdier utenfor det predikerte intervallet, merkes de som avvik.

Denne kontinuerlige tilbakekoblingen sikrer at overvåkingen forblir relevant selv når datavolumer eller mønstre vokser naturlig.

---

## Eksempelscenarier

### Uventet fall i antall rader
Et datasett inneholder vanligvis rundt 500 000 rader per dag.  
Når en ny leveranse bare inneholder 50 000 rader, merker digna det som et avvik og viser hvor langt verdien ligger fra det innlærte intervallet.

### Ombyttede kolonner oppdaget
Den gjennomsnittlige strenglengden i `last_name` tilsvarer plutselig den i `first_name`.  
digna gjenkjenner avviket i måltallsmønstrene og varsler om en mulig ombytting av kolonner.

### Uventet kategori oppdaget
En kolonne med østerrikske byer inneholder plutselig «Zürich».  
Basert på historiske fordelinger merker digna den nye verdien som uventet og varsler brukeren.

---

## Integrasjon med andre moduler

- **digna Data Analytics** — aggregerer avvikshistorikk og volatilitetsmåltall for å avdekke langsiktige trender.  
- **digna Data Validation** — håndhever eksplisitte forretningsregler for deterministiske kvalitetskontroller.  
- **digna Data Timeliness** — overvåker når data ankommer, og kobler forsinkelser til forekomsten av avvik.  
- **digna Data Schema Tracker** — oppdager strukturelle endringer som kan forklare nye avvik.

---

## Typiske bruksområder

- Oppdage manglende eller dupliserte datalastinger.  
- Identifisere ombyttede eller avkortede kolonner.  
- Oppdage fordelingsdrift i numeriske eller kategoriske egenskaper.  
- Finne uventede referanseverdier eller koder.  
- Overvåke kontinuerlige innlastingspipelines for uregelmessigheter.  
- Følge den samlede **kvaliteten på og observerbarheten for data** på tvers av domener.

---

## Fordeler

- Umiddelbar oppdagelse av unormal dataatferd.  
- Fjerner behovet for manuell justering av terskler.  
- Reduserer driftsarbeidet i store datamiljøer.  
- Bygger tillit til analyse- og rapporteringssystemer.  
- Styrker **datakvaliteten** og **dataobserverbarheten** fra ende til ende.

---

## Relaterte digna-moduler

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — trend- og volatilitetsmåltall.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — regelbasert dataverifisering.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — overvåking av leveranseplaner for data.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — oppdagelse av skjemaendringer.

---

## Oppsummering

Modulen **digna Data Anomalies** utgjør kjernen i dignas KI-drevne **Data Observability Platform**.  
Ved kontinuerlig å overvåke sentrale måltall, lære mønstre og identifisere avvik hjelper den virksomheter med å sikre at **datakvaliteten** forblir pålitelig, stabil og forklarbar — uten manuell konfigurasjon.
