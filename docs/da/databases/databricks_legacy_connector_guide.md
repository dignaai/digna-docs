---
title: Databricks Connector (Legacy, uden Unity Catalog) | digna Dokumentation
description: Konfigurer *digna* til at oprette forbindelse til Databricks uden Unity Catalog ved hjælp af den native Python-connector eller Simba Spark ODBC-driver. Understøtter token-baseret autentifikation og fleksibel tilslutning.
image: /assets/logo_square.png
---

# Source Connector for Databricks - uden Unity Catalog

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til Databricks ved enten at bruge den native Python-connector eller ODBC-driveren.

Den henviser til skærmen **"Opret en databaseforbindelse"**.

![Opret en databaseforbindelse](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Understøttet autentifikation:** Personal Access Token (PAT) kun

> For andre autentifikationsmetoder, brug venligst ODBC-driveren.

### Personal Access Token (PAT)

For at autentificere med et personal access token, se den officielle Databricks-dokumentation:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Konfiguration (Native Driver)

Angiv følgende oplysninger i skærmen **"Opret en databaseforbindelse"**:

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

ODBC-driveren understøtter et bredere udvalg af autentifikations- og tilslutningsmuligheder. Dette afsnit fokuserer på token-baseret autentifikation ved hjælp af **Simba Spark ODBC Driver**.

### 1. Installer ODBC-driveren

Installer **Simba Spark ODBC Driver** ved at følge leverandørens officielle installationsvejledning.

### 2. Konfigurer ODBC Data Source

Følg disse trin for at konfigurere en ny ODBC-data source ved brug af et Personal Access Token:

#### Trin 1
![Trin 1](images/databricks/create_odbc_data_source_step1.png)

#### Trin 2
![Trin 2](images/databricks/create_odbc_data_source_step2.png)

#### Trin 3
![Trin 3](images/databricks/create_odbc_data_source_step3.png)

#### Trin 4
![Trin 4](images/databricks/create_odbc_data_source_step4.png)

#### Trin 5 – Test forbindelsen

Klik på knappen **TEST**. En vellykket forbindelse bør se sådan ud:

![Trin 5](images/databricks/create_odbc_data_source_step5.png)

---

Nu kan du konfigurere *digna* til at bruge ODBC-forbindelsen, enten med en **DSN (Data Source Name)** eller en **DSN-less** opsætning.

---

### A. DSN-baseret konfiguration

#### *digna* Konfiguration

I skærmen **"Opret en databaseforbindelse"** angiv følgende:

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

> `DSN` skal matche navnet, der er defineret i din ODBC-driverkonfiguration.

---

### B. DSN-less konfiguration

#### *digna* Konfiguration

I skærmen **"Opret en databaseforbindelse"** angiv følgende:

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