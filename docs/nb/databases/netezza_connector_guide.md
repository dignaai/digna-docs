---
title: Netezza-tilkobling – Databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna for å koble til Netezza ved hjelp av NetezzaSQL ODBC-driveren. Støtter passordbasert autentisering med DSN eller DSN-less oppsett for fleksibel tilkobling.
image: /assets/logo_square.png
---


# Source Connector for Netezza

Denne veiledningen beskriver hvordan du konfigurerer *digna* for å koble til Netezza ved hjelp av ODBC-driveren.

Den refererer til skjermen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC Driver

ODBC-driveren kan støtte en rekke autentiserings- og tilkoblingsalternativer. Denne seksjonen fokuserer på passordbasert autentisering ved bruk av driveren **NetezzaSQL**.

### 1. Installer ODBC-driveren

Installer driveren **NetezzaSQL** (eller tilsvarende) ved å følge leverandørens offisielle installasjonsveiledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trinnene for å konfigurere en ny ODBC-datakilde med passordbasert autentisering:

#### Trinn 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Avhengig av din Netezza-driver, oppsett og sikkerhetskrav, kan det hende du også må oppgi data i fanene **Advanced DSN Options**, **SSL DSN Options** eller **Driver Options**. For et enklest mulig oppsett er det tilstrekkelig å oppgi data i **DSN Options**.

Klikk på knappen **Test Connection**.

#### Trinn 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Når du får suksessskjermen, er ODBC riktig konfigurert.

---

Nå kan du konfigurere *digna* til å bruke ODBC-tilkoblingen, enten med en **DSN (Data Source Name)** eller et **DSN-less** oppsett.

---

### A. DSN-basert konfigurering

#### *digna* Konfigurasjon

I skjermen **"Create a Database Connection"**, oppgi følgende:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN` må samsvare med navnet som er definert i ODBC-driverkonfigurasjonen din.

---

### B. DSN-less konfigurering

#### *digna* Konfigurasjon

I skjermen **"Create a Database Connection"**, oppgi følgende:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```