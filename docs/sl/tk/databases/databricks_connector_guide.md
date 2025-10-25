---
title: Databricks vmesnik z Unity Catalog – integracija baze podatkov | digna dokumentacija
description: Konfigurirajte digna za povezavo z Databricks (Unity Catalog) z uporabo lokalnega Python konektorja ali ODBC gonilnika. Podpira overjanje na osnovi žetona in prilagodljive možnosti povezave.
image: /assets/logo_square.png
---

# Databricks virni konektor - Unity Catalog

Ta vodič razlaga, kako konfigurirati *digna*, da se poveže z Databricks z uporabo lokalnega Python konektorja ali ODBC gonilnika.

To se nanaša na zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Lokalni Python gonilnik

**Knjižnica:** `databricks-sql-connector`  
**Podprto overjanje:** Samo Personal Access Token (PAT)

> ⚠️ Za druge metode overjanja uporabite ODBC gonilnik.

### Osebni dostopni žeton (PAT)

Za overjanje z uporabo osebnega dostopnega žetona si oglejte uradno dokumentacijo Databricks:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfiguracija (lokalni gonilnik)

Na zaslonu **"Create a Database Connection"** vnesite naslednje podatke:

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

## ODBC gonilnik

ODBC gonilnik podpira širši nabor možnosti overjanja in povezav. Ta razdelek se osredotoča na overjanje na osnovi žetona z uporabo **Simba Spark ODBC Driver**.

### 1. Namestite ODBC gonilnik

Namestite **Simba Spark ODBC Driver** po uradnem namestitvenem navodilu ponudnika.

### 2. Konfigurirajte ODBC vir podatkov

Za konfiguracijo novega ODBC vira podatkov z uporabo osebnega dostopnega žetona sledite naslednjim korakom:

#### Korak 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Korak 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Korak 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Korak 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Korak 5 – Preizkusite povezavo

Kliknite gumb TEST. Uspešna povezava bi morala izgledati takole:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Zdaj lahko *digna* nastavite za uporabo ODBC povezave bodisi z **DSN (Data Source Name)** ali z **DSN-less** konfiguracijo.

---

### A. DSN‑osnovana konfiguracija

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 `DSN` mora ustrezati imenu, ki ste ga definirali v nastavitvah ODBC gonilnika.

---

### B. DSN-less konfiguracija

#### *digna* konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

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