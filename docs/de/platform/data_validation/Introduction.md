---
title: Data Validation – Regelbasierte Prüfungen für Compliance & Prüfbarkeit | digna Dokumentation
description: Entdecken Sie, wie digna Data Validation deterministische, regelbasierte Prüfungen mit Schwellenwerten, Bereichen und Referenzlisten durchsetzt. Gewährleisten Sie Compliance, Prüfbarkeit und regulatorische Berichterstattung in Finanzwesen, Gesundheitswesen und anderen datensensitiven Branchen.
image: /assets/logo_square.png
keywords:
  - Data Validation
  - regelbasierte Datenprüfungen
  - Datenqualität
  - Qualität der Daten
  - Daten-Observability
  - Schwellenwerte und Bereiche
  - Validierung von Referenzlisten
  - Prüfbarkeit
  - Compliance-Überwachung
  - digna Data Validation
lang: en
robots: index, follow
og_title: Data Validation – Regelbasierte Prüfungen für Compliance & Prüfbarkeit | digna Dokumentation
og_description: digna Data Validation setzt deterministische, regelbasierte Prüfungen mit Schwellen, Bereichen und Referenzlisten durch. Entwickelt für regulierte Branchen, gewährleistet es Compliance, Transparenz und Prüfbarkeit.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

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
