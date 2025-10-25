---
title: Apache Hive Connector – Databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna for å koble til Apache Hive ved å bruke den innebygde PyHive-driveren eller Cloudera ODBC-driveren. Støtter passordbasert autentisering og DSN- eller DSN-less-oppsett.
image: /assets/logo_square.png
---


# Kilde-tilkobling for Hive

Denne guiden beskriver hvordan du konfigurerer *digna* for å koble til Hive ved å bruke enten den native Python-connectoren eller ODBC-driveren.

Den viser til skjermen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `PyHive`  
**Støttede autentiseringsmetoder:** Kun passordbasert autentisering

> ⚠️ For andre autentiseringsmetoder, bruk ODBC-driveren.

### *digna*-konfigurasjon (Native Driver)

Oppgi følgende informasjon i skjermen **"Create a Database Connection"**:

```
Technology:      Apache Hive
Host Address:    Servernavn eller IP-adresse
Host Port:       Portnummer, f.eks. 10000
Database Name:   Skjema som inneholder kildedataene
Schema Name:     Skjema som inneholder kildedataene
User Name:       Databasenavn for brukeren
User Password:   Passord for brukeren
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC-driveren kan støtte et bredere spekter av autentiserings- og tilkoblingsalternativer. Denne delen fokuserer på passordbasert autentisering ved bruk av driveren **Cloudera ODBC Driver for Apache Hive**.

### 1. Installer ODBC-driveren

Installer **Cloudera ODBC Driver for Apache Hive** (eller tilsvarende) ved å følge leverandørens offisielle installasjonsveiledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trinnene for å konfigurere en ny ODBC-datakilde med passordbasert autentisering:

#### Trinn 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Trinn 2 – Test tilkoblingen

Oppgi passordet og klikk på **Test**-knappen.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Etter en vellykket test, klikk på **OK**-knappen.

---

Nå kan du konfigurere *digna* til å bruke ODBC-tilkoblingen, enten med en **DSN (Data Source Name)** eller et **DSN-less** oppsett.

---

### A. DSN-basert konfigurasjon

#### *digna*-konfigurasjon

I skjermen **"Create a Database Connection"**, oppgi følgende:

```
Technology:      Apache Hive
Database Name:   Skjema som inneholder kildedataene (samme som Schema Name)
Schema Name:     Skjema som inneholder kildedataene
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{ditt passord i krøllparenteser}"
```

> 🔹 `DSN` må samsvare med navnet som er definert i ODBC-driverkonfigurasjonen din.

---

### B. DSN-less-konfigurasjon

#### *digna*-konfigurasjon

I skjermen **"Create a Database Connection"**, oppgi følgende:

```
Technology:      Apache Hive
Database Name:   Skjema som inneholder kildedataene (samme som Schema Name)
Schema Name:     Skjema som inneholder kildedataene
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "ditt servernavn eller IP-adresse"
name: "PORT",       value: "Portnummer, f.eks. 10000"
name: "Schema",     value: "Skjema som inneholder kildedataene"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```