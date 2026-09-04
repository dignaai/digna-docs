---
title: Snowflake'i ühendaja – andmebaasi integratsioon | digna dokumentatsioon
description: Konfigureerige digna ühenduma Snowflake'iga, kasutades Python-konnektorit või Snowflake ODBC draiverit. Toetab paroolipõhist autentimist DSN-iga või DSN-vaba seadistusega.
image: /assets/logo_square.png
---


# Snowflake'i allika konnektor

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Snowflake'iga kas natiivse Python-konnektori või ODBC-draiveri abil.

Viitab ekraanile **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natiivne Python-draiver

**Library:** `snowflake-connector-python`  
**Toetatud autentimine:** Ainult paroolipõhine autentimine

> Muude autentimismeetodite korral kasutage palun ODBC-draiverit.

### *digna* konfiguratsioon (natiivne draiver)

Sisestage järgmine info ekraanil **"Create a Database Connection"**:

```
Technology:      Snowflake
Host Address:    Snowflake konto nimi
Host Port:       Pole vajalik
Database Name:   Andmebaas, mis sisaldab lähte-skeemi
Schema Name:     Skeem, mis sisaldab lähteandmeid
User Name:       Kasutajanimi ja warehouse vormingus "user<@>warehouse"
User Password:   Kasutaja parool
Use ODBC:        Keelatud (vaikimisi)
```

---

## ODBC-draiver

ODBC-draiver võib toetada laiemat valikut autentimis- ja ühendusvõimalusi. See lõik keskendub paroolipõhisele autentimisele, kasutades **SnowflakeDSIIDriver**i.

### 1. Installige ODBC-draiver

Installige **SnowflakeDSIIDriver** järgides tootja ametlikku installijuhendit.

### 2. Konfigureerige ODBC andmeallikas

Järgige neid samme, et konfigureerida uus ODBC andmeallikas paroolipõhise autentimisega:

#### Step 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Märkused:
- Kui te ei sisesta väärtusi väljadele Database, Schema ja Warehouse, peate need esitama ODBC omadustena *digna* andmeallika konfiguratsiooni ajal.
- Välja "Server" väärtus koosneb teie Snowflake konto nimest, millele järgneb ".snowflakecomputing.com"

#### Step 2 – Test the connection

Klõpsake nuppu **TEST**. Edukas ühendus peaks välja nägema selline:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Nüüd saate konfigureerida *digna* kasutama ODBC-ühendust kas **DSN (Data Source Name)**-i või **DSN-vaba** seadistuse kaudu.

---

### A. DSN-põhine konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Create a Database Connection"** sisestage järgmine:

```
Technology:      Snowflake
Database Name:   Andmebaas, mis sisaldab lähte-skeemi
Schema Name:     Skeem, mis sisaldab lähteandmeid
Use ODBC:        Lubatud
```

#### ODBC omadused

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Andmebaas, mis sisaldab lähte-skeemi"
name: "Schema",         value: "Skeem, mis sisaldab lähteandmeid"
name: "Warehouse",      value: "Warehouse, mida kasutada SQL-ide täitmiseks"
```

> `DSN` peab vastama teie ODBC draiveri konfiguratsioonis määratud nimele.

---

### B. DSN-vaba konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Create a Database Connection"** sisestage järgmine:

```
Technology:      Snowflake
Database Name:   Skeem, mis sisaldab lähteandmeid (sama mis Schema Name)
Schema Name:     Skeem, mis sisaldab lähteandmeid
Use ODBC:        Lubatud
```

#### ODBC omadused

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Andmebaas, mis sisaldab lähte-skeemi"
name: "Schema",     value: "Skeem, mis sisaldab lähteandmeid"
name: "Warehouse",  value: "Warehouse, mida kasutada SQL-ide täitmiseks"
```