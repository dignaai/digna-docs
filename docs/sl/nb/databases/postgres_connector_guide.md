---
title: PostgreSQL Connector – Povezava z bazo podatkov | digna-dokumentacija
description: Konfigurirajte digna za povezavo s PostgreSQL z uporabo Python gonilnika psycopg ali PostgreSQL ODBC gonilnika. Podpira avtentikacijo z geslom z nastavitvijo DSN ali brez DSN.
image: /assets/logo_square.png
---


# Povezava s podatkovnim virom za PostgreSQL

Ta vodič opisuje, kako konfigurirati *digna* za povezavo s Postgresom z uporabo bodisi native Python konektorja bodisi ODBC gonilnika.

Navaja zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativni Python gonilnik

**Library:** `psycopg`  
**Podprta avtentikacija:** Samo avtentikacija z geslom

> ⚠️ Za druge metode avtentikacije uporabite ODBC gonilnik.

### *digna*-konfiguracija (nativni gonilnik)

Na zaslonu **"Create a Database Connection"** vnesite naslednje podatke:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor metod avtentikacije in možnosti povezave. Ta razdelek se osredotoča na avtentikacijo z geslom z uporabo gonilnika **PostgreSQL Unicode(x64)**.

### 1. Namestite ODBC gonilnik

Namestite **PostgreSQL Unicode(x64)** (ali ekvivalent) tako, da sledite uradnim navodilom dobavitelja.

### 2. Konfigurirajte ODBC podatkovni vir

Sledite tem korakom za konfiguracijo novega ODBC podatkovnega vira, ki uporablja avtentikacijo z geslom:

#### Korak 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Opomba: Če vaš nabor podatkov zahteva, da izberete določen "SSLMode", poskrbite, da ga uporabite tudi pri definiranju konfiguracije brez DSN.

#### Korak 2 – Preizkusite povezavo

Kliknite gumb **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC-povezavo, bodisi z **DSN (Data Source Name)** ali z **nastavitvijo brez DSN**.

---

### A. Konfiguracija z DSN

#### *digna*-konfiguracija

Na zaslonu **"Create a Database Connection"**, vnesite naslednje:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN` se mora ujemati z imenom, ki je določeno v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### *digna*-konfiguracija

Na zaslonu **"Create a Database Connection"**, vnesite naslednje:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```