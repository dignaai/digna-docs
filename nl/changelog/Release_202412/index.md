# Wijzigingen – Release 2024.12

De release 2024.12 levert een nieuwe set functies en verbeteringen die digna meer geautomatiseerd, flexibel en bedrijfsklaar maken.  
Deze versie verbetert planning, rapportage, queryverwerking en de nauwkeurigheid van anomaliedetectie.  

---

## Nieuwe functies

### Ingebouwde Scheduler
Inspecties zijn niet langer uitsluitend afhankelijk van de opdrachtregel of API-aanroepen.  
Met de **nieuwe digna Scheduler** kunnen inspecties automatisch worden uitgevoerd op gedefinieerde tijden.  

- Ondersteunt **Cron-expressies** voor terugkerende schema’s (dagelijks, wekelijks of aangepaste intervallen).  
- Biedt precieze controle via **offsets**, **startdatums** en **einddatums**.  
- Hiermee kunnen teams ervoor zorgen dat alle kritieke data-bronnen consequent en zonder handmatige inspanning worden geïnspecteerd.  

---

### Rapporten in PDF-formaat
Teams kunnen nu eenvoudig resultaten delen met belanghebbenden via **PDF-exporten**.  

- Grafieken, statistieken en anomalieresultaten kunnen worden geëxporteerd in een professioneel PDF-formaat.  
- Rapporten combineren **visualisaties** en **onderliggende data** om zowel technische als zakelijke gebruikers te bedienen.  
- Vermindert de noodzaak voor externe tools voor het maken van rapporten.  

---

### Nieuw kolomtype: `CUSTOM`
Om meer flexibiliteit te bieden, introduceert digna een nieuw **`CUSTOM` kolomtype**.  

- Gebruikers kunnen precies definiëren welke **statistieken en metrics** worden toegepast op specifieke attributen.  
- Perfect voor speciale gevallen die niet in standaardcategorieën zoals NUMERICAL of CATEGORICAL passen.  
- Helpt analyses gefocust te houden en resultaten relevant voor de zakelijke context te maken.  

---

### Nieuwe plaatsaanduiders in snapshot-queries
Snapshot-queries zijn nu eenvoudiger en minder foutgevoelig dankzij **dynamische plaatsaanduiders**.  

- Tokens zoals `#date+n#` of `#date-n#` passen datums automatisch aan in queries.  
- Voorbeeld:  
  - `#date+1#` → morgen  
  - `#date-2#` → twee dagen geleden  
- Voorkomt handmatige datum-berekeningen en zorgt voor consistentie binnen teams.  

---

### Drempeloptimalisatie
Anomaliedrempels zijn nu intelligenter en contextbewuster.  

- Voor metrics zoals **NULL COUNT** worden lagere drempels automatisch begrensd op **0**.  
- Voorkomt ongeldige of zinloze drempels.  
- Leidt tot minder false positives en betrouwbaardere anomaliedetectie.  

---

## Algemene verbeteringen
- Verfijnde **UI-componenten** in project- en attribuutconfiguratie-weergaven.  
- Verbeterde **dashboardprestaties** voor grote datavolumes.  
- Uitgebreidere **logging en foutmeldingen** voor het oplossen van problemen.  

---

## Samenvatting
Release 2024.12 versterkt digna als platform voor **datakwaliteit, anomaliedetectie en observability**.  
Met automatisering via scheduling, deelbare PDF-rapporten, aanpasbare kolommen, vereenvoudigde snapshot-queries en slimmere drempels wordt digna nog waardevoller voor zowel technische gebruikers als zakelijke belanghebbenden.