---
title: Data Schema Tracker – Schema‑Evolution überwachen | digna Dokumentation
description: Erfahren Sie, wie digna Data Schema Tracker Spaltenänderungen, Datentyp‑Updates und Schema‑Drift überwacht. Erkennen und alarmieren Sie bei absichtlichen und unbeabsichtigten Schemaänderungen, um ETL‑Ausfälle, fehlerhafte Dashboards und Verlust der Daten‑Observability zu verhindern.
canonical_url: https://docs.digna.ai/platform/data_schema_tracker/
image: /assets/logo_square.png
keywords:
  - data schema tracker
  - Schema‑Drift‑Erkennung
  - Überwachung der Schema‑Evolution
  - Metadaten‑Observability
  - Daten‑Observability
  - Datenqualität
  - Überwachung der Datenstruktur
  - Datenbank‑Metadaten
  - Stabilität von ETL‑Pipelines
  - digna Data Schema Tracker
lang: de
robots: index, follow
og_title: Data Schema Tracker – Schema‑Evolution überwachen | digna Dokumentation
og_description: digna Data Schema Tracker überwacht Schema‑Drift, Datentyp‑Änderungen und Spaltenupdates. Erhalten Sie Benachrichtigungen, bevor ETL‑Pipelines oder Dashboards aufgrund unerwarteter Strukturänderungen ausfallen.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Schema‑Evolution überwachen
<h1 style="display:none;">KI‑gesteuertes Modul für Metadaten‑Observability und Datenqualität – digna Data Schema Tracker</h1>

---

## Zweck

Der **Data Schema Tracker** hält Sie darüber informiert, wie sich Ihre Datenbankstrukturen entwickeln.  
Er überwacht kontinuierlich **Tabellenschemata, Spalten und Datentypen**, um **Schema‑Drift** zu erkennen — absichtliche oder unbeabsichtigte strukturelle Änderungen, die Pipelines, ETL‑Jobs oder BI‑Dashboards stören können.

Indem Transparenz in der Schema‑Evolution sichergestellt wird, hilft digna Organisationen, **Vertrauen in die Datenqualität** zu erhalten, die **Observability von Datensystemen** zu wahren und kostspielige Produktionsvorfälle zu vermeiden, die durch unerkannte Schemaänderungen ausgelöst werden.

---

## Technische Übersicht

### Was es überwacht

- **Hinzugefügte oder entfernte Spalten** – erkennt neu eingeführte, umbenannte oder gelöschte Spalten.  
- **Änderungen von Datentypen** – identifiziert Änderungen wie `INT → VARCHAR` oder `DATE → TIMESTAMP`.  
- **Änderungen an Tabellen und Views** – verfolgt Erstellung, Umbenennung oder Entfernung von Tabellen und Views.  
- **Unterschiede zwischen Umgebungen** – vergleicht Schema‑Versionen zwischen Dev, Test und Production.  

### Erkennung & Benachrichtigung

- Scannt **Datenbank‑Metadaten** oder **Systemkataloge** direkt innerhalb Ihrer Datenplattform.  
- Vergleicht jeden Schema‑Snapshot mit der zuvor bekannten Version, die im digna Observability‑Schema gespeichert ist.  
- Generiert **Echtzeit‑Benachrichtigungen** im Dashboard, über die API oder externe Benachrichtigungskanäle (E‑Mail, Slack, Webhook).  
- Protokolliert jede Schema‑Version zur **historischen Nachverfolgung und Prüfbereitschaft**.

---

## Architektur und Ausführung

- **Ausführung innerhalb der Datenbank:** digna läuft vollständig in Ihrer Umgebung und liest Metadaten‑Views ab, ohne Nutzdaten zu extrahieren.  
- **Leichtgewichtige Scans:** greift nur auf strukturelle Informationen zu — niemals auf Benutzerdaten.  
- **Zentrale Speicherung:** Schema‑Metadaten und Drift‑Aufzeichnungen werden im digna Observability‑Schema für Visualisierung und Analysen abgelegt.  
- **Automatisierung:** unterstützt geplante oder ereignisbasierte Scans über digna Core oder externe Orchestrierungs‑Tools.  

---

## Beispielanwendungsfälle

| Anwendungsfall | Beschreibung |
|----------------|--------------|
| **Überwachung der ETL‑Stabilität** | Erkennt Änderungen in upstream‑Strukturen, bevor Pipelines wegen Schema‑Mismatches ausfallen. |
| **Zuverlässigkeit von Business Intelligence** | Verhindert fehlerhafte Dashboards, die durch umbenannte oder fehlende Spalten entstehen. |
| **Data Warehouse‑Governance** | Pflegt eine prüfbare Historie der Schema‑Evolution für Compliance und Impact‑Analysen. |
| **Integrationsüberwachung** | Stellt sicher, dass Data‑Lake‑ und Warehouse‑Schemata nach Strukturupdates synchron bleiben. |

---

## Vorteile

| Bereich | Vorteil |
|--------|---------|
| **Datenqualität** | Verhindert unerkannte Schema‑Drifts, die Datenpipelines korrumpieren oder ungültig machen können. |
| **Observability** | Ergänzt strukturelles Monitoring zur Gesamt‑Observability von Datenökosystemen. |
| **Compliance** | Bewahrt versionierte Schema‑Historien für Audit, Rückverfolgbarkeit und Change‑Control. |
| **Vorbeugung** | Erkennt strukturelle Probleme, bevor sie sich auf Reporting oder Produktion auswirken. |

---

## Funktionsweise

1. **Snapshot‑Erfassung** – digna nimmt die aktuellen Schema‑Metadaten auf.  
2. **Vergleich** – der neue Snapshot wird verglichen