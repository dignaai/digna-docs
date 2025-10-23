---
title: digna Release 2024.12 | Änderungsprotokoll & Neue Funktionen
description: Entdecken Sie, was neu ist in digna Release 2024.12. Diese Version führt einen integrierten Scheduler, PDF-Berichte, flexible Custom-Spalten, dynamische Snapshot-Query-Platzhalter und eine intelligentere Schwellenwertoptimierung ein, um Anomalieerkennung und Datenqualitätsüberwachung zu verbessern.
keywords: digna Release 2024.12, digna Änderungsprotokoll, Release Notes, built-in scheduler, PDF-Berichte, custom column type, snapshot query placeholders, threshold optimization, Datenobservability, Datenqualitätsüberwachung, Anomalieerkennung
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Changelog – Release 2024.12

Das Release 2024.12 liefert eine neue Reihe von Features und Verbesserungen, die digna automatisierter, flexibler und einsatzbereiter für den Business-Kontext machen.  
Diese Version verbessert Scheduling, Reporting, Query-Verarbeitung und die Genauigkeit der Anomalieerkennung.  

---

## Neue Funktionen

### Integrierter Scheduler
Inspektionen sind nicht mehr ausschließlich von der Kommandozeile oder API-Aufrufen abhängig.  
Mit dem **neuen digna Scheduler** können Inspektionen automatisch zu definierten Zeiten ausgeführt werden.  

- Unterstützt **Cron-Ausdrücke** für wiederkehrende Zeitpläne (täglich, wöchentlich oder benutzerdefinierte Intervalle).  
- Bietet präzise Steuerung durch **Offsets**, **Startdaten** und **Enddaten**.  
- Ermöglicht Teams, sicherzustellen, dass alle kritischen Datenquellen konsistent und ohne manuellen Aufwand geprüft werden.  

---

### Berichte im PDF-Format
Teams können Ergebnisse jetzt einfach mit Stakeholdern teilen – über **PDF-Exporte**.  

- Diagramme, Metriken und Anomalieergebnisse können in einem professionellen PDF-Format exportiert werden.  
- Berichte kombinieren **Visualisierungen** und **zugrundeliegende Daten**, um sowohl technische als auch geschäftliche Nutzer zu bedienen.  
- Eliminieren die Notwendigkeit externer Tools zur Berichtserstellung.  

---

### Neuer Spaltentyp: `CUSTOM`
Um mehr Flexibilität zu bieten, führt digna einen neuen **`CUSTOM` Spaltentyp** ein.  

- Nutzer können genau definieren, welche **Statistiken und Metriken** auf bestimmte Attribute angewendet werden.  
- Ideal für Sonderfälle, die nicht in Standardkategorien wie NUMERICAL oder CATEGORICAL passen.  
- Hilft dabei, Analysen fokussiert zu halten und Ergebnisse im Geschäftskontext relevant zu machen.  

---

### Neue Platzhalter in Snapshot-Queries
Snapshot-Queries sind jetzt einfacher und weniger fehleranfällig dank **dynamischer Platzhalter**.  

- Tokens wie `#date+n#` oder `#date-n#` passen Datumsangaben in Queries automatisch an.  
- Beispiel:  
  - `#date+1#` → morgen  
  - `#date-2#` → vor zwei Tagen  
- Eliminieren manuelle Datumsberechnungen und sorgen für Konsistenz innerhalb von Teams.  

---

### Schwellenwert-Optimierung
Anomalie-Schwellenwerte sind jetzt intelligenter und kontextsensitiver.  

- Für Metriken wie **NULL COUNT** werden niedrigere Schwellenwerte automatisch auf **0** begrenzt.  
- Verhindert ungültige oder sinnlose Schwellenwerte.  
- Führt zu weniger False Positives und zuverlässigerer Anomalieerkennung.  

---

## Allgemeine Verbesserungen
- Verfeinerte **UI-Komponenten** in den Ansichten für Projekt- und Attributkonfiguration.  
- Verbesserte **Dashboard-Performance** bei großen Datenmengen.  
- Erweiterte **Logging- und Fehlermeldungen** zur Fehlerbehebung.  

---

## Zusammenfassung
Release 2024.12 stärkt digna als Plattform für **Datenqualität, Anomalieerkennung und Observability**.  
Mit Automatisierung durch Scheduling, teilbaren PDF-Berichten, anpassbaren Spalten, vereinfachten Snapshot-Queries und intelligenteren Schwellenwerten wird digna für technische Anwender und Business-Stakeholder noch wertvoller.