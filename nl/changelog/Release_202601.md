# Changelog – Release 2026.01  

Met Release 2026.01 introduceert digna belangrijke verbeteringen in datasourcemodellering, connectiebeheer en inspectiebruikbaarheid.  
Deze release vergroot de flexibiliteit in alle modules en breidt de dekking voor **gegevenskwaliteit en validatie** aanzienlijk uit.

---

## Nieuwe functies  

### Globale databaseverbindingen  
- Databaseverbindingen worden nu op **globaal niveau** geconfigureerd.  
- Globale verbindingen kunnen hergebruikt worden in **alle projecten**, wat configuratie en onderhoud vereenvoudigt.  
- **Impact:** Vermindert operationele overhead en zorgt voor consistente connectiviteit over omgevingen heen.

### Meerdere bronverbindingen per project  
- Projecten kunnen nu verwijzen naar **meerdere bronverbindingconfiguraties**.  
- Maakt flexibelere opstellingen mogelijk voor complexe datalandschappen per project.  
- **Impact:** Ondersteunt realistische enterprise-architecturen met heterogene databronnen.

### Logische datasources  
- Datasources vertegenwoordigen nu een **logische laag** binnen een project.  
- Elke datasource kan ondersteund worden door:
    - een **databasetabel**
    - een **databaseview**
    - een **aangepaste SQL-query**  
- Deze scheiding bevordert hergebruik, duidelijkheid en inspectiemodellering over modules heen.  
- **Impact:** Ontkoppelt inspecties en regels voor gegevenskwaliteit van fysieke opslag, wat onderhoudbaarheid en hergebruik verbetert.

### Anomaly Relevance Condition  
- Een **Anomaly Relevance Condition** kan nu worden gedefinieerd om de evaluatie van anomalie-status op datasetniveau te sturen.  
- Statistieken worden onafhankelijk berekend van of de voorwaarde is ingesteld of voldaan.  
- Als de voorwaarde **niet is voldaan**, geeft **digna Data Anomalies** geen anomalie-status (groen / geel / rood).  
- **Voorbeeld:** Sluit de dataset uit van anomalie-evaluatie wanneer het aantal records minder is dan 10.
- **Impact:** Zorgt ervoor dat anomalieën alleen geëvalueerd worden in relevante zakelijke contexten.

### Per-module notificatieconfiguratie  
- Notificaties kunnen nu **per module** rechtstreeks in digna worden geconfigureerd.  
- Biedt onafhankelijke controle over het waarschuwingsgedrag voor **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** en andere modules.  
- **Impact:** Maakt precieze alertingstrategieën mogelijk die aansluiten bij teamverantwoordelijkheden en criticaliteit.

### Inspectieresultaten exporteren (CSV)  
- Gebruikers kunnen nu **inspectieresultaten downloaden als CSV-bestanden**.  
- Maakt offline analyse, rapportage en integratie met externe tools mogelijk.  
- **Impact:** Vereenvoudigt audits, rapportage en downstream data quality-analyse.

---

## Uitgebreide mogelijkheden voor gegevensvalidatie  

Met deze release ondersteunt **digna Data Validation** nu een uitgebreide set regels voor gegevenskwaliteit:

- **Validatieregels op rijniveau**  
- **Uniciteitscontroles over meerdere kolommen**  
- **Validatie van referentiële integriteit tussen datasources**

Samen stellen deze controles in staat om **structurele en relationele regels voor gegevenskwaliteit** af te dwingen in complexe datalandschappen.

### Uniciteitscontroles voor meerdere kolommen
- Geïntroduceerd: **Uniciteitscontroles** voor een configureerbare **set kolommen**.  
- Maakt validatie van samengestelde sleutels en zakelijke uniciteitsbeperkingen mogelijk.  
- **Impact:** Detecteert dubbele zakelijke entiteiten die niet met enkelkolomcontroles te identificeren zijn.

### Referentiële integriteitscontroles
- Geïntroduceerd: **Referentiële integriteitscontroles** om relaties tussen datasources te valideren.  
- Zorgt ervoor dat **foreign key-waarden** in een brondatasource bestaan in een verwijzende doeldatasource.  
- Helpt bij het vroegtijdig detecteren van verweesde records, gebroken relaties en inconsistenties in gegevens.  
- Ontworpen om te werken met **logische datasources**, inclusief views en aangepaste SQL.  
- **Use cases:** datawarehouse-integriteit, wettelijke rapportage, masterdataconsistentie en betrouwbare downstream-analytics.

---

## Wie profiteert van deze release  

- **Data Engineers:** Flexibeler datasourcemodellering en herbruikbare databaseverbindingen  
- **Teams voor gegevenskwaliteit & governance:** Uitgebreide validatiedekking inclusief relationele integriteitsregels  
- **Analytics- & BI-teams:** Schonere inputs en exporteerbare inspectieresultaten  
- **Platformeigenaren:** Minder configuratiecomplexiteit en verbeterde operationele onderhoudbaarheid

---

## CLI-updates  
- Geen wijzigingen

---