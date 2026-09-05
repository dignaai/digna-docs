# Data Schema Tracker – Monitor Schema Evolution
<h1 style="display:none;">AI-gedreven module voor metadata-observability en datakwaliteit – digna Data Schema Tracker</h1>

---

## Doel

De **Data Schema Tracker** houdt je op de hoogte van hoe de structuren van je databases evolueren.  
Hij bewaakt continu **tabelschema's, kolommen en datatypes** om **schema drift** te detecteren — opzettelijke of onopzettelijke structurele wijzigingen die pijplijnen, ETL-jobs of BI-dashboards kunnen verstoren.

Door transparantie te bieden in schema-evolutie helpt digna organisaties om **vertrouwen in de datakwaliteit** te behouden, de **observability van datasystemen** te waarborgen en kostbare incidenten in productie door onopgemerkte schemawijzigingen te voorkomen.

---

## Technisch Overzicht

### Wat het bewaakt

- **Toegevoegde of Verwijderde Kolommen** – Detecteert nieuw geïntroduceerde, opnieuw benoemde of verwijderde kolommen.  
- **Wijzigingen in Datatypes** – Herkent veranderingen zoals `INT → VARCHAR` of `DATE → TIMESTAMP`.  
- **Wijzigingen in Tabellen en Views** – Volgt creatie, hernoeming of verwijdering van tabellen en views.  
- **Verschillen tussen Omgevingen** – Vergelijkt schema-versies tussen Dev, Test en Production omgevingen.  

### Detectie & Alerting

- Scant **database metadata** of **system catalogs** rechtstreeks binnen je data-platform.  
- Vergelijkt elke schema-snapshot met de eerder bekende versie die is opgeslagen in digna’s observability schema.  
- Genereert **real-time waarschuwingen** in het dashboard, via API of externe notificatiekanalen (e-mail, Slack, webhook).  
- Logt elke schema-versie voor **historische tracking en audit-readiness**.

---

## Architectuur en Uitvoering

- **In-Database Uitvoering:** digna draait volledig binnen jouw omgeving en bevraagt metadata-views zonder enige data te extraheren.  
- **Lichte Scans:** heeft alleen toegang tot structurele informatie — nooit tot gebruikersdata.  
- **Gecentraliseerde Opslag:** schema-metadata en drift-records worden opgeslagen in het digna observability schema voor visualisatie en analyse.  
- **Automatisering:** ondersteunt geplande of event-gestuurde scans via digna Core of externe orchestratie-tools.  

---

## Voorbeeldgebruikscases

| Use Case | Description |
|-----------|--------------|
| **ETL Stability Monitoring** | Detecteer structurele wijzigingen stroomopwaarts voordat pijplijnen falen door schema-onverenigbaarheden. |
| **Business Intelligence Reliability** | Voorkom kapotte dashboards veroorzaakt door hernoemde of ontbrekende kolommen. |
| **Data Warehouse Governance** | Houd een controleerbare geschiedenis van schema-evolutie voor compliance en impactanalyse. |
| **Integration Oversight** | Zorg dat data lake- en warehouse-schema's synchroon blijven na structurele updates. |

---

## Voordelen

| Area | Benefit |
|------|----------|
| **Data Quality** | Voorkomt onopgemerkte schema drift die data-pijplijnen kan corrupt maken of ongeldig kan maken. |
| **Observability** | Voegt structurele monitoring toe aan de algehele observability van data-ecosystemen. |
| **Compliance** | Bewaart versiegeschiedenis van schema's voor audit, traceerbaarheid en change control. |
| **Prevention** | Detecteert structurele problemen voordat ze doorslaan in rapportage- of productieproblemen. |

---

## Hoe Het Werkt

1. **Snapshotverzameling** – digna neemt de huidige schema-metadata op.  
2. **Vergelijking** – de nieuwe snapshot wordt vergeleken