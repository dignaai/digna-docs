---
title: Povezovalnik Databricks z Unity Catalog – integracija baze podatkov | digna Dokumentacija
description: Konfigurirajte *digna* za povezavo z Databricks z Unity Catalog z uporabo native Python connectorja ali ODBC gonilnika. Podpira avtorizacijo s tokenom in prilagodljive možnosti povezave.
image: /assets/logo_square.png
---

# Povezava vira podatkov za Databricks – z Unity Catalog

Ta vodič opisuje, kako konfigurirati *digna* za povezavo z Databricks z uporabo bodisi native Python-connectorja ali ODBC-gonilnika.

Pokaže zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> ⚠️ Za druge metode avtentikacije uporabite ODBC gonilnik.

### Personal Access Token (PAT)

Za avtorizacijo z osebnim dostopnim žetonom si oglejte uradno Databricks dokumentacijo:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Provide the following information in the **"Create a Database Connection"** screen:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC-gonilnik podpira širši nabor možnosti avtentikacije in povezovanja. Ta razdelek se osredotoča na token-bazirano avtentikacijo z uporabo **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Namestite **Simba Spark ODBC Driver** tako, da sledite uradnemu vodniku za namestitev proizvajalca.

### 2. Configure the ODBC Data Source

Sledite tem korakom za konfiguracijo nove ODBC-datakilde z uporabo Personal Access Token:

#### Korak 1
![Korak 1](images/databricks/create_odbc_data_source_step1.png)

#### Korak 2
![Korak 2](images/databricks/create_odbc_data_source_step2.png)

#### Korak 3
![Korak 3](images/databricks/create_odbc_data_source_step3.png)

#### Korak 4
![Korak 4](images/databricks/create_odbc_data_source_step4.png)

#### Korak 5 – Preizkusite povezavo

Kliknite gumb **TEST**. Uspešna povezava izgleda takole:

![Korak 5](images/databricks/create_odbc_data_source_step5.png)

---

Zdaj lahko konfigurirate *digna*, da uporabi ODBC-povezavo, bodisi z **DSN (Data Source Name)** ali z nastavitvijo **brez DSN**.

---

### A. Konfiguracija z DSN

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. Konfiguracija brez DSN

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
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