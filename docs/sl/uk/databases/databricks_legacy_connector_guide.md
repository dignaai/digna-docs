---
title: Povezovalnik Databricks (Legacy, brez Unity Catalog) | dokumentacija digna
description: Nastavite digna za povezavo z Databricks brez Unity Catalog z uporabo nativnega Python-connectorja ali Simba Spark ODBC gonilnika. Podprta je avtentikacija na osnovi Personal Access Token in prilagodljive možnosti povezave.
image: /assets/logo_square.png
---

# Povezovalnik Databricks — brez Unity Catalog

Ta vodič opisuje, kako nastaviti *digna* za povezavo z Databricks z uporabo nativnega Python-connectorja ali ODBC-gonilnika.

Vodič se nanaša na zaslon **"Create a Database Connection"**.

![Ustvari povezavo z bazo podatkov](images/data_source_config_input_mask.png)

---

## Nativni Python-gonilnik

**Knjižnica:** `databricks-sql-connector`  
**Podprta avtentikacija:** samo Personal Access Token (PAT)

> ⚠️ Za druge metode avtentikacije uporabite ODBC-gonilnik.

### Personal Access Token (PAT)

Če se želite avtenticirati z uporabo Personal Access Token, glejte uradno dokumentacijo Databricks:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### Konfiguracija *digna* (nativni gonilnik)

Vnesite naslednje podatke na zaslonu **"Create a Database Connection"**:

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

## ODBC-gonilnik

ODBC-gonilnik podpira širši nabor metod avtentikacije in možnosti povezave. V tem razdelku je opisana avtentikacija na osnovi žetona z uporabo **Simba Spark ODBC Driver**.

### 1. Namestite ODBC-gonilnik

Namestite **Simba Spark ODBC Driver**, sledite uradnim navodilom dobavitelja.

### 2. Nastavite vir podatkov ODBC

Sledite tem korakom za nastavitev novega vira podatkov ODBC z uporabo Personal Access Token:

#### Korak 1
![Korak 1](images/databricks/create_odbc_data_source_step1.png)

#### Korak 2
![Korak 2](images/databricks/create_odbc_data_source_step2.png)

#### Korak 3
![Korak 3](images/databricks/create_odbc_data_source_step3.png)

#### Korak 4
![Korak 4](images/databricks/create_odbc_data_source_step4.png)

#### Korak 5 – Test povezave

Kliknite gumb **TEST**. Uspešna povezava bo videti tako:

![Korak 5](images/databricks/create_odbc_data_source_step5.png)

---

Zdaj lahko nastavite *digna* za uporabo ODBC-povezave — bodisi prek **DSN (Data Source Name)** ali v **DSN-less** konfiguraciji.

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

#### Lastnosti ODBC

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 `DSN` mora ustrezati imenu, določenemu v nastavitvah vašega ODBC-gonilnika.

---

### B. DSN-less konfiguracija

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Lastnosti ODBC

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