---
title: Snowflake-Connector – Datenbankintegration | digna Dokumentation
description: Konfigurieren Sie digna für die Verbindung zu Snowflake über ODBC mit einer DSN-losen Verbindungszeichenfolge. Behandelt den Snowflake-ODBC-Treiber, programmatische Zugriffstoken, die Auswahl von Warehouse und Rolle sowie die Verbindungseinstellungen auf digna-Seite.
image: /assets/logo_square.png
---


# Quell-Connector für Snowflake

Diese Anleitung beschreibt, wie Sie *digna* für die Verbindung zu Snowflake über **ODBC**
konfigurieren, und zwar mit einer **DSN-losen** Verbindungszeichenfolge.

Die digna-Seite der Einrichtung ist für jede Technologie gleich — wo Verbindungen angelegt
werden, wie Eigenschaftswerte verschlüsselt werden, wie eine Verbindung getestet wird und was
die Profiling-Modi bedeuten. Das ist in der [Übersicht über Datenbankverbindungen](overview.md)
beschrieben. Diese Seite behandelt, was für Snowflake spezifisch ist.

---

## 1. ODBC-Treiber installieren {: #1-install-the-odbc-driver }

Installieren Sie den **Snowflake ODBC Driver** auf dem Rechner, auf dem das *digna*-Backend
läuft, und folgen Sie dabei
[Snowflakes Installationsanleitung](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Der Treiber registriert sich als **SnowflakeDSIIDriver**. Lesen Sie den genauen registrierten
Namen auf Ihrem Host ab, wie unter
[ODBC-Treiber auf dem digna-Host installieren](overview.md#install-the-driver) beschrieben.

---

## 2. ODBC-Eigenschaften {: #2-odbc-properties }

Snowflake wird mit einem **programmatischen Zugriffstoken (PAT)** erreicht — dem
Authentifizierungsweg, gegen den *digna* geprüft ist, und dem, den Snowflake für Konten
verlangt, bei denen die reine Passwortanmeldung gesperrt ist.

!!! important "Ein Beispiel, keine Spezifikation"

    Der folgende Satz ist eine Kombination, von der bekannt ist, dass sie funktioniert. Die
    Eigenschaften gehören zum Snowflake-ODBC-Treiber, daher unterscheiden sich ihre Namen,
    Standardwerte und zulässigen Werte zwischen Treiberversionen und Plattformen, und welche
    Authentifizierungsoptionen Ihr Konto zulässt, entscheidet die Sicherheitsrichtlinie des
    Kontos. Nehmen Sie dies als Ausgangspunkt und prüfen Sie die Dokumentation der von Ihnen
    installierten Treiberversion.

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Muss dem auf dem *digna*-Host registrierten Treibernamen entsprechen |
| `Server` | `<account>.snowflakecomputing.com` | Kontobezeichner plus Suffix, z. B. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Snowflake-Benutzer, zu dem das Token gehört |
| `Database` | `TEST` | Datenbank, die die Quellschemata enthält. Es ist die einzige Datenbank, die diese Verbindung profilieren kann |
| `Schema` | `PUBLIC` | Standardschema der Sitzung |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Wählt die Token-Authentifizierung |
| `token` | `<programmatic access token>` | **Encrypted** ankreuzen |

Die resultierende Verbindungszeichenfolge sieht so aus:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse und Rolle

Abfragen brauchen ein Warehouse. Hat der *digna*-Benutzer ein Standard-Warehouse und eine
Standardrolle, übernimmt die Sitzung beides und es muss nichts konfiguriert werden. Andernfalls
ergänzen Sie:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse, das die Profiling-Abfragen ausführt |
| `Role` | `DIGNA_READER` | Rolle, deren Berechtigungen die Sitzung verwendet |

!!! tip "Geben Sie digna ein eigenes Warehouse"

    Ein separates, kleines Warehouse mit automatischer Unterbrechung hält die Profiling-Kosten
    sichtbar und verhindert, dass *digna* mit interaktiven Benutzern um Rechenleistung
    konkurriert.

### Passwort-Authentifizierung

Wo das Konto es noch zulässt, funktioniert anstelle des Tokens auch ein Passwort — lassen Sie
`authenticator` und `token` weg und ergänzen Sie:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `PWD` | `<password>` | **Encrypted** ankreuzen |

---

## 3. *digna*-Konfiguration {: #3-digna-configuration }

Geben Sie im Bildschirm **Add DB Connection** Folgendes an:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Hinweise zu Snowflake {: #4-notes-on-snowflake }

- **Token laufen ab.** Ein programmatisches Zugriffstoken wird mit einer Lebensdauer ausgestellt,
  und das Profiling endet an dem Tag, an dem sie abläuft. Notieren Sie das Ablaufdatum beim
  Erstellen und tragen Sie das neue Token in die Eigenschaft `token` ein — verschlüsselte Werte
  lassen sich ersetzen, aber nicht zurücklesen.
- **Eine Verbindung sieht eine Datenbank.** *digna* bietet die Schemata der in `Database`
  genannten Datenbank an, weil Snowflake nur die aktuelle Datenbank als Katalog meldet.
  Quelltabellen in einer anderen Datenbank brauchen eine eigene Verbindung.
- **Bezeichner sind in Großbuchstaben**, sofern sie nicht in Anführungszeichen angelegt wurden.
  *digna* verwendet die Namen so, wie Snowflake sie meldet.
- **Profiling-Modi.** *Permanent* legt die Arbeitstabellen im **Work Schema** an, die Rolle
  braucht dort also `CREATE TABLE`. *Session* verwendet `CREATE TEMPORARY TABLE` und rührt das
  **Work Schema** nicht an. *Standard* benötigt nur Lesezugriff — und überhaupt keine
  Schreibrechte.

---

## 5. Treiber überprüfen (optional) {: #5-verifying-the-driver-optional }

Für eine DSN-lose Verbindung ist es nicht erforderlich, eine ODBC-Datenquelle einzurichten, aber
der Dialog des Treibers ist ein bequemer Weg, um vor der Eingabe in *digna* zu bestätigen, dass
der Treiber, die Konto-URL und Ihre Anmeldedaten funktionieren.

#### Schritt 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Hinweise:

- Der Wert für **Server** besteht aus Ihrem Snowflake-Kontobezeichner, gefolgt von
  `.snowflakecomputing.com`.
- **Database**, **Schema** und **Warehouse**, die Sie hier eingeben, entsprechen den
  Eigenschaften `Database`, `Schema` und `Warehouse` in [Abschnitt 2](#2-odbc-properties).

#### Schritt 2 – Verbindung testen

Klicken Sie auf die Schaltfläche **TEST**. Eine erfolgreiche Verbindung sollte so aussehen:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)
