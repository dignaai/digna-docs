# Source Connector for Snowflake

Acest ghid descrie cum să configurezi *digna* pentru a se conecta la Snowflake folosind fie connectorul nativ Python, fie driverul ODBC.

Se referă la ecranul **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `snowflake-connector-python`  
**Supported Authentication:** Password-based authentication only

> Pentru alte metode de autentificare, folosiți driverul ODBC.

### *digna* Configuration (Native Driver)

Furnizați următoarele informații în ecranul **"Create a Database Connection"**:

```
Technology:      Snowflake
Host Address:    Snowflake account name
Host Port:       Not needed
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
User Name:       User name and warehouse in the format "user<@>warehouse"
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Driverul ODBC poate oferi o gamă mai largă de opțiuni de autentificare și conectivitate. Această secțiune se concentrează pe autentificarea pe bază de parolă folosind **SnowflakeDSIIDriver**.

### 1. Install the ODBC Driver

Instalați **SnowflakeDSIIDriver** urmând ghidul oficial de instalare al furnizorului.

### 2. Configure the ODBC Data Source

Urmați pașii de mai jos pentru a configura o nouă sursă de date ODBC folosind autentificare pe bază de parolă:

#### Step 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Notes: 
- Dacă nu furnizați valori pentru Database, Schema și Warehouse, va trebui să le furnizați ca proprietăți ODBC în timpul configurării sursei de date *digna*.
- Valoarea pentru "Server" constă din numele contului Snowflake urmat de ".snowflakecomputing.com"

#### Step 2 – Test the connection

Faceți clic pe butonul **TEST**. O conexiune reușită ar trebui să arate astfel:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Now you can configure *digna* to use the ODBC connection, either with a **DSN (Data Source Name)** or a **DSN-less** setup.

---

### A. DSN-Based Configuration

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```