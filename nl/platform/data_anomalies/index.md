# digna Data Anomalies – AI-gebaseerde detectie van datakwaliteitsproblemen

**AI-gestuurde observability voor altijd beschikbare datavertrouwen**

digna Data Anomalies is onderdeel van de **digna Data Observability Platform** — een modulaire oplossing die de **kwaliteit van data** verbetert door continu te analyseren hoe datasets zich in de tijd gedragen.

Het leert automatisch wat “normaal” is voor je data en waarschuwt wanneer het gedrag verandert — zonder statische drempels te definiëren of één enkele regel te schrijven.  
De module draait rechtstreeks binnen je database, zodat data nooit je omgeving verlaat.

---

## Doel van digna Data Anomalies

De **digna Data Anomalies**-module biedt continue **observability van data** door vooraf gedefinieerde statistische metrics te berekenen en bij te houden, zoals:

- Datavolume en recordaantallen  
- Verhoudingen ontbrekende waarden  
- Waardedistributies en histogrammen  
- Numerieke bereikwaarden en gemiddelden  
- Kolom-uniciteit en tekstlengte  

Deze metrics worden automatisch verzameld voor elke dataset.  
Op basis hiervan bouwt digna modellen die het typische gedrag van elke metric representeren — waarbij dagelijkse, wekelijkse of seizoensgebonden patronen worden geleerd.  
Eenmaal getraind voorspelt de module verwachte waarden voor nieuwe data en detecteert afwijkingen die kunnen wijzen op kwaliteitsproblemen, procesfouten of upstream-wijzigingen.

---

## Belangrijkste mogelijkheden

- Leert automatisch het verwachte datagedrag met AI — geen configuratie van drempels.  
- Detecteert plotselinge dalingen, pieken of drift in datavolumes en distributies.  
- Identificeert gewisselde kolommen of foutieve mappings tussen attributen.  
- Markeert onverwachte categorische waarden (bijv. nieuwe regio’s of codes).  
- Ondersteunt alle kolomtypes: numeriek, categorisch of niet-gespecificeerd.  
- Werkt volledig binnen de klantomgeving — geen databeweging.  
- Integreert met **digna Data Analytics** voor langetermijntrendanalyses.

---

## Hoe het werkt

### Stap 1 – Metricberekening
digna berekent een set profielmetrics voor elke tabel en kolom.  
Deze metrics beschrijven de structuur en het statistische gedrag van je data en worden opgeslagen voor verdere analyse.

### Stap 2 – Modeltraining
Op basis van historische metricwaarden traint digna compacte machine-learningmodellen (signature models) die het normale bereik van elke metric vastleggen.

### Stap 3 – Automatische drempelbepaling
Met behulp van *conformal inference* berekent digna adaptieve betrouwbaarheidsintervallen (auto-thresholds) die met je data mee-evolueren.  
Als nieuwe metricwaarden buiten het voorspelde bereik vallen, worden ze als anomalieën gemarkeerd.

Deze continue feedbackloop zorgt ervoor dat de monitoring relevant blijft, zelfs wanneer datavolumes of patronen van nature veranderen.

---

## Voorbeeldscenario’s

### Onverwachte daling in recordvolume
Een dataset bevat doorgaans rond de 500.000 records per dag.  
Als een nieuwe levering slechts 50.000 records bevat, markeert digna dit als een anomalie en toont hoe ver de waarde afwijkt van het geleerde bereik.

### Gewisselde kolommen gedetecteerd
De gemiddelde stringlengte van `last_name` komt plots overeen met die van `first_name`.  
digna herkent de afwijking in metricpatronen en signaleert een mogelijke kolomwissel.

### Onverwachte categorie gedetecteerd
Een kolom met Oostenrijkse steden bevat plots “Zurich”.  
Op basis van historische distributies markeert digna de nieuwe waarde als onverwacht en waarschuwt de gebruiker.

---

## Integratie met andere modules

- **digna Data Analytics** — aggregeert anomaliegeschiedenis en volatiliteitsmetrics om langetermijntrends zichtbaar te maken.  
- **digna Data Validation** — handhaaft expliciete businessregels voor deterministische kwaliteitscontroles.  
- **digna Data Timeliness** — monitort aankomsttijden van data en correleert vertragingen met anomaliegebeurtenissen.  
- **digna Data Schema Tracker** — detecteert structurele wijzigingen die nieuwe anomalieën kunnen verklaren.

---

## Typische use cases

- Detecteren van ontbrekende of dubbele dataloads.  
- Identificeren van gewisselde of afgeknotte kolommen.  
- Detecteren van distributiedrift in numerieke of categorische kenmerken.  
- Vinden van onverwachte referentiewaarden of codes.  
- Monitoren van continue ingest-pijplijnen op afwijkingen.  
- Bijhouden van de algehele **kwaliteit en observability van data** over domeinen heen.

---

## Voordelen

- Directe detectie van abnormaal datagedrag.  
- Elimineren van handmatige drempelafstemming.  
- Vermindert operationele inspanning in grote dataomgevingen.  
- Vergroot vertrouwen in analytics- en rapportagesystemen.  
- Versterkt de **kwaliteit van data** en end-to-end **data observability**.

---

## Gerelateerde digna Modules

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — trend- en volatiliteitsmetrics.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — regelgebaseerde dataverificatie.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — monitoring van data-levertijden.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — detectie van schemawijzigingen.

---

## Samenvatting

De **digna Data Anomalies**-module vormt het hart van digna’s AI-gedreven **Data Observability Platform**.  
Door continu sleutelmetrics te monitoren, patronen te leren en afwijkingen te identificeren, helpt het organisaties ervoor te zorgen dat de **kwaliteit van data** betrouwbaar, stabiel en verklaarbaar blijft — zonder handmatige configuratie.