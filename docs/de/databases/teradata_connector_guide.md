---
title: Teradata Connector – Datenbankintegration | digna Dokumentation
description: Konfigurieren Sie digna so, dass eine Verbindung zu Teradata über den Python-Treiber teradatasql oder den Teradata ODBC-Treiber hergestellt wird. Unterstützt passwortbasierte Authentifizierung mit DSN- oder DSN-losen Setups.
image: /assets/logo_square.png
---


# Quell-Connector für Teradata

Diese Anleitung beschreibt, wie Sie *digna* so konfigurieren, dass eine Verbindung zu Teradata entweder über den nativen Python-Connector oder über den ODBC-Treiber hergestellt wird.

Sie bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Bibliothek:** `teradatasql`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna* Konfiguration (nativer Treiber)

Geben Sie auf dem Bildschirm **"Create a Database Connection"** die folgenden Informationen an:

```
Name:               Name der Verbindung. Wird zur Referenzierung der Verbindung in anderen Bildschirmen verwendet.
Technology:         Teradata
Host Address:       Servername oder IP-Adresse
Host Port:          Portnummer, z. B. 1025
Database Name:      Kann leer gelassen werden. digna behandelt Datenbanken als Schemas für Teradata.
User Name:          Datenbank-Benutzername
User Password:      Passwort des Benutzers
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den geprüften Tag werden in eine permanente Tabelle kopiert und die Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und die Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in dieses Schema gelegt.
Use ODBC:           Deaktiviert (Standard)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine breitere Palette an Authentifizierungs- und Konnektivitätsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf die passwortbasierte Authentifizierung mit dem Treiber **Teradata Database ODBC Driver 20.00**.

### 1. ODBC-Treiber installieren

Installieren Sie den Treiber **Teradata Database ODBC Driver 20.00** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. ODBC-Datenquelle konfigurieren

Gehen Sie wie folgt vor, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Schritt 1](images/teradata/create_odbc_data_source_step1.png)

Klicken Sie auf die Schaltfläche **Test**.

#### Schritt 2
![Schritt 2](images/teradata/create_odbc_data_source_step2.png)

Geben Sie Benutzername und Passwort ein.

Klicken Sie auf die Schaltfläche **OK**.  
Wenn Sie den Erfolgsbildschirm sehen, ist ODBC korrekt konfiguriert.

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder mit einem **DSN (Data Source Name)** oder in einem **DSN-losen** Setup.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Geben Sie auf dem Bildschirm **"Create a Database Connection"** die folgenden Informationen an:

```
Name:               Name der Verbindung. Wird zur Referenzierung der Verbindung in anderen Bildschirmen verwendet.
Technology:         Teradata
Database Name:      Kann leer gelassen werden. digna behandelt Datenbanken als Schemas für Teradata.
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den geprüften Tag werden in eine permanente Tabelle kopiert und die Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und die Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in dieses Schema gelegt.
Use ODBC:           Aktiviert
```

#### ODBC Properties

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "Ihr Datenbank-Benutzer"
name: "PWD",        value: "Ihr Datenbank-Passwort"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-loses Setup

#### *digna* Konfiguration

Geben Sie auf dem Bildschirm **"Create a Database Connection"** die folgenden Informationen an:

```
Name:               Name der Verbindung. Wird zur Referenzierung der Verbindung in anderen Bildschirmen verwendet.
Technology:         Teradata
Database Name:      Kann leer gelassen werden. digna behandelt Datenbanken als Schemas für Teradata.
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den geprüften Tag werden in eine permanente Tabelle kopiert und die Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und die Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in dieses Schema gelegt.
Use ODBC:           Aktiviert
```

#### ODBC Properties

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "Ihr Servername oder Ihre IP-Adresse"
name: "UID",        value: "Ihr Datenbank-Benutzer"
name: "PWD",        value: "Ihr Datenbank-Passwort"
```