---
title: digna Release 2024.12 | Änderungsprotokoll & Neue Funktionen
description: Entdecken Sie, was neu ist in digna Release 2024.12. Diese Version führt einen integrierten Scheduler, PDF-Berichte, flexible benutzerdefinierte Spalten, dynamische Platzhalter in Snapshot-Abfragen und intelligentere Schwellenwertoptimierung zur Verbesserung der Anomalieerkennung und Datenqualitätsüberwachung ein.
keywords: digna Release 2024.12, digna changelog, Versionshinweise, integrierter Scheduler, PDF-Berichte, benutzerdefinierter Spaltentyp, Snapshot-Abfrage-Platzhalter, Schwellenwertoptimierung, Datenobservability, Datenqualitätsüberwachung, Anomalieerkennung
image: /assets/logo_square.png
---



# Änderungsprotokoll – Release 2024.12

Das Release 2024.12 bringt eine Reihe neuer Funktionen und Verbesserungen, die digna automatisierter, flexibler und einsatzbereit für das Business machen.  
Diese Version verbessert Planung, Reporting, Abfrageverarbeitung und die Genauigkeit der Anomalieerkennung.  

---

## Neue Funktionen

### Integrierter Scheduler
Inspektionen sind nicht mehr ausschließlich auf die Kommandozeile oder API-Aufrufe angewiesen.  
Mit dem **neuen digna Scheduler** können Inspektionen automatisch zu definierten Zeiten ausgeführt werden.  

- Unterstützt **Cron expressions** für wiederkehrende Zeitpläne (täglich, wöchentlich oder benutzerdefinierte Intervalle).  
- Bietet präzise Steuerung durch **Offsets**, **Startdaten** und **Enddaten**.  
- Ermöglicht Teams, sicherzustellen, dass alle kritischen Datenquellen konsistent und ohne manuellen Aufwand geprüft werden.  

---

### Berichte im PDF-Format
Teams können Ergebnisse jetzt einfach mit Stakeholdern über **PDF-Exporte** teilen.  

- Diagramme, Kennzahlen und Anomalieergebnisse lassen sich im professionellen PDF-Format exportieren.  
- Berichte kombinieren **Visualisierungen** und **zugrundeliegende Daten**, sodass sie sowohl technischen als auch fachlichen Anwendern dienen.  
- Eliminert die Notwendigkeit externer Tools zur Berichtserstellung.  

---

### Neuer Spaltentyp: `CUSTOM`
Um mehr Flexibilität zu bieten, führt digna einen neuen **`CUSTOM`-Spaltentyp** ein.  

- Nutzer können genau definieren, welche **Statistiken und Metriken** auf bestimmte Attribute angewendet werden.  
- Ideal für Sonderfälle, die nicht in Standardkategorien wie NUMERICAL oder CATEGORICAL passen.  
- Hilft dabei, Analysen fokussiert zu halten und Ergebnisse im Geschäftskontext relevant zu machen.  

---

### Neue Platzhalter in Snapshot-Abfragen
Snapshot-Abfragen sind jetzt einfacher und weniger fehleranfällig dank **dynamischer Platzhalter**.  

- Tokens wie `#date+n#` oder `#date-n#` passen Datumsangaben in Abfragen automatisch an.  
- Beispiel:  
  - `#date+1#` → morgen  
  - `#date-2#` → vor zwei Tagen  
- Eliminiert manuelle Datumsberechnungen und sorgt für Konsistenz in den Teams.  

---

### Schwellenwertoptimierung
Anomalieschwellenwerte sind jetzt intelligenter und kontextsensitiver.  

- Für Metriken wie **NULL COUNT** werden untere Schwellenwerte automatisch auf **0** begrenzt.  
- Verhindert ungültige oder sinnfreie Schwellenwerte.  
- Führt zu weniger False Positives und zuverlässigerer Anomalieerkennung.  

---

## Allgemeine Verbesserungen
- Verfeinerte **UI-Komponenten** in Projekt- und Attributkonfigurationsansichten.  
- Verbesserte **Dashboard-Performance** für große Datenvolumina.  
- Erweiterte **Logging- und Fehlermeldungen** zur Fehlerbehebung.  

---

## Zusammenfassung
Das Release 2024.12 stärkt digna als Plattform für **Datenqualität, Anomalieerkennung und Observability**.  
Mit Automatisierung durch Scheduling, teilbaren PDF-Berichten, anpassbaren Spalten, vereinfachten Snapshot-Abfragen und intelligenteren Schwellenwerten wird digna für technische Anwender und Fachbereiche noch wertvoller.