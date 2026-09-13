# Quell-Connector für Databricks

Diese Anleitung beschreibt, wie Sie *digna* für die Verbindung zu Databricks über **ODBC**
konfigurieren, und zwar mit einer **DSN-losen** Verbindungszeichenfolge.

Die digna-Seite der Einrichtung ist für jede Technologie gleich — wo Verbindungen angelegt
werden, wie Eigenschaftswerte verschlüsselt werden, wie eine Verbindung getestet wird und was
die Profiling-Modi bedeuten. Das ist in der [Übersicht über Datenbankverbindungen](overview.md)
beschrieben. Diese Seite behandelt, was für Databricks spezifisch ist.

!!! note "Unity Catalog ist erforderlich"

    *digna* liest die verfügbaren Kataloge aus `system.information_schema.catalogs`, der
    Workspace muss daher für Unity Catalog aktiviert sein. Frühere *digna*-Releases boten eine
    separate Technologie „Databricks Legacy“ für Workspaces ohne Unity Catalog an; sie steht
    nicht mehr zur Verfügung.

---

## 1. ODBC-Treiber installieren {: #1-install-the-odbc-driver }

Installieren Sie den **Databricks ODBC Driver** auf dem Rechner, auf dem das *digna*-Backend
läuft, und folgen Sie dabei
[der Installationsanleitung von Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

Je nach Version registriert sich der Treiber als **Simba Spark ODBC Driver** oder als
**Databricks ODBC Driver**. Lesen Sie den genauen registrierten Namen auf Ihrem Host ab, wie
unter [ODBC-Treiber auf dem digna-Host installieren](overview.md#install-the-driver)
beschrieben.

---

## 2. Verbindungsdaten zusammentragen {: #2-gather-the-connection-details }

Alle Werte stammen aus dem SQL-Warehouse (oder Cluster), das *digna* verwenden soll. Öffnen Sie
es im Databricks-Workspace und gehen Sie zu **Connection details**:

| Databricks-Feld | Verwendet als |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, normalerweise `443` |
| **HTTP path** | `HTTPPath` |

Erstellen Sie für die Authentifizierung ein **persönliches Zugriffstoken** — siehe
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Token gehören zu einem Benutzer oder Service Principal, und dieser Principal benötigt
`USE CATALOG`, `USE SCHEMA` und `SELECT` auf die Quelldaten.

---

## 3. ODBC-Eigenschaften {: #3-odbc-properties }

!!! important "Ein Beispiel, keine Spezifikation"

    Der folgende Satz ist eine Kombination, von der bekannt ist, dass sie funktioniert. Die
    Eigenschaften gehören zum Databricks-/Simba-Treiber, daher unterscheiden sich ihre Namen,
    Standardwerte und zulässigen Werte zwischen Treiberversionen — der Treiber wurde mehr als
    einmal umbenannt und seine Authentifizierungsoptionen erweitert — und zwischen Plattformen.
    Nehmen Sie dies als Ausgangspunkt und prüfen Sie die Dokumentation der von Ihnen
    installierten Treiberversion.

Fügen Sie im Bildschirm **Add DB Connection** die folgenden Eigenschaften hinzu:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Muss dem auf dem *digna*-Host registrierten Treibernamen entsprechen |
| `Host` | `<workspace>.cloud.databricks.com` | Server-Hostname des Warehouse, z. B. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | HTTP-Pfad des Warehouse oder Clusters |
| `SSL` | `1` | Databricks-Endpunkte sind ausschließlich TLS |
| `ThriftTransport` | `2` | HTTP-Transport, den die SQL-Endpunkte sprechen |
| `AuthMech` | `3` | Token-Authentifizierung |
| `UID` | `token` | Das wörtliche Wort `token`, kein Benutzername |
| `PWD` | `dapi…` | Das persönliche Zugriffstoken. **Encrypted** ankreuzen |
| `UseNativeQuery` | `1` | Reicht das SQL von *digna* unverändert durch — siehe unten |

Die resultierende Verbindungszeichenfolge sieht so aus:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Behalten Sie `UseNativeQuery=1` bei"

    Mit `UseNativeQuery=0` — der Voreinstellung des Treibers — schreibt der Treiber eingehendes
    SQL in das um, was er für portable ODBC-Syntax hält. *digna* erzeugt bereits
    Databricks-SQL, daher kann das Umschreiben Backtick-Quoting und Datumsliterale verändern,
    und das Profiling scheitert dann an Anweisungen, die so, wie sie geschrieben sind, gültig
    wären.

### OAuth statt Token

Für einen Service Principal mit OAuth-Machine-to-Machine-Authentifizierung ersetzen Sie
`AuthMech`, `UID` und `PWD` durch:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client Credentials |
| `Auth_Client_ID` | `<application id>` | Service Principal |
| `Auth_Client_Secret` | `<client secret>` | **Encrypted** ankreuzen |

---

## 4. *digna*-Konfiguration {: #4-digna-configuration }

Geben Sie im Bildschirm **Add DB Connection** Folgendes an:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Hinweise zu Databricks {: #5-notes-on-databricks }

- **Das Warehouse muss laufen** oder startbereit sein, wenn *digna* sich verbindet. Ein
  Warehouse, das aus dem gestoppten Zustand hochfährt, kann länger brauchen als das
  Verbindungs-Timeout — schlägt der Test nach einer Ruhephase beim ersten Versuch fehl,
  wiederholen Sie ihn.
- **Kataloge kommen aus dem Workspace.** Anders als bei den meisten Technologien erreicht eine
  Databricks-Verbindung jeden Katalog, den der Principal sehen darf, sodass eine einzige
  Verbindung Quellen über mehrere Kataloge hinweg bedienen kann.
- **Profiling-Modi.** *Permanent* legt die Arbeitstabellen im **Work Schema** innerhalb des
  Katalogs der Quelle an, der Principal braucht dort also `CREATE TABLE`. *Session* verwendet
  `CREATE TEMPORARY TABLE` und rührt das **Work Schema** nicht an. *Standard* benötigt nur
  Lesezugriff.
- **Serverlose Warehouses funktionieren** genauso; nur `HTTPPath` unterscheidet sich.

---

## 6. Treiber überprüfen (optional) {: #6-verifying-the-driver-optional }

Für eine DSN-lose Verbindung ist es nicht erforderlich, eine ODBC-Datenquelle einzurichten, aber
der Dialog des Treibers ist ein bequemer Weg, um vor der Eingabe in *digna* zu bestätigen, dass
der Treiber, das Warehouse und das Token funktionieren.

#### Schritt 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Schritt 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Schritt 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Schritt 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Schritt 5 – Verbindung testen

Klicken Sie auf die Schaltfläche **TEST**. Eine erfolgreiche Verbindung sollte so aussehen:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

Host, HTTP-Pfad und Token, die Sie hier eingegeben haben, sind genau die Werte, die die
Eigenschaften in [Abschnitt 3](#3-odbc-properties) annehmen.