# Wijzigingslog – Release 2026.06  

Met Release 2026.06 zet digna een grote stap vooruit op het gebied van automatisering, uitbreidbaarheid en platformbruikbaarheid.  
Deze release introduceert de nieuwe **digna Python SDK**, officiële **Docker-implementatieondersteuning**, een vernieuwde dashboardervaring en verbeterde draagbaarheid voor het beheer van validatieregels.

---

## Bekijk de release

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — een rondleiding door deze release op het YouTube-kanaal van digna.*

---

## Nieuwe functies  

### digna Python SDK – Automatiseer alles met Python  
- Installatie via:
  ```bash
  pip install digna-sdk
  ```
- Programmeerbaar beheer en automatisering van digna met Python  
- Maak projecten aan en configureer ze via code  
- Trigger inspecties en monitoring-executies  
- Beheer datasets, regels en configuraties programmeerbaar  
- Profileer tabellen en extraheer metadata-inzichten  
- Exporteer profiling- en datakwaliteitsresultaten naar externe repositories en systemen  
- Integreer met notebooks, orchestration tools en CI/CD-pijplijnen  

**Impact:** Maakt volledig infrastructure-as-code mogelijk en biedt diepe automatisering van datakwaliteits- en observability-workflows met Python.

---

### Docker-ondersteuning – Vereenvoudigde deployment & operatie  
- Officiële Docker-image-ondersteuning voor digna  
- Snelle en consistente setup in verschillende omgevingen  
- Vereenvoudigde onboarding voor development, test en productie  
- Eenvoudige integratie met Kubernetes en containerplatforms  
- Verbeterde draagbaarheid en reproduceerbaarheid van deployments  

**Impact:** Maakt digna eenvoudiger te deployen en te beheren in moderne cloud-native architecturen.

---

### QueryMode – Flexibele SQL-uitvoeringsstrategie

Stel de query-uitvoeringsstrategie in: **Single** of **Combined** modus

**Single Mode**: Elke statistiek wordt berekend met één dedicated SQL-query

  - Ideaal voor grote datasources waar geheugenbeperkingen een rol spelen
  - Voorkomt resource-uitputting bij gecombineerde queries (out of memory, spool-limieten)
  - Hoger aantal queries maar lagere geheugendruk per query

**Combined Mode**: Alle statistieken worden berekend binnen één enkele SQL-query

  - Vermindert het totale aantal queries en netwerkoverhead
  - Optimaliseert prestaties wanneer datasources in het geheugen beheersbaar zijn
  - Efficiënter voor frequente, parallelle uitvoeringen

**Impact:** Geeft gebruikers fijnmazige controle over query-executie om prestaties, resourcegebruik en geheugenzekerheid af te stemmen op de kenmerken van hun datasource.

---

### Configureerbaar voorspellingsmodel

Het model achter anomaliedetectie weegt nu concurrerende verklaringen van elke reeks tegen elkaar af – een patroon gecombineerd met een interpretatie van de meest recente waarnemingen – en combineert hun voorspellingen naar gelang van hoe sterk elke verklaring wordt ondersteund. Eén extreme waarde kan niet langer doorwerken in de volgende voorspellingen.

Twee instellingen op het nieuwe tabblad **Model** van de datasource sturen het model, elk van `0.0` tot `1.0` met `0.5` als standaard:

- **Break Sensitivity** – hoe snel een sprong naar een nieuw niveau of een kerende trend als echt wordt aangenomen in plaats van als uitschieters te worden behandeld
- **Model Complexity** – hoeveel structuur het model zoekt, van kalendereffecten en één niveauverschuiving tot onbekende cycli, dag-van-de-maandeffecten en maandelijkse resets

Beide kunnen op elk moment worden teruggezet naar hun standaardwaarden. Zie [Modelinstellingen](../platform/data_anomalies/how_it_works.md#model-settings) voor hoe elk ervan werkt.

**Impact:** Geeft gebruikers controle over het voorspellingsmodel zelf, naast de bestaande instellingen Sensitivity en Memory op de tolerantieband, die nu op het tabblad **Thresholds** staan.

---

### Meldingsbeheer voor anomalieën

- Nieuw tabblad **Notifications** in de anomalie-instellingen van de datasource:
  - **Minimum Alerts** – hoeveel mislukte controles (geen onzekere) een inspectie nodig heeft voordat een melding wordt verzonden (standaard `1`)
  - **Pause After Notification (Days)** – hoe lang een abonnement stil blijft na een melding over de datasource (standaard `0`, geen pauze)
- Abonnees krijgen nu een melding wanneer een inspectie volledig mislukt (**Notify Inspection Errors**)
- Elke melding linkt rechtstreeks naar de pagina waar die over gaat – de mislukte controles van de inspectie, of de weergaven van Schema Tracker en Timeliness
- Duidelijkere abonnementsschakelaars: **Notify on Passed Inspections**, **Notify Inspection Errors**, **Notify Data Volume Checks**

**Zo werken meldingen:** meldingen worden verzonden via **notificatiekanalen** – Email (via een SMTP-verbinding), Slack of Jira – die beheerders instellen en kunnen controleren met **Test Notification Channel**. Een **abonnement** koppelt een kanaal aan een project: het omvat alle of geselecteerde datasources, en de schakelaars bepalen waarover het rapporteert – elke module (Data Anomalies, Data Validation, Data Analytics, Timeliness, Schema Tracker en datavolumecontroles), inspecties die volledig mislukken en optioneel ook geslaagde inspecties.

**Impact:** Minder, maar beter bruikbare meldingen – geïsoleerde afwijkingen en aanhoudende anomalieën overspoelen het kanaal niet langer.

---

### Herontworpen dashboardervaring  
- Gemoderniseerd en verbeterd UI/UX-ontwerp  
- Duidelijkere navigatie en structuur  
- Betere zichtbaarheid van monitoringresultaten en datakwaliteitsinzichten  
- Verbeterde leesbaarheid van alerts, statistieken en dashboards  
- Snellere toegang tot cruciale operationele informatie  

**Impact:** Verhoogt de gebruiksvriendelijkheid en dagelijkse productiviteit voor alle gebruikers.

---

### Uitgebreide import & export voor validatieregels  
- Verbeterde import/exportfunctionaliteit voor validatieregels  
- Eenvoudigere migratie tussen omgevingen en projecten  
- Betere herbruikbaarheid van gestandaardiseerde regelsets  
- Verbeterde governance en lifecycle-management van regels  
- Vereenvoudigde samenwerking tussen teams  

**Impact:** Maakt schaalbaar en consistent beheer van datakwaliteit across de organisatie mogelijk.

---

## Platformverbeteringen  

- Volledige Python SDK-integratie voor automatisering  
- Gefcontaineriseerde deployment via Docker  
- Verbeterde UX door het herontworpen dashboard  
- Uitgebreide draagbaarheid van validatielogica  

---

## Wie profiteert van deze release  

- Data Engineers: automatisering, SDK-gebruik, pipeline-integratie  
- Platformteams: vereenvoudigde deployment via Docker  
- Data Governance Teams: herbruikbaar beheer van validatieregels  
- Analytics Teams: verbeterde gebruiksvriendelijkheid en zichtbaarheid van inzichten  

---

## CLI-updates  
- Toegevoegde SDK-integratiesteun  
- Verbeterde import/export-workflows  
- Algemeen stabielheids- en prestatieverbeteringen