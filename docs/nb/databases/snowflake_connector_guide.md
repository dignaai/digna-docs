---
title: Snowflake Connector – Databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna for å koble til Snowflake ved hjelp av Python-connectoren eller Snowflake ODBC-driveren. Støtter passordbasert autentisering med DSN- eller DSN-løs oppsett.
image: /assets/logo_square.png
---


# Source Connector for Snowflake

Denne guiden beskriver hvordan du konfigurerer *digna* for å koble til Snowflake ved hjelp av enten den native Python-connectoren eller ODBC-driveren.

Den viser til skjermen **"Create a Database Connection"**.

![Opprett en databaseforbindelse](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `snowflake-connector-python`  
**Støttet autentisering:** Kun passordbasert autentisering

> ⚠️ For andre autentiseringsmetoder, vennligst bruk ODBC-driveren.

### *digna*-konfigurasjon (native driver)

Oppgi følgende informasjon i skjermen **"Create a Database Connection"**:

```
Teknologi:        Snowflake
Vertadresse:      Snowflake-kontonavn
Vertport:         Ikke nødvendig
Databasenavn:     Database som inneholder kildeskjemaet
Schema Name:      Schema som inneholder kildedataene
Brukernavn:       Brukernavn og warehouse i formatet "user<@>warehouse"
Brukerpassord:    Passord for brukeren
Bruk ODBC:        Deaktivert (standard)
```

---

## ODBC Driver

ODBC-driveren kan støtte et bredere spekter av autentiserings- og tilkoblingsmuligheter. Denne seksjonen fokuserer på passordbasert autentisering ved bruk av **SnowflakeDSIIDriver**.

### 1. Installer ODBC-driveren

Installer **SnowflakeDSIIDriver** ved å følge leverandørens offisielle installasjonsveiledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trinnene for å konfigurere en ny ODBC-datakilde ved hjelp av passordbasert autentisering:

#### Trinn 1
![Trinn 1](images/snowflake/create_odbc_data_source_step1.png)

Merk:
- Hvis du ikke oppgir verdier for Database, Schema og Warehouse, må du oppgi dem som ODBC-egenskaper under *digna*-datakildekonfigurasjonen.
- Verdien for "Server" består av Snowflake-kontonavnet ditt etterfulgt av ".snowflakecomputing.com"

#### Trinn 2 – Test tilkoblingen

Klikk på **TEST**-knappen. En vellykket tilkobling bør se slik ut:

![Trinn 2](images/snowflake/create_odbc_data_source_step2.png)

---

Nå kan du konfigurere *digna* til å bruke ODBC-tilkoblingen, enten med en **DSN (Data Source Name)** eller et **DSN-løst** oppsett.

---

### A. DSN-basert konfigurasjon

#### *digna*-konfigurasjon

I skjermen **"Create a Database Connection"**, oppgi følgende:

```
Teknologi:        Snowflake
Databasenavn:     Database som inneholder kildeskjemaet
Schema Name:      Schema som inneholder kildedataene
Bruk ODBC:        Aktivert
```

#### ODBC-egenskaper

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{ditt passord i krøllparenteser}"

valgfritt:
name: "Database",       value: "Database som inneholder kildeskjemaet"
name: "Schema",         value: "Schema som inneholder kildedataene"
name: "Warehouse",      value: "Warehouse som skal brukes for kjøring av SQL-ene"
```

> 🔹 `DSN` må samsvare med navnet som er definert i ODBC-driverkonfigurasjonen din.

---

### B. DSN-løst konfigurasjon

#### *digna*-konfigurasjon

I skjermen **"Create a Database Connection"**, oppgi følgende:

```
Teknologi:        Snowflake
Databasenavn:     Schema som inneholder kildedataene (samme som Schema Name)
Schema Name:      Schema som inneholder kildedataene
Bruk ODBC:        Aktivert
```

#### ODBC-egenskaper

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com"
name: "UID",        value: "din Snowflake-bruker"
name: "PWD",        value: "ditt Snowflake-passord"
name: "Database",   value: "Database som inneholder kildeskjemaet"
name: "Schema",     value: "Schema som inneholder kildedataene"
name: "Warehouse",  value: "Warehouse som skal brukes for kjøring av SQL-ene"
```