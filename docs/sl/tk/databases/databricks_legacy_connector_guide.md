---
title: Povezovalnik za Databricks (Legacy, brez Unity Catalog) | digna dokumentacija
description: Konfiguracija *digna* za povezavo z Databricks brez Unity Catalog z uporabo native Python connector ali Simba Spark ODBC gonilnika. Podpira overjanje na osnovi žetona in prilagodljive možnosti povezave.
image: /assets/logo_square.png
---

# Povezovalnik za Databricks - brez Unity Catalog

Ta vodič pojasnjuje, kako konfigurirati *digna* za Databricks z uporabo native Python connector ali ODBC gonilnika.

It refers to the screen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> ⚠️ Za druge metode overjanja uporabite ODBC gonilnik.

### Personal Access Token (PAT)

Za overjanje s osebnim dostopnim žetonom si oglejte uradno dokumentacijo Databricks:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfiguracija (Native gonilnik)

Vnesite spodnje podatke na zaslon **"Create a Database Connection"**:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC gonilnik podpira širši nabor metod overjanja in možnosti povezave. Ta razdelek se osredotoča na overjanje na osnovi žetona z uporabo **Simba Spark ODBC Driver**.

### 1. Namestite ODBC gonilnik

Namestite **Simba Spark ODBC Driver** tako, da sledite uradnemu namestitvenemu vodniku ponudnika.

### 2. Konfigurirajte ODBC podatkovni vir

Za konfiguracijo novega ODBC podatkovnega vira z uporabo osebnega dostopnega žetona sledite tem korakom:

#### Korak 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Korak 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Korak 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Korak 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Korak 5 – Preizkusite povezavo

Kliknite gumb **TEST**. Uspešna povezava naj izgleda tako:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Zdaj lahko *digna* konfigurirate za uporabo ODBC povezave bodisi z **DSN (Data Source Name)** ali brez **DSN**.

---

### A. Konfiguracija na osnovi DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 `DSN` se mora ujemati z imenom, definiranem v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```