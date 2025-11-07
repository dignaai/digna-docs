---
title: Data Validation – Regelsgebaseerde controles voor naleving & auditabiliteit | digna Documentation
description: Ontdek hoe digna Data Validation deterministische, regelsgebaseerde controles afdwingt met drempels, bereiken en referentielijsten. Zorg voor naleving, auditbaarheid en rapportage voor gereguleerde sectoren zoals financiën en gezondheidszorg.
image: /assets/logo_square.png
keywords:
  - data validation
  - rule-based data checks
  - data quality
  - quality of data
  - data observability
  - thresholds and ranges
  - reference list validation
  - auditability
  - compliance monitoring
  - digna data validation
lang: nl
robots: index, follow
og_title: Data Validation – Regelsgebaseerde controles voor naleving & auditabiliteit | digna Documentation
og_description: digna Data Validation handhaaft deterministische, regelsgebaseerde controles met drempels, bereiken en referentielijsten. Ontworpen voor gereguleerde sectoren; het waarborgt naleving, transparantie en auditbaarheid.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Regelsgebaseerde controles
<h1 style="display:none;">AI-gestuurde Data Validation-module voor Datakwaliteit en Observability – digna</h1>

---

## Doel

De **Data Validation**-module waarborgt de **kwaliteit van data** door nauwkeurige, regelsgebaseerde controles.  
Het stelt organisaties in staat deterministische zakelijke en technische validatielogica te definiëren, zodat data voldoet aan nalevingsnormen, contractuele SLA's en wettelijke vereisten.

Door *in-database regeluitvoering*, *volledige auditsporen* en *integratie met andere digna modules* te combineren, garandeert **Data Validation** consistente en traceerbare **Datakwaliteit en Observability** in complexe enterprise-omgevingen.

---

## Technisch overzicht

### Ondersteunde validatietypen

- **Gelijkheidscontroles**  
  Bevestig dat waarden overeenkomen met verwachte resultaten (bijv. referentiecodes, Booleaanse flags, categorische mappings).

- **Drempels & bereiken**  
  Valideer numerieke metingen of KPI's tegen gedefinieerde limieten — statisch of dynamisch afgeleid.

- **Referentielijsten & lookups**  
  Controleer of veldwaarden aanwezig zijn in goedgekeurde masterdatasets (bijv. btw-codes, ISO-landenlijsten, productcatalogi).

- **Consistentie tussen kolommen**  
  Zorg voor relationele correctheid (bijv. valuta komt overeen met regio, risicocategorie past bij activumtype).

- **Regels voor nullafhandeling**  
  Detecteer onverwachte null- of lege waarden in kritieke kolommen.

### Uitvoering en logging

- **In-database verwerking** – Alle validatieregels worden rechtstreeks in uw database uitgevoerd (Teradata, Snowflake, Databricks, PostgreSQL, enz.).  
- **Geen data-extractie** – digna verplaatst nooit ruwe gegevens buiten uw omgeving.  
- **Volledige traceerbaarheid** – Elk regelresultaat wordt gelogd met tijdstempel, verantwoordelijke dataset, recordaantallen en geslaagd/ongegrond uitkomsten.  
- **Audit**