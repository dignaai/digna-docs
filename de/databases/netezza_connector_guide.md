# Quell-Connector für Netezza

Dieser Leitfaden beschreibt, wie *digna* so konfiguriert wird, dass eine Verbindung zu Netezza über den ODBC-Treiber hergestellt wird.

Er bezieht sich auf den Bildschirm **"Datenbankverbindung erstellen"**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## ODBC-Treiber

Der ODBC-Treiber kann eine Reihe von Authentifizierungs- und Konnektivitätsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung mit dem Treiber **NetezzaSQL**.

### 1. Installieren des ODBC-Treibers

Installieren Sie den Treiber **NetezzaSQL** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Herstellers.

### 2. Konfigurieren der ODBC-Datenquelle

Gehen Sie folgendermaßen vor, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Schritt 1](images/netezza/create_odbc_data_source_step1.png)

Abhängig von Ihrem Netezza-Treiber, den Installations- und Sicherheitsanforderungen müssen Sie eventuell auch Angaben in den Reitern **Advanced DSN Options**, **SSL DSN Options** oder **Driver Options** machen. Für die einfachste Einrichtung genügt es, Angaben in **DSN Options** zu machen.

Klicken Sie auf die Schaltfläche **Test Connection**.

#### Schritt 2
![Schritt 2](images/netezza/create_odbc_data_source_step2.png)

Wenn der Erfolgsbildschirm erscheint, ist ODBC korrekt konfiguriert.

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder mit einem **DSN (Data Source Name)** oder mit einer **DSN-losen** Einrichtung.

---

### A. DSN-basierte Konfiguration

#### *digna*-Konfiguration

Im Bildschirm **"Datenbankverbindung erstellen"** geben Sie Folgendes an:

```
Name:               Name der Verbindung. Dieser Name wird in anderen Bildschirmen zur Referenzierung der Verbindung verwendet.
Technology:         Netezza
Database Name:      Datenbank, die die Quellschemata enthält
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert und die Metriken werden auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und die Metriken werden auf diesen temporären Daten berechnet.
Work Schema Name:   Beim Einsatz des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-lose Konfiguration

#### *digna*-Konfiguration

Im Bildschirm **"Datenbankverbindung erstellen"** geben Sie Folgendes an:

```
Name:               Name der Verbindung. Dieser Name wird in anderen Bildschirmen zur Referenzierung der Verbindung verwendet.
Technology:         Netezza
Database Name:      Datenbank, die die Quellschemata enthält
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert und die Metriken werden auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und die Metriken werden auf diesen temporären Daten berechnet.
Work Schema Name:   Beim Einsatz des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```