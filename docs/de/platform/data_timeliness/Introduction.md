---
title: Data Timeliness – Überwachung pünktlicher Lieferungen | digna Documentation
description: Erfahren Sie, wie digna Data Timeliness sicherstellt, dass Daten zum erwarteten Zeitpunkt eintreffen. Erkennen Sie verspätete oder fehlende Lieferungen, überwachen Sie SLAs und schützen Sie Geschäftsprozesse vor stillen Verzögerungen. KI-gestützte Erkennung für verbesserte Datenqualität und Observability von Datenpipelines.
image: /assets/logo_square.png
keywords:
  - data timeliness
  - Lieferüberwachung
  - Datenqualität
  - Qualität der Daten
  - Beobachtbarkeit von Daten
  - Erkennung verspäteter Daten
  - Benachrichtigung bei fehlenden Daten
  - SLA-Überwachung
  - KI-gestützte Lieferanalyse
  - digna data timeliness
lang: en
robots: index, follow
og_title: Data Timeliness – On-Time Delivery Monitoring | digna Documentation
og_description: digna Data Timeliness detects delayed or missing data deliveries automatically using AI. Protect business processes, monitor SLAs, and ensure timely, reliable data across all pipelines.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – Überwachung pünktlicher Lieferungen

---

## Zweck

Das **Data Timeliness**-Modul stellt sicher, dass **Daten pünktlich eintreffen** – jedes Mal.  
Es überwacht kontinuierlich Lieferpläne und erkennt automatisch, wenn Datensätze, Tabellen oder Dateien **verspätet, fehlend oder unvollständig** sind.  

Durch die Kombination von KI-Lernen mit benutzerdefinierten Zeitplänen ermöglicht *digna* Organisationen, nachgelagerte Fehler zu verhindern und strikte **SLA (Service Level Agreement)**-Ziele sowohl für **Datenqualität** als auch für die **Observability von Datenpipelines** einzuhalten.

---

## Technische Übersicht

### Doppelte Überwachungsmodi
- **KI-gelernte Ankunftsmuster**  
  digna lernt automatisch den natürlichen Rhythmus Ihrer Datenlieferungen — täglich, stündlich oder ereignisgesteuert — indem historische Zeitstempel und Abschlusszeiten analysiert werden.  
  Es passt sich an Änderungen in Geschäftskalendern, Wochenenden oder Monatsendspitzen an.

- **Benutzerdefinierte Zeitpläne**  
  Benutzer können erwartete Lieferzeiten explizit definieren (z. B. *an jedem Werktag vor 7:30 Uhr*).  
  digna vergleicht die tatsächliche Ankunftszeit mit dem geplanten Zeitplan und löst Warnungen aus, wenn Daten verspätet oder fehlend sind.

### Erkennungsmechanismus
- Bewertet **Metadaten-Zeitstempel**, **Datensatzanzahlen** und **Tabellenfrische**  
- Erkennt **eingefrorene ETL-Jobs**, **fehlgeschlagene Extraktionen** und **partielle Dateiankünfte**  
- Integriert sich mit *Data Anomalies* und *Data Validation* für kombinierte Erkenntnisse

---

## Erkennungsszenarien

| Scenario | Description |
|-----------|--------------|
| **Late data arrival** | Täglich eingehender Marktdatenfeed ist um zwei Stunden verspätet, wodurch Berichte SLAs verpassen |
| **Missing load** | Eine geplante Tabelle oder Partition wurde für das aktuelle Datum nicht aktualisiert |
| **Chained dependency delay** | Verzögerung eines vorgelagerten Jobs beeinträchtigt die Aktualisierung nachgelagerter Pipelines |
| **Weekend pattern shift** | Das KI-Modell passt sich automatisch an, wenn an Sonntagen keine Daten erwartet werden |

---

## Architektur und Ausführung

- **In-database-Ausführung:** digna führt Timeliness-Checks direkt in Ihrer Datenbank oder Ihrem Data Warehouse aus.  
- **Leichter Metadatenzugriff:** liest Job-Zeitstempel, Datensatzanzahlen und Partitioninformationen — keine Datenextraktion erforderlich.  
- **Konfigurierbare Frequenz:** Überwachung pro Datensatz, Schema oder Pipeline planbar.  
- **Modular übergreifende Warnungen:** Ergebnisse können visuelle Warnungen in *Inspection Hub* oder Benachrichtigungen per E-Mail, Slack oder API auslösen.  

---

## Beispielanwendungsfälle

- **Finanzmarkt-Feeds:** Verzögerungen bei Preis- oder Handelsdatenupdates erkennen.  
- **Data Warehouse Loads:** Überwachen, wenn nächtliche ETL-Jobs später als erwartet fertig werden.  
- **Datenaustausch zwischen Teams:** Sicherstellen, dass Abteilungsdatenlieferungen vor täglichen Cutoffs erfolgen.  
- **Regulatorische Berichterstattung:** Bestätigen, dass Einreichungen den neuesten verfügbaren Datensnapshot enthalten.  

---

## Vorteile

| Area | Benefit |
|------|----------|
| **Business Continuity** | Verhindert betriebliche Unterbrechungen durch verspätete oder fehlende Daten |
| **Data Quality** | Verbessert Zuverlässigkeit und Konsistenz von Datenpipelines |
| **Compliance** | Stellt SLA-Einhaltung und Prüfbarkeit sicher |
| **Automation** | KI beseitigt manuelle Nachverfolgung von Zeitplänen |
| **Integration** | Arbeitet nahtlos mit *Data Analytics* zusammen, um Timeliness-Trends über die Zeit zu visualisieren |

---

## Wie digna erwartete Lieferzeiten lernt

1. **Historische Analyse:** digna beobachtet frühere Ladezeiten und -dauern.  
2. **KI-Modellierung:** Maschinelles Lernen erstellt eine dynamische Basislinie für erwartete Ankünfte.  
3. **Überwachung:** Jede neue Lieferung wird mit der Basislinie verglichen.  
4. **Alerting:** Abweichungen lösen Warnungen mit kontextuellen Metriken und Konfidenzwerten aus.  

Dieser kontinuierliche Lernansatz passt sich verändernden Prozessen an und hält False Positives gering.

---

## Häufig gestellte Fragen

**Kann ich meine eigenen Lieferzeiten definieren?**  
Ja. digna unterstützt sowohl feste Benutzerschedules als auch KI-gelernte Muster.

**Kann es sich in mein ETL- oder Orchestrierungstool integrieren?**  
Ja. digna integriert sich mit Tools wie Airflow, dbt, Informatica oder benutzerdefinierten Schedulern.

**Wo findet die Berechnung statt?**  
Alle Analysen laufen innerhalb Ihrer Datenbank oder Ihres Cloud-Warehouses — es wird kein externer Service verwendet.

**Was passiert, wenn Daten verspätet sind?**  
digna löst Alerts im Dashboard, im Inspection Hub und über API/Webhooks aus, um Betriebsteams sofort zu benachrichtigen.

---


**digna Data Timeliness** hilft, **Vertrauen in Daten** zu sichern, indem es **KI-gesteuerte Erkennung**, **lokale Ausführung** und **Datenobservability** kombiniert — alles innerhalb Ihrer kontrollierten Umgebung.