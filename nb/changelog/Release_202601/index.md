# Changelog – Release 2026.01  

Med utgivelsen 2026.01 introduserer digna store forbedringer i modellering av datakilder, håndtering av tilkoblinger og brukervennlighet ved inspeksjoner.  
Denne utgivelsen øker fleksibiliteten i alle moduler og utvider betydelig dekningen for **datakvalitet og validering**.

---

## Nye funksjoner  

### Globale databasetilkoblinger  
- Databasetilkoblinger konfigureres nå på et **globalt nivå**.  
- Globale tilkoblinger kan gjenbrukes på tvers av **alle prosjekter**, noe som forenkler konfigurasjon og vedlikehold.  
- **Konsekvens:** Reduserer driftsmessig overhead og sikrer konsekvent tilkobling på tvers av miljøer.

### Flere kildeforbindelser per prosjekt  
- Prosjekter kan nå referere til **flere kilde-tilkoblingskonfigurasjoner**.  
- Legger til rette for mer fleksible oppsett for komplekse datalandskap per prosjekt.  
- **Konsekvens:** Støtter realistiske bedriftsarkitekturer med heterogene datakilder.

### Logiske datakilder  
- Datakilder representerer nå et **logisk lag** innen et prosjekt.  
- Hver datakilde kan være basert på:
    - en **databasetabell**
    - en **databasevisning**
    - en **egendefinert SQL-spørring**  
- Denne separasjonen forbedrer gjenbruk, tydelighet og inspeksjonsmodellering på tvers av moduler.  
- **Konsekvens:** Skiller inspeksjoner og regler for datakvalitet fra fysisk lagring, noe som forbedrer vedlikeholdbarheten og gjenbruk.

### Anomali-relevansbetingelse  
- En **Anomaly Relevance Condition** kan nå defineres for å styre vurdering av anomalistatus på datasettnivå.  
- Statistikk beregnes uavhengig av om betingelsen er satt eller oppfylt.  
- Hvis betingelsen **ikke er oppfylt**, gir **digna Data Anomalies** ikke anomalistatus (grønn / gul / rød).  
- **Eksempel:** Ekskluder datasettet fra anomalivurdering når antallet poster er under 10.  
- **Konsekvens:** Sikrer at anomalier kun vurderes i relevante forretningskontekster.

### Varslingskonfigurasjon per modul  
- Varsler kan nå konfigureres **per modul** direkte i digna.  
- Gir uavhengig kontroll over varslingsatferd for **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation**, og andre moduler.  
- **Konsekvens:** Muliggjør presise varslingsstrategier tilpasset teamansvar og kritikalitet.

### Eksport av inspeksjonsresultater (CSV)  
- Brukere kan nå **laste ned inspeksjonsresultater som CSV-filer**.  
- Legger til rette for offline-analyse, rapportering og integrasjon med eksterne verktøy.  
- **Konsekvens:** Forenkler revisjoner, rapportering og videre data kvalitetsanalyse.

---

## Utvidede muligheter for datavalidering  

Med denne utgivelsen støtter **digna Data Validation** nå et omfattende sett med datakvalitetsregler:

- **Valideringsregler på radnivå**  
- **Unikhetssjekker på tvers av flere kolonner**  
- **Referanseintegritetsvalidering på tvers av datakilder**

Sammen gjør disse kontrollene det mulig å håndheve **strukturelle og relasjonelle regler for datakvalitet** på tvers av komplekse datalandskap.

### Unikhetssjekker for flere kolonner
- Introduserer **unikhetssjekker** for et konfigurerbart **sett med kolonner**.  
- Gjør det mulig å validere sammensatte nøkler og unikhetsbegrensninger på forretningsnivå.  
- **Konsekvens:** Oppdager dupliserte forretningsentiteter som ikke kan identifiseres med enkeltkolonne-sjekker.

### Referanseintegritetskontroller
- Introduserer **referanseintegritetskontroller** for å validere relasjoner mellom datakilder.  
- Sikrer at **verdier i fremmednøkler** i en kilde-datakilde finnes i en referert mål-datakilde.  
- Hjelper med å oppdage foreldreløse poster, brutte relasjoner og konsistensproblemer tidlig.  
- Designet for å fungere med **logiske datakilder**, inkludert visninger og egendefinert SQL.  
- **Bruksområder:** datalagerintegritet, regulatorisk rapportering, konsistens i masterdata og pålitelig downstream-analyse.

---

## Hvem drar nytte av denne utgivelsen  

- **Dataingeniører:** Mer fleksibel modellering av datakilder og gjenbrukbare databasetilkoblinger  
- **Team for datakvalitet og styring:** Utvidet valideringsdekning inkludert regler for referanseintegritet  
- **Analytics- og BI-team:** Renere input og eksporterbare inspeksjonsresultater  
- **Plattformeiere:** Redusert konfigurasjonskompleksitet og forbedret driftsmessig vedlikeholdbarhet

---

## CLI-oppdateringer  
- Ingen endringer

---