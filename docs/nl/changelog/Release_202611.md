---
title: digna Release 2026.11 | Data Reconciliation, digna Agentic & digna Engine
description: Lees wat er nieuw is in digna Release 2026.11. Deze versie introduceert drie grote toevoegingen - digna Data Reconciliation, digna Agentic met de digna MCP Server, en de digna Engine, die controles op referentiële integriteit tussen verschillende databasetechnologieën mogelijk maakt.
keywords: digna Release 2026.11, digna-wijzigingslog, digna Data Reconciliation, datareconciliatie, ETL-validatie, reconciliatie van bron naar doel, digna Agentic, digna MCP Server, AI-agents datakwaliteit, digna Engine, referentiële integriteit tussen verbindingen, query-attributen, data profiling, data observability
image: /assets/logo_square.png
---

# Wijzigingslog – Release 2026.11  

Release 2026.11 draait om drie grote toevoegingen:

- **digna Data Reconciliation**: controleert of data consistent blijft terwijl deze tussen systemen wordt verplaatst  
- **digna Agentic**: stelt digna open voor AI-agents via de digna MCP Server  
- **digna Engine**: profileert data optioneel binnen digna en maakt controles op referentiële integriteit tussen verschillende databasetechnologieën mogelijk  

---

## Nieuwe functies  

### digna Data Reconciliation (Beta) – Consistentie van bron naar doel  
Data passeert vaak meerdere systemen voordat het in een rapport terechtkomt. digna Data Reconciliation vergelijkt een **doel**-datasource met de **bronnen** waaruit deze is opgebouwd, en waarschuwt wanneer ze niet langer overeenkomen.

- Geconfigureerd als benoemde regels op het nieuwe tabblad **Data Reconciliation** van de doel-datasource  
- Elke datasource van het project waarvoor Data Reconciliation is ingeschakeld, kan als bron dienen  
- Toepassingen zijn onder meer standaard reconciliatieprocedures en het valideren van de resultaten van ETL-processen  
- Twee soorten regels: **Exact** en **AI**  

**Exact-regels – Reconciliatie als datakwaliteitsregel**: u definieert precies wat er tussen één bron en één doel moet overeenkomen, net als bij een datakwaliteitsregel.

  - Vergelijk één bron-datasource met één doel-datasource  
  - Koppel een controle op het doel aan een controle op de bron via statistiek en attribuut, bijv. aantallen rijen of de som van een bedragkolom  
  - Sta een verschil toe met een **absolute** tolerantie (bijv. ± 10) of een **relative** tolerantie (bijv. ± 0,5 % van de bron)  
  - De tijdlijn toont het verschil van elke dag ten opzichte van de tolerantie  

**AI-regels – Reconciliatie als data observability**: digna leert hoe een doel zijn bronnen volgt, op dezelfde manier waarop digna data in andere modules observeert, en waarschuwt wanneer die relatie verbroken wordt.

  - Combineer controles van meerdere bron-datasources met de controles van één doel  
  - De logica ertussen (joins, filters, aggregaties) hoeft u niet te kennen of uit te schrijven  
  - Een model leert uit de historie hoe het doel zijn bronnen op dezelfde dag volgt  
  - Elke controle op het doel wordt voorspeld op basis van de bronwaarden van die dag, en digna waarschuwt wanneer het doel buiten de band van de eigen eerdere fouten van de regel valt  
  - Elke regel heeft zijn eigen **Model settings**: **Sensitivity**, **Memory** en **Model Complexity**  

Reconciliatiecontroles verschijnen op het dashboard met een tijdlijn per regel. Ze tellen mee voor de algehele inspectiestatus en activeren meldingen.

**Impact:** Dekt beide kanten van reconciliatie af. Exact-regels handhaven bekende controles tussen bron en doel, en AI-regels bewaken complexe stromen zoals ETL-processen, zodat data die onderweg verloren gaat of verandert wordt opgemerkt zonder handgeschreven reconciliatie-SQL.

---

### digna Agentic (Beta) – digna voor AI-agents  
De eerste versie van digna Agentic. AI-agents kunnen nu met digna werken, zakelijke vragen over uw data beantwoorden en helpen uw configuratie te verbeteren.

**digna MCP Server**: laat Claude en andere AI-agents met digna werken via het Model Context Protocol.

  - Beheer projecten, datasources, regels, inspectieschema's en abonnementen  
  - Lees inspectiestatussen tot op het niveau van de afzonderlijke controle, om alerts te onderzoeken  

**Beschrijvingen bij datasources en attributen**: beschrijf in gewone taal wat een datasource of attribuut bevat.

  - AI-agents gebruiken de beschrijvingen om uw data te interpreteren  
  - Stel zakelijke vragen over uw data, en AI-agents beantwoorden ze op basis van wat digna monitort  
  - Als de huidige configuratie van digna een vraag niet kan beantwoorden, stelt de AI-agent waar mogelijk wijzigingen aan de datasource en zijn attributen voor, bijv. het toevoegen van een nieuwe dataset  

**Impact:** Hiermee stelt u zakelijke vragen over uw data in gewone taal, en helpen AI-agents digna te configureren en datakwaliteitsproblemen te onderzoeken.

---

### digna Engine – Profileer waar u wilt  
Standaard profileert digna data waar deze zich bevindt: in de brondatabase. De digna Engine voegt een optie toe: digna exporteert de data uit de bron en profileert deze binnen de digna Engine.

- Optioneel, niet verplicht: profiling in de brondatabase blijft beschikbaar  
- Per databaseverbinding gekozen als **profileringslocatie**: **Source Database** of **digna Engine**  
- Beschikbaar voor elke ondersteunde brontechnologie  

**Referentiële integriteit tussen verbindingen**: sommige controles vereisen dat data wordt geëxporteerd. Voor deze gevallen breidt de digna Engine **digna Data Validation** uit.

  - **Controles op referentiële integriteit** tussen datasources op **verschillende databaseverbindingen**, ook bij verschillende databasetechnologieën (bijv. Oracle en PostgreSQL)  
  - Werkt met beide profileringslocaties: bij Source Database worden alleen de sleutelkolommen naar de digna Engine geëxporteerd  
  - Het dashboard toont wanneer een controle over twee verbindingen loopt  

**Impact:** Hiermee kiest u waar data wordt geprofileerd, en worden relaties afgedwongen tussen systemen die op verschillende databasetechnologieën draaien.

---

## Verbeteringen in profiling  

Deze release geeft gebruikers ook meer controle over wat er wordt geprofileerd en hoe.

### Query-attributen – Door de gebruiker gedefinieerde kolommen  
- Definieer kunstmatige kolommen: een SQL-expressie over een of meer kolommen van de datasource  
- Elk query-attribuut heeft een eigen naam  
- Wordt geprofileerd en gecontroleerd zoals elk ander attribuut  

### Kolomcategorie DATE  
- Nieuwe categorie **Date** voor attributen  
- Metrieken ten opzichte van de geïnspecteerde datum  

### Profiling op aanvraag  
- Profileer elk attribuut op basis van de volledige momentopname van één datum, zonder een inspectie uit te voeren  
- Helpt bij het instellen van het kolomtype van het attribuut: **Numerical**, **Categorical**, **Date** of **Unspecified**  

---

## Wie profiteert van deze release  

- **Data Engineers:** validatie van ETL-resultaten met digna Data Reconciliation  
- **Finance-, risk- en controllingteams:** standaard reconciliatieprocedures als Exact-regels in digna Data Reconciliation  
- **Datakwaliteit- en Data Governance-teams:** referentiële integriteit over databasetechnologieën heen met de digna Engine  
- **Zakelijke gebruikers:** zakelijke vragen over data beantwoord door AI-agents met digna Agentic  
- **AI- en automatiseringsteams:** AI-agents die met digna werken via digna Agentic  

---

## CLI-updates  
- Geen wijzigingen  

---
