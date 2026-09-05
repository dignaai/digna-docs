# Data Timeliness – On-Time Delivery Monitoring
<h1 style="display:none;">AI-gestuurde Data Timeliness-module voor Data Quality en observability – digna</h1>

---

## Doel

De **Data Timeliness**-module zorgt ervoor dat **data op tijd aankomt** — elke keer.  
Het bewaakt continu leveringsschema's en detecteert automatisch wanneer datasets, tabellen of bestanden **vertraagd, ontbreken of onvolledig** zijn.  

Door AI-leren te combineren met door gebruikers gedefinieerde schema's, stelt *digna* organisaties in staat om downstream fouten te voorkomen en strikte **SLA (Service Level Agreement)**-doelstellingen voor zowel **Data Quality** als **observability van datapijplijnen** te handhaven.

---

## Technisch overzicht

### Twee monitoringmodi
- **AI-geleerde aankomstpatronen**  
  digna leert automatisch het natuurlijke ritme van uw dataleveringen — dagelijks, elk uur of event-driven — door historische tijdstempels en voltooiingstijden te analyseren.  
  Het past zich aan veranderingen in bedrijfsagenda's, weekenden of pieken aan het einde van de maand aan.

- **Door gebruiker gedefinieerde schema's**  
  Gebruikers kunnen verwachte levertijden expliciet definiëren (bijv. *elke werkdag voor 07:30*).  
  digna vergelijkt de feitelijke aankomsttijd met het geplande schema en geeft waarschuwingen wanneer data te laat of afwezig is.

### Detectiemechanisme
- Evalueert **metadata-tijdstempels**, **aantal records** en **table freshness**  
- Detecteert **gestopte ETL-jobs**, **mislukte extracties** en **gedeeltelijke bestandsaankomsten**  
- Integreert met *Data Anomalies* en *Data Validation* voor gecombineerde inzichten

---

## Detectiescenario's

| Scenario | Beschrijving |
|-----------|--------------|
| **Late data arrival** | Dagelijkse marktdatafeed twee uur vertraagd, waardoor rapporten SLA's missen |
| **Missing load** | Een geplande tabel of partitie is niet bijgewerkt voor de huidige datum |
| **Chained dependency delay** | Vertraging in een upstream job beïnvloedt de refresh van downstream pipelines |
| **Weekend pattern shift** | AI-model past zich automatisch aan wanneer er op zondagen geen data wordt verwacht |

---

## Architectuur en uitvoering

- **In-database uitvoering:** digna voert timeliness-checks rechtstreeks in uw database of datawarehouse uit.  
- **Lichte metadata-toegang:** leest jobtijdstempels, recordaantallen en partitie-informatie — geen data-extractie vereist.  
- **Configureerbare frequentie:** plan monitoring per dataset, schema of pipeline.  
- **Cross-module waarschuwingen:** resultaten kunnen visuele waarschuwingen triggeren in *Inspection Hub* of notificaties via e-mail, Slack of API.  

---

## Voorbeelden van gebruik

- **Financiële marktfeeds:** detecteer vertragingen in prijs- of handelsdata-updates.  
- **Data Warehouse Loads:** bewaak wanneer nachtelijke ETL-jobs later dan verwacht klaar zijn.  
- **Data-uitwisseling tussen teams:** zorg dat departementale data-leveringen plaatsvinden vóór dagelijkse deadlines.  
- **Regelgevende rapportage:** bevestig dat inzendingen de meest recente beschikbare datasnapshot bevatten.  

---

## Voordelen

| Gebied | Voordeel |
|------|----------|
| **Business Continuity** | Voorkomt operationele verstoringen door vertraagde of ontbrekende data |
| **Data Quality** | Verbetert betrouwbaarheid en consistentie van datapijplijnen |
| **Compliance** | Zorgt voor naleving van SLA's en audittransparantie |
| **Automation** | AI elimineert handmatige schema-tracking |
| **Integration** | Werkt naadloos samen met *Data Analytics* om timeliness-trends in de tijd te visualiseren |

---

## Hoe digna verwachte levertijden leert

1. **Historische analyse:** digna observeert eerdere laadtijden en duur.  
2. **AI-modellering:** machine learning creëert een dynamische baseline voor verwachte aankomst.  
3. **Monitoring:** elke nieuwe levering wordt vergeleken met de baseline.  
4. **Alerting:** afwijkingen triggeren meldingen met contextuele metrics en confidence-scores.  

Deze continue leerbenadering past zich aan evoluerende processen aan en houdt false positives laag.

---

## Veelgestelde vragen

**Kan ik mijn eigen levertijden definiëren?**  
Ja. digna ondersteunt zowel vaste door gebruikers ingestelde schema's als AI-geleerde patronen.

**Kan het integreren met mijn ETL- of orchestratie-tool?**  
Ja. digna integreert met tools zoals Airflow, dbt, Informatica of custom schedulers.

**Waar vindt de berekening plaats?**  
Alle analyses draaien binnen uw database of cloud warehouse — er wordt geen externe service gebruikt.

**Wat gebeurt er wanneer data te laat is?**  
digna geeft waarschuwingen in het dashboard, Inspection Hub en via API/webhooks om operationele teams direct te informeren.

---


**digna Data Timeliness** helpt vertrouwen in data te waarborgen door **AI-gedreven detectie**, **on-premises uitvoering** en **data observability** te combineren — allemaal binnen uw gecontroleerde omgeving.