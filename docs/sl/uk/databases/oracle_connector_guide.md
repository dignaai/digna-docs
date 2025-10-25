---
title: Konektor Oracle – Integracija podatkovnih baz | Dokumentacija digna
description: Nastavite digna za povezavo z Oracle z uporabo gonilnika python-oracledb ali Oracle ODBC gonilnika. Podprta je overitev z geslom s pomočjo DSN ali brez DSN.
image: /assets/logo_square.png
---


# Povezovalnik vira za Oracle

Ta vodič opisuje, kako nastaviti *digna* za povezavo z Oracle DB z uporabo izvornega Python-konektorja ali ODBC gonilnika.

Nanaša se na zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Izvorni Python-gonilnik

**Library:** `python-oracledb`  
**Podprta overitev:** samo overitev z geslom

> ⚠️ Za druge metode overitve uporabite ODBC gonilnik.

### Konfiguracija *digna* (izvorni gonilnik)

Na zaslonu **"Create a Database Connection"** vnesite naslednje informacije:

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

ODBC gonilnik lahko podpira širši nabor načinov overitve in povezav. Ta razdelek se osredotoča na overitev z geslom z uporabo gonilnika **Oracle in OraDB21Home1**.

### 1. Namestite ODBC gonilnik

Namestite **Oracle in OraDB21Home1** (ali podoben) po uradnih navodilih ponudnika.

### 2. Konfigurirajte ODBC vir podatkov

Izvedite te korake za nastavitev novega ODBC vira podatkov z overitvijo z geslom:

#### Korak 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Opomba:
TNS Service Name mora biti nastavljen v datoteki tnsnames.ora vaše namestitve Oracle odjemalca. Tu navedete opis povezave (host, port, service name).

#### Korak 2 – Testiranje povezave

Kliknite gumb **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Vnesite geslo in kliknite **OK**.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC povezavo, bodisi z **DSN (Data Source Name)** ali s konfiguracijo **brez DSN**.

---

### A. Konfiguracija na osnovi DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Lastnosti ODBC

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 Vrednost `DSN` mora biti enaka imenu, določenemu v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Lastnosti ODBC

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```