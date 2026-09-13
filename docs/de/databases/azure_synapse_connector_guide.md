---
title: Azure-Synapse-Connector – Datenbankintegration | digna Dokumentation
description: Konfigurieren Sie digna für die Verbindung zu Azure Synapse Analytics über ODBC mit einer DSN-losen Verbindungszeichenfolge. Unterstützt serverlose und dedizierte SQL-Pools, mit den erforderlichen ODBC-Eigenschaften und den Verbindungseinstellungen auf digna-Seite.
image: /assets/logo_square.png
---


# Quell-Connector für Azure Synapse Analytics

Diese Anleitung beschreibt, wie Sie *digna* für die Verbindung zu Azure Synapse Analytics über
**ODBC** konfigurieren, und zwar mit einer **DSN-losen** Verbindungszeichenfolge. Sowohl
serverlose als auch dedizierte SQL-Pools werden unterstützt.

Die digna-Seite der Einrichtung ist für jede Technologie gleich — wo Verbindungen angelegt
werden, wie Eigenschaftswerte verschlüsselt werden, wie eine Verbindung getestet wird und was
die Profiling-Modi bedeuten. Das ist in der [Übersicht über Datenbankverbindungen](overview.md)
beschrieben. Diese Seite behandelt, was für Azure Synapse spezifisch ist.

!!! note "Technologie"

    Synapse spricht den SQL-Server-Dialekt, die Verbindung wird daher mit **Technology:
    SQL Server** angelegt. Für einen lokalen Server siehe
    [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. ODBC-Treiber installieren {: #1-install-the-odbc-driver }

Installieren Sie **ODBC Driver 18 for SQL Server** auf dem Rechner, auf dem das *digna*-Backend
läuft, und folgen Sie dabei
[Microsofts Installationsanleitung](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server);
lesen Sie den genauen registrierten Treibernamen auf Ihrem Host ab, wie unter
[ODBC-Treiber auf dem digna-Host installieren](overview.md#install-the-driver) beschrieben.

---

## 2. ODBC-Eigenschaften {: #2-odbc-properties }

!!! important "Ein Beispiel, keine Spezifikation"

    Der folgende Satz ist eine Kombination, von der bekannt ist, dass sie funktioniert. Die
    Eigenschaften gehören zum Microsoft-ODBC-Treiber, daher unterscheiden sich ihre Namen,
    Standardwerte und zulässigen Werte zwischen Treiberversionen und Plattformen, und was der
    Workspace verlangt, hängt davon ab, wie er konfiguriert ist — Pool-Typ,
    Authentifizierungsmethode, Firewall. Nehmen Sie dies als Ausgangspunkt und prüfen Sie die
    Dokumentation der von Ihnen installierten Treiberversion.

Fügen Sie im Bildschirm **Add DB Connection** die folgenden Eigenschaften hinzu:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Muss dem auf dem *digna*-Host registrierten Treibernamen entsprechen |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Workspace-Name plus Endpunkt-Suffix — siehe unten |
| `DATABASE` | `dignadata` | Datenbank, die die Quellschemata enthält. Es ist die einzige Datenbank, die diese Verbindung profilieren kann |
| `UID` | `sqladminuser` | SQL-Login |
| `PWD` | `<password>` | **Encrypted** ankreuzen |

Die resultierende Verbindungszeichenfolge sieht so aus:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### Der Wert von `SERVER`

Nehmen Sie den Namen des Synapse-Workspace und hängen Sie das Endpunkt-Suffix an:

| Pool | `SERVER` |
|---|---|
| **Serverloser SQL-Pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedizierter SQL-Pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Der Teil `-ondemand` wird leicht übersehen"

    Ohne ihn löst der Name auf den dedizierten Endpunkt auf, und die Verbindung scheitert
    entweder oder erreicht stillschweigend einen anderen Pool als beabsichtigt. Beide Endpunkte
    werden im Azure-Portal auf der Übersichtsseite des Workspace angezeigt.

### Firewall

Die Firewall des Synapse-Workspace muss die ausgehende Adresse des *digna*-Hosts zulassen.
Tragen Sie sie im Workspace unter **Networking** ein, bevor Sie die Verbindung testen — eine
blockierte Adresse zeigt sich als Verbindungs-Timeout, nicht als Authentifizierungsfehler.

### Authentifizierung mit Microsoft Entra ID

Statt eines SQL-Logins kann sich der Treiber gegen Entra ID authentifizieren. Ersetzen Sie
`UID`/`PWD` durch die Authentifizierungsmethode, die Ihr Workspace erwartet, zum Beispiel:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` nimmt dann die Anwendungs-(Client-)ID auf und `PWD` das Client-Secret |
| `Authentication` | `ActiveDirectoryMSI` | Verwaltete Identität des *digna*-Hosts, keine Anmeldedaten nötig |

---

## 3. *digna*-Konfiguration {: #3-digna-configuration }

Geben Sie im Bildschirm **Add DB Connection** Folgendes an:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Hinweise zu Azure Synapse {: #4-notes-on-azure-synapse }

- **Serverlose Pools unterstützen nur *Standard*-Profiling.** Ein serverloser SQL-Pool kann in
  einer Datenbank keine Tabellen anlegen, daher kann weder *Permanent*- noch
  *Session*-Profiling laufen. *Standard* berechnet die Metriken direkt auf der Quelle, was
  zugleich die günstigere Option ist, da serverlos nach verarbeiteter Datenmenge abgerechnet
  wird.
- **Eine Verbindung sieht eine Datenbank.** *digna* bietet die Schemata der in `DATABASE`
  genannten Datenbank an, weil Synapse wie SQL Server nur die aktuelle Datenbank als Katalog
  meldet.
- **Verschlüsselung ist standardmäßig aktiv** in Driver 18, und Synapse-Endpunkte legen gültige
  öffentliche Zertifikate vor, daher ist weder eine `Encrypt`- noch eine
  `TrustServerCertificate`-Eigenschaft nötig.
- **Ein serverloser Endpunkt fährt beim ersten Verbinden unter Umständen aus dem Ruhezustand
  hoch.** Läuft der Verbindungstest bei einem länger ungenutzten Pool in ein Timeout,
  wiederholen Sie ihn.

---

## 5. Treiber überprüfen (optional) {: #5-verifying-the-driver-optional }

Für eine DSN-lose Verbindung ist es nicht erforderlich, eine ODBC-Datenquelle einzurichten, aber
der Assistent des Treibers ist ein bequemer Weg, um vor der Eingabe in *digna* zu bestätigen,
dass der Treiber funktioniert und dass der Workspace Ihre Anmeldedaten akzeptiert.

#### Schritt 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Füllen Sie das Feld „Server“ aus.
Verwenden Sie den Namen des Synapse-Workspace und ergänzen Sie ihn um „.sql.azuresynapse.net“.  
**Achtung**: Wenn Sie sich über einen serverlosen SQL-Pool verbinden möchten, achten Sie darauf,
„-ondemand“ einzufügen, wie im Screenshot oben gezeigt.

Klicken Sie auf die Schaltfläche **Next >**.

#### Schritt 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Wählen Sie die Authentifizierungsmethode (z. B. Benutzername und Passwort)
und geben Sie die erforderlichen Daten an.

Klicken Sie auf die Schaltfläche **Next >**.

#### Schritt 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Wählen Sie die ANSI-konformen Einstellungen und klicken Sie dann auf die Schaltfläche **Next >**.

#### Schritt 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Sie können die Standardeinstellungen belassen oder nach Bedarf Optionen wählen
und auf die Schaltfläche **Finish** klicken.

#### Schritt 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klicken Sie nun auf die Schaltfläche **Test datasource**.

#### Schritt 6
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

Ein Erfolgsbildschirm bestätigt, dass der Treiber, der Endpunkt und die Anmeldedaten
funktionieren. Die Werte, die Sie eingegeben haben, sind genau die Werte, die die Eigenschaften
in [Abschnitt 2](#2-odbc-properties) annehmen.
