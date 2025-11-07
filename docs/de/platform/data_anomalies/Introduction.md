---
title: Data Anomalies – Automatisierte Erkennung
description: Erfahren Sie, wie digna Data Anomalies automatisch Volumenabfälle, fehlende Werte, Verteilungsschwankungen und unerwartete Muster erkennt, ohne manuelle Regeln zu schreiben. Verbessern Sie die Datenqualität und die Observability von Datenpipelines mit KI-gestützter Anomalieerkennung.
image: /assets/logo_square.png
keywords:
  - Datenanomalien
  - KI-Anomalieerkennung
  - Überwachung der Datenqualität
  - Datenqualität
  - Daten-Observability
  - Erkennung fehlender Daten
  - Überwachung des Datenvolumens
  - Verteilungsdrift
  - Datenverlässlichkeit
  - digna data anomalies
lang: de
robots: index, follow
og_title: Data Anomalies – Automatisierte Erkennung | digna Documentation
og_description: digna Data Anomalies erkennt automatisch Unregelmäßigkeiten im Datenvolumen, in Werten und Verteilungen ohne manuelle Regeln — und verbessert so Datenqualität und Observability plattformübergreifend.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Anomalies – Automatisierte Erkennung
<h1 style="display:none;">KI-gesteuertes Modul für Datenqualität und Observability – digna Data Anomalies</h1>

---

## Zweck

Das **Data Anomalies**-Modul identifiziert automatisch Unregelmäßigkeiten in Ihren Datensätzen — ganz ohne Regelprogrammierung.  
Es überwacht kontinuierlich **die Qualität der Datenlieferung**, lernt, wie „normal“ aussieht, und erkennt Abweichungen in Echtzeit.

Durch KI-basierte Erkennung erkennt digna *stille Datenfehler* wie fehlende, duplizierte oder beschädigte Datensätze, die Berichte, ML-Modelle und Dashboards verfälschen können.

---

## Technische Übersicht

### Analysierte Metriken

digna profiliert kontinuierlich die folgenden Aspekte Ihrer Daten:

- **Datensatzvolumen** – Gesamtanzahl der Zeilen, täglich oder batch-basiert  
- **Fehlende Werte** – Erkennung von null- oder leeren Feldern  
- **Verteilungen und Histogramme** – Überwachung von Formänderungen in den Daten  
- **Wertbereiche** – automatische Identifikation von außerhalb liegenden oder extremen Werten  
- **Eindeutigkeit** – Prüfen auf doppelte Schlüssel oder wiederholte Einträge  

### Intelligente Anomalieerkennung

- Nutzt **historisches Lernen**, um erwartete Grenzen dynamisch zu definieren  
- Erkennt Abweichungen in **Volumen, Wertverteilungen oder logischen Beziehungen**  
- Setzt KI ein, um Schwellenwerte automatisch anhand von Tageszeiten oder saisonalen Mustern anzupassen  
- Unterscheidet zwischen **statistischen Schwankungen** und echten Anomalien  
- Liefert detaillierte Metriken und Konfidenzwerte pro Datensatz und Spalte  

---

## Erkennungsszenarien

Nachfolgend Beispiele aus der Praxis, die vom **Data Anomalies**-Modul automatisch erkannt werden:

| Scenario | Description |
|-----------|--------------|
| **Volume drops or spikes** | Fehlende Hälfte der täglichen Transaktionen, doppelte Batch-Ladevorgänge oder plötzliche Datenanstiege |
| **Missing or null values** | Datenextraktionen abgeschlossen, aber kritische Spalten bleiben leer |
| **Distribution drifts** | Durchschnittlicher Einkaufspreis oder Transaktionsanzahl pro Region verändert sich unerwartet |
| **Column swaps** | Spalten wie *first_name* und *last_name* wurden während des ETL versehentlich vertauscht |
| **Unexpected categorical values** | z. B. „Zurich“ erscheint in der Liste österreichischer Städte |
| **Sudden uniqueness loss** | Früher eindeutige IDs beginnen sich aufgrund von fehlerhaften Joins upstream zu duplizieren |

---

## Architektur und Ausführung

- **Ausführung in der Datenbank:** Die gesamte Anomalieerkennungslogik wird *im Datenbank-Engine* ausgeführt (Teradata, Snowflake, Databricks, PostgreSQL usw.)  
- **Keine Datenbewegung:** digna liest nur Metriken und transferiert niemals Rohdaten extern  
- **Inkrementelle Updates:** Pro Lauf werden nur neue Datensegmente analysiert, um effizient zu bleiben  
- **Konfigurierbare Prüfintervalle:** Stündlich, täglich oder durch upstream-Prozesse ausgelöst  
- **Ergebnisablage:** Metriken und Anomalie-Flags werden zurück in dignas Observability-Schema geschrieben zur Visualisierung und Alarmierung  

---

## Vorteile

| Area | Benefit |
|------|----------|
| **Automation** | Eliminierung hunderter manueller SQL- oder Regeldefinitionen |
| **Precision** | Erkennt Probleme, die statische Schwellenwerte oft übersehen |
| **Scalability** | Überwacht effizient Millionen von Datensätzen pro Tabelle |
| **Integration** | Funktioniert nahtlos mit *digna Data Analytics* für Trendanalysen |
| **Compliance** | Sorgt für kontinuierliche Kontrolle über die **Qualität und Observability von Daten** |
| **Transparency** | Bietet Konfidenzwerte, Zeitstempel und Begründungscodes für jede Anomalie |

---

## Wie digna „Normal“ lernt

1. **Profiling-Phase:** digna sammelt Metriken aus historischen Datensätzen.  
2. **Lernphase:** KI-Modelle identifizieren wiederkehrende Muster (saisonal, wöchentlich, täglich).  
3. **Monitoring-Phase:** Zukünftige Datensätze werden mit dynamisch gelernten Schwellenwerten verglichen.  
4. **Alerting-Phase:** Abweichungen außerhalb statistischer Konfidenzgrenzen werden als Anomalien gemeldet.  

Alle Modelle sind erklärbar, deterministisch und für Unternehmensdatenvolumina optimiert.

---

## Beispielanwendungsfälle

- Überwachung der Datenqualität in **Banktransaktionssystemen**  
- Erkennung von Ladefehlern in **ETL- oder Data-Warehouse-Jobs**  
- Identifikation abnormaler Kundenaktivitäten in **Telekommunikationsaufzeichnungen**  
- Überwachung der Konsistenz klinischer Daten in **Healthcare-Analytics-Pipelines**  
- Verhinderung defekter Dashboards in **BI- und Reporting-Umgebungen**

---

## Häufig gestellte Fragen

**Does Data Anomalies require predefined rules?**  
Nein — das Modul lernt das Verhalten der Daten automatisch.

**Can I still define specific thresholds if needed?**  
Ja. digna erlaubt die Kombination von KI-basierter und regelbasierter Erkennung (via *Data Validation*).

**How are false positives minimized?**  
Das Modul verwendet adaptives Lernen und statistische Konfidenzbewertung, um normale saisonale Variationen zu ignorieren.

**Where does computation happen?**  
Alle Verarbeitungen laufen innerhalb Ihrer Datenbank — digna extrahiert niemals Rohdaten.

**Is it suitable for sensitive or regulated data?**  
Ja. digna läuft vollständig on-premises oder in privaten Clouds und entspricht europäischen Compliance-Standards.