# Kildeconnector til Databricks - med Unity Catalog

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til Databricks ved hjælp af enten den native Python-connector eller ODBC-driveren.

Den henviser til skærmen **"Opret en databaseforbindelse"**.

![Opret en databaseforbindelse](images/data_source_config_input_mask.png)

---

## Native Python-driver

**Bibliotek:** `databricks-sql-connector`  
**Understøttet autentificering:** Kun Personal Access Token (PAT)

> For andre godkendelsesmetoder, brug venligst ODBC-driveren.

### Personal Access Token (PAT)

For at godkende ved hjælp af en personal access token, se den officielle Databricks-dokumentation:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfiguration (Native Driver)

Angiv følgende oplysninger i skærmen **"Opret en databaseforbindelse"**:

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

## ODBC-driver

ODBC-driveren understøtter et bredere udvalg af godkendelses- og forbindelsesmuligheder. Dette afsnit fokuserer på token-baseret godkendelse ved brug af **Simba Spark ODBC Driver**.

### 1. Installer ODBC-driveren

Installer **Simba Spark ODBC Driver** ved at følge leverandørens officielle installationsvejledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trin for at konfigurere en ny ODBC-datakilde ved hjælp af en Personal Access Token:

#### Trin 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Trin 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Trin 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Trin 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Trin 5 – Test forbindelsen

Klik på **TEST**-knappen. En vellykket forbindelse bør se sådan ud:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Nu kan du konfigurere *digna* til at bruge ODBC-forbindelsen, enten med en **DSN (Data Source Name)** eller en **DSN-less** opsætning.

---

### A. DSN-baseret konfiguration

#### *digna*-konfiguration

I skærmen **"Opret en databaseforbindelse"**, angiv følgende:

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

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less konfiguration

#### *digna*-konfiguration

I skærmen **"Opret en databaseforbindelse"**, angiv følgende:

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