# Data Validation – Regelbasierte Prüfungen

---

## Zweck

Das **Data Validation**-Modul stellt die **Datenqualität** durch präzise, regelbasierte Prüfungen sicher.  
Es ermöglicht Organisationen, deterministische geschäftliche und technische Validierungslogik zu definieren und sicherzustellen, dass Daten Compliance-Standards, vertraglichen SLAs und regulatorischen Anforderungen entsprechen.

Durch die Kombination von *in-database rule execution*, *complete audit trails* und *integration with other digna modules* garantiert **Data Validation** konsistente und nachvollziehbare **Datenqualität und Observability** in komplexen Unternehmensumgebungen.

---

## Technische Übersicht

### Unterstützte Validierungstypen

- **Gleichheitsprüfungen**  
  Bestätigen, dass Werte den erwarteten Ergebnissen entsprechen (z. B. Referenzcodes, boolesche Flags, kategorische Zuordnungen).

- **Schwellenwerte & Bereiche**  
  Validieren numerischer Messgrößen oder KPIs gegenüber definierten Grenzen — statisch oder dynamisch abgeleitet.

- **Referenzlisten & Lookups**  
  Prüfen, ob Feldwerte innerhalb genehmigter Stammdatensätze vorhanden sind (z. B. USt-IDs, ISO-Länderliste, Produktkataloge).

- **Spaltenübergreifende Konsistenz**  
  Sicherstellen relationaler Korrektheit (z. B. Währung stimmt mit Region überein, Risikokategorie passt zum Anlagetyp).

- **Nullbehandlungsregeln**  
  Erkennen unerwarteter Null- oder Leerwerte in kritischen Spalten.

### Ausführung und Protokollierung

- **In-Database Processing** – Alle Validierungsregeln werden direkt in Ihrer Datenbank ausgeführt (Teradata, Snowflake, Databricks, PostgreSQL, etc.).  
- **Keine Datenextraktion** – digna überträgt niemals Rohdaten außerhalb Ihrer Umgebung.  
- **Vollständige Nachvollziehbarkeit** – Jedes Regelresultat wird mit Zeitstempel, verantwortlichem Dataset, Datensatzanzahlen und Bestehen/Nichtbestehen protokolliert.  
- **Audit**