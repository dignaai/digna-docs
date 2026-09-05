# Data Schema Tracker – Overvåk skjemaendringer

---

## Formål

**Data Schema Tracker** holder deg oppdatert på hvordan databasestrukturene dine utvikler seg.  
Den overvåker kontinuerlig **tabellskjemaer, kolonner og datatyper** for å oppdage **schema drift** — tilsiktede eller utilsiktede strukturelle endringer som kan forstyrre pipelines, ETL-jobber eller BI-dashbord.

Ved å sikre åpenhet om skjemaenes utvikling hjelper digna organisasjoner med å opprettholde **tillit til datakvaliteten**, ivareta **observability av datasystemer** og unngå kostbare produksjonshendelser forårsaket av uoppdagede skjemaendringer.

---

## Teknisk oversikt

### Hva den overvåker

- **Tilføyde eller fjernede kolonner** – Oppdager nye, omdøpte eller slettede kolonner.  
- **Endringer i datatyper** – Identifiserer endringer som `INT → VARCHAR` eller `DATE → TIMESTAMP`.  
- **Endringer i tabeller og visninger** – Sporer oppretting, omdøping eller fjerning av tabeller og visninger.  
- **Forskjeller mellom miljøer** – Sammenligner skjemaversjoner mellom Dev-, Test- og produksjonsmiljøer.  

### Deteksjon og varsling

- Skanner **databasemetadata** eller **systemkataloger** direkte i dataplattformen din.  
- Sammenligner hvert skjemaøyeblikksbilde med den forrige kjente versjonen som er lagret i dignas observability-skjema.  
- Genererer **sanntidsvarsler** i dashbordet, via API eller eksterne varslingskanaler (e-post, Slack, webhook).  
- Logger hver skjemaversjon for **historisk sporing og revisjonsberedskap**.

---

## Arkitektur og kjøring

- **Kjøring i databasen:** digna kjører helt innenfor ditt miljø og spør mot metadatavisninger uten å hente ut data.  
- **Lett skanning:** får kun tilgang til strukturell informasjon — aldri brukerdata.  
- **Sentralisert lagring:** skjemametadata og drift-hendelser lagres i dignas observability-skjema for visualisering og analyse.  
- **Automatisering:** støtter planlagte eller hendelsesbaserte skanninger via digna Core eller eksterne orkestreringsverktøy.  

---

## Brukseksempler

| Brukstilfelle | Beskrivelse |
|-----------|--------------|
| **Overvåking av ETL-stabilitet** | Oppdag strukturendringer oppstrøms før pipelines feiler på grunn av skjemaavvik. |
| **Pålitelig Business Intelligence** | Forhindre ødelagte dashbord forårsaket av omdøpte eller manglende kolonner. |
| **Styring av datavarehus** | Oppretthold en reviderbar historikk over skjemaenes utvikling for etterlevelse og konsekvensanalyse. |
| **Oversikt over integrasjoner** | Sørg for at skjemaer i data lake og datavarehus forblir synkroniserte etter strukturelle oppdateringer. |

---

## Verdi

| Område | Fordel |
|------|----------|
| **Datakvalitet** | Forhindrer uoppdaget schema drift som kan ødelegge eller ugyldiggjøre datapipelines. |
| **Observability** | Legger strukturell overvåking til den samlede observability av dataøkosystemer. |
| **Etterlevelse** | Opprettholder versjonert skjemahistorikk for revisjon, sporbarhet og endringskontroll. |
| **Forebygging** | Oppdager strukturelle problemer før de forplanter seg til rapporterings- eller produksjonsfeil. |

---

## Slik fungerer det

1. **Innsamling av øyeblikksbilde** – digna fanger opp gjeldende skjemametadata.  
2. **Sammenligning** – det nye øyeblikksbildet sammenlignes