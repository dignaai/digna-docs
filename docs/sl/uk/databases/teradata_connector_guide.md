---
title: Teradata Connector – integracija baze podatkov | dokumentacija digna
description: Nastavite digna za povezavo s Teradata z uporabo Python-gonilnika teradatasql ali Teradata ODBC gonilnika. Podprto je preverjanje pristnosti z geslom v konfiguracijah z DSN ali brez DSN.
image: /assets/logo_square.png
---


# Povezovalnik vira za Teradata

V tem vodniku je opisano, kako nastaviti *digna* za povezavo s Teradata z uporabo izvornega Python-konektorja ali ODBC gonilnika.

Ta navodila se nanašajo na zaslon **«Create a Database Connection»**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Izvorni Python-gonilnik

**Library:** `teradatasql`  
**Podprto preverjanje pristnosti:** samo preverjanje pristnosti z geslom

> ⚠️ Za druge metode preverjanja pristnosti uporabite ODBC gonilnik.

### Konfiguracija *digna* (izvorni gonilnik)

Na zaslonu **"Create a Database Connection"** vnesite naslednje informacije:

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

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti preverjanja pristnosti in povezovanja. V tem razdelku je opisano preverjanje pristnosti z geslom z uporabo gonilnika **Teradata Database ODBC Driver 20.00**.

### 1. Namestitev ODBC gonilnika

Namestite gonilnik **Teradata Database ODBC Driver 20.00** (ali podoben), v skladu z uradnim namestitvenim vodnikom dobavitelja.

### 2. Konfiguracija ODBC vira podatkov

Upoštevajte naslednje korake za nastavitev novega ODBC vira s preverjanjem pristnosti z geslom:

#### Korak 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Kliknite gumb **Test**.

#### Korak 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Vnesite uporabniško ime in geslo.

Kliknite gumb **OK**. Ko se prikaže obvestilo o uspešni nastavitvi, je ODBC pravilno nastavljen.

---

Zdaj lahko nastavite *digna* za uporabo ODBC povezave — bodisi z uporabo **DSN (Data Source Name)** ali v konfiguraciji brez DSN (DSN-less).

---

### A. Konfiguracija na podlagi DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 Vrednost `DSN` se mora ujemati z imenom, določenim v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN (DSN-less)

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```