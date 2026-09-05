# Data Anomalies – Automatisk detektion
<h1 style="display:none;">AI-drevet modul for datakvalitet og observabilitet – digna Data Anomalies</h1>

---

## Formål

Modulet **Data Anomalies** identificerer automatisk uregelmæssigheder i dine datasæt — ingen regelskrivning nødvendig.  
Det overvåger kontinuerligt **kvaliteten af dataleverancerne**, lærer hvad der er “normalt” og opdager afvigelser i realtid.

Ved at bruge AI-baseret detektion genkender digna *stille datafejl* såsom manglende, duplikerede eller korrupte poster, der kan forvrænge rapporter, ML-modeller og dashboards.

---

## Teknisk overblik

### Analyserede målepunkter

digna profilerer løbende følgende aspekter af dine data:

- **Antal rækker** – totalt antal rækker, dagligt eller batch-baseret  
- **Manglende værdier** – detektion af null- eller tomme felter  
- **Fordelinger og histogrammer** – overvågning af ændringer i dataværdiernes form  
- **Værdiernes interval** – automatisk identifikation af værdier uden for forventet område eller ekstreme værdier  
- **Unikhed** – kontrol for duplikerede nøgler eller gentagne poster  

### Intelligent anomalidetektion

- Anvender **historisk læring** til dynamisk at definere forventede grænser  
- Opdager afvigelser i **volumen, værdifordelinger eller logiske sammenhænge**  
- Bruger AI til automatisk at tilpasse tærskler baseret på tidspunkt på dagen eller sæsonmønstre  
- Skelner mellem **statistiske udsving** og reelle anomalier  
- Producerer detaljerede målepunkter og konfidensscores pr. datasæt og kolonne  

---

## Detektionsscenarier

Nedenfor er eksempler på virkelige problemer, der automatisk fanges af modulet **Data Anomalies**:

| Scenarie | Beskrivelse |
|-----------|--------------|
| **Volumenfald eller -spidser** | Manglende halvdelen af daglige transaktioner, duplikerede batchindlæsninger eller pludselige datastigninger |
| **Manglende eller null-værdier** | Dataudtræk gennemført, men kritiske kolonner står tomme |
| **Distribution ændringer** | Gennemsnitligt købebeløb eller transaktionsantal pr. region ændrer sig uventet |
| **Kolonnebytte** | Kolonner som *first_name* og *last_name* bliver ved et uheld byttet under ETL |
| **Uventede kategoriske værdier** | f.eks. “Zurich” dukker op under en liste over østrigske byer |
| **Pludseligt tab af unikhed** | Tidligere unikke ID'er begynder at duplikere på grund af upstream join-fejl |

---

## Arkitektur og eksekvering

- **Kørsel i databasen:** Al anomalidetektionslogik eksekveres *i database-motoren* (Teradata, Snowflake, Databricks, PostgreSQL osv.)  
- **Ingen dataflytning:** digna læser kun målepunkter, overfører aldrig rådata eksternt  
- **Inkrementelle opdateringer:** Kun nye datasegmenter analyseres hver kørsel for effektivitet  
- **Konfigurerbar inspektionsfrekvens:** Time-, dags- eller trigger-baseret af upstream-processer  
- **Resultatlagring:** Målepunkter og anomaliflag skrives tilbage til dignas observability-schema til visualisering og alarmering  

---

## Fordele

| Område | Fordel |
|------|----------|
| **Automatisering** | Eliminering af hundredevis af manuelle SQL- eller regeldefinitioner |
| **Præcision** | Opfanger problemer, som statiske tærskler ofte overser |
| **Skalerbarhed** | Overvåger millioner af poster pr. tabel effektivt |
| **Integration** | Arbejder problemfrit sammen med *Data Analytics* for trendanalyse |
| **Compliance** | Sikrer kontinuerlig kontrol over **kvaliteten og observabiliteten af data** |
| **Transparens** | Leverer konfidensscores, tidsstempler og årsagskoder for hver anomali |

---

## Hvordan digna lærer “normalt”

1. **Profileringsfase:** digna indsamler målepunkter fra historiske datasæt.  
2. **Læringsfase:** AI-modeller identificerer tilbagevendende mønstre (sæson-, uge-, dagmønstre).  
3. **Overvågningsfase:** Fremtidige datasæt sammenlignes med dynamisk lærte tærskler.  
4. **Alarmeringsfase:** Afvigelser ud over statistiske konfidensgrænser rapporteres som anomalier.  

Alle modeller er forklarlige, deterministiske og optimerede til virksomheders datavolumener.

---

## Eksempler på anvendelsestilfælde

- Overvågning af datakvalitet i **banktransaktionssystemer**  
- Detektion af fejl i indlæsning i **ETL eller datalagerjob**  
- Identifikation af unormal kundeadfærd i **telekommunikationsdata**  
- Overvågning af klinisk datakonsistens i **sundhedsanalytiske pipelines**  
- Forebyggelse af ødelagte dashboards i **BI- og rapporteringsmiljøer**

---

## Ofte stillede spørgsmål

**Kræver Data Anomalies foruddefinerede regler?**  
Nej — modulet lærer automatisk ud fra dataadfærden.

**Kan jeg stadig definere specifikke tærskler, hvis det er nødvendigt?**  
Ja. digna tillader kombination af AI-baseret og regelbaseret detektion (via *Data Validation*).

**Hvordan minimeres falske positiver?**  
Modulet bruger adaptiv læring og statistisk konfidensscoring til at ignorere normale sæsonvariationer.

**Hvor foregår beregningerne?**  
Al behandling køres i din database — digna udtrækker aldrig rådata.

**Er det egnet til følsomme eller regulerede data?**  
Ja. digna kan køre fuldt **on-premises eller i privat cloud** og overholder europæiske compliance-standarder.

---