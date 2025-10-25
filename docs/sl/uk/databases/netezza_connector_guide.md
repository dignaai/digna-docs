---
title: Netezza Connector – Integracija baze podatkov | digna Dokumentacija
description: Konfigurirajte digna za povezavo z Netezza z uporabo ODBC gonilnika NetezzaSQL. Podprto je overjanje z geslom z uporabo DSN ali brez DSN za prilagodljivo povezavo.
image: /assets/logo_square.png
---


# Povezava vira za Netezza

Ta vodnik opisuje, kako konfigurirati *digna* za povezavo z Netezza preko ODBC gonilnika.

Sklicuje se na zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC gonilnik

ODBC gonilnik lahko podpira različne možnosti overjanja in povezovanja. Ta razdelek obravnava overjanje z geslom z uporabo gonilnika **NetezzaSQL**.

### 1. Namestite ODBC gonilnik

Namestite gonilnik **NetezzaSQL** (ali podoben) v skladu z uradnim navodilom ponudnika.

### 2. Konfigurirajte ODBC vir podatkov

Sledite naslednjim korakom za nastavitev novega ODBC vira podatkov z overjanjem z geslom:

#### Korak 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Glede na vaš Netezza gonilnik, zahteve za konfiguracijo in varnost, boste morda morali navesti podatke tudi na zavihkih **Advanced DSN Options**, **SSL DSN Options** ali **Driver Options**. Za najpreprostejšo nastavitev je dovolj navesti podatke na zavihku **DSN Options**.

Kliknite gumb **Test Connection**.

#### Korak 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Ko se prikaže zaslon o uspehu, je ODBC pravilno nastavljen.

---

Zdaj lahko konfigurirate *digna* za uporabo ODBC povezave — bodisi z **DSN (Data Source Name)** bodisi v načinu **DSN-less**.

---

### A. Konfiguracija na podlagi DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN` mora ustrezati imenu, določenemu v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN (DSN-less)

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```