---
title: PostgreSQL-Connector – Datenbankintegration | digna Dokumentation
description: Konfigurieren Sie digna für die Verbindung zu PostgreSQL über ODBC mit einer DSN-losen Verbindungszeichenfolge. Behandelt den psqlODBC-Treiber, die erforderlichen ODBC-Eigenschaften, SSL-Modi und die Verbindungseinstellungen auf digna-Seite.
image: /assets/logo_square.png
---


# Quell-Connector für PostgreSQL

Diese Anleitung beschreibt, wie Sie *digna* für die Verbindung zu PostgreSQL über **ODBC**
konfigurieren, und zwar mit einer **DSN-losen** Verbindungszeichenfolge.

Die digna-Seite der Einrichtung ist für jede Technologie gleich — wo Verbindungen angelegt
werden, wie Eigenschaftswerte verschlüsselt werden, wie eine Verbindung getestet wird und was
die Profiling-Modi bedeuten. Das ist in der [Übersicht über Datenbankverbindungen](overview.md)
beschrieben. Diese Seite behandelt, was für PostgreSQL spezifisch ist.

---

## 1. ODBC-Treiber installieren {: #1-install-the-odbc-driver }

Installieren Sie den PostgreSQL-ODBC-Treiber (**psqlODBC**) auf dem Rechner, auf dem das
*digna*-Backend läuft, und folgen Sie dabei der offiziellen Installationsanleitung des
Herstellers.

Der Treiber registriert sich unter einem Namen, der je nach Plattform und Paket abweicht — meist
**PostgreSQL Unicode(x64)** unter Windows und **PostgreSQL ODBC Driver(UNICODE)** unter Linux.
Lesen Sie den genauen Namen auf Ihrem Host ab, wie unter
[ODBC-Treiber auf dem digna-Host installieren](overview.md#install-the-driver) beschrieben, und
verwenden Sie diesen Namen für die Eigenschaft `DRIVER` weiter unten.

---

## 2. ODBC-Eigenschaften {: #2-odbc-properties }

!!! important "Ein Beispiel, keine Spezifikation"

    Der folgende Satz ist eine Kombination, von der bekannt ist, dass sie funktioniert. Die
    Eigenschaften gehören zum psqlODBC-Treiber, daher unterscheiden sich ihre Namen,
    Standardwerte und zulässigen Werte zwischen Treiberversionen und Plattformen, und auch das,
    was Ihr Server verlangt — insbesondere SSL — kann abweichen. Nehmen Sie dies als
    Ausgangspunkt und prüfen Sie die Dokumentation der von Ihnen installierten Treiberversion.

Fügen Sie im Bildschirm **Add DB Connection** die folgenden Eigenschaften hinzu:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Muss dem auf dem *digna*-Host registrierten Treibernamen entsprechen |
| `SERVER` | `db.example.com` | Servername oder IP-Adresse |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Datenbank, die die Quellschemata enthält. Es ist die einzige Datenbank, die diese Verbindung profilieren kann |
| `UID` | `digna_source_user` | Datenbankbenutzer |
| `PWD` | `<password>` | **Encrypted** ankreuzen |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` oder `verify-full` — muss vom Server akzeptiert werden |

Die resultierende Verbindungszeichenfolge sieht so aus:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Jede weitere psqlODBC-Option lässt sich als zusätzliche Eigenschaft ergänzen — zum Beispiel
`ReadOnly=1` für eine schreibgeschützte Sitzung oder `ConnSettings`, um beim Verbindungsaufbau
`SET`-Anweisungen auszuführen.

---

## 3. *digna*-Konfiguration {: #3-digna-configuration }

Geben Sie im Bildschirm **Add DB Connection** Folgendes an:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Hinweise zu PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` muss zum Server passen.** Ein mit `hostssl` konfigurierter Server weist
  `SSLMode=disable` zurück, und `verify-ca` oder `verify-full` benötigen zusätzlich das
  Stammzertifikat, das dem Treiber auf dem *digna*-Host zur Verfügung stehen muss. Wenn Sie beim
  Testen des Treibers einen bestimmten Modus wählen mussten, verwenden Sie hier denselben.
- **Eine Verbindung sieht eine Datenbank.** *digna* bietet die Schemata der in `DATABASE`
  genannten Datenbank an, weil PostgreSQL nur die aktuelle Datenbank als Katalog meldet.
  Quelltabellen in einer anderen Datenbank brauchen eine eigene Verbindung.
- **Profiling-Modi.** *Permanent* legt die Arbeitstabellen im **Work Schema** an, der Benutzer
  braucht dort also `CREATE`. *Session* verwendet `CREATE TEMPORARY TABLE` und rührt das
  **Work Schema** nicht an. *Standard* benötigt nur Lesezugriff.

---

## 5. Treiber überprüfen (optional) {: #5-verifying-the-driver-optional }

Für eine DSN-lose Verbindung ist es nicht erforderlich, eine ODBC-Datenquelle einzurichten, aber
der Dialog des Treibers ist ein bequemer Weg, um vor der Eingabe in *digna* zu bestätigen, dass
der Treiber funktioniert und dass der Server Ihre Anmeldedaten und Ihren SSL-Modus akzeptiert.

#### Schritt 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### Schritt 2 – Verbindung testen

Klicken Sie auf die Schaltfläche **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

Die Werte, die Sie hier eingegeben haben, sind genau die Werte, die die Eigenschaften in
[Abschnitt 2](#2-odbc-properties) annehmen.
