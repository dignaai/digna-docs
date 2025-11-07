---
title: Data Timeliness – Überwachung der termingerechten Lieferung | digna Dokumentation
description: Erfahren Sie, wie digna Data Timeliness sicherstellt, dass Daten zum erwarteten Zeitpunkt ankommen. Erkennen Sie verspätete oder fehlende Lieferungen, überwachen Sie SLAs und schützen Sie Geschäftsprozesse vor stillen Verzögerungen. KI-gestützte Erkennung für verbesserte Datenqualität und Observability von Datenpipelines.
canonical_url: https://docs.digna.ai/platform/data_timeliness/
image: /assets/logo_square.png
keywords:
  - daten pünktlichkeit
  - lieferüberwachung
  - datenqualität
  - qualität der daten
  - observability von datenpipelines
  - verspätete daten erkennung
  - fehlende daten alarmierung
  - sla überwachung
  - ai lieferungsanalyse
  - digna data timeliness
lang: de
robots: index, follow
og_title: Data Timeliness – Überwachung der termingerechten Lieferung | digna Dokumentation
og_description: digna Data Timeliness erkennt verzögerte oder fehlende Datenlieferungen automatisiert mit KI. Schützen Sie Geschäftsprozesse, überwachen Sie SLAs und gewährleisten Sie rechtzeitige, zuverlässige Daten in allen Pipelines.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – On-Time Delivery Monitoring
<h1 style="display:none;">AI-Driven Data Timeliness Module for Data Quality and Observability – digna</h1>

---

## Purpose

Das **Data Timeliness** Modul stellt sicher, dass **Daten pünktlich geliefert werden** – jedes Mal.  
Es überwacht kontinuierlich Lieferpläne und erkennt automatisch, wenn Datensätze, Tabellen oder Dateien **verspätet, fehlend oder unvollständig** sind.  

Durch die Kombination von KI-Lernen mit benutzerdefinierten Zeitplänen ermöglicht *digna* Organisationen, nachgelagerte Fehler zu vermeiden und strenge **SLA (Service Level Agreement)**-Ziele für sowohl **Datenqualität** als auch **Observability von Datenpipelines** einzuhalten.

---

## Technical Overview

### Dual Monitoring Modes
- **AI-Learned Arrival Patterns**  
  digna lernt automatisch den natürlichen Rhythmus Ihrer Datenlieferungen – täglich, stündlich oder ereignisgesteuert – indem historische Zeitstempel und Abschlusszeiten analysiert werden.  
  Es passt sich an Änderungen in Geschäftskalendern, Wochenenden oder Monatsend-Spitzen an.

- **User-Defined Schedules**  
  Benutzer können erwartete Lieferzeiten explizit definieren (z. B. *an jedem Werktag vor 07:30 Uhr*).  
  digna vergleicht die tatsächliche Ankunftszeit mit dem geplanten Zeitplan und löst Warnungen aus, wenn Daten verspätet oder fehlend sind.

### Detection Mechanism
- Bewertet **Metadaten-Zeitstempel**, **Datensatzanzahlen** und **Tabellenfreshness**  
- Erkennt **hängende ETL-Jobs**, **fehlgeschlagene Extraktionen** und **partielle Dateiankünfte**  
- Integriert sich mit *Data Anomalies* und *Data Validation* für kombinierte Erkenntnisse

---

## Detection Scenarios

| Scenario | Description |
|-----------|--------------|
| **Late data arrival** | Täglicher Marktdatenfeed ist um zwei Stunden verspätet, wodurch Berichte SLAs verpassen |
| **Missing load** | Eine geplante Tabelle oder Partition wurde für das aktuelle Datum nicht aktualisiert |
| **Chained dependency delay** | Verzögerung eines Upstream-Jobs beeinträchtigt die Aktualisierung der nachgelagerten Pipeline |
| **Weekend pattern shift** | Das KI-Modell passt sich automatisch an, wenn sonntags keine Daten erwartet werden |

---

## Architecture and Execution

- **In-database execution:** digna führt Timeliness-Checks direkt in Ihrer Datenbank oder Ihrem Data Warehouse aus.  
- **Lightweight metadata access:** liest Job-Zeitstempel, Datensatzanzahlen und Partitioninformationen — keine Datenextraktion erforderlich.  
- **Configurable frequency:** planen Sie die Überwachung pro Datensatz, Schema oder Pipeline.  
- **Cross-module alerts:** Ergebnisse können visuelle Warnungen im *Inspection Hub* auslösen oder Benachrichtigungen per E-Mail, Slack oder API senden.  

---

## Example Use Cases

- **Financial Market Feeds:** Verzögerungen bei Preis- oder Handelsdatenupdates erkennen.  
- **Data Warehouse Loads:** Überwachen, wenn nächtliche ETL-Jobs später als erwartet abgeschlossen werden.  
- **Data Sharing Between Teams:** Sicherstellen, dass teaminterne Datenlieferungen vor täglichen Cutoffs erfolgen.  
- **Regulatory Reporting:** Bestätigen, dass Einreichungen den neuesten verfügbaren Datensnapshot enthalten.  

---

## Benefits

| Area | Benefit |
|------|----------|
| **Business Continuity** | Verhindert Betriebsstörungen durch verspätete oder fehlende Daten |
| **Data Quality** | Erhöht die Zuverlässigkeit und Konsistenz von Datenpipelines |
| **Compliance** | Stellt SLA-Einhaltung und Prüftransparenz sicher |
| **Automation** | KI eliminiert manuelle Nachverfolgung von Zeitplänen |
| **Integration** | Arbeitet nahtlos mit *Data Analytics* zusammen, um Timeliness-Trends über die Zeit zu visualisieren |

---

## How digna Learns Expected Delivery Times

1. **Historical Analysis:** digna beobachtet frühere Ladezeiten und Laufzeiten.  
2. **AI Modeling:** Maschinelles Lernen erstellt eine dynamische Basislinie für die erwartete Ankunft.  
3. **Monitoring:** Jede neue Lieferung wird mit der Basislinie verglichen.  
4. **Alerting:** Abweichungen lösen Alerts mit kontextbezogenen Metriken und Vertrauensscores aus.  

Dieser kontinuierliche Lernansatz passt sich an sich entwickelnde Prozesse an und hält gleichzeitig die Anzahl falsch-positiver Meldungen gering.

---

## Frequently Asked Questions

**Can I define my own delivery times?**  
Ja. digna unterstützt sowohl feste Benutzerschedules als auch AI-gelernte Muster.

**Can it integrate with my ETL or orchestration tool?**  
Ja. digna integriert sich mit Werkzeugen wie Airflow, dbt, Informatica oder benutzerdefinierten Scheduler-Lösungen.

**Where does computation happen?**  
Alle Analysen laufen in Ihrer Datenbank oder Ihrem Cloud-Warehouse — es wird kein externer Service verwendet.

**What happens when data is late?**  
digna löst Alerts im Dashboard, im Inspection Hub sowie über API/Webhooks aus, um Operationsteams sofort zu informieren.

---


**digna Data Timeliness** hilft, **Vertrauen in Daten** zu gewährleisten, indem es **KI-gesteuerte Erkennung**, **On-Premises-Ausführung** und **Daten-Observability** kombiniert — alles innerhalb Ihrer kontrollierten Umgebung.