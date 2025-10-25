---
title: Teradata-tilkobling – Databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna for å koble til Teradata ved å bruke teradatasql Python-driveren eller Teradata ODBC-driveren. Støtter passordbasert autentisering med DSN eller DSN-løse oppsett.
image: /assets/logo_square.png
---


# Source Connector for Teradata

Denne veiledningen beskriver hvordan du konfigurerer *digna* for å koble til Teradata ved å bruke enten den native Python-connectoren eller ODBC-driveren.

Den viser til skjermen **"Opprett en databaseforbindelse"**.

![Opprett en databaseforbindelse](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `teradatasql`  
**Støttet autentisering:** Kun passordbasert autentisering

> ⚠️ For andre autentiseringsmetoder, bruk ODBC-driveren.

### *digna*-konfigurasjon (native driver)

Oppgi følgende informasjon i skjermen **"Opprett en databaseforbindelse"**:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC-driveren kan støtte et bredere spekter av autentiserings- og tilkoblingsmuligheter. Denne seksjonen fokuserer på passordbasert autentisering ved bruk av driveren **Teradata Database ODBC Driver 20.00**.

### 1. Installer ODBC-driveren

Installer driveren **Teradata Database ODBC Driver 20.00** (eller tilsvarende) ved å følge leverandørens offisielle installasjonsveiledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trinnene for å konfigurere en ny ODBC-datakilde ved bruk av passordbasert autentisering:

#### Trinn 1
![Trinn 1](images/teradata/create_odbc_data_source_step1.png)

Klikk på **Test**-knappen.

#### Trinn 2
![Trinn 2](images/teradata/create_odbc_data_source_step2.png)

Oppgi brukernavn og passord.

Klikk på **OK**-knappen.
Når du får suksessskjermen, er ODBC konfigurert riktig.

---

Nå kan du konfigurere *digna* til å bruke ODBC-tilkoblingen, enten med en **DSN (Data Source Name)** eller et **DSN-løst** oppsett.

---

### A. DSN-basert konfigurasjon

#### *digna*-konfigurasjon

I skjermen **"Opprett en databaseforbindelse"**, oppgi følgende:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN` må samsvare med navnet som er definert i ODBC-driverkonfigurasjonen din.

---

### B. DSN-løst konfigurasjon

#### *digna*-konfigurasjon

I skjermen **"Opprett en databaseforbindelse"**, oppgi følgende:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```