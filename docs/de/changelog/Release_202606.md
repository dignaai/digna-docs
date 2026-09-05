---
title: digna Release 2026.06 | Python SDK, Docker-Bereitstellung & Erweiterte Validierungsverwaltung
description: Erfahren Sie, was neu ist in digna Release 2026.06. Diese Version führt das neue digna Python SDK, Docker-Bereitstellungsunterstützung, ein überarbeitetes Dashboard-Erlebnis und erweiterte Import-/Export-Funktionen für Validierungsregeln ein.
keywords: digna Release 2026.06, digna Python SDK, digna Docker-Unterstützung, Automatisierung der Datenqualität, Datenprofiling, Import/Export von Validierungsregeln, digna Dashboard, Data Observability Platform, Python-API, Metadaten-Automatisierung
image: /assets/logo_square.png
---

# Änderungsprotokoll – Release 2026.06  

Mit Release 2026.06 macht digna einen großen Schritt nach vorn in den Bereichen Automatisierung, Erweiterbarkeit und Plattformbenutzbarkeit.  
Dieses Release führt das neue **digna Python SDK**, offizielle **Docker-Bereitstellungsunterstützung**, ein überarbeitetes Dashboard-Erlebnis und eine verbesserte Portabilität für das Management von Validierungsregeln ein.

---

## Neue Funktionen  

### digna Python SDK – Automatisieren Sie alles mit Python  
- Installieren via:
  ```bash
  pip install digna-sdk
  ```
- Programmgesteuerte Verwaltung und Automatisierung von digna mit Python  
- Projekte per Code erstellen und konfigurieren  
- Inspektionen und Monitoring-Ausführungen auslösen  
- Datasets, Regeln und Konfigurationen programmgesteuert verwalten  
- Tabellen profilieren und Metadaten-Einblicke extrahieren  
- Profiling- und Data-Quality-Ergebnisse in externe Repositories und Systeme exportieren  
- Integration mit Notebooks, Orchestrierungs-Tools und CI/CD-Pipelines  

**Auswirkung:** Ermöglicht vollständiges Infrastructure-as-Code und tiefe Automatisierung von Data-Quality- und Observability-Workflows mit Python.

---

### Docker-Unterstützung – Vereinfachte Bereitstellung & Betrieb  
- Offizielle Docker-Image-Unterstützung für digna  
- Schnelle und konsistente Einrichtung über Umgebungen hinweg  
- Vereinfachtes Onboarding für Entwicklung, Test und Produktion  
- Einfache Integration mit Kubernetes und Container-Plattformen  
- Verbesserte Portabilität und Reproduzierbarkeit von Deployments  

**Auswirkung:** Macht digna leichter in modernen cloud-nativen Architekturen bereitstell- und betreibbar.

---

### QueryMode – Flexible SQL-Ausführungsstrategie

Konfigurieren Sie die Abfrageausführungsstrategie: **Single** oder **Combined** Modus

**Single-Modus**: Jede Statistik wird mit einer eigenen dedizierten SQL-Abfrage berechnet

  - Ideal für große Datenquellen, bei denen Speicherbeschränkungen eine Rolle spielen  
  - Verhindert Ressourcenerschöpfung durch kombinierte Abfragen (Out-of-Memory, Spool-Limits)  
  - Höhere Anzahl an Abfragen, aber geringere Speicherbelastung pro Abfrage

**Combined-Modus**: Alle Statistiken werden innerhalb einer einzigen SQL-Abfrage berechnet

  - Reduziert die Gesamtanzahl der Abfragen und den Netzwerk-Overhead  
  - Optimiert die Performance, wenn Datenquellen im Speicher handhabbar sind  
  - Effizienter bei häufigen, parallelen Ausführungen

**Auswirkung:** Gibt Nutzern feingranulare Kontrolle über die Abfrageausführung, um Performance, Ressourcennutzung und Speicher-Sicherheit basierend auf den Eigenschaften ihrer Datenquelle auszubalancieren.

---

### Überarbeitetes Dashboard-Erlebnis  
- Modernisiertes und verbessertes UI/UX-Design  
- Klarere Navigation und Struktur  
- Bessere Sichtbarkeit von Monitoring-Ergebnissen und Data-Quality-Einblicken  
- Verbesserte Lesbarkeit von Alerts, Statistiken und Dashboards  
- Schnellere Zugriffsmöglichkeiten auf wichtige betriebliche Informationen  

**Auswirkung:** Steigert die Benutzerfreundlichkeit und die tägliche Produktivität für alle Nutzer.

---

### Erweiterter Import & Export für Validierungsregeln  
- Verbesserte Import-/Export-Funktionalität für Validierungsregeln  
- Einfachere Migration zwischen Umgebungen und Projekten  
- Bessere Wiederverwendung standardisierter Regelsets  
- Verbesserte Governance und Lifecycle-Management von Regeln  
- Vereinfachte Zusammenarbeit zwischen Teams  

**Auswirkung:** Ermöglicht skalierbare und konsistente Data-Quality-Governance im gesamten Unternehmen.

---

## Plattformverbesserungen  

- Vollständige Integration des Python SDKs für Automatisierung  
- Containerisierte Bereitstellung via Docker  
- Verbesserte UX durch das überarbeitete Dashboard  
- Erweiterte Portabilität der Validierungslogik  

---

## Wer profitiert von dieser Version  

- Data Engineers: Automatisierung, SDK-Nutzung, Pipeline-Integration  
- Plattform-Teams: Vereinfachte Bereitstellung via Docker  
- Data-Governance-Teams: Wiederverwendbares Management von Validierungsregeln  
- Analytics-Teams: Verbesserte Usability und bessere Sichtbarkeit von Insights  

---

## CLI-Aktualisierungen  
- SDK-Integrationsunterstützung hinzugefügt  
- Verbesserte Import-/Export-Workflows  
- Allgemeine Stabilitäts- und Performance-Verbesserungen