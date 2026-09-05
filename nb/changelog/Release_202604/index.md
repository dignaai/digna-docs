# Endringslogg – Utgivelse 2026.04  

Med utgivelsen 2026.04 utvider digna betydelig sine muligheter innen analyse og datavalidering.  
Denne utgivelsen introduserer avansert tidsserieanalyse, gjenbrukbare valideringskomponenter og sentralisert verdistandardisering.

---

## Nye funksjoner  

### Analytics Chart – Tidsserieanalyse uten datafagkunnskap  
- Ny **Analytics Chart** for interaktiv tidsserieanalyse  
- Innebygde analytiske metoder:
    - Lineær, kvadratisk og kubisk regresjon  
    - Stykkevis (piecewise) regresjon med konfigurerbare bruddpunkter  
    - Glattingsmetoder  
    - Kvantilanalyse  
- Automatisk identifikasjon av trender, sesongvariasjoner og mønsterendringer  
- Residualanalyse for dypere innsikt i avvik  
- Tidsserier beregnes automatisk for hvert datasett  

**Effekt:** Gjør det mulig å forstå kompleks datatferd over tid uten å kreve datafaglig ekspertise eller eksterne verktøy.

---

### Enumerations – Sentral definisjon av tillatte verdier  
- Definer gjenbrukbare sett med tillatte verdier (f.eks. land, delstater, statuskoder)  
- Valider kolonneverdier mot forhåndsdefinerte enumerasjoner i **digna Data Validation**  
- Gjenbruk enumerasjoner på tvers av prosjekter og datakilder  
- Bruk enumerasjoner overalt via `#ENUM:MY_ENUM#`  
- Alle kontroller kjøres **direkte i kildedatabasen**  

**Effekt:** Sikrer konsistente og standardiserte dataverdier på tvers av organisasjonen.

---

### Valideringsregelmaler – Gjenbrukbar logikk for datakvalitet  
- Definer gjenbrukbare valideringsregler (f.eks. sjekk for mellomrom, NOT NULL, formatkontroller)  
- Bruk maler på tvers av flere datasett  
- Sikre konsistent regel-logikk på tvers av prosjekter  
- Reduser duplisering og manuell konfigurering  
- Alle kontroller kjøres **direkte i kildedatabasen**  

**Effekt:** Muliggjør skalerbar og høyytelses datavalidering uten dataflytting.

---

### Relevansbetingelser på statistikknivå  
- Definer relevansbetingelser på **kolonnenivå for hver statistikk**  
- Utvider konseptet med relevansbetingelser for anomalier  
- Kontroller når en statistikk skal anses som relevant  
- Reduser støy ved å ekskludere ikke-kritiske situasjoner  

**Effekt:** Forbedrer signalet ved å fokusere kun på meningsfulle avvik.

---

## Utvidede Data Analytics- og valideringsmuligheter  

Med denne utgivelsen utvider digna både **datainnsikt** og **standardisering av datavalidering**:

- Avansert **tidsseriefortolkning** uten behov for datafagkunnskap  
- Sentralt definert **tillatte verdier via enumerasjoner**  
- Gjenbrukbar **valideringslogikk via maler**  
- Finkornet kontroll over **relevansen av statistikk og varsler**  

Sammen gjør disse funksjonene det mulig for organisasjoner å ikke bare oppdage problemer, men også **forstå, standardisere og kontrollere datakvaliteten**.

---

## Hvem får nytte av denne utgivelsen  

- Dataingeniører: Gjenbrukbar valideringslogikk og bedre kontroll over overvåkingsoppsettet  
- Team for datakvalitet og styring: Standardiserte regler og konsekvent datavalidering på tvers av systemer  
- Analyse- og BI-team: Bedre forståelse av trender og avvik  
- Platformeiere: Økt adopsjon gjennom forenklet analyse og skalerbar validering  

---

## CLI-oppdateringer  
- Ingen endringer  

---