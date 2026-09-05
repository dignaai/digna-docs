# Source Connector for Databricks - without Unity Catalog

Denne veiledningen beskriver hvordan du konfigurerer *digna* for å koble til Databricks ved enten å bruke den native Python-connectoren eller ODBC-driveren.

Den viser til skjermen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> For andre autentiseringsmetoder, bruk ODBC-driveren.

### Personal Access Token (PAT)

For å autentisere med et personal access token, se den offisielle Databricks-dokumentasjonen:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Oppgi følgende informasjon i skjermen **"Create a Database Connection"**:

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

ODBC-driveren støtter et bredere spekter av autentiserings- og tilkoblingsalternativer. Denne seksjonen fokuserer på token-basert autentisering ved bruk av **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Installer **Simba Spark ODBC Driver** ved å følge leverandørens offisielle installasjonsveiledning.

### 2. Configure the ODBC Data Source

Følg disse stegene for å konfigurere en ny ODBC-datakilde ved bruk av Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Klikk på **TEST**-knappen. En vellykket tilkobling skal se slik ut:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Nå kan du konfigurere *digna* til å bruke ODBC-tilkoblingen, enten med en **DSN (Data Source Name)** eller en **DSN-less** oppsett.

---

### A. DSN-Based Configuration

#### *digna* Configuration

I skjermen **"Create a Database Connection"**, oppgi følgende:

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

> `DSN` må samsvare med navnet som er definert i ODBC-driverkonfigurasjonen din.

---

### B. DSN-less Configuration

#### *digna* Configuration

I skjermen **"Create a Database Connection"**, oppgi følgende:

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