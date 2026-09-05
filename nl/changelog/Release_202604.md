# Wijzigingen – Release 2026.04  

Met Release 2026.04 breidt digna zijn mogelijkheden op het gebied van analytics en datavalidatie flink uit.  
Deze release introduceert geavanceerde tijdreeksanalyse, herbruikbare validatiecomponenten en gecentraliseerde waardestandaardisatie.

---

## Nieuwe functies  

### Analytics Chart – Tijdreeksanalyse zonder Data Science  
- Nieuwe **Analytics Chart** voor interactieve tijdreeksanalyse  
- Ingebouwde analytische methoden:
    - Lineaire, kwadratische en kubieke regressie  
    - Piecewise-regressie met configureerbare breekpunten  
    - Smoothing-technieken  
    - Kwantielanalyse  
- Automatische identificatie van trends, seizoenspatronen en patroonveranderingen  
- Residualenanalyse voor diepere inzichten in afwijkingen  
- Tijdreeksen worden automatisch berekend voor elke dataset  

**Impact:** Maakt het mogelijk voor gebruikers om complex gedrag in data door de tijd heen te begrijpen zonder data science-expertise of externe tools.

---

### Enumerations – Centrale definitie van toegestane waarden  
- Definieer herbruikbare sets van toegestane waarden (bijv. landen, staten, statuscodes)  
- Valideer kolomwaarden tegen vooraf gedefinieerde enumeraties in **digna Data Validation**  
- Hergebruik enumeraties over projecten en databronnen heen  
- Gebruik enumeraties overal via `#ENUM:MY_ENUM#`  
- Alle controles worden **direct in de brondatabase** uitgevoerd  

**Impact:** Zorgt voor consistente en gestandaardiseerde datawaarden binnen de organisatie.

---

### Validation Rule Templates – Herbruikbare data quality-logica  
- Definieer herbruikbare validatieregels (bijv. controles op witruimte, NOT NULL, formaatcontroles)  
- Pas templates toe op meerdere datasets  
- Zorg voor consistente regel-logica over projecten heen  
- Verminder duplicatie en handmatige configuratie  
- Alle controles worden **direct in de brondatabase** uitgevoerd  

**Impact:** Maakt schaalbare en high-performance datavalidatie mogelijk zonder data te verplaatsen.

---

### Relevantievoorwaarden op statistiekniveau  
- Definieer relevantievoorwaarden op **kolomniveau voor elke statistiek**  
- Breidt het concept van anomalie-relevantievoorwaarden uit  
- Bepaal wanneer een statistiek als relevant moet worden beschouwd  
- Verminder ruis door niet-kritieke situaties uit te sluiten  

**Impact:** Verbetert de signaalkwaliteit door alleen te focussen op betekenisvolle afwijkingen.

---

## Uitgebreide Data Analytics & Validatie-mogelijkheden  

Met deze release breidt digna zowel het begrip van data als de standaardisatie van datavalidatie uit:

- Geavanceerde **tijdreeksinterpretatie** zonder data science-kennis  
- Gecentraliseerde definitie van **toegestane waarden via enumeraties**  
- Herbruikbare **validatielogica via templates**  
- Fijnmazige controle over **relevantie van statistieken en alerts**  

Samen stellen deze mogelijkheden organisaties in staat niet alleen problemen te detecteren, maar ook **datakwaliteit te begrijpen, te standaardiseren en te beheersen**.

---

## Wie profiteert van deze release  

- **Data Engineers:** Herbruikbare validatielogica en verbeterde controle over monitoring-gedrag  
- **Data Quality & Governance Teams:** Gestandaardiseerde regels en consistente datavalidatie over systemen heen  
- **Analytics & BI Teams:** Beter inzicht in trends en afwijkingen  
- **Platform Owners:** Grotere adoptie door vereenvoudigde analytics en schaalbare validatie  

---

## CLI-updates  
- Geen wijzigingen  

---