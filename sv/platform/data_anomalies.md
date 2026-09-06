# digna Data Anomalies – AI-baserad upptäckt av problem med datakvalitet

**AI-driven observabilitet för konstant datatillit**

digna Data Anomalies är en del av **digna Data Observability Platform** — en modulär lösning som förbättrar **datakvaliteten** genom att kontinuerligt analysera hur dataset beter sig över tid.

Den lär sig automatiskt hur "normalt" ser ut för dina data och varnar när beteendet förändras — utan att du behöver definiera statiska tröskelvärden eller skriva en enda regel.  
Modulen körs direkt i din databas, så data lämnar aldrig din miljö.

---

## Syftet med digna Data Anomalies

Modulen **digna Data Anomalies** tillhandahåller kontinuerlig **observabilitet av data** genom att beräkna och spåra fördefinierade statistiska mått såsom:

- Datavolymer och antal poster  
- Andel saknade värden  
- Värdefördelningar och histogram  
- Numeriska intervall och medelvärden  
- Kolumnunikhet och textlängd  

Dessa mått samlas automatiskt in för varje dataset.  
Med hjälp av dem bygger digna modeller som representerar det typiska beteendet för varje mått — och lär sig dagliga, veckovisa eller säsongsmässiga mönster.  
När modellerna är tränade predicerar modulen förväntade värden för ny data och identifierar avvikelser som kan tyda på kvalitetsproblem, processfel eller förändringar uppströms.

---

## Nyckelfunktioner

- Lär sig förväntat databetende automatiskt med AI — ingen konfiguration av tröskelvärden.  
- Upptäcker plötsliga fall, toppar eller drift i datavolymer och fördelningar.  
- Identifierar utbytta kolumner eller felaktiga mappningar mellan attribut.  
- Markerar oväntade kategorivärden (t.ex. nya regioner eller koder).  
- Stöder alla kolumntyper: numeriska, kategoriska eller ospecificerade.  
- Körs helt i kundens miljö — ingen dataflytt.  
- Integreras med **digna Data Analytics** för långsiktig trendanalys.

---

## Hur det fungerar

### Steg 1 – Beräkning av mått
digna beräknar en uppsättning profilmått för varje tabell och kolumn.  
Dessa mått beskriver strukturen och det statistiska beteendet i dina data och sparas för vidare analys.

### Steg 2 – Modellträning
Baserat på historiska måttvärden tränar digna kompakta maskininlärningsmodeller (signaturmodeller) som fångar det normala intervallet för varje mått.

### Steg 3 – Automatisk tröskelsättning
Genom att använda *conformal inference* beräknar digna adaptiva konfidensintervall (auto-trösklar) som utvecklas tillsammans med dina data.  
Om nya måttvärden faller utanför det predicerade intervallet markeras de som avvikelser.

Denna kontinuerliga feedback-loop säkerställer att övervakningen förblir relevant även när datavolymer eller mönster naturligt förändras.

---

## Exempelscenarier

### Ovårdad minskning i postvolym
Ett dataset innehåller vanligtvis omkring 500 000 poster per dag.  
När en ny leverans endast innehåller 50 000 poster flaggar digna en avvikelse och visar hur långt värdet avviker från sitt inlärda intervall.

### Upptäckt av utbytta kolumner
Medellängden på strängar i `last_name` matchar plötsligt den i `first_name`.  
digna upptäcker avvikelsen i måttmönstren och indikerar en möjlig kolumnväxling.

### Oväntrad kategori upptäckt
En kolumn som listar österrikiska städer innehåller plötsligt "Zurich".  
Basera på historiska fördelningar markerar digna det nya värdet som oväntat och varnar användaren.

---

## Integration med andra moduler

- **digna Data Analytics** — aggregerar anomhistorik och volatilitetsmått för att avslöja långsiktiga trender.  
- **digna Data Validation** — upprätthåller explicita affärsregler för deterministiska kvalitetskontroller.  
- **digna Data Timeliness** — övervakar ankomsttider för data och korrelerar förseningar med förekomster av anomalier.  
- **digna Data Schema Tracker** — upptäcker strukturella förändringar som kan förklara nya anomalier.

---

## Typiska användningsfall

- Upptäckt av saknade eller dubbla dataladdningar.  
- Identifiering av utbytta eller trunkerade kolumner.  
- Upptäckt av drift i fördelningar för numeriska eller kategoriska variabler.  
- Hittande av oväntade referensvärden eller koder.  
- Övervakning av kontinuerliga ingestpipelines för avvikelser.  
- Spårning av den övergripande **kvaliteten och observabiliteten av data** över domäner.

---

## Fördelar

- Omedelbar upptäckt av onormalt databetende.  
- Eliminerar manuell justering av tröskelvärden.  
- Minskar driftinsatsen för stora datamiljöer.  
- Ökar förtroendet för analys- och rapportsystem.  
- Stärker **datakvaliteten** och end-to-end **dataobservability**.

---

## Relaterade digna-moduler

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — trend- och volatilitetsmått.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — regelbaserad dataverifiering.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — övervakning av dataleveransscheman.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — upptäckt av schemafӧrändringar.

---

## Sammanfattning

Modulen **digna Data Anomalies** utgör kärnan i dignas AI-drivna **Data Observability Platform**.  
Genom att kontinuerligt övervaka nyckelmått, lära mönster och identifiera avvikelser hjälper den organisationer att säkerställa att **datakvaliteten** förblir pålitlig, stabil och förklarbar — utan manuell konfiguration.