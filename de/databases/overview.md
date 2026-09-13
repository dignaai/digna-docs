# Übersicht über Datenbankverbindungen

---

## Inhaltsverzeichnis

1. [Wie Verbindungen funktionieren](#how-connections-work)
2. [Anleitungen je Technologie](#technology-guides)
3. [Voraussetzung: ODBC-Treiber auf dem digna-Host installieren](#install-the-driver)
4. [Eine Datenbankverbindung anlegen](#create-a-database-connection)
5. [ODBC-Eigenschaften](#odbc-properties)
6. [Eigenschaftswerte verschlüsseln](#encrypting-property-values)
7. [Eine Verbindung testen](#testing-a-connection)
8. [Welche Datenbank die Verbindung sieht](#which-database-the-connection-sees)
9. [Profiling-Modus und Work Schema](#profiling-mode-and-work-schema)
10. [Stattdessen einen DSN verwenden](#using-a-dsn-instead)
11. [Fehlersuche](#troubleshooting)

---

## Wie Verbindungen funktionieren {: #how-connections-work }

*digna* erreicht jede Quelltechnologie über **ODBC**. Eine Verbindung ist eine Liste von
ODBC-Eigenschaften, die Sie als Schlüssel-Wert-Paare eingeben. Wenn *digna* die Verbindung
öffnet, fügt es diese Paare zu einer Verbindungszeichenfolge zusammen — `Key=Value`, getrennt
durch `;`, in der von Ihnen angegebenen Reihenfolge — und übergibt sie dem ODBC-Treibermanager
auf dem *digna*-Host.

Dass Sie die Eigenschaften selbst eingeben, macht die Einrichtung **DSN-los**: Die Verbindung
trägt alles, was der Treiber braucht, sodass auf dem Host keine ODBC-Datenquelle (DSN)
registriert werden muss. Das ist der empfohlene Weg, *digna* zu konfigurieren, weil die
Verbindungsdefinition vollständig in *digna* liegt und mit ihm umzieht.

### Warum ODBC {: #why-odbc }

Frühere Releases boten die Wahl zwischen einem technologiespezifischen Treiber und ODBC,
ausgewählt über den Schalter **Use ODBC**. Ab Release 2026.06 setzt *digna* allein auf ODBC.
Eine einzige, standardisierte Schnittstelle bietet mehr als ein Satz maßgeschneiderter Treiber:

- **Authentifizierung** — die Authentifizierung ist Teil von ODBC, sodass eine Verbindung alles
  nutzen kann, was ihr Treiber unterstützt: Passwörter, Tokens und PATs, Kerberos und Active
  Directory, MFA und browserbasiertes Single Sign-on, Cloud-Identitäten, Client-Zertifikate und
  TLS. Neue Verfahren kommen mit einem Treiber-Update, statt auf ein *digna*-Release zu warten.
- **Von den Datenbankherstellern gepflegte Treiber** — der herstellereigene Treiber folgt neuen
  Serverversionen und Sicherheitsupdates, und Sie können ihn unabhängig von *digna* nach Ihrem
  eigenen Zeitplan aktualisieren.
- **Eine einheitliche Konfiguration** — jede Technologie ist eine Liste von
  Schlüssel-Wert-Eigenschaften, mit derselben Oberfläche, derselben Verschlüsselung sensibler
  Werte und derselben Fehlersuche, statt unterschiedlicher Felder je Quelle.
- **Feinabstimmung und Reichweite** — Treiberoptionen wie Timeouts, TLS-Einstellungen, Proxys
  und Fetch-Größen stehen für jede Quelle zur Verfügung, und jede Technologie mit einem
  konformen ODBC-Treiber lässt sich anbinden, auch solche, für die *digna* keine eigene
  Anleitung veröffentlicht.

!!! note "Was sich in der Oberfläche geändert hat"

    Den Schalter **Use ODBC** und die separaten Felder für Host, Port, Datenbank, Benutzer und
    Passwort gibt es nicht mehr. Eine Verbindung, die nicht bereits ODBC verwendet, braucht ihre
    ODBC-Eigenschaften, bevor sie wieder funktioniert — siehe
    [Eine Datenbankverbindung anlegen](#create-a-database-connection).

---

## Anleitungen je Technologie {: #technology-guides }

Die Eigenschaftsnamen unterscheiden sich je Treiber, und jede Technologie hat ein bis zwei
Besonderheiten, die die anderen nicht haben. Die folgenden Anleitungen decken diesen Teil ab;
diese Seite behandelt die *digna*-Seite, die für alle gleich ist.

!!! important "Die Eigenschaftssätze in den Anleitungen sind Beispiele"

    Jede Anleitung zeigt eine Kombination, von der bekannt ist, dass sie funktioniert — die, auf
    die *digna* getestet ist. Sie ist ein Ausgangspunkt, keine Spezifikation: Die Eigenschaften
    gehören zum ODBC-Treiber, und welche es gibt, wie sie heißen und welche Werte sie annehmen,
    unterscheidet sich zwischen Treiberversionen und Herstellern, zwischen Windows, Linux und
    macOS und danach, wie der Quellserver konfiguriert ist — Authentifizierungsmethode, TLS,
    Gateway, Port. Rechnen Sie damit, den einen oder anderen Wert anzupassen, und betrachten Sie
    die Dokumentation der von Ihnen installierten Treiberversion als maßgeblich.

| Technologie | Anleitung | Wissenswert |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverlose Pools brauchen `-ondemand` im Hostnamen und unterstützen nur *Standard*-Profiling |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Token-Authentifizierung: `UID=token`, PAT in `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Kataloge kommen vom Treiber, nicht aus einer Abfrage |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Der Treibername steht in geschweiften Klammern: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` nimmt entweder einen vollständigen Connect-Deskriptor oder einen `tnsnames.ora`-Alias |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` muss zu dem passen, was der Server verlangt |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` entscheidet, welche Schemata *digna* sehen kann |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Das programmatische Zugriffstoken ist der getestete Authentifizierungsweg |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Der Host gehört in `DBCNAME`; Datenbanken wirken wie Schemata |

---

## Voraussetzung: ODBC-Treiber auf dem digna-Host installieren {: #install-the-driver }

*digna* öffnet Quellverbindungen von dem **Server aus, auf dem das digna-Backend läuft**, nicht
vom Browser. Der ODBC-Treiber muss daher auf diesem Rechner installiert und sein Name beim
lokalen Treibermanager registriert sein.

=== "Windows"

    Installieren Sie den 64-Bit-Treiber des Herstellers, öffnen Sie dann den
    **ODBC-Datenquellen-Administrator (64 Bit)** und wechseln Sie auf den Reiter **Drivers**.
    Die dort aufgeführten Namen sind genau die Werte, die Sie für die Eigenschaft `Driver`
    verwenden dürfen.

=== "Linux"

    Installieren Sie **unixODBC** und den Treiber des Herstellers und lassen Sie sich dann die
    registrierten Treibernamen ausgeben:

    ```bash
    odbcinst -q -d
    ```

    Die in Klammern ausgegebenen Namen sind die Werte, die Sie für die Eigenschaft `Driver`
    verwenden dürfen. Sie stammen aus `/etc/odbcinst.ini` (oder aus der Datei, die
    `odbcinst -j` meldet).

=== "macOS"

    Installieren Sie **unixODBC** (zum Beispiel mit `brew install unixodbc`) und den Treiber des
    Herstellers und lassen Sie sich dann die registrierten Treibernamen ausgeben:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Der Treibername muss Zeichen für Zeichen übereinstimmen"

    `Driver` wird unverändert an den Treibermanager übergeben. `Simba Spark ODBC Driver` und
    `Simba Spark ODBC Driver 64` sind für den Treibermanager unterschiedliche Treiber, und ein
    nicht registrierter Name erzeugt einen *data source name not found*-Fehler, obwohl gar kein
    DSN im Spiel ist.

Statt eines registrierten Namens akzeptieren alle gängigen Treibermanager auch den vollständigen
Pfad zur Treiberbibliothek, zum Beispiel
`Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Das ist nützlich, wenn der Treiber
installiert, aber nicht registriert ist.

---

## Eine Datenbankverbindung anlegen {: #create-a-database-connection }

Öffnen Sie das **Admin Panel**, gehen Sie auf den Reiter **Database Connections** und klicken
Sie auf **Add DB Connection**. Der Bildschirm fragt fünf Dinge ab:

| Feld | Beschreibung |
|---|---|
| **Name** | Name der Verbindung. Über ihn wird die Verbindung in anderen Bildschirmen referenziert. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake oder Hive. Wählt den SQL-Dialekt, den *digna* erzeugt, muss also zur Quelle passen — nicht zum Treiber. Azure Synapse Analytics ist eine **SQL Server**-Verbindung. |
| **ODBC Properties** | Die Schlüssel-Wert-Paare, die unter [ODBC-Eigenschaften](#odbc-properties) beschrieben sind. |
| **Profiling Mode** | *Standard*, *Permanent* oder *Session* — siehe [Profiling-Modus und Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Schema, das die Arbeitstabellen für *Permanent*-Profiling enthält. |

Eine Verbindung wird zentral verwaltet und dann einem oder mehreren Projekten zugewiesen, sodass
dieselbe Verbindung mehrere Projekte bedienen kann.

---

## ODBC-Eigenschaften {: #odbc-properties }

Klicken Sie für jede Eigenschaft auf **Add Property** und füllen Sie **Key**, **Value** und, bei
Geheimnissen, das Kontrollkästchen **Encrypted** aus. Jede Technologie-Anleitung führt einen
Beispielsatz für die betreffende Technologie auf, den Sie an Ihre Treiberversion und Ihren
Server anpassen — siehe [den Hinweis oben](#technology-guides).

Unabhängig vom Treiber deckt ein Eigenschaftssatz dieselben vier Dinge ab:

- **`Driver`** — den registrierten Treibernamen, wie [oben](#install-the-driver) beschrieben.
- **Die Adresse des Servers** — der Schlüssel unterscheidet sich je Treiber: `SERVER`, `HOST`,
  `DBCNAME`, `Server` oder, bei Oracle, der Connect-Deskriptor `DBQ`.
- **Anmeldedaten** — meist `UID` und `PWD`; Snowflake verwendet `UID` plus ein `token`, und
  Databricks den wörtlichen Benutzer `token` plus das persönliche Zugriffstoken in `PWD`.
- **Die Datenbank oder den Katalog, in dem gearbeitet wird**, sofern die Technologie so etwas
  hat — siehe [Welche Datenbank die Verbindung sieht](#which-database-the-connection-sees).

Alles Weitere, was der Treiber dokumentiert, lässt sich genauso ergänzen —
Verbindungs-Pooling, Socket-Timeouts, Kerberos-Einstellungen, Proxy-Einstellungen. *digna*
interpretiert die Eigenschaften nicht; es reicht sie nur weiter.

!!! warning "Werte werden nicht escaped — setzen Sie alles mit Semikolon in geschweifte Klammern"

    Da die Eigenschaften mit `;` verbunden werden, würde ein Wert, der selbst `;` enthält, die
    Verbindungszeichenfolge an der falschen Stelle teilen. Setzen Sie solche Werte in geschweifte
    Klammern: `PWD={p@ss;word}`. Dasselbe gilt für Werte mit `=` oder führenden Leerzeichen.
    Deshalb werden manche Treiber üblicherweise geklammert geschrieben, wie `{NetezzaSQL}` oder
    `{SnowflakeDSIIDriver}`.

---

## Eigenschaftswerte verschlüsseln {: #encrypting-property-values }

Kreuzen Sie **Encrypted** für jede Eigenschaft an, die ein Geheimnis enthält — `PWD`, `token`,
ein Client-Secret. Der Wert wird dann verschlüsselt, bevor er im *digna*-Repository gespeichert
wird, im Bildschirm maskiert und nur beim Zusammensetzen der Verbindungszeichenfolge
entschlüsselt.

!!! tip "Tipp"

    Ein verschlüsselter Wert kann nicht zurückgelesen werden, weder in der Oberfläche noch über
    die API — er kann nur ersetzt werden. Bewahren Sie Geheimnisse zusätzlich in Ihrem eigenen
    Passwortmanager auf.

Eigenschaften, die kein Geheimnis sind — Treibername, Host, Port, Datenbank —, lassen Sie am
besten unverschlüsselt, damit sie für den lesbar bleiben, der die Verbindung später betreut.

---

## Eine Verbindung testen {: #testing-a-connection }

Klicken Sie im Dialog *Add DB Connection* auf **Test**, **bevor** Sie speichern. Der Test
verwendet die aktuell im Formular stehenden Werte und baut eine echte Verbindung auf, meldet
also genau das, worauf eine Inspektion stoßen würde — einen falschen Treibernamen, ein
abgelehntes Passwort, einen nicht erreichbaren Host. Es wird nichts gespeichert: Die
Testverbindung wird zurückgerollt, ob sie gelingt oder scheitert.

Bei einer bereits bestehenden Verbindung fahren Sie im Reiter **Database Connections** über ihre
Zeile und klicken auf das **Stecker**-Symbol, um sie erneut zu testen. Das ist der schnellste
Weg zu prüfen, ob eine Quelle nach einem Passwortwechsel oder einer Firewall-Änderung erreichbar
ist.

---

## Welche Datenbank die Verbindung sieht {: #which-database-the-connection-sees }

Wenn Sie eine Datenquelle hinzufügen, bietet *digna* die Kataloge, Schemata und Tabellen an, die
die Verbindung erreichen kann. Wie weit das reicht, hängt von der Technologie ab:

| Technologie | Angebotene Kataloge |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Nur die **aktuelle** Datenbank der Verbindung |
| **Teradata**, **Netezza**, **Databricks** | Alle Datenbanken oder Kataloge, die der Benutzer sehen darf |
| **Hive**, **Impala** | Vom Treiber gemeldet |

!!! important "Eine Verbindung, eine Datenbank"

    Bei PostgreSQL, SQL Server, Oracle und Snowflake müssen die Eigenschaften auf die Datenbank
    zeigen, die die Quellschemata enthält — `DATABASE=…`, `Database=…` oder den Servicenamen
    innerhalb von Oracles `DBQ`. Tabellen in einer anderen Datenbank sind über diese Verbindung
    nicht erreichbar; legen Sie dafür eine zweite Verbindung an.

---

## Profiling-Modus und Work Schema {: #profiling-mode-and-work-schema }

Der Profiling-Modus bestimmt, wie *digna* Daten verarbeitet und Metriken berechnet:

- **Standard:** Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu
  kopieren.
- **Permanent:** Die Daten des inspizierten Tages werden in eine permanente Tabelle kopiert, und
  die Metriken werden auf den kopierten Daten berechnet.
- **Session:** Die Daten werden in eine Sitzungs- oder temporäre Tabelle kopiert, und die
  Metriken werden auf diesen temporären Daten berechnet.

Der Modus entscheidet, was dem Verbindungsbenutzer erlaubt sein muss:

| Modus | Schreibt | Rechte, die der Verbindungsbenutzer braucht |
|---|---|---|
| **Standard** | nichts | Lesen auf den Quelltabellen |
| **Permanent** | eine Tabelle je Datenquelle im **Work Schema** | Tabellen im **Work Schema** anlegen und löschen |
| **Session** | eine temporäre Tabelle, die die Datenbank mit der Sitzung verwirft | Temporäre Tabellen anlegen — **Work Schema** wird nicht verwendet |

*Standard* liest nur, was es zum Modus der Wahl macht, wenn *digna* nur Lesezugriff erhält. Das
**Work Schema** wird nur bei *Permanent* gelesen, es lohnt sich aber, es trotzdem auszufüllen,
damit die Verbindung weiter funktioniert, falls der Modus später geändert wird.

---

## Stattdessen einen DSN verwenden {: #using-a-dsn-instead }

Ein DSN funktioniert weiterhin — `DSN` ist einfach eine weitere Eigenschaft:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

Der DSN muss auf dem *digna*-Host registriert sein, und zwar für dasselbe Benutzerkonto, unter
dem das *digna*-Backend läuft, und als **System-DSN**, wenn *digna* als Dienst läuft. Alles, was
im DSN konfiguriert ist, lässt sich überschreiben, indem Sie es zusätzlich als Eigenschaft
angeben.

DSN-los ist die dokumentierte Voreinstellung, weil es diesen Zustand auf dem Host vermeidet: Die
Verbindung ist vollständig in *digna* beschrieben, und ein neuer *digna*-Host braucht den
installierten Treiber, aber nichts konfiguriert.

---

## Fehlersuche {: #troubleshooting }

### Datenquellenname nicht gefunden / kein Standardtreiber angegeben

**Symptome:**
- Die Schaltfläche **Test** meldet einen Fehler, der *data source name not found* erwähnt,
  obwohl die Einrichtung DSN-los ist

**Ursachen & Lösungen:**
1. Der Wert von `Driver` entspricht keinem registrierten Treibernamen — vergleichen Sie ihn mit
   dem Reiter **Drivers** des *ODBC-Datenquellen-Administrators (64 Bit)* oder mit
   `odbcinst -q -d`
2. Der Treiber ist auf Ihrer Arbeitsstation installiert, aber nicht auf dem *digna*-Host
3. Der Treiber ist 32-Bit, während *digna* 64-Bit ist — installieren Sie den 64-Bit-Treiber
4. Die Eigenschaft `Driver` fehlt ganz, und es wurde auch kein `DSN` angegeben
5. Unter Linux und macOS ist der Treiber installiert, aber nicht registriert — geben Sie
   stattdessen den vollständigen Pfad zur Treiberbibliothek an oder registrieren Sie ihn in
   `odbcinst.ini`

---

### Der Verbindungstest läuft in ein Timeout

**Symptome:**
- **Test** hängt und scheitert dann nach etwa einer halben Minute

**Ursachen & Lösungen:**
1. Host oder Port sind vom *digna*-Host aus nicht erreichbar — prüfen Sie die Firewall und, bei
   Cloud-Quellen, die IP-Freigabeliste
2. Der Hostname stimmt, aber der Port gehört zu einem anderen Dienst
3. Die Quelle braucht länger als die standardmäßigen 30 Sekunden, um eine Verbindung
   anzunehmen — erhöhen Sie `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` im Abschnitt `[base]` der
   `config.toml` (`0` wartet unbegrenzt) und starten Sie das Backend neu
4. Ein serverloser Endpunkt fährt aus dem Ruhezustand hoch — wiederholen Sie den Versuch, und
   wenn das regelmäßig vorkommt, erhöhen Sie wie oben das Login-Timeout

---

### Die Authentifizierung scheitert, obwohl die Anmeldedaten stimmen

**Symptome:**
- Der Treiber meldet ungültige Anmeldedaten, aber derselbe Benutzer funktioniert in einem
  anderen SQL-Client

**Ursachen & Lösungen:**
1. Das Passwort enthält `;` — setzen Sie den Wert in geschweifte Klammern: `{p@ss;word}`
2. Ein abschließendes Leerzeichen wurde in den Wert kopiert
3. Der Treiber erwartet einen bestimmten Authentifizierungsmechanismus — zum Beispiel
   `AuthMech` bei den Hive- und Databricks-Treibern oder `authenticator` bei Snowflake
4. Der Wert wurde verschlüsselt gespeichert und danach bearbeitet — verschlüsselte Werte lassen
   sich nicht zurücklesen, geben Sie das Geheimnis also vollständig neu ein
5. Ein Token ist abgelaufen — persönliche Zugriffstoken und programmatische Zugriffstoken werden
   mit einem Ablaufdatum ausgestellt

---

### Der Datenquellen-Bildschirm bietet die erwartete Datenbank oder das erwartete Schema nicht an

**Symptome:**
- Beim Hinzufügen einer Datenquelle fehlen Kataloge, Schemata oder Tabellen

**Ursachen & Lösungen:**
1. Die Verbindung zeigt auf eine andere Datenbank — siehe
   [Welche Datenbank die Verbindung sieht](#which-database-the-connection-sees)
2. Dem Verbindungsbenutzer fehlen Leserechte auf das Schema oder auf das Data Dictionary
3. **Technology** passt nicht zur Quelle, daher fragt *digna* das falsche Data Dictionary ab
4. Bei Snowflake ist dem Benutzer kein Standard-Warehouse zugewiesen und es wurde keine
   `Warehouse`-Eigenschaft angegeben, sodass Metadatenabfragen nicht laufen können

---

### Das Profiling scheitert, während der Verbindungstest gelingt

**Symptome:**
- **Test** ist erfolgreich, aber eine Inspektion scheitert, wenn Arbeitstabellen angelegt werden

**Ursachen & Lösungen:**
1. *Permanent*-Profiling ist ausgewählt und der Verbindungsbenutzer kann im **Work Schema**
   keine Tabellen anlegen — erteilen Sie die Rechte oder wechseln Sie zu *Session* oder
   *Standard*
2. **Work Schema** ist leer oder nennt ein Schema, das nicht existiert, während
   *Permanent*-Profiling ausgewählt ist
3. *Session*-Profiling ist ausgewählt und der Verbindungsbenutzer darf keine temporären Tabellen
   anlegen
4. Eine lange laufende Profiling-Abfrage erreicht das Abfrage-Timeout — erhöhen Sie
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` im Abschnitt `[base]` der `config.toml` (Standard 3600
   Sekunden, `0` deaktiviert das Timeout)

---

## Bewährte Vorgehensweisen

**TUN SIE DIES:**

- Installieren und registrieren Sie den Treiber auf dem *digna*-Host, bevor Sie die Verbindung
  konfigurieren
- Kreuzen Sie **Encrypted** für jedes Passwort und jedes Token an
- Klicken Sie vor dem Speichern auf **Test** und testen Sie nach einem Passwortwechsel erneut
- Benennen Sie Verbindungen nach Quelle und Umgebung, zum Beispiel `sales_dwh_prod`
- Geben Sie *digna* einen eigenen Datenbankbenutzer, schreibgeschützt, wo
  *Standard*-Profiling genügt
- Behalten Sie eine Verbindung je Quelldatenbank und legen Sie lieber eine zweite an, als die
  erste umzustellen

**TUN SIE DIES NICHT:**

- Geheimnisse unverschlüsselt speichern oder einen Datenbankbenutzer zwischen *digna* und
  anderen Werkzeugen teilen
- Einen 32-Bit-Treiber mit einer 64-Bit-*digna*-Installation verwenden
- Sich auf einen Benutzer-DSN verlassen, wenn *digna* als Dienst läuft — er ist dann nicht
  sichtbar
- Einen Wert, der `;` enthält, ohne geschweifte Klammern in eine Eigenschaft eintragen
- **Work Schema** auf ein Schema zeigen lassen, das Quelldaten enthält

---

## Support

Brauchen Sie Hilfe bei einer Datenbankverbindung?

- **E-Mail:** support@digna.ai
- **Dokumentation:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**