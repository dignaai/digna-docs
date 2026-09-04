---
title: digna Release 2026.04 | Analytics Chart, Enumerationen & Vorlagen für Validierungsregeln
description: Erfahren Sie, was neu ist in digna Release 2026.04. Diese Version führt erweiterte Zeitreihenanalysen mit dem Analytics Chart, wiederverwendbare Vorlagen für Validierungsregeln, Enumerationen für erlaubte Werte und Relevanzbedingungen auf Spaltenebene ein.
keywords: digna Release 2026.04, digna Änderungsprotokoll, Data Analytics, Zeitreihenanalyse, Regression, Vorlagen für Datenvalidierung, Enumerationen, Validierung erlaubter Werte, Datenqualitätsregeln, Datenbeobachtbarkeit
image: /assets/logo_square.png
---

# Änderungsprotokoll – Release 2026.04  

Mit Release 2026.04 erweitert digna seine Fähigkeiten im Bereich Analytics und Datenvalidierung deutlich.  
Dieses Release führt erweiterte Zeitreihenanalysen, wiederverwendbare Validierungskomponenten und eine zentrale Standardisierung von Werten ein.

---

## Neue Funktionen  

### Analytics Chart – Zeitreihenanalyse ohne Data-Science-Kenntnisse  
- Neues **Analytics Chart** für interaktive Zeitreihenanalysen  
- Eingebaute analytische Methoden:
    - Lineare, quadratische und kubische Regression  
    - Stückweise Regression mit konfigurierbaren Breakpoints  
    - Glättungsverfahren  
    - Quantilanalyse  
- Automatische Erkennung von Trends, Saisonalität und Musteränderungen  
- Residualanalyse für tiefere Einblicke in Abweichungen  
- Zeitreihen werden automatisch für jedes Dataset berechnet  

**Auswirkung:** Ermöglicht es Nutzern, komplexes Datenverhalten über die Zeit zu verstehen, ohne Data-Science-Expertise oder externe Tools zu benötigen.

---

### Enumerationen – Zentrale Definition erlaubter Werte  
- Definieren Sie wiederverwendbare Mengen erlaubter Werte (z. B. Länder, Bundesländer, Statuscodes)  
- Validieren Sie Spaltenwerte anhand vordefinierter Enumerationen in **digna Data Validation**  
- Nutzen Sie Enumerationen projekt- und datenquellenübergreifend wieder  
- Verwenden Sie Enumerationen überall via `#ENUM:MY_ENUM#`  
- Alle Prüfungen werden **direkt in der Quelldatenbank** ausgeführt  

**Auswirkung:** Stellt konsistente und standardisierte Datenwerte in der gesamten Organisation sicher.

---

### Vorlagen für Validierungsregeln – Wiederverwendbare Logik für Datenqualität  
- Definieren Sie wiederverwendbare Validierungsregeln (z. B. Whitespace-Prüfungen, NOT NULL, Formatprüfungen)  
- Wenden Sie Vorlagen auf mehrere Datasets an  
- Stellen Sie konsistente Regel-Logik über Projekte hinweg sicher  
- Reduzieren Sie Duplikation und manuelle Konfiguration  
- Alle Prüfungen werden **direkt in der Quelldatenbank** ausgeführt  

**Auswirkung:** Ermöglicht skalierbare und leistungsfähige Datenvalidierung ohne Datenverschiebung.

---

### Relevanzbedingungen auf Statistik-Ebene  
- Definieren Sie Relevanzbedingungen auf **Spaltenebene für jede Statistik**  
- Erweitert das Konzept der Relevanzbedingungen für Anomalien  
- Steuern Sie, wann eine Statistik als relevant betrachtet werden soll  
- Verringern Sie Störsignale, indem nicht-kritische Situationen ausgeschlossen werden  

**Auswirkung:** Verbessert die Signalqualität, indem nur bedeutende Abweichungen in den Fokus gerückt werden.

---

## Erweiterte Data Analytics- und Validierungsfunktionen  

Mit diesem Release erweitert digna sowohl das **Datenverständnis** als auch die **Standardisierung der Datenvalidierung**:

- Erweiterte **Zeitreiheninterpretation** ohne Data-Science-Wissen  
- Zentrale Definition von **erlaubten Werten via Enumerationen**  
- Wiederverwendbare **Validierungslogik via Vorlagen**  
- Feingranulare Kontrolle über die **Relevanz von Statistiken und Alerts**  

Gemeinsam ermöglichen diese Funktionen Organisationen nicht nur, Probleme zu erkennen, sondern auch **Datenqualität zu verstehen, zu standardisieren und zu steuern**.

---

## Wer profitiert von diesem Release  

- Dateningenieure: Wiederverwendbare Validierungslogik und verbesserte Kontrolle über das Monitoring-Verhalten  
- Teams für Datenqualität und Governance: Standardisierte Regeln und konsistente Datenvalidierung systemübergreifend  
- Analytics- & BI-Teams: Besseres Verständnis von Trends und Abweichungen  
- Plattformverantwortliche: Höhere Adoptionsrate durch vereinfachte Analysen und skalierbare Validierung  

---

## CLI-Updates  
- Keine Änderungen  

---