---
title: Netezza-Connector – Datenbankintegration | digna Dokumentation
description: Konfigurieren Sie digna für die Verbindung zu Netezza über ODBC mit einer DSN-losen Verbindungszeichenfolge. Behandelt den NetezzaSQL-Treiber, die erforderlichen ODBC-Eigenschaften und die Verbindungseinstellungen auf digna-Seite.
image: /assets/logo_square.png
---


# Quell-Connector für Netezza

Diese Anleitung beschreibt, wie Sie *digna* für die Verbindung zu Netezza über **ODBC**
konfigurieren, und zwar mit einer **DSN-losen** Verbindungszeichenfolge.

Die digna-Seite der Einrichtung ist für jede Technologie gleich — wo Verbindungen angelegt
werden, wie Eigenschaftswerte verschlüsselt werden, wie eine Verbindung getestet wird und was
die Profiling-Modi bedeuten. Das ist in der [Übersicht über Datenbankverbindungen](overview.md)
beschrieben. Diese Seite behandelt, was für Netezza spezifisch ist.

---

## 1. ODBC-Treiber installieren {: #1-install-the-odbc-driver }

Installieren Sie den **NetezzaSQL**-ODBC-Treiber (Teil der IBM-Netezza-Client-Tools) auf dem
Rechner, auf dem das *digna*-Backend läuft, und folgen Sie dabei der offiziellen
Installationsanleitung des Herstellers.

Lesen Sie den genauen registrierten Treibernamen auf Ihrem Host ab, wie unter
[ODBC-Treiber auf dem digna-Host installieren](overview.md#install-the-driver) beschrieben.

---

## 2. ODBC-Eigenschaften {: #2-odbc-properties }

!!! important "Ein Beispiel, keine Spezifikation"

    Der folgende Satz ist eine Kombination, von der bekannt ist, dass sie funktioniert. Die
    Eigenschaften gehören zum NetezzaSQL-Treiber, daher unterscheiden sich ihre Namen,
    Standardwerte und zulässigen Werte zwischen Client-Versionen und Plattformen, und eine
    TLS-gesicherte Appliance benötigt mehr als die hier gezeigten Eigenschaften. Nehmen Sie dies
    als Ausgangspunkt und prüfen Sie die Dokumentation der von Ihnen installierten
    Client-Version.

Fügen Sie im Bildschirm **Add DB Connection** die folgenden Eigenschaften hinzu:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Muss dem auf dem *digna*-Host registrierten Treibernamen entsprechen. Die geschweiften Klammern sind die übliche Schreibweise für diesen Namen |
| `SERVER` | `netezza.example.com` | Servername oder IP-Adresse |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Datenbank, in der die Sitzung startet |
| `UID` | `ADMIN` | Datenbankbenutzer |
| `PWD` | `<password>` | **Encrypted** ankreuzen |

Die resultierende Verbindungszeichenfolge sieht so aus:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Je nach Treiberversion, Einrichtung und Sicherheitsanforderungen können weitere Eigenschaften
nötig sein — zum Beispiel `SecurityLevel` und `CaCertFile` für eine TLS-gesicherte Appliance.
Jede Option, die die Dialoge *Advanced*, *SSL* und *Driver* des Treibers anbieten, lässt sich
als Eigenschaft ergänzen.

---

## 3. *digna*-Konfiguration {: #3-digna-configuration }

Geben Sie im Bildschirm **Add DB Connection** Folgendes an:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Hinweise zu Netezza {: #4-notes-on-netezza }

- **Kataloge und Schemata gelten beide.** *digna* listet die Datenbanken, die der Benutzer sehen
  darf (aus `_V_DATABASE`), als Kataloge und darunter deren Schemata (aus `_V_SCHEMA`) auf,
  sodass eine Verbindung Quellen in mehr als einer Datenbank bedienen kann. `DATABASE` legt nur
  fest, wo die Sitzung startet.
- **Bezeichner sind in Großbuchstaben**, sofern sie nicht in Anführungszeichen angelegt wurden —
  deshalb verwenden die obigen Beispiele `TEST` und `ADMIN`.
- **Profiling-Modi.** *Permanent* legt die Arbeitstabellen im **Work Schema** an, der Benutzer
  braucht dort also `CREATE TABLE`. *Session* verwendet `CREATE TEMPORARY TABLE` und rührt das
  **Work Schema** nicht an. *Standard* benötigt nur Lesezugriff.

---

## 5. Treiber überprüfen (optional) {: #5-verifying-the-driver-optional }

Für eine DSN-lose Verbindung ist es nicht erforderlich, eine ODBC-Datenquelle einzurichten, aber
der Dialog des Treibers ist ein bequemer Weg, um vor der Eingabe in *digna* zu bestätigen, dass
der Treiber und Ihre Anmeldedaten funktionieren.

#### Schritt 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Die Felder unter **DSN Options** entsprechen eins zu eins den Eigenschaften in
[Abschnitt 2](#2-odbc-properties). Je nach Netezza-Treiber, Einrichtung und
Sicherheitsanforderungen benötigen Sie möglicherweise auch Angaben in den Reitern
**Advanced DSN Options**, **SSL DSN Options** oder **Driver Options**; für die einfachste
Einrichtung genügt **DSN Options**.

Klicken Sie auf die Schaltfläche **Test Connection**.

#### Schritt 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Wenn der Erfolgsbildschirm erscheint, funktioniert der Treiber und die Werte sind korrekt.
