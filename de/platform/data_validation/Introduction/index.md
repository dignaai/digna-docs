# Data Validation – Regelbasierte Prüfungen
<h1 style="display:none;">KI-gestütztes Data Validation-Modul für Datenqualität und Observability – digna</h1>

---

## Zweck

Das **Data Validation**-Modul sichert die **Datenqualität** durch präzise, regelbasierte Prüfungen.  
Es ermöglicht Organisationen, deterministische geschäftliche und technische Validierungslogiken zu definieren und stellt sicher, dass Daten Compliance-Standards, vertragliche SLAs und regulatorische Anforderungen erfüllen.

Durch die Kombination von *In-Database-Regelausführung*, *vollständigen Audit-Trails* und *Integration mit anderen digna-Modulen* gewährleistet **Data Validation** konsistente und nachvollziehbare **Datenqualität und Observability** in komplexen Unternehmensumgebungen.

---

## Technische Übersicht

### Unterstützte Validierungstypen

- **Gleichheitsprüfungen**  
  Bestätigen, dass Werte den erwarteten Ergebnissen entsprechen (z. B. Referenzcodes, boolesche Flags, kategoriale Zuordnungen).

- **Schwellenwerte & Bereiche**  
  Validierung numerischer Messgrößen oder KPIs gegen definierte Grenzen — statisch oder dynamisch abgeleitet.

- **Referenzlisten & Lookups**  
  Überprüfen, ob Feldwerte innerhalb genehmigter Stammdatensätze vorhanden sind (z. B. USt.-Codes, ISO-Länderliste, Produktkataloge).

- **Spaltenübergreifende Konsistenz**  
  Sicherstellen relationaler Korrektheit (z. B. Währung stimmt mit Region überein, Risikokategorie passt zum Anlagetyp).

- **Regeln zum Umgang mit Nullwerten**  
  Erkennen unerwarteter Null- oder Leerwerte in kritischen Spalten.

### Ausführung und Protokollierung

- **In-Database-Processing** – Alle Validierungsregeln werden direkt in Ihrer Datenbank ausgeführt (Teradata, Snowflake, Databricks, PostgreSQL usw.).  
- **Keine Datenextraktion** – digna überträgt niemals Rohdaten aus Ihrer Umgebung.  
- **Volle Nachvollziehbarkeit** – Jedes Regelresultat wird mit Zeitstempel, verantwortlichem Dataset, Anzahl der Datensätze und Bestanden/Nicht bestanden protokolliert.  
- **Audit**