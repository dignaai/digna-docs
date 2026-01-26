---
title: digna Release 2026.01 | Logische Datasources, Globale Verbindungen & Erweiterte Data Validation
description: Erfahren Sie, was neu ist in digna Release 2026.01. Diese Version führt globale Datenbankverbindungen, logische Datasources, Bedingungen zur Relevanz von Anomalien, CSV-Exporte und erweiterte Data Validation einschließlich Referential-Integrity-Prüfungen ein.
keywords: digna Release 2026.01, digna changelog, digna datasource, digna database connections, digna Data Anomalies, digna Data Validation, referential integrity validation, data quality rules, data observability, digna CSV export
image: /assets/logo_square.png
---

# Changelog – Release 2026.01  

Mit Release 2026.01 bringt digna wesentliche Verbesserungen im Datasource-Modelling, im Connection-Management und in der Benutzbarkeit von Inspektionen.  
Dieses Release erhöht die Flexibilität in allen Modulen und erweitert die **Abdeckung von Datenqualität und Validierung** deutlich.

---

## 🚀 Neue Features  

### Globale Datenbankverbindungen  
- Datenbankverbindungen werden jetzt auf einer **globalen Ebene** konfiguriert.  
- Globale Verbindungen können in **allen Projekten** wiederverwendet werden, was Konfiguration und Wartung vereinfacht.  
- **Auswirkung:** Reduziert den Betriebsaufwand und gewährleistet konsistente Konnektivität über Umgebungen hinweg.

### Mehrere Quellverbindungen pro Projekt  
- Projekte können nun **mehrere Quell-Verbindungskonfigurationen** referenzieren.  
- Ermöglicht flexiblere Setups für komplexe Datenlandschaften innerhalb eines Projekts.  
- **Auswirkung:** Unterstützt realistische Unternehmensarchitekturen mit heterogenen Datenquellen.

### Logische Datasources  
- Datasources repräsentieren jetzt eine **logische Schicht** innerhalb eines Projekts.  
- Jede Datasource kann unterstützt werden durch:
    - eine **Datenbanktabelle**
    - eine **Datenbank-View**
    - eine **benutzerdefinierte SQL-Abfrage**  
- Diese Trennung verbessert Wiederverwendung, Klarheit und das Inspektionsmodell über die Module hinweg.  
- **Auswirkung:** Entkoppelt Inspektionen und Data-Quality-Regeln von der physischen Speicherung, verbessert Wartbarkeit und Wiederverwendbarkeit.

### Bedingung zur Relevanz von Anomalien  
- Eine **Bedingung zur Relevanz von Anomalien** kann nun definiert werden, um die Bewertung des Anomalie-Status auf Datensatzebene zu steuern.  
- Statistiken werden unabhängig davon berechnet, ob die Bedingung gesetzt oder erfüllt ist.  
- Wenn die Bedingung **nicht erfüllt** ist, liefert **digna Data Anomalies** keinen Anomalie-Status (grün / gelb / rot).  
- **Beispiel:** Schließe das Dataset von der Anomalie-Bewertung aus, wenn die Anzahl der Datensätze unter 10 liegt.  
- **Auswirkung:** Stellt sicher, dass Anomalien nur in relevanten fachlichen Kontexten bewertet werden.

### Pro-Modul Benachrichtigungskonfiguration  
- Benachrichtigungen können jetzt **pro Modul** direkt in digna konfiguriert werden.  
- Ermöglicht unabhängige Steuerung des Alarmverhaltens für **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** und andere Module.  
- **Auswirkung:** Erlaubt präzise Alarmierungsstrategien, abgestimmt auf Teamverantwortlichkeiten und Kritikalität.

### Export von Inspektionsergebnissen (CSV)  
- Benutzer können Inspektionsergebnisse nun als **CSV-Dateien herunterladen**.  
- Ermöglicht Offline-Analysen, Berichterstattung und Integration mit externen Tools.  
- **Auswirkung:** Vereinfacht Prüfungen, Reporting und nachgelagerte Datenqualitäts-Analysen.

---

## 🧪 Erweiterte Data Validation-Fähigkeiten  

Mit diesem Release unterstützt **digna Data Validation** jetzt ein umfassendes Set an Data-Quality-Regeln:

- **Zeilenbasierte Validierungsregeln**  
- **Mehrspaltige Eindeutigkeitsprüfungen**  
- **Referentielle Integritätsprüfungen über Datasources hinweg**

Diese Prüfungen zusammen ermöglichen die Durchsetzung von **strukturellen und relationalen Datenqualitätsregeln** über komplexe Datenlandschaften hinweg.

### Eindeutigkeitsprüfungen für mehrere Spalten
- Einführung von **Eindeutigkeitsprüfungen** für eine konfigurierbare **Menge von Spalten**.  
- Ermöglicht die Validierung zusammengesetzter Schlüssel und fachlicher Eindeutigkeitsbedingungen.  
- **Auswirkung:** Erkennt doppelte fachliche Entitäten, die mit Einzelspaltenprüfungen nicht identifizierbar sind.

### Referential-Integrity-Prüfungen
- Einführung von **Referential-Integrity-Prüfungen**, um Beziehungen zwischen Datasources zu validieren.  
- Stellt sicher, dass **Fremdschlüsselwerte** in einer Quell-Datasource in der referenzierten Ziel-Datasource existieren.  
- Hilft, verwaiste Datensätze, gebrochene Beziehungen und Inkonsistenzen frühzeitig zu erkennen.  
- Konzipiert zur Verwendung mit **logischen Datasources**, einschließlich Views und benutzerdefinierter SQL-Abfragen.  
- **Anwendungsfälle:** Data-Warehouse-Integrität, regulatorische Berichterstattung, Stammdaten-Konsistenz und verlässliche nachgelagerte Analysen.

---

## 🎯 Wer profitiert von diesem Release  

- **Data Engineers:** Flexibleres Datasource-Modelling und wiederverwendbare Datenbankverbindungen  
- **Data Quality & Governance Teams:** Erweiterte Validierungsabdeckung einschließlich relationaler Integritätsregeln  
- **Analytics & BI Teams:** Sauberere Eingabedaten und exportierbare Inspektionsergebnisse  
- **Platform Owners:** Reduzierte Konfigurationskomplexität und verbesserte operative Wartbarkeit

---

## 🛠 CLI-Updates  
- Keine Änderungen

---