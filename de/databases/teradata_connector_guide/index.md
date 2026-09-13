# Quell-Connector für Teradata

Diese Anleitung beschreibt, wie Sie *digna* für die Verbindung zu Teradata über **ODBC**
konfigurieren, und zwar mit einer **DSN-losen** Verbindungszeichenfolge.

Die digna-Seite der Einrichtung ist für jede Technologie gleich — wo Verbindungen angelegt
werden, wie Eigenschaftswerte verschlüsselt werden, wie eine Verbindung getestet wird und was
die Profiling-Modi bedeuten. Das ist in der [Übersicht über Datenbankverbindungen](overview.md)
beschrieben. Diese Seite behandelt, was für Teradata spezifisch ist.

---

## 1. ODBC-Treiber installieren {: #1-install-the-odbc-driver }

Installieren Sie den **ODBC Driver for Teradata** auf dem Rechner, auf dem das *digna*-Backend
läuft, und folgen Sie dabei der offiziellen Installationsanleitung des Herstellers.

Der Treiber registriert sich mit seiner Version im Namen, zum Beispiel
**Teradata Database ODBC Driver 20.00**. Lesen Sie den genauen registrierten Namen auf Ihrem
Host ab, wie unter
[ODBC-Treiber auf dem digna-Host installieren](overview.md#install-the-driver) beschrieben.

---

## 2. ODBC-Eigenschaften {: #2-odbc-properties }

!!! important "Ein Beispiel, keine Spezifikation"

    Der folgende Satz ist eine Kombination, von der bekannt ist, dass sie funktioniert. Die
    Eigenschaften gehören zum Teradata-ODBC-Treiber, daher unterscheiden sich ihre Namen,
    Standardwerte und zulässigen Werte zwischen Treiberversionen — die Version ist Teil des
    Treibernamens selbst — und zwischen Plattformen. Nehmen Sie dies als Ausgangspunkt und
    prüfen Sie die Dokumentation der von Ihnen installierten Treiberversion.

Fügen Sie im Bildschirm **Add DB Connection** die folgenden Eigenschaften hinzu:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Muss dem auf dem *digna*-Host registrierten Treibernamen entsprechen |
| `DBCNAME` | `teradata.example.com` | Servername oder IP-Adresse. Teradatas eigener Name für die Host-Eigenschaft |
| `UID` | `digna_source_user` | Datenbankbenutzer |
| `PWD` | `<password>` | **Encrypted** ankreuzen |

Die resultierende Verbindungszeichenfolge sieht so aus:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Nützliche zusätzliche Eigenschaften:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `MechanismName` | `TD2` | Anmeldemechanismus. `TD2` ist die Teradata-Voreinstellung; verwenden Sie `LDAP` für die Verzeichnisauthentifizierung |
| `DefaultDatabase` | `dad` | Datenbank, in der die Sitzung startet |
| `CharacterSet` | `UTF8` | Setzen Sie dies, wenn der voreingestellte Sitzungszeichensatz Nicht-ASCII-Daten verstümmeln würde |

---

## 3. *digna*-Konfiguration {: #3-digna-configuration }

Geben Sie im Bildschirm **Add DB Connection** Folgendes an:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Hinweise zu Teradata {: #4-notes-on-teradata }

- **Eine Teradata-Datenbank ist ein Katalog, kein Schema.** *digna* listet die Datenbanken, die
  der Benutzer sehen darf (aus `DBC.DatabasesV`), als Kataloge auf; die Schema-Ebene entfällt.
  Wählen Sie beim Hinzufügen einer Datenquelle die Datenbank als Katalog; das Schema wird als
  *nicht zutreffend* gemeldet.
- **Eine Verbindung erreicht jede zugelassene Datenbank**, sodass eine einzige Verbindung
  Quellen über mehrere Datenbanken hinweg bedienen kann — anders als bei den Technologien, bei
  denen die Verbindung an eine Datenbank gebunden ist.
- **Work Schema ist eine Datenbank.** Nennen Sie für *Permanent*-Profiling die
  Teradata-Datenbank, die die Arbeitstabellen enthält, und geben Sie dem Benutzer dort
  `CREATE TABLE`-Rechte sowie eine `PERM`-Speicherzuteilung — eine Datenbank ohne Perm-Speicher
  kann keine Tabelle aufnehmen.
- **Profiling-Modi.** *Permanent* legt Tabellen im **Work Schema** an. *Session* verwendet eine
  `VOLATILE`-Tabelle, die `SPOOL`-Speicher benötigt, aber keinen Perm-Speicher und keine Rechte
  im **Work Schema**. *Standard* benötigt nur Lesezugriff.

---

## 5. Treiber überprüfen (optional) {: #5-verifying-the-driver-optional }

Für eine DSN-lose Verbindung ist es nicht erforderlich, eine ODBC-Datenquelle einzurichten, aber
der Dialog des Treibers ist ein bequemer Weg, um vor der Eingabe in *digna* zu bestätigen, dass
der Treiber und Ihre Anmeldedaten funktionieren.

#### Schritt 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Das Feld **Name or IP address** entspricht hier der Eigenschaft `DBCNAME` in
[Abschnitt 2](#2-odbc-properties).

Klicken Sie auf die Schaltfläche **Test**.

#### Schritt 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Geben Sie Benutzername und Passwort an und klicken Sie dann auf die Schaltfläche **OK**. Ein
Erfolgsbildschirm bestätigt, dass der Treiber und die Anmeldedaten funktionieren.