---
title: Netezza Connector – Datenbankintegration | digna Dokumentation
description: Konfigurieren Sie digna so, dass es sich mit Netezza über den NetezzaSQL ODBC-Treiber verbindet. Unterstützt passwortbasierte Authentifizierung mit DSN- oder DSN‑losen Setups für flexible Konnektivität.
image: /assets/logo_square.png
---


# Source Connector for Netezza

Dieser Leitfaden beschreibt, wie Sie *digna* so konfigurieren, dass es sich über den ODBC-Treiber mit Netezza verbindet.

Er bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC Driver

Der ODBC-Treiber kann eine Reihe von Authentifizierungs- und Konnektivitätsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung mit dem Treiber **NetezzaSQL**.

### 1. Install the ODBC Driver

Installieren Sie den Treiber **NetezzaSQL** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. Configure the ODBC Data Source

Befolgen Sie diese Schritte, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Step 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Abhängig von Ihrem Netezza-Treiber, den Setup- und Sicherheitsanforderungen müssen Sie möglicherweise auch Angaben in den Tabs **Advanced DSN Options**, **SSL DSN Options** oder **Driver Options** machen. Für die einfachste Einrichtung reicht es in der Regel aus, Angaben in **DSN Options** zu machen.

Klicken Sie auf die Schaltfläche **Test Connection**.

#### Step 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Wenn Sie den Erfolgsbildschirm erhalten, ist ODBC korrekt konfiguriert.

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung entweder mit einem **DSN (Data Source Name)** oder in einer **DSN-less** Konfiguration verwendet wird.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Im Bildschirm **"Create a Database Connection"** geben Sie Folgendes an:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

Im Bildschirm **"Create a Database Connection"** geben Sie Folgendes an:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```