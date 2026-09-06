# Data Schema Tracker – Schema-Entwicklung überwachen

---

## Zweck

Der **Data Schema Tracker** informiert Sie darüber, wie sich Ihre Datenbankstrukturen entwickeln.  
Er überwacht kontinuierlich **Tabellen-Schemata, Spalten und Datentypen**, um **Schema-Drift** zu erkennen — beabsichtigte oder unbeabsichtigte strukturelle Änderungen, die Pipelines, ETL-Jobs oder BI-Dashboards stören können.

Indem er Transparenz bei der Schema-Entwicklung sicherstellt, hilft digna Organisationen, **Vertrauen in die Datenqualität** zu erhalten, die **Beobachtbarkeit von Datensystemen** aufrechtzuerhalten und kostspielige Produktionsvorfälle zu vermeiden, die durch unentdeckte Schemaänderungen entstehen.

---

## Technische Übersicht

### Was überwacht wird

- **Hinzufügte oder entfernte Spalten** – Erkennt neu eingeführte, umbenannte oder gelöschte Spalten.  
- **Änderungen von Datentypen** – Identifiziert Änderungen wie `INT → VARCHAR` oder `DATE → TIMESTAMP`.  
- **Änderungen an Tabellen und Views** – Verfolgt Erstellung, Umbenennung oder Löschung von Tabellen und Views.  
- **Umgebungsübergreifende Unterschiede** – Vergleicht Schema-Versionen zwischen Dev-, Test- und Produktionsumgebungen.  

### Erkennung & Alarmierung

- Durchsucht **Datenbank-Metadaten** oder **Systemkataloge** direkt innerhalb Ihrer Datenplattform.  
- Vergleicht jeden Schema-Snapshot mit der zuvor bekannten Version, die im digna Observability-Schema gespeichert ist.  
- Erzeugt **Echtzeitwarnungen** im Dashboard, per API oder über externe Benachrichtigungskanäle (E-Mail, Slack, Webhook).  
- Protokolliert jede Schema-Version für **historische Nachverfolgung und Prüfungsbereitschaft**.

---

## Architektur und Ausführung

- **Ausführung innerhalb der Datenbank:** digna läuft vollständig in Ihrer Umgebung und fragt Metadatenansichten ab, ohne irgendwelche Daten zu extrahieren.  
- **Leichtgewichtige Scans:** greift nur auf Strukturinformationen zu — niemals auf Benutzerdaten.  
- **Zentrale Speicherung:** Schema-Metadaten und Drift-Aufzeichnungen werden im digna Observability-Schema für Visualisierung und Analysen gespeichert.  
- **Automatisierung:** unterstützt zeitgesteuerte oder ereignisbasierte Scans über digna Core oder externe Orchestrierungstools.  

---

## Beispielanwendungsfälle

| Anwendungsfall | Beschreibung |
|-----------|--------------|
| **Überwachung der ETL-Stabilität** | Erkennt Änderungen in Upstream-Strukturen, bevor Pipelines aufgrund von Schemainkonsistenzen ausfallen. |
| **Zuverlässigkeit von Business Intelligence** | Verhindert fehlerhafte Dashboards, die durch umbenannte oder fehlende Spalten verursacht werden. |
| **Governance des Data Warehouse** | Erhält eine prüfbare Historie der Schema-Entwicklung für Compliance und Impact-Analysen. |
| **Integrationsüberwachung** | Stellt sicher, dass Data Lake- und Data Warehouse-Schemata nach strukturellen Änderungen synchron bleiben. |

---

## Vorteile

| Bereich | Vorteil |
|------|----------|
| **Datenqualität** | Verhindert unerkannte Schema-Drifts, die Datenpipelines beschädigen oder ungültig machen können. |
| **Beobachtbarkeit** | Ergänzt die Gesamtbeobachtbarkeit von Datenökosystemen um strukturelles Monitoring. |
| **Compliance** | Erhält eine versionierte Schema-Historie für Audit, Rückverfolgbarkeit und Änderungsmanagement. |
| **Prävention** | Erkennt strukturelle Probleme, bevor sie sich auf Reporting oder Produktion auswirken. |

---

## Funktionsweise

1. **Snapshot-Erfassung** – digna erfasst die aktuellen Schema-Metadaten.  
2. **Vergleich** – der neue Snapshot wird verglichen