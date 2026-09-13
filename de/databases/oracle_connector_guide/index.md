# Quell-Connector für Oracle

Diese Anleitung beschreibt, wie Sie *digna* für die Verbindung zur Oracle Database über **ODBC**
konfigurieren, und zwar mit einer **DSN-losen** Verbindungszeichenfolge.

Die digna-Seite der Einrichtung ist für jede Technologie gleich — wo Verbindungen angelegt
werden, wie Eigenschaftswerte verschlüsselt werden, wie eine Verbindung getestet wird und was
die Profiling-Modi bedeuten. Das ist in der [Übersicht über Datenbankverbindungen](overview.md)
beschrieben. Diese Seite behandelt, was für Oracle spezifisch ist.

---

## 1. ODBC-Treiber installieren {: #1-install-the-odbc-driver }

Der Oracle-ODBC-Treiber ist Teil des **Oracle Client** (das Instant-Client-Paket „ODBC“ genügt).
Installieren Sie ihn auf dem Rechner, auf dem das *digna*-Backend läuft, und folgen Sie dabei
der offiziellen Installationsanleitung des Herstellers.

Der Treiber registriert sich als **Oracle in `<OracleHomeName>`** — zum Beispiel
`Oracle in OraDB21Home1` oder `Oracle in instantclient_21_13`. Der Home-Name unterscheidet sich
je nach Installation, lesen Sie den genauen Namen daher auf Ihrem Host ab, wie unter
[ODBC-Treiber auf dem digna-Host installieren](overview.md#install-the-driver) beschrieben.

---

## 2. ODBC-Eigenschaften {: #2-odbc-properties }

!!! important "Ein Beispiel, keine Spezifikation"

    Der folgende Satz ist eine Kombination, von der bekannt ist, dass sie funktioniert. Die
    Eigenschaften gehören zum Oracle-ODBC-Treiber, daher unterscheiden sich ihre Namen,
    Standardwerte und zulässigen Werte zwischen Client-Versionen, und insbesondere der
    Treibername hängt vom Oracle-Home auf Ihrem Host ab. Nehmen Sie dies als Ausgangspunkt und
    prüfen Sie die Dokumentation der von Ihnen installierten Client-Version.

Fügen Sie im Bildschirm **Add DB Connection** die folgenden Eigenschaften hinzu:

| Schlüssel | Beispielwert | Hinweise |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Muss dem auf dem *digna*-Host registrierten Treibernamen entsprechen |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Die Datenbank, zu der verbunden wird — siehe unten |
| `UID` | `DIGNA_SOURCE_USER` | Datenbankbenutzer |
| `PWD` | `<password>` | **Encrypted** ankreuzen |

Die resultierende Verbindungszeichenfolge sieht so aus:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### Der Wert von `DBQ`

`DBQ` akzeptiert drei Formen. Für *digna* sind sie gleichwertig; sie unterscheiden sich darin,
was auf dem *digna*-Host konfiguriert sein muss:

| Form | Beispiel | Erfordert |
|---|---|---|
| **Vollständiger Connect-Deskriptor** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Nichts — alles steht in der Eigenschaft. Empfohlen |
| **TNS-Alias** | `DIGNA_SOURCE` | Der Alias muss in der `tnsnames.ora` des Oracle Client auf dem *digna*-Host vorhanden sein |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Einen Oracle Client, der Easy Connect unterstützt (12c und später) |

!!! tip "Bevorzugen Sie den vollständigen Deskriptor"

    Ein TNS-Alias verlagert die halbe Verbindungsdefinition in eine Datei auf dem *digna*-Host,
    wo sie leicht vergessen wird, wenn der Host neu aufgesetzt oder *digna* verschoben wird. Der
    vollständige Deskriptor hält die Verbindung in sich geschlossen — und genau darum geht es bei
    einer DSN-losen Einrichtung.

Beachten Sie: Die Klammern eines Deskriptors sind innerhalb einer Verbindungszeichenfolge
unproblematisch; enthält Ihr Passwort jedoch `;`, setzen Sie es in geschweifte Klammern:
`PWD={p@ss;word}`.

---

## 3. *digna*-Konfiguration {: #3-digna-configuration }

Geben Sie im Bildschirm **Add DB Connection** Folgendes an:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Hinweise zu Oracle {: #4-notes-on-oracle }

- **Schemata sind Benutzer.** *digna* listet Oracle-Benutzer als Schemata auf, das Quellschema
  ist also der Eigentümer der Tabellen — im obigen Beispiel `DIGNA_SOURCE_USER`. Der
  Verbindungsbenutzer benötigt `SELECT` auf diese Tabellen, entweder direkt oder über eine Rolle.
- **Eine Verbindung sieht eine Datenbank.** Der Katalog, den *digna* anbietet, ist die Datenbank,
  an der die Verbindung hängt; `DBQ` entscheidet also, welcher Service und damit welche Datenbank
  profiliert wird.
- **Bezeichner sind nach dem Quoten case-sensitiv.** *digna* quotet die Namen, die es aus dem
  Data Dictionary liest — und das ist, was Oracle speichert: Großbuchstaben für nicht gequotete
  Objekte.
- **Profiling-Modi.** *Permanent* legt die Arbeitstabellen im **Work Schema** an, der Benutzer
  braucht dort also `CREATE TABLE` und eine Quota auf dem Tablespace. *Session* verwendet eine
  private temporäre Tabelle (`ORA$PTT_…`, Oracle 18c und später) und rührt das **Work Schema**
  nicht an. *Standard* benötigt nur Lesezugriff.

---

## 5. Treiber überprüfen (optional) {: #5-verifying-the-driver-optional }

Für eine DSN-lose Verbindung ist es nicht erforderlich, eine ODBC-Datenquelle einzurichten, aber
der Dialog des Treibers ist ein bequemer Weg, um vor der Eingabe in *digna* zu bestätigen, dass
der Oracle Client, der Servicename und Ihre Anmeldedaten funktionieren.

#### Schritt 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Der hier angebotene **TNS Service Name** stammt aus der `tnsnames.ora` Ihrer
Oracle-Client-Installation — dort ist der Alias und mit ihm Host, Port und Servicename
definiert. In *digna* können Sie den Alias als `DBQ` verwenden oder stattdessen den
vollständigen Deskriptor.

#### Schritt 2 – Verbindung testen

Klicken Sie auf die Schaltfläche **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Geben Sie das Passwort an und klicken Sie auf die Schaltfläche **OK**.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

Eine Erfolgsmeldung bestätigt, dass der Treiber und die Anmeldedaten funktionieren.