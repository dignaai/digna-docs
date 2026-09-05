---
title: Databricks Connector (Legacy, ohne Unity Catalog) | digna Dokumentation
description: Konfigurieren Sie digna, um eine Verbindung zu Databricks ohne Unity Catalog entweder mit dem nativen Python-Connector oder dem Simba Spark ODBC-Treiber herzustellen. Unterstützt tokenbasierte Authentifizierung und flexible Konnektivität.
image: /assets/logo_square.png
---

# Quell-Connector für Databricks – ohne Unity Catalog

Diese Anleitung beschreibt, wie Sie *digna* so konfigurieren, dass eine Verbindung zu Databricks entweder über den nativen Python-Connector oder den ODBC-Treiber hergestellt wird.

Es bezieht sich auf den Bildschirm **„Datenbankverbindung erstellen“**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Bibliothek:** `databricks-sql-connector`  
**Unterstützte Authentifizierung:** nur Personal Access Token (PAT)

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### Personal Access Token (PAT)

Zur Authentifizierung mit einem Personal Access Token lesen Sie bitte die offizielle Databricks-Dokumentation:  
[Wie Sie ein PAT erhalten](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna*-Konfiguration (nativer Treiber)

Geben Sie die folgenden Informationen im Bildschirm **„Datenbankverbindung erstellen“** an:

```
Name:               Name der Verbindung. Diese wird in anderen Bildschirmen zur Referenz verwendet.
Technologie:        Databricks (Legacy)
Host-Adresse:       Databricks-Hostname, z. B. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host-Port:          443
Datenbankname:      Dieser Parameter wird bei Databricks ohne Unity Catalog nicht verwendet
Benutzername:       HTTP-Pfad, der von Databricks bereitgestellt wird, z. B. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
Benutzerpasswort:   Personal Access Token, z. B. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Profiling-Modus:    Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den untersuchten Tag werden in eine permanente Tabelle kopiert und Metriken auf diesen kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
ODBC verwenden:     Deaktiviert (Standard)
```

---

## ODBC-Treiber

Der ODBC-Treiber unterstützt eine breitere Palette an Authentifizierungs- und Konnektivitätsoptionen. Dieser Abschnitt konzentriert sich auf tokenbasierte Authentifizierung mit dem **Simba Spark ODBC Driver**.

### 1. Installieren des ODBC-Treibers

Installieren Sie den **Simba Spark ODBC Driver** gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. Konfigurieren der ODBC-Datenquelle

Befolgen Sie diese Schritte, um eine neue ODBC-Datenquelle mit einem Personal Access Token zu konfigurieren:

#### Schritt 1
![Schritt 1](images/databricks/create_odbc_data_source_step1.png)

#### Schritt 2
![Schritt 2](images/databricks/create_odbc_data_source_step2.png)

#### Schritt 3
![Schritt 3](images/databricks/create_odbc_data_source_step3.png)

#### Schritt 4
![Schritt 4](images/databricks/create_odbc_data_source_step4.png)

#### Schritt 5 – Verbindung testen

Klicken Sie auf die **TEST**-Schaltfläche. Eine erfolgreiche Verbindung sieht etwa so aus:

![Schritt 5](images/databricks/create_odbc_data_source_step5.png)

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung entweder mit einem **DSN (Data Source Name)** oder einer **DSN-losen** Konfiguration verwendet wird.

---

### A. DSN-basierte Konfiguration

#### *digna*-Konfiguration

Geben Sie im Bildschirm **„Datenbankverbindung erstellen“** Folgendes an:

```
Name:               Name der Verbindung. Diese wird in anderen Bildschirmen zur Referenz verwendet.
Technologie:        Databricks (Legacy)
Datenbankname:      Dieser Parameter wird bei Databricks ohne Unity Catalog nicht verwendet
Profiling-Modus:    Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den untersuchten Tag werden in eine permanente Tabelle kopiert und Metriken auf diesen kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
ODBC verwenden:     Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DSN",    value: "*digna*data_databricks"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-losen Konfiguration

#### *digna*-Konfiguration

Geben Sie im Bildschirm **„Datenbankverbindung erstellen“** Folgendes an:

```
Name:               Name der Verbindung. Diese wird in anderen Bildschirmen zur Referenz verwendet.
Technologie:        Databricks (Legacy)
Datenbankname:      Dieser Parameter wird bei Databricks ohne Unity Catalog nicht verwendet
Profiling-Modus:    Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den untersuchten Tag werden in eine permanente Tabelle kopiert und Metriken auf diesen kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
ODBC verwenden:     Aktiviert
```

#### ODBC-Eigenschaften

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```