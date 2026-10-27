---
title: digna Release 2026.11 | Data Reconciliation, digna Agentic og digna Engine
description: Lær hva som er nytt i digna Release 2026.11. Denne versjonen introduserer tre store nyheter - digna Data Reconciliation, digna Agentic med digna MCP Server, og digna Engine, som muliggjør kontroller av referanseintegritet mellom ulike databaseteknologier.
keywords: digna Release 2026.11, digna endringslogg, digna Data Reconciliation, dataavstemming, ETL-validering, avstemming fra kilde til mål, digna Agentic, digna MCP Server, AI-agenter datakvalitet, digna Engine, referanseintegritet på tvers av tilkoblinger, spørringsattributter, dataprofilering, dataobservabilitet
image: /assets/logo_square.png
---

# Endringslogg – Release 2026.11  

Release 2026.11 er bygget rundt tre store nyheter:

- **digna Data Reconciliation**: kontrollerer at data forblir konsistente når de flyttes mellom systemer  
- **digna Agentic**: åpner digna for AI-agenter gjennom digna MCP Server  
- **digna Engine**: profilerer valgfritt data inne i digna, og muliggjør kontroller av referanseintegritet mellom ulike databaseteknologier  

---

## Nye funksjoner  

### digna Data Reconciliation (Beta) – Konsistens fra kilde til mål  
Data passerer ofte gjennom flere systemer før de havner i en rapport. digna Data Reconciliation sammenligner en **mål**-datakilde med **kildene** den ble bygget fra, og varsler når de ikke lenger stemmer overens.

- Konfigureres som navngitte regler på den nye fanen **Data Reconciliation** i måldatakilden  
- Enhver datakilde i prosjektet der Data Reconciliation er slått på, kan være en kilde  
- Bruksområder omfatter blant annet standard avstemmingsrutiner og validering av resultatene fra ETL-prosesser  
- To typer regler: **Exact** og **AI**  

**Exact-regler – Avstemming som en datakvalitetsregel**: Du definerer nøyaktig hva som må stemme overens mellom én kilde og ett mål, slik som i en datakvalitetsregel.

  - Sammenlign én kildedatakilde med én måldatakilde  
  - Koble en kontroll i målet med en kontroll i kilden etter statistikk og attributt, f.eks. antall rader eller summen av en beløpskolonne  
  - Tillat en differanse med en **absolute** toleranse (f.eks. ± 10) eller en **relative** toleranse (f.eks. ± 0,5 % av kilden)  
  - Tidslinjen viser hver dags differanse mot toleransen  

**AI-regler – Avstemming som dataobservabilitet**: digna lærer hvordan et mål følger kildene sine, på samme måte som digna observerer data i andre moduler, og varsler når sammenhengen brytes.

  - Kombiner kontroller fra flere kildedatakilder med kontrollene i ett mål  
  - Du trenger ikke å kjenne til eller skrive ned logikken mellom dem (joins, filtre, aggregeringer)  
  - En modell lærer av historikken hvordan målet følger kildene sine samme dag  
  - Hver kontroll i målet predikeres fra dagens kildeverdier, og digna varsler når målet går utenfor båndet som dannes av regelens egne tidligere feil  
  - Hver regel har sine egne **Model settings**: **Sensitivity**, **Memory** og **Model Complexity**  

Avstemmingskontroller vises på Dashboard med en tidslinje per regel. De teller med i den samlede inspeksjonsstatusen og utløser varsler.

**Effekt:** Dekker begge sider av avstemmingen. Exact-regler håndhever kjente kontroller mellom kilde og mål, og AI-regler overvåker komplekse flyter som ETL-prosesser, slik at data som går tapt eller endres underveis, fanges opp uten håndskrevet avstemmings-SQL.

---

### digna Agentic (Beta) – digna for AI-agenter  
Den første versjonen av digna Agentic. AI-agenter kan nå jobbe med digna, svare på forretningsspørsmål om dataene dine og hjelpe til med å forbedre konfigurasjonen din.

**digna MCP Server**: Lar Claude og andre AI-agenter jobbe med digna gjennom Model Context Protocol.

  - Administrer prosjekter, datakilder, regler, inspeksjonsplaner og abonnementer  
  - Les inspeksjonsstatuser helt ned til den enkelte kontrollen for å undersøke varsler  

**Beskrivelser av datakilder og attributter**: Beskriv med vanlig språk hva en datakilde eller et attributt inneholder.

  - AI-agenter bruker beskrivelsene til å tolke dataene dine  
  - Still forretningsspørsmål om dataene dine, så svarer AI-agentene ut fra det digna overvåker  
  - Hvis dignas nåværende konfigurasjon ikke kan svare på et spørsmål, foreslår AI-agenten der det er mulig endringer i datakilden og attributtene dens, f.eks. å legge til et nytt datasett  

**Effekt:** Lar deg stille forretningsspørsmål om dataene dine med vanlig språk, og lar AI-agenter hjelpe til med å konfigurere digna og undersøke datakvalitetsproblemer.

---

### digna Engine – Profiler der du velger  
Som standard profilerer digna data der de ligger, i kildedatabasen. digna Engine legger til et alternativ: digna eksporterer dataene fra kilden og profilerer dem inne i digna Engine.

- Valgfritt, ikke obligatorisk: profilering i kildedatabasen er fortsatt tilgjengelig  
- Velges per databasetilkobling som dens **profileringssted**: **Source Database** eller **digna Engine**  
- Tilgjengelig for alle støttede kildeteknologier  

**Referanseintegritet på tvers av tilkoblinger**: Noen kontroller krever at data eksporteres. digna Engine utvider **digna Data Validation** for disse tilfellene.

  - **Kontroller av referanseintegritet** mellom datakilder på **ulike databasetilkoblinger**, også med ulike databaseteknologier (f.eks. Oracle og PostgreSQL)  
  - Fungerer med begge profileringsstedene: for Source Database eksporteres bare nøkkelkolonnene til digna Engine  
  - Dashboardet viser når en kontroll kjører på tvers av to tilkoblinger  

**Effekt:** Lar deg velge hvor data profileres, og håndhever relasjoner mellom systemer som kjører på ulike databaseteknologier.

---

## Forbedringer av profilering  

Denne utgivelsen gir også brukerne mer kontroll over hva som profileres og hvordan.

### Spørringsattributter – Brukerdefinerte kolonner  
- Definer kunstige kolonner: et SQL-uttrykk over én eller flere kolonner i datakilden  
- Hvert spørringsattributt har sitt eget navn  
- Profileres og kontrolleres som alle andre attributter  

### Kolonnekategorien DATE  
- Ny kategori **Date** for attributter  
- Måltall relativt til den inspiserte datoen  

### Profilering ved behov  
- Profiler hvilket som helst attributt mot et fullstendig øyeblikksbilde for én dato, uten å kjøre en inspeksjon  
- Hjelper deg med å angi attributtets kolonnetype: **Numerical**, **Categorical**, **Date** eller **Unspecified**  

---

## Hvem drar nytte av denne utgivelsen  

- **Dataingeniører:** Validering av ETL-resultater med digna Data Reconciliation  
- **Økonomi-, risiko- og controllingteam:** Standard avstemmingsrutiner som eksakte regler i digna Data Reconciliation  
- **Team for datakvalitet og datastyring:** Referanseintegritet på tvers av databaseteknologier med digna Engine  
- **Forretningsbrukere:** Forretningsspørsmål om data besvart av AI-agenter med digna Agentic  
- **AI- og automatiseringsteam:** AI-agenter som jobber med digna gjennom digna Agentic  

---

## CLI-oppdateringer  
- Ingen endringer  

---
