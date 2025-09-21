---
title: PostgreSQL Connector – Database Integration | digna Documentation
description: Configure digna to connect to PostgreSQL using the psycopg Python driver or the PostgreSQL ODBC driver. Supports password-based authentication with DSN or DSN-less setups.
canonical_url: https://docs.digna.ai/databases/postgres_connector_guide/
image: /assets/logo_square.png
---


# Source Connector for PostgreSQL

This guide describes how to configure *digna* to connect to Postgres using either the native Python connector or the ODBC driver.

It refers to the screen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `psycopg`  
**Supported Authentication:** Password-based authentication only

> ⚠️ For other authentication methods, please use the ODBC driver.

### *digna* Configuration (Native Driver)

Provide the following information in the **"Create a Database Connection"** screen:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

The ODBC driver may support a broader range of authentication and connectivity options. This section focuses on password-based authentication using the driver **PostgreSQL Unicode(x64)**.

### 1. Install the ODBC Driver

Install the **PostgreSQL Unicode(x64)** (or similar) by following the vendor’s official installation guide.

### 2. Configure the ODBC Data Source

Follow these steps to configure a new ODBC data source using password-based authentication:

#### Step 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Note: If your database setup requires you to choose a specific "SSLMode", please make sure to also use this when defining a DSN-less configuration.

#### Step 2 – Test the connection

Click the **Test Connection** button.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Now you can configure *digna* to use the ODBC connection, either with a **DSN (Data Source Name)** or a **DSN-less** setup.

---

### A. DSN-Based Configuration

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```
