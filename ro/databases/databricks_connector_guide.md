# Source Connector for Databricks - with Unity Catalog

Acest ghid descrie cum să configurezi *digna* pentru a se conecta la Databricks folosind fie conectorul Python nativ, fie driverul ODBC.

Se referă la ecranul **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> Pentru alte metode de autentificare, folosește driverul ODBC.

### Personal Access Token (PAT)

Pentru a te autentifica folosind un personal access token, consultă documentația oficială Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Furnizează următoarele informații în ecranul **"Create a Database Connection"**:

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

Driverul ODBC suportă o gamă mai largă de opțiuni de autentificare și conectivitate. Această secțiune se concentrează pe autentificarea bazată pe token folosind **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Instalează **Simba Spark ODBC Driver** urmând ghidul oficial de instalare al vendorului.

### 2. Configure the ODBC Data Source

Urmează acești pași pentru a configura un nou data source ODBC folosind un Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Apasă butonul **TEST**. O conexiune reușită ar trebui să arate astfel:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Acum poți configura *digna* să folosească conexiunea ODBC, fie cu un **DSN (Data Source Name)**, fie într-o configurație **fără DSN**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

În ecranul **"Create a Database Connection"**, furnizează următoarele:

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

### B. DSN-less Configuration

#### *digna* Configuration

În ecranul **"Create a Database Connection"**, furnizează următoarele:

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