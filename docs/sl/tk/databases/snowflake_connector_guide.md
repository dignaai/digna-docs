---
title: Povezovalnik Snowflake – Integracija podatkovne baze | digna Dokumentacija
description: Konfigurirajte digna za povezavo s Snowflake z uporabo Python povezovalnika ali Snowflake ODBC gonilnika. Podpira preverjanje pristnosti na osnovi gesla z namestitvami z DSN ali brez DSN.
image: /assets/logo_square.png
---


# Povezovalnik vira za Snowflake

Ta vodnik pojasnjuje, kako povezati *digna* s Snowflake z uporabo lokalnega Python povezovalnika ali ODBC gonilnika.

Ta dokument se nanaša na zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Lokalni Python gonilnik

**Knjižnica:** `snowflake-connector-python`  
**Podprte metode preverjanja pristnosti:** Samo preverjanje pristnosti z geslom

> ⚠️ Za druge metode preverjanja pristnosti uporabite ODBC gonilnik.

### *digna* konfiguracija (lokalni gonilnik)

Na zaslonu **"Create a Database Connection"** vnesite naslednje podatke:

```
Technology:      Snowflake
Host Address:    ime Snowflake računa
Host Port:       Ni potrebno
Database Name:   baza podatkov, ki vsebuje izvorno shemo
Schema Name:     shema, ki vsebuje izvorne podatke
User Name:       uporabniško ime in warehouse v formatu "user<@>warehouse"
User Password:   geslo uporabnika
Use ODBC:        Onemogočeno (privzeto)
```

---

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti preverjanja pristnosti in povezave. Ta razdelek se osredotoča na preverjanje pristnosti z geslom z uporabo **SnowflakeDSIIDriver**.

### 1. Namestite ODBC gonilnik

Sledite uradnim navodilom ponudnika za namestitev **SnowflakeDSIIDriver**.

### 2. Konfigurirajte ODBC vir podatkov

Za konfiguracijo novega ODBC vira podatkov z uporabo preverjanja pristnosti z geslom sledite tem korakom:

#### Korak 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Opombe: 
- Če ne navedete vrednosti za Database, Schema in Warehouse, jih boste morali navesti kot ODBC lastnosti med konfiguracijo vira podatkov v *digna*.
- Vrednost "Server" nastane z dodajanjem ".snowflakecomputing.com" na konec imena vašega Snowflake računa.

#### Korak 2 – Preizkusite povezavo

Kliknite gumb TEST. Uspešna povezava bo izgledala takole:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Zdaj lahko *digna* konfigurirate za uporabo ODBC povezave; bodisi z **DSN (Data Source Name)** ali z **brez DSN** namestitvijo.

---

### A. Konfiguracija z DSN

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Snowflake
Database Name:   baza podatkov, ki vsebuje izvorno shemo
Schema Name:     shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{vaše geslo v zavitih oklepajih}"

neobvezno:
name: "Database",       value: "baza podatkov, ki vsebuje izvorno shemo"
name: "Schema",         value: "shema, ki vsebuje izvorne podatke"
name: "Warehouse",      value: "warehouse, ki se bo uporabljal za izvajanje poizvedb SQL"
```

> 🔹 `DSN` mora ustrezati imenu, definiranemu v konfiguraciji ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Snowflake
Database Name:   shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Schema Name:     shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "baza podatkov, ki vsebuje izvorno shemo"
name: "Schema",     value: "shema, ki vsebuje izvorne podatke"
name: "Warehouse",  value: "warehouse, ki se bo uporabljal za izvajanje poizvedb SQL"
```