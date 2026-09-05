# Data Validation – Reglerbaserade kontroller
<h1 style="display:none;">AI-driven Data Validation-modul för datakvalitet och observabilitet – digna</h1>

---

## Syfte

Modulen **Data Validation** säkerställer **datakvalitet** genom precisa, reglerbaserade kontroller.  
Den gör det möjligt för organisationer att definiera deterministisk affärs- och teknisk valideringslogik, och säkerställer att data uppfyller efterlevnadsstandarder, kontraktuella SLA:er och regulatoriska krav.

Genom att kombinera *in-database rule execution*, *kompletta revisionsspår* och *integration med andra digna-moduler* garanterar **Data Validation** konsekvent och spårbar **datakvalitet och observabilitet** i komplexa företagsmiljöer.

---

## Teknisk översikt

### Stödda valideringstyper

- **Likhetskontroller**  
  Bekräfta att värden matchar förväntade resultat (t.ex. referenskoder, booleska flaggor, kategorimappningar).

- **Tröskelvärden & intervall**  
  Validera numeriska mått eller KPI:er mot definierade gränser — statiska eller dynamiskt härledda.

- **Referenslistor & uppslag**  
  Kontrollera om fältvärden finns i godkända masterdatasätt (t.ex. moms-koder, ISO-landlistor, produktkataloger).

- **Konsistens mellan kolumner**  
  Säkerställ relationskorrekthet (t.ex. att valuta stämmer överens med region, att riskkategori matchar tillgångstyp).

- **Regler för null-hantering**  
  Upptäck oväntade null- eller tomma värden i kritiska kolumner.

### Körning och loggning

- **In-Database Processing** – Alla valideringsregler körs direkt i din databas (Teradata, Snowflake, Databricks, PostgreSQL osv.).  
- **Ingen dataexport** – digna överför aldrig rådata utanför din miljö.  
- **Fullständig spårbarhet** – Varje regelresultat loggas med tidsstämpel, ansvarigt dataset, antal poster och godkänd/underkänd-utfall.  
- **Revision**