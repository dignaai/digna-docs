# Änderungsprotokoll – Release 2026.01  

Mit Release 2026.01 führt digna bedeutende Verbesserungen im Datasource-Modell, im Verbindungsmanagement und in der Benutzbarkeit der Inspektionen ein.  
Dieses Release erhöht die Flexibilität über alle Module hinweg und erweitert deutlich die **Abdeckung von Datenqualität und Validierung**.

---

## Neue Funktionen  

### Globale Datenbankverbindungen  
- Datenbankverbindungen werden nun auf einer **globalen Ebene** konfiguriert.  
- Globale Verbindungen können in **allen Projekten** wiederverwendet werden, was Konfiguration und Wartung vereinfacht.  
- **Auswirkung:** Reduziert den betrieblichen Aufwand und sorgt für konsistente Konnektivität über Umgebungen hinweg.

### Mehrere Quellverbindungen pro Projekt  
- Projekte können jetzt auf **mehrere Quellverbindungs-Konfigurationen** verweisen.  
- Erlaubt flexiblere Setups für komplexe Datenlandschaften innerhalb eines Projekts.  
- **Auswirkung:** Unterstützt realistische Unternehmensarchitekturen mit heterogenen Datenquellen.

### Logische Datasources  
- Datasources repräsentieren jetzt eine **logische Schicht** innerhalb eines Projekts.  
- Jede Datasource kann durch Folgendes hinterlegt sein:
   - eine **Datenbanktabelle**
   - eine **Datenbankansicht**
   - eine **benutzerdefinierte SQL-Anweisung**  
- Diese Trennung verbessert Wiederverwendbarkeit, Klarheit und das Inspektionsmodell über die Module hinweg.  
- **Auswirkung:** Entkoppelt Inspektionen und Regeln zur Datenqualität von der physischen Speicherung und verbessert Wartbarkeit und Wiederverwendung.

### Bedingung zur Relevanz von Anomalien  
- Eine **Bedingung zur Relevanz von Anomalien** kann nun definiert werden, um die Bewertung des Anomalie-Status auf Ebene eines Datensatzes zu steuern.  
- Statistiken werden unabhängig davon berechnet, ob die Bedingung gesetzt oder erfüllt ist.  
- Wenn die Bedingung **nicht erfüllt ist**, liefert **digna Data Anomalies** keinen Anomalie-Status (grün / gelb / rot).  
- **Beispiel:** Schließen Sie den Datensatz von der Anomaliebewertung aus, wenn die Anzahl der Datensätze unter 10 liegt.  
- **Auswirkung:** Stellt sicher, dass Anomalien nur in relevanten Geschäftskontexten bewertet werden.

### Pro-Modul-Benachrichtigungskonfiguration  
- Benachrichtigungen können jetzt **pro Modul** direkt in digna konfiguriert werden.  
- Ermöglicht die unabhängige Steuerung des Alarming-Verhaltens für **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** und andere Module.  
- **Auswirkung:** Ermöglicht präzise Alerting-Strategien, die an Teamverantwortlichkeiten und Kritikalität ausgerichtet sind.

### Export von Inspektionsergebnissen (CSV)  
- Benutzer können Inspektionsergebnisse jetzt als **CSV-Dateien herunterladen**.  
- Ermöglicht Offline-Analyse, Reporting und Integration mit externen Tools.  
- **Auswirkung:** Vereinfacht Audits, Berichterstattung und nachgelagerte Analysen zur Datenqualität.

---

## Erweiterte Möglichkeiten der Datenvalidierung  

Mit diesem Release unterstützt **digna Data Validation** jetzt eine umfassende Menge an Regeln zur Datenqualität:

- **Validierungsregeln auf Zeilenebene**  
- **Mehrspaltige Eindeutigkeitsprüfungen**  
- **Validierung referenzieller Integrität über Datasources hinweg**

Gemeinsam ermöglichen diese Prüfungen die Durchsetzung **struktureller und relationaler Regeln zur Datenqualität** über komplexe Datenlandschaften hinweg.

### Eindeutigkeitsprüfungen für mehrere Spalten
- Eingeführt wurden **Eindeutigkeitsprüfungen** für eine konfigurierbare **Menge von Spalten**.  
- Ermöglicht die Validierung zusammengesetzter Schlüssel und eindeutiger geschäftsbezogener Einschränkungen.  
- **Auswirkung:** Erkennt doppelte Geschäftseinheiten, die mit Einzelspaltenprüfungen nicht identifiziert werden können.

### Prüfungen der referenziellen Integrität
- Eingeführt wurden **Prüfungen der referenziellen Integrität**, um Beziehungen zwischen Datasources zu validieren.  
- Stellt sicher, dass **Fremdschlüsselwerte** in einer Quell-Datasource in der referenzierten Ziel-Datasource existieren.  
- Unterstützt Validierung über:
  - verschiedene Tabellen oder Ansichten  
  - verschiedene Schemata  
  - verschiedene Datenbankverbindungen innerhalb desselben Projekts  
- Hilft dabei, verwaiste Datensätze, gebrochene Beziehungen und Inkonsistenzen frühzeitig zu erkennen.  
- Entwickelt, um mit **logischen Datasources** zu arbeiten, einschließlich Ansichten und benutzerdefiniertem SQL.  
- **Anwendungsfälle:** Datenbank-Integrität im Data Warehouse, regulatorische Berichterstattung, Stammdatenkonsistenz und verlässliche nachgelagerte Analysen.

---

## Wer profitiert von dieser Version  

- **Data Engineers:** Flexibleres Datasource-Modell und wiederverwendbare Datenbankverbindungen  
- **Teams für Datenqualität & Governance:** Erweiterte Validierungsabdeckung einschließlich relationaler Integritätsregeln  
- **Analytics- & BI-Teams:** Sauberere Eingabedaten und exportierbare Inspektionsergebnisse  
- **Platform Owner:** Reduzierte Konfigurationskomplexität und verbesserte operative Wartbarkeit

---

## CLI-Aktualisierungen  
- Keine Änderungen

---