---
title: Snowflake Connector – integracija podatkovne baze | dokumentacija digna
description: Nastavite digna za povezavo do Snowflake z uporabo Python-konektorja ali ODBC-voznikov. Podprta je avtentikacija z geslom v konfiguracijah z DSN ali brez DSN.
image: /assets/logo_square.png
---


# Vir povezave za Snowflake

Ta vodnik opisuje, kako nastaviti *digna* za povezavo do Snowflake z uporabo bodisi izvornega Python-konektorja ali ODBC-voznikov.

Sklicuje se na zaslon **«Ustvari povezavo do baze podatkov»**.

![Ustvari povezavo do baze podatkov](images/data_source_config_input_mask.png)

---

## Izvorni Python-voznik

**Knjižnica:** `snowflake-connector-python`  
**Podprta avtentikacija:** samo avtentikacija z geslom

> ⚠️ Za druge metode avtentikacije uporabite ODBC-voznik.

### Konfiguracija *digna* (izvorni voznik)

Na zaslonu **«Ustvari povezavo do baze podatkov»** vnesite naslednje informacije:

```
Technology:      Snowflake
Host Address:    Ime Snowflake računa
Host Port:       Ni potrebno
Database Name:   Baza podatkov, ki vsebuje izvorno shemo
Schema Name:     Shema, ki vsebuje izvorne podatke
User Name:       Uporabniško ime in warehouse v formatu "user<@>warehouse"
User Password:   Geslo uporabnika
Use ODBC:        Izklopljeno (privzeto)
```

---

## ODBC-voznik

ODBC-voznik lahko podpira širši nabor možnosti avtentikacije in povezovanja. Ta razdelek je osredotočen na avtentikacijo z geslom z uporabo **SnowflakeDSIIDriver**.

### 1. Namestite ODBC-voznik

Namestite **SnowflakeDSIIDriver** v skladu z uradnim navodilom za namestitev ponudnika.

### 2. Nastavite ODBC vir podatkov

Upoštevajte te korake za nastavitev novega ODBC vira podatkov z avtentikacijo z geslom:

#### Korak 1
![Korak 1](images/snowflake/create_odbc_data_source_step1.png)

Opombe:
- Če ne navedete vrednosti za Database, Schema in Warehouse, jih boste morali navesti kot lastnosti ODBC med konfiguracijo vira podatkov v *digna*.
- Vrednost za "Server" je sestavljena iz imena vašega Snowflake računa z dodanim ".snowflakecomputing.com"

#### Korak 2 – Preizkus povezave

Kliknite gumb **TEST**. Uspešna povezava izgleda takole:

![Korak 2](images/snowflake/create_odbc_data_source_step2.png)

---

Zdaj lahko nastavite *digna*, da uporablja ODBC-povezavo, bodisi z **DSN (Data Source Name)** ali v **brez-DSN** konfiguraciji.

---

### A. Konfiguracija na osnovi DSN

#### Konfiguracija *digna*

Na zaslonu **«Ustvari povezavo do baze podatkov»** vnesite naslednje:

```
Technology:      Snowflake
Database Name:   Baza podatkov, ki vsebuje izvorno shemo
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Vklopljeno
```

#### Lastnosti ODBC

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

neobvezno:
name: "Database",       value: "Baza podatkov, ki vsebuje izvorno shemo"
name: "Schema",         value: "Shema, ki vsebuje izvorne podatke"
name: "Warehouse",      value: "Warehouse za izvajanje SQL-ukazov"
```

> 🔹 Vrednost `DSN` mora ustrezati imenu, določeni v konfiguraciji vašega ODBC-voznik.

---

### B. Konfiguracija brez DSN

#### Konfiguracija *digna*

Na zaslonu **«Ustvari povezavo do baze podatkov»** vnesite naslednje:

```
Technology:      Snowflake
Database Name:   Shema, ki vsebuje izvorne podatke (isto kot Schema Name)
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Vklopljeno
```

#### Lastnosti ODBC

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com"
name: "UID",        value: "your snowflake user"
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Baza podatkov, ki vsebuje izvorno shemo"
name: "Schema",     value: "Shema, ki vsebuje izvorne podatke"
name: "Warehouse",  value: "Warehouse za izvajanje SQL-ukazov"
```