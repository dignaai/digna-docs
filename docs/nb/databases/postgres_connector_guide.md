---
title: PostgreSQL Connector – Databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna for å koble til PostgreSQL ved å bruke psycopg Python-driveren eller PostgreSQL ODBC-driveren. Støtter passordbasert autentisering med DSN- eller DSN-løs oppsett.
image: /assets/logo_square.png
---


# Kilde-tilkobling for PostgreSQL

Denne guiden beskriver hvordan du konfigurerer *digna* for å koble til Postgres ved hjelp av enten den native Python-connectoren eller ODBC-driveren.

Den refererer til skjermen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativ Python-driver

**Library:** `psycopg`  
**Støttet autentisering:** Kun passordbasert autentisering

> For andre autentiseringsmetoder, vennligst bruk ODBC-driveren.

### *digna*-konfigurasjon (nativ driver)

Oppgi følgende informasjon i skjermen **"Create a Database Connection"**:

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

## ODBC-driver

ODBC-driveren kan støtte et bredere spekter av autentiserings- og tilkoblingsalternativer. Denne seksjonen fokuserer på passordbasert autentisering ved bruk av driveren **PostgreSQL Unicode(x64)**.

### 1. Installer ODBC-driveren

Installer **PostgreSQL Unicode(x64)** (eller tilsvarende) ved å følge leverandørens offisielle installasjonsveiledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trinnene for å konfigurere en ny ODBC-datakilde som bruker passordbasert autentisering:

#### Trinn 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Merk: Hvis databasesettet ditt krever at du velger en spesifikk "SSLMode", sørg for å også bruke denne når du definerer en DSN-løs konfigurering.

#### Trinn 2 – Test tilkoblingen

Klikk på knappen **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Nå kan du konfigurere *digna* til å bruke ODBC-tilkoblingen, enten med en **DSN (Data Source Name)** eller et **DSN-løst** oppsett.

---

### A. DSN-basert konfigurasjon

#### *digna*-konfigurasjon

I skjermen **"Create a Database Connection"**, oppgi følgende:

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

> `DSN` må samsvare med navnet som er definert i din ODBC-driverkonfigurasjon.

---

### B. DSN-løs konfigurasjon

#### *digna*-konfigurasjon

I skjermen **"Create a Database Connection"**, oppgi følgende:

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