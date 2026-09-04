---
title: digna Release 2026.06 | Python SDK, Docker-Bereitstellung & Verbesserte Validierungsverwaltung
description: Erfahren Sie, was neu ist in digna Release 2026.06. Diese Version führt das neue digna Python SDK, Docker-Unterstützung für die Bereitstellung, ein überarbeitetes Dashboard und erweiterte Import-/Export-Funktionen für Validierungsregeln ein.
keywords: digna Release 2026.06, digna Python SDK, digna Docker-Unterstützung, Automatisierung der Datenqualität, Datenprofiling, Import/Export von Validierungsregeln, digna-Dashboard, Data Observability Plattform, Python API, Metadaten-Automatisierung
image: /assets/logo_square.png
---

# Changelog – Release 2026.06  

Mit Release 2026.06 macht digna einen großen Schritt nach vorn in den Bereichen Automatisierung, Erweiterbarkeit und Plattform-Benutzbarkeit.  
Dieses Release führt das neue **digna Python SDK**, offizielle **Docker-Unterstützung**, ein überarbeitetes Dashboard-Erlebnis und verbesserte Portabilität für das Management von Validierungsregeln ein.

---

## Neue Funktionen  

### digna Python SDK – Automatisieren Sie alles mit Python  
- Installieren mit:
  ```bash
  pip install digna-sdk
  ```
- digna programmgesteuert mit Python verwalten und automatisieren  
- Projekte per Code erstellen und konfigurieren  
- Inspektionen und Monitoring-Ausführungen auslösen  
- Datensätze, Regeln und Konfigurationen programmgesteuert verwalten  
- Tabellen profilieren und Metadaten-Einblicke extrahieren  
- Profiling- und Data-Quality-Ergebnisse in externe Repositories und Systeme exportieren  
- Integration mit Notebooks, Orchestrierungs-Tools und CI/CD-Pipelines  

**Auswirkung:** Ermöglicht vollständige Infrastructure-as-Code-Workflows und tiefe Automatisierung von Data-Quality- und Observability-Prozessen mit Python.

---

### Docker-Unterstützung – Vereinfachte Bereitstellung & Betrieb  
- Offizielle Docker-Image-Unterstützung für digna  
- Schnelle und konsistente Einrichtung über verschiedene Umgebungen hinweg  
- Vereinfachtes Onboarding für Entwicklung, Test und Produktion  
- Einfache Integration mit Kubernetes und Container-Plattformen  
- Verbesserte Portabilität und Reproduzierbarkeit von Deployments  

**Auswirkung:** Macht digna leichter in modernen cloud-nativen Architekturen zu deployen und zu betreiben.

---

### QueryMode – Flexible SQL-Ausführungsstrategie

Konfigurieren Sie die Query-Ausführungsstrategie: **Single** oder **Combined** Mode

**Single Mode**: Jede Kennzahl wird mit einer eigenen SQL-Abfrage berechnet

  - Ideal für große Datenquellen, bei denen Speicherbeschränkungen relevant sind  
  - Verhindert Ressourcenerschöpfung bei kombinierten Abfragen (Out-of-Memory, Spool-Limits)  
  - Höhere Anzahl an Abfragen, aber geringerer Speicherbedarf pro Abfrage

**Combined Mode**: Alle Kennzahlen werden in einer einzigen SQL-Abfrage berechnet

  - Reduziert die Gesamtanzahl der Abfragen und den Netzwerk-Overhead  
  - Optimiert die Performance, wenn Datenquellen im Speicher handhabbar sind  
  - Effizienter bei häufigen, parallelen Ausführungen

**Auswirkung:** Gibt Anwendern feinkörnige Kontrolle über die Query-Ausführung, um Performance, Ressourcennutzung und Speichersicherheit basierend auf den Eigenschaften ihrer Datenquelle auszubalancieren.

---

### Überarbeitetes Dashboard-Erlebnis  
- Modernisiertes und verbessertes UI/UX-Design  
- Klarere Navigation und Struktur  
- Bessere Sichtbarkeit von Monitoring-Ergebnissen und Data-Quality-Einblicken  
- Verbesserte Lesbarkeit von Alerts, Statistiken und Dashboards  
- Schnellere Zugriffe auf wichtige operative Informationen  

**Auswirkung:** Verbessert die Bedienbarkeit und die tägliche Produktivität aller Anwender.

---

### Erweiterter Import & Export für Validierungsregeln  
- Verbesserte Import-/Export-Funktionalität für Validierungsregeln  
- Einfachere Migration zwischen Umgebungen und Projekten  
- Bessere Wiederverwendbarkeit standardisierter Regelsets  
- Verbesserte Governance und Lifecycle-Management für Regeln  
- Vereinfachte Zusammenarbeit zwischen Teams  

**Auswirkung:** Ermöglicht skalierbare und konsistente Data-Quality-Governance über die gesamte Organisation.

---

## Plattform-Verbesserungen  

- Vollständige Integration des Python SDK für Automatisierung  
- Containerisierte Bereitstellung via Docker  
- Verbesserte UX durch überarbeitetes Dashboard  
- Erweiterte Portabilität der Validierungslogik  

---

## Wer profitiert von diesem Release  

- Data Engineers: Automatisierung, SDK-Nutzung, Pipeline-Integration  
- Plattform-Teams: Vereinfachte Bereitstellung via Docker  
- Data-Governance-Teams: Wiederverwendbares Management von Validierungsregeln  
- Analytics-Teams: Verbesserte Usability und Sichtbarkeit von Insights  

---

## CLI-Updates  
- SDK-Integrationsunterstützung hinzugefügt  
- Verbesserte Import-/Export-Workflows  
- Allgemeine Stabilitäts- und Performance-Verbesserungen