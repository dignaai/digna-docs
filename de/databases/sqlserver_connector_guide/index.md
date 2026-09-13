# Quell-Connector für MS SQL Server

Diese Anleitung beschreibt, wie Sie *digna* für die Verbindung zu Microsoft SQL Server über
**ODBC** konfigurieren, und zwar mit einer **DSN-losen** Verbindungszeichenfolge.

Die digna-Seite der Einrichtung ist für jede Technologie gleich — wo Verbindungen angelegt
werden, wie Eigenschaftswerte verschlüsselt werden, wie eine Verbindung getestet wird und was
die Profiling-Modi bedeuten. Das ist in der [Übersicht über Datenbankverbindungen](overview.md)
beschrieben. Diese Seite behandelt, was für SQL Server spezifisch ist.

!!! note "Azure Synapse Analytics"

    Synapse wird ebenfalls als SQL-Server-Verbindung konfiguriert, mit einem anderen Hostnamen
    und einigen zusätzlichen Überlegungen — siehe
    [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. ODBC-Treiber installieren {: #1-install-the-odbc-driver }

Installieren Sie **ODBC Driver 18 for SQL Server** auf dem Rechner, auf dem das *digna*-Backend
läuft, und folgen Sie dabei
[Microsofts Installationsanleitung](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Der Treiber, der unter dem schlichten Namen **SQL Server** mit Windows ausgeliefert wird,
funktioniert ebenfalls, ist aber längst überholt und unterstützt weder moderne TLS-Einstellungen
noch die Azure-Authentifizierung. Verwenden Sie ihn nur dort, wo die Installation des aktuellen
Treibers nicht möglich ist.

Lesen Sie den genauen registrierten Treibernamen auf Ihrem Host ab, wie unter
[ODBC-Treiber auf dem digna-Host installieren](overview.md#install-the-driver) beschrieben.

---

## 2. ODBC-Eigenschaften {: #2-odbc-properties }

!!! important "Ein Beispiel, keine Spezifikation"

    Der folgende Satz ist eine Kombination, von der bekannt ist, dass sie funktioniert. Die
    Eigenschaften gehören zum Microsoft-ODBC-Treiber, daher unterscheiden sich ihre Namen,
    Standardwerte und zulässigen Werte zwischen Treiberversionen — Driver 18 verschlüsselt
    standardmäßig, Driver 17 tat das nicht — und zwischen Plattformen. Nehmen Sie dies als
    Ausgangspunkt und prüfen Sie die Dokumentation der von Ihnen installierten Treiberversion.

Fügen Sie im Bildschirm **Add DB Connection** die folgenden Eigenschaften hinzu:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Muss dem auf dem *digna*-Host registrierten Treibernamen entsprechen |
| `SERVER` | `sql.example.com` | Servername oder IP-Adresse. Benannte Instanzen: `host\instance`; abweichender Port: `host,1433` |
| `PORT` | `1433` | Entfällt, wenn der Port bereits Teil von `SERVER` ist |
| `DATABASE` | `digna_source_db` | Datenbank, die die Quellschemata enthält. Es ist die einzige Datenbank, die diese Verbindung profilieren kann |
| `UID` | `digna_source_user` | Datenbankbenutzer |
| `PWD` | `<password>` | **Encrypted** ankreuzen |

Die resultierende Verbindungszeichenfolge sieht so aus:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Verschlüsselung mit ODBC Driver 18

Driver 18 verschlüsselt Verbindungen standardmäßig und prüft das Serverzertifikat. Gegenüber
einem Server mit einem Zertifikat, dem Ihr *digna*-Host nicht vertraut — typischerweise einem
selbstsignierten Zertifikat — schlägt der Verbindungsaufbau mit einem Zertifikatskettenfehler
fehl. Ergänzen Sie:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `Encrypt` | `yes` | Voreinstellung in Driver 18; setzen Sie `no` nur, wenn der Server kein TLS beherrscht |
| `TrustServerCertificate` | `yes` | Überspringt die Zertifikatsprüfung. In Testumgebungen praktisch; in der Produktion sollten Sie das Zertifikat lieber installieren |

### Windows-Authentifizierung

Um sich als das Konto zu verbinden, unter dem der *digna*-Dienst läuft, statt mit einem
SQL-Login, lassen Sie `UID` und `PWD` weg und ergänzen Sie:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `Trusted_Connection` | `yes` | Das *digna*-Dienstkonto benötigt die Datenbankrechte |

---

## 3. *digna*-Konfiguration {: #3-digna-configuration }

Geben Sie im Bildschirm **Add DB Connection** Folgendes an:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Hinweise zu MS SQL Server {: #4-notes-on-ms-sql-server }

- **Eine Verbindung sieht eine Datenbank.** *digna* bietet die Schemata der in `DATABASE`
  genannten Datenbank an, weil SQL Server nur die aktuelle Datenbank als Katalog meldet.
  Quelltabellen in einer anderen Datenbank brauchen eine eigene Verbindung.
- **Profiling-Modi.** *Permanent* legt die Arbeitstabellen im **Work Schema** an, der Benutzer
  braucht dort also `CREATE TABLE`. *Session* verwendet lokale temporäre Tabellen (`#wt_…`) in
  `tempdb` und rührt das **Work Schema** nicht an. *Standard* benötigt nur Lesezugriff.
- **`SERVER` trägt Instanz und Port.** Bei einer benannten Instanz muss für `host\instance` der
  SQL Server Browser erreichbar sein; `host,port` umgeht das.

---

## 5. Treiber überprüfen (optional) {: #5-verifying-the-driver-optional }

Für eine DSN-lose Verbindung ist es nicht erforderlich, eine ODBC-Datenquelle einzurichten, aber
der Assistent des Treibers ist ein bequemer Weg, um vor der Eingabe in *digna* zu bestätigen,
dass der Treiber funktioniert und dass der Server Ihre Anmeldedaten akzeptiert.

#### Schritt 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Klicken Sie auf die Schaltfläche **Next >**.

#### Schritt 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Wählen Sie die Authentifizierungsmethode (z. B. Benutzername und Passwort)
und geben Sie die erforderlichen Daten an.

Klicken Sie auf die Schaltfläche **Next >**.

#### Schritt 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Wählen Sie die ANSI-konformen Einstellungen und klicken Sie dann auf die Schaltfläche **Next >**.

#### Schritt 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Sie können die Standardeinstellungen belassen oder nach Bedarf Protokollierungsoptionen wählen
und auf die Schaltfläche **Finish** klicken.

#### Schritt 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Klicken Sie nun auf die Schaltfläche **Test datasource**.

#### Schritt 6
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

Ein Erfolgsbildschirm bestätigt, dass der Treiber und die Anmeldedaten funktionieren. Die Werte,
die Sie eingegeben haben, sind genau die Werte, die die Eigenschaften in
[Abschnitt 2](#2-odbc-properties) annehmen.