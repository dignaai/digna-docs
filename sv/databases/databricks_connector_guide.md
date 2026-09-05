# Source Connector for Databricks - with Unity Catalog

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Databricks med antingen den inbyggda Python-connectorn eller ODBC-drivrutinen.

Den hänvisar till skärmen **"Skapa en databasanslutning"**.

![Skapa en databasanslutning](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> För andra autentiseringsmetoder, använd ODBC-drivrutinen.

### Personal Access Token (PAT)

För att autentisera med en personal access token, se Databricks officiella dokumentation:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Ange följande information i skärmen **"Skapa en databasanslutning"**:

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

ODBC-drivrutinen stödjer ett bredare utbud av autentiserings- och uppkopplingsalternativ. Denna sektion fokuserar på token-baserad autentisering med hjälp av **Simba Spark ODBC Driver**.

### 1. Installera ODBC-drivrutinen

Installera **Simba Spark ODBC Driver** genom att följa leverantörens officiella installationsguide.

### 2. Konfigurera ODBC-datakällan

Följ dessa steg för att konfigurera en ny ODBC-datakälla med en Personal Access Token:

#### Steg 1
![Steg 1](images/databricks/create_odbc_data_source_step1.png)

#### Steg 2
![Steg 2](images/databricks/create_odbc_data_source_step2.png)

#### Steg 3
![Steg 3](images/databricks/create_odbc_data_source_step3.png)

#### Steg 4
![Steg 4](images/databricks/create_odbc_data_source_step4.png)

#### Steg 5 – Testa anslutningen

Klicka på **TEST**-knappen. En lyckad anslutning ser ut så här:

![Steg 5](images/databricks/create_odbc_data_source_step5.png)

---

Nu kan du konfigurera *digna* att använda ODBC-anslutningen, antingen med en **DSN (Data Source Name)** eller en **DSN-less** konfiguration.

---

### A. DSN-baserad konfiguration

#### *digna* Configuration

I skärmen **"Skapa en databasanslutning"**, ange följande:

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

#### *digna* Configuration

I skärmen **"Skapa en databasanslutning"**, ange följande:

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