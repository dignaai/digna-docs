# Changelog – Release 2025.09  

Mit Release 2025.09 führt digna eine neue **modulare Architektur** ein und bringt **fünf spezialisierte Module** für Data Quality und Observability.  
Dieses Release stärkt außerdem die Authentifizierung und verbessert das Benachrichtigungsmanagement in der gesamten Plattform.  

---

## Neue Features  

### Modulares Design  
- digna folgt jetzt einer **modularen Architektur**.  
- Kund:innen können nur die Module aktivieren, die sie benötigen, und bei wachsendem Bedarf weitere hinzufügen.  
- Vorherige Funktionalität ist jetzt Teil von **digna Data Anomalies**.  

### Neue Module  
- **digna Data Anomalies** – KI-gestützte Erkennung von Anomalien in Datenvolumen, Verteilungen und fehlenden Werten.  
- **digna Data Analytics** – Zeitreihenbasierte Auswertung von Observability-Metriken zur Erkennung langfristiger Trends und Volatilität.  
- **digna Data Timeliness** – Überwachung erwarteter Datenankunftszeiten, sowohl KI-basiert als auch regelbasiert.  
- **digna Data Validation** – Regelbasierte Prüfungen auf Datensatzebene zur Sicherstellung der Einhaltung von Geschäftsregeln.  
- **digna Data Schema Tracker** – Erkennung von Schemaveränderungen (DDL-Änderungen) in überwachten Datenbanken.  

### MFA via OIDC  
- Unterstützung für **Mehrfaktor-Authentifizierung (MFA)** mit OIDC Single Sign-On.  
- Bietet unternehmensgerechte Sicherheit für alle Benutzeranmeldungen.  

### Benachrichtigungs-E-Mails pro Modul  
- Benachrichtigungen werden jetzt **pro Modul** versendet, wodurch sich Alerts aus Data Anomalies, Data Analytics und anderen Modulen leichter trennen lassen.  

---

## CLI-Updates  

- **Neuer Befehl: `inspect-cancel`** – Inspektionen nach Request-ID abbrechen oder alle aktiven Anfragen beenden.  
- **Neuer Befehl: `check-config`** – Konfigurationsdateien vor dem Start validieren.  
- **Neuer Befehl: `remove-orphans`** – Verwaiste Repository-Einträge bereinigen.  
- **Verbesserter `inspect`-Befehl** – Neue Option `--bypass-backend` (`-bb`) und standardisierte Rückgabecodes (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Dokumentation  
- Neue Anleitungen:  
  - Single Sign-On-Integrationsanleitung