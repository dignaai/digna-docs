---
title: Povezava z Oracle – Integracija baze podatkov | digna-dokumentacija
description: Konfigurirajte digna za povezavo z Oracle z uporabo python-oracledb gonilnika ali Oracle ODBC gonilnika. Podpira avtentikacijo z geslom z DSN ali brez DSN.
image: /assets/logo_square.png
---


# Povezovalnik vira za Oracle

Ta vodič opisuje, kako konfigurirati *digna* za povezavo z Oracle DB z uporabo bodisi nativnega Python-connectorja bodisi ODBC-gonilnika.

Vodič se nanaša na zaslon **"Create a Database Connection"**.

![Ustvarite povezavo z bazo podatkov](images/data_source_config_input_mask.png)

---

## Nativni Python-gonilnik

**Library:** `python-oracledb`  
**Podprta avtentikacija:** Samo avtentikacija z geslom

> ⚠️ Za druge metode avtentikacije uporabite ODBC-gonilnik.

### *digna*-konfiguracija (nativni gonilnik)

Vnesite naslednje informacije na zaslonu **"Create a Database Connection"**:

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

## ODBC-gonilnik

ODBC-gonilnik lahko podpira širši nabor možnosti avtentikacije in povezovanja. Ta razdelek se osredotoča na avtentikacijo z geslom z uporabo gonilnika **Oracle in OraDB21Home1**.

### 1. Namestite ODBC-gonilnik

Namestite **Oracle in OraDB21Home1** (ali ustrezno) po uradnem namestitvenem vodiču dobavitelja.

### 2. Konfigurirajte ODBC-vir podatkov

Sledite tem korakom za konfiguracijo novega ODBC-virja podatkov z avtentikacijo z geslom:

#### Korak 1
![Korak 1](images/oracle/create_odbc_data_source_step1.png)

Opomba:
TNS Service Name mora biti konfiguriran v datoteki tnsnames.ora v vaši namestitvi Oracle odjemalca. Tukaj določite opis povezave (host, port, service name).

#### Korak 2 – Testirajte povezavo

Kliknite gumb **Test Connection**.

![Korak 2](images/oracle/create_odbc_data_source_step2.png)

Vnesite geslo in kliknite gumb **OK**.

![Korak 2](images/oracle/create_odbc_data_source_step3.png)

---

Zdaj lahko konfigurirate *digna* za uporabo ODBC-povezave bodisi z **DSN (Data Source Name)** ali v **brez-DSN** konfiguraciji.

---

### A. DSN-osnovana konfiguracija

#### *digna*-konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

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

> 🔹 `DSN` se mora ujemati z imenom, ki je definirano v konfiguraciji vašega ODBC-gonilnika.

---

### B. Nastavitev brez DSN

#### *digna*-konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```