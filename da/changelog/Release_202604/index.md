# Ændringslog – Release 2026.04  

Med Udgivelse 2026.04 udvider digna betydeligt sine kapaciteter inden for analytics og datavalidering.  
Denne udgivelse introducerer avanceret tidsserieanalyse, genanvendelige valideringskomponenter og centraliseret værdistandardisering.

---

## Nye funktioner  

### Analytics Chart – Tidsserieanalyse uden data science  
- Nyt **Analytics Chart** til interaktiv tidsserieanalyse  
- Indbyggede analytiske metoder:
    - Lineær, kvadratisk og kubisk regression  
    - Piecewise-regression med konfigurerbare brudpunkter  
    - Smoothing-teknikker  
    - Kvantilanalyse  
- Automatisk identifikation af trends, sæsonvariationer og mønsterskift  
- Residualanalyse for dybere indsigt i afvigelser  
- Tidsserier beregnes automatisk for hvert datasæt  

**Effekt:** Giver brugere mulighed for at forstå kompleks datadynamik over tid uden data science-ekspertise eller eksterne værktøjer.

---

### Enumerations – Central definition af tilladte værdier  
- Definér genanvendelige sæt af tilladte værdier (fx lande, regioner, statuskoder)  
- Valider kolonneværdier mod foruddefinerede enumerations i **digna Data Validation**  
- Genbrug enumerations på tværs af projekter og datakilder  
- Brug enumerations alle steder via `#ENUM:MY_ENUM#`  
- Alle kontroller udføres **direkte i kildedatabasen**  

**Effekt:** Sikrer konsistente og standardiserede dataværdier på tværs af organisationen.

---

### Validation Rule Templates – Genanvendelig datakvalitetslogik  
- Definér genanvendelige valideringsregler (fx kontroller for whitespace, NOT NULL, formatkontroller)  
- Anvend skabeloner på tværs af flere datasæt  
- Sikr ensartet regel-logik på tværs af projekter  
- Reducer duplikation og manuel konfiguration  
- Alle kontroller udføres **direkte i kildedatabasen**  

**Effekt:** Muliggør skalerbar og højtydende datavalidering uden databevægelser.

---

### Relevansbetingelser på statistikniveau  
- Definér relevansbetingelser på **kolonneniveau for hver statistik**  
- Udvider konceptet med anomalirelevansbetingelser  
- Kontroller, hvornår en statistik skal betragtes som relevant  
- Reducer støj ved at udelukke ikke-kritiske situationer  

**Effekt:** Forbedrer signal-kvaliteten ved kun at fokusere på meningsfulde afvigelser.

---

## Udvidede Data Analytics & Validation-muligheder  

Med denne udgivelse udvider digna både forståelsen af data og standardiseringen af datavalidering:

- Avanceret **tidsseriefortolkning** uden krav om data science-viden  
- Centraliseret definition af **tilladte værdier via enumerations**  
- Genanvendelig **valideringslogik via skabeloner**  
- Finkornet kontrol over **relevans af statistikker og alerts**  

Sammen gør disse funktioner det muligt for organisationer ikke blot at opdage problemer, men også at **forstå, standardisere og styre datakvaliteten**.

---

## Hvem får gavn af denne udgivelse  

- **Data Engineers:** Genanvendelig valideringslogik og forbedret kontrol over overvågningsadfærd  
- **Data Quality & Governance Teams:** Standardiserede regler og konsistent datavalidering på tværs af systemer  
- **Analytics & BI Teams:** Bedre forståelse af trends og afvigelser  
- **Platform Owners:** Øget adoption gennem simplificeret analytics og skalerbar validering  

---

## CLI-opdateringer  
- Ingen ændringer  

---