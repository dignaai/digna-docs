# Quell-Connector für Hive

Diese Anleitung beschreibt, wie Sie *digna* für die Verbindung zu Apache Hive über **ODBC**
konfigurieren, und zwar mit einer **DSN-losen** Verbindungszeichenfolge.

Die digna-Seite der Einrichtung ist für jede Technologie gleich — wo Verbindungen angelegt
werden, wie Eigenschaftswerte verschlüsselt werden, wie eine Verbindung getestet wird und was
die Profiling-Modi bedeuten. Das ist in der [Übersicht über Datenbankverbindungen](overview.md)
beschrieben. Diese Seite behandelt, was für Hive spezifisch ist.

---

## 1. ODBC-Treiber installieren {: #1-install-the-odbc-driver }

Installieren Sie den **Cloudera ODBC Driver for Apache Hive** auf dem Rechner, auf dem das
*digna*-Backend läuft, und folgen Sie dabei der offiziellen Installationsanleitung des
Herstellers.

Lesen Sie den genauen registrierten Treibernamen auf Ihrem Host ab, wie unter
[ODBC-Treiber auf dem digna-Host installieren](overview.md#install-the-driver) beschrieben.

---

## 2. ODBC-Eigenschaften {: #2-odbc-properties }

!!! important "Ein Beispiel, keine Spezifikation"

    Der folgende Satz ist eine Kombination, von der bekannt ist, dass sie funktioniert. Die
    Eigenschaften gehören zum Cloudera-Hive-Treiber, daher unterscheiden sich ihre Namen,
    Standardwerte und zulässigen Werte zwischen Treiberversionen und Plattformen, und was
    HiveServer2 akzeptiert, hängt vollständig davon ab, wie der Cluster abgesichert ist —
    Authentifizierungsmechanismus, Transportmodus, TLS, Gateway. Nehmen Sie dies als
    Ausgangspunkt und prüfen Sie die Dokumentation der von Ihnen installierten Treiberversion.

Fügen Sie im Bildschirm **Add DB Connection** die folgenden Eigenschaften hinzu:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Muss dem auf dem *digna*-Host registrierten Treibernamen entsprechen |
| `HOST` | `hive.example.com` | Hostname oder IP-Adresse von HiveServer2 |
| `PORT` | `10000` | HiveServer2-Port; `10001` für HTTP-Transport |

Die resultierende Verbindungszeichenfolge sieht so aus:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Authentifizierung

Ein ungesicherter HiveServer2 akzeptiert die drei obigen Eigenschaften unverändert. Wo
Authentifizierung aktiviert ist, ergänzen Sie:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `AuthMech` | `3` | `0` keine Authentifizierung, `2` nur Benutzername, `3` Benutzername und Passwort, `1` Kerberos |
| `UID` | `digna_source_user` | Erforderlich für `AuthMech` `2` und `3` |
| `PWD` | `<password>` | Erforderlich für `AuthMech` `3`. **Encrypted** ankreuzen |

Für Kerberos (`AuthMech=1`) benötigt der *digna*-Host zusätzlich ein gültiges Ticket oder eine
Keytab sowie die Eigenschaften `KrbHostFQDN`, `KrbServiceName` und `KrbRealm`, die der Treiber
dokumentiert.

### Transport und TLS

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `ThriftTransport` | `2` | `0` binär (Voreinstellung, Port 10000), `1` SASL, `2` HTTP (Port 10001, und das, was ein Knox-Gateway erwartet) |
| `HTTPPath` | `cliservice` | Mit `ThriftTransport=2` |
| `SSL` | `1` | Wo HiveServer2 TLS-gesichert ist |
| `Schema` | `dignadata` | Hive-Datenbank, in der die Sitzung startet. Optional — *digna* qualifiziert seine Abfragen |

---

## 3. *digna*-Konfiguration {: #3-digna-configuration }

Geben Sie im Bildschirm **Add DB Connection** Folgendes an:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Hinweise zu Hive {: #4-notes-on-hive }

- **Kataloge kommen vom Treiber.** Hive hat keinen eigenen Katalog, daher übernimmt *digna*, was
  der Treiber meldet — normalerweise einen einzelnen Eintrag namens `HIVE` — und listet die
  Hive-Datenbanken als Schemata darunter auf.
- **Work Schema ist eine Hive-Datenbank.** Für *Permanent*-Profiling benötigt der Benutzer darin
  das Recht, Tabellen anzulegen und zu löschen, und der zugrunde liegende Speicherort muss
  beschreibbar sein.
- **Profiling-Modi.** *Permanent* legt die Arbeitstabellen im **Work Schema** an. *Session*
  verwendet `CREATE TEMPORARY TABLE`, wofür ein HiveServer2 nötig ist, der temporäre Tabellen
  unterstützt, und rührt das **Work Schema** nicht an. *Standard* benötigt nur Lesezugriff und
  ist der Modus der Wahl auf einem Cluster, auf dem *digna* überhaupt keinen Schreibzugriff hat.
- **Profiling ist eine Reihe von Abfragen, kein Scan.** Jede Statistik wird von HiveServer2
  berechnet, daher sollte die Queue, in die der Benutzer von *digna* einreicht, genügend
  Kapazität für das Inspektionsfenster haben.

---

## 5. Treiber überprüfen (optional) {: #5-verifying-the-driver-optional }

Für eine DSN-lose Verbindung ist es nicht erforderlich, eine ODBC-Datenquelle einzurichten, aber
der Dialog des Treibers ist ein bequemer Weg, um vor der Eingabe in *digna* zu bestätigen, dass
der Treiber, der Transportmodus und Ihre Anmeldedaten funktionieren.

#### Schritt 1
![Step 1](images/hive/create_odbc_data_source_step1.png)

Die Felder **Host**, **Port**, **Database**, **Mechanism** und **Thrift Transport** entsprechen
hier den Eigenschaften `HOST`, `PORT`, `Schema`, `AuthMech` und `ThriftTransport` in
[Abschnitt 2](#2-odbc-properties).

#### Schritt 2 – Verbindung testen

Geben Sie das Passwort an und klicken Sie auf die Schaltfläche **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Klicken Sie nach einem erfolgreichen Test auf die Schaltfläche **OK**.