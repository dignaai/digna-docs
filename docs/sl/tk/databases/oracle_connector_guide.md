---
title: Oracle Povezovalnik – Integracija baze podatkov | digna dokumentacija
description: Konfigurirajte digna za povezavo z Oracle z uporabo gonilnika python-oracledb ali Oracle ODBC. Podpira overjanje z geslom z nastavitvami z DSN ali brez DSN.
image: /assets/logo_square.png
---


# Viri za Oracle

Ta vodnik pojasnjuje, kako povezati *digna* z bazo podatkov Oracle z uporabo lokalne Python povezave ali ODBC gonilnika.

To se nanaša na zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Lokalni Python gonilnik

**Knjiznica:** `python-oracledb`  
**Podprto overjanje:** Samo overjanje z geslom

> ⚠️ Za druge metode overjanja uporabite ODBC gonilnik.

### Konfiguracija *digna* (lokalni gonilnik)

Na zaslonu **"Create a Database Connection"** predložite naslednje podatke:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti overjanja in povezav. Ta razdelek se osredotoča na overjanje z geslom z uporabo gonilnika **Oracle in OraDB21Home1**.

### 1. Namestite ODBC gonilnik

Namestite gonilnik **Oracle in OraDB21Home1** (ali podoben) po uradnemu namestitvenemu vodniku ponudnika.

### 2. Konfigurirajte ODBC vir podatkov

Za konfiguracijo novega ODBC vira podatkov z overjanjem z geslom sledite tem korakom:

#### Korak 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Opomba:
TNS Service Name mora biti konfiguriran v datoteki tnsnames.ora vaše Oracle odjemalske namestitve. Tukaj zagotovite identifikator povezave (host, port, service name).

#### Korak 2 – Preizkusite povezavo

Kliknite gumb **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Vnesite geslo in kliknite **OK**.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Zdaj lahko *digna* konfigurirate za uporabo ODBC povezave bodisi z **DSN (Data Source Name)** bodisi z nastavitvijo brez DSN.

---

### A. Konfiguracija na osnovi DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** predložite naslednje:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 `DSN` mora ustrezati imenu, definiranemu v vaši konfiguraciji ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** predložite naslednje:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user"
name: "PWD",        value: "your oracle password"
```