---
title: digna Release 2025.09 | Modulares Design, fünf neue Module, MFA via OIDC
description: Erfahren Sie, was neu ist in digna Release 2025.09. Diese Version führt eine modulare Architektur, fünf neue Module, MFA via OIDC und pro Modul Benachrichtigungen ein.
keywords: digna Release 2025.09, digna Änderungsprotokoll, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modulares Design, digna OIDC MFA
image: /assets/logo_square.png
---

# Änderungsprotokoll – Release 2025.09  

Mit Release 2025.09 führt digna eine neue **modulare Architektur** ein und bringt **fünf spezialisierte Module** für Datenqualität und Observability.  
Diese Version stärkt außerdem die Authentifizierung und verbessert das Benachrichtigungsmanagement über die gesamte Plattform.  

---

## Neue Funktionen  

### Modulares Design  
- digna folgt jetzt einer **modularen Architektur**.  
- Kundinnen und Kunden können nur die Module aktivieren, die sie benötigen, und bei steigendem Bedarf weitere hinzufügen.  
- Frühere Funktionalität ist jetzt Teil von **digna Data Anomalies**.  

### Neue Module  
- **digna Data Anomalies** – KI-gestützte Erkennung von Anomalien in Datenvolumina, Verteilungen und fehlenden Werten.  
- **digna Data Analytics** – Zeitreihenanalyse von Observability-Metriken zur Erkennung langfristiger Trends und Volatilität.  
- **digna Data Timeliness** – Überwachung der erwarteten Ankunftszeiten von Daten, sowohl KI-basiert als auch regelbasiert.  
- **digna Data Validation** – Regelbasierte Prüfungen auf Datensatzebene zur Sicherstellung der Einhaltung von Geschäftsregeln.  
- **digna Data Schema Tracker** – Erkennung von Schemaänderungen (DDL-Änderungen) in überwachten Datenbanken.  

### MFA über OIDC  
- Unterstützung für **Multi-Factor Authentication (MFA)** mit OIDC Single Sign-On.  
- Gewährleistet Sicherheit auf Unternehmensniveau für alle Benutzeranmeldungen.  

### Benachrichtigungs-E-Mails pro Modul  
- Benachrichtigungen werden jetzt **pro Modul** versendet, wodurch es einfacher wird, Alerts von Data Anomalies, Data Analytics und anderen Modulen zu trennen.  

---

## CLI-Updates  

- **Neuer Befehl: `inspect-cancel`** – Inspektionen nach Anfrage-ID abbrechen oder alle aktiven Anfragen beenden.  
- **Neuer Befehl: `check-config`** – Konfigurationsdateien vor dem Start validieren.  
- **Neuer Befehl: `remove-orphans`** – Verwaiste Repository-Einträge bereinigen.  
- **Verbesserter `inspect`-Befehl** – Neue Option `--bypass-backend` (`-bb`) und standardisierte Rückgabecodes (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Dokumentation  
- Neue Anleitungen:  
  - Single Sign-On Integrationsanleitung