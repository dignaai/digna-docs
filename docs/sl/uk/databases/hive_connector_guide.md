---
title: Apache Hive Connector – Integracija baz podatkov | digna dokumentacija
description: Konfigurirajte digna za povezavo z Apache Hive z uporabo izvornega PyHive gonilnika ali Cloudera ODBC gonilnika. Podpira overjanje z geslom in nastavitve z DSN ali brez DSN.
image: /assets/logo_square.png
---


# Vhodni konektor za Hive

Ta vodnik opisuje, kako konfigurirati *digna* za povezavo s Hive z uporabo bodisi izvornega Python konektorja bodisi ODBC gonilnika.

Sklicuje se na zaslon **"Ustvari povezavo z bazo podatkov"**.

![Ustvari povezavo z bazo podatkov](images/data_source_config_input_mask.png)

---

## Izvorni Python gonilnik

**Knjižnica:** `PyHive`  
**Podprto overjanje:** Samo overjanje z geslom

> ⚠️ Za druge metode overjanja uporabite ODBC gonilnik.

### Konfiguracija *digna* (izvorni gonilnik)

Na zaslonu **"Ustvari povezavo z bazo podatkov"** navedite naslednje podatke:

```
Technology:      Apache Hive
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 10000
Database Name:   Schema that contains the source data
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti overjanja in povezljivosti. Ta razdelek se osredotoča na overjanje z geslom z uporabo gonilnika **Cloudera ODBC Driver for Apache Hive**.

### 1. Namestite ODBC gonilnik

Namestite **Cloudera ODBC Driver for Apache Hive** (ali podoben) tako, da sledite uradnemu namestitvenemu vodiču proizvajalca.

### 2. Konfigurirajte ODBC vir podatkov

Sledite tem korakom za konfiguracijo novega ODBC vira podatkov z overjanjem z geslom:

#### Korak 1
![Korak 1](images/hive/create_odbc_data_source_step1.png)


#### Korak 2 – Preizkusite povezavo

Vnesite geslo in kliknite gumb **Preizkusi**.

![Korak 2](images/hive/create_odbc_data_source_step2.png)

Po uspešnem preizkusu kliknite gumb **V redu**.

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC povezavo, bodisi z **DSN (Data Source Name)** ali z nastavitvijo **brez DSN**.

---

### A. Konfiguracija z DSN

#### Konfiguracija *digna*

Na zaslonu **"Ustvari povezavo z bazo podatkov"** navedite naslednje:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 `DSN` se mora ujemati z imenom, določenim v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### Konfiguracija *digna*

Na zaslonu **"Ustvari povezavo z bazo podatkov"** navedite naslednje:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 10000"
name: "Schema",     value: "Schema that contains the source data"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```