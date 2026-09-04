---
title: MS SQL Server Connector – Database Integration | digna Documentation
description: Configure digna to connect to Microsoft SQL Server using the pymssql Python driver or the SQL Server ODBC driver. Supports password-based authentication with DSN or DSN-less setups.
image: /assets/logo_square.png
---


# Source Connector for MS SQL Server

This guide describes how to configure *digna* to connect to SQLServer using either the native Python connector or the ODBC driver.

It refers to the screen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Password-based authentication only

> For other authentication methods, please use the ODBC driver.

### *digna* Configuration (Native Driver)

Provide the following information in the **"Create a Database Connection"** screen:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         MS SQL Server
Host Address:       Server name or IP address
Host Port:          Port number, e.g. 1433
Database Name:      Database name
User Name:          Database user name
User Password:      Password for the user
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" profiling mode, work tables will be placed in this schema.
Use ODBC:           Disabled (default)
```

---

## ODBC Driver

The ODBC driver may support a broader range of authentication and connectivity options. This section focuses on password-based authentication using the driver **SQL Server**.

### 1. Install the ODBC Driver

Install the driver **SQL Server** (or similar) by following the vendor’s official installation guide.

### 2. Configure the ODBC Data Source

Follow these steps to configure a new ODBC data source using password-based authentication:

#### Step 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Click the **Next >** button.

#### Step 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Choose the authentication method (e.g. username and password)
and provide the required data.

Click the **Next >** button.

#### Step 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Choose the ANSI compliant settings then click the **Next >** button.

#### Step 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

You can leave the default settings or choose logging options as needed 
and click the **Finish** button. 

#### Step 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Now click the **Test datasource** button.

#### Step 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

When you receive the success screen, ODBC is configured properly.

---

Now you can configure *digna* to use the ODBC connection, either with a **DSN (Data Source Name)** or a **DSN-less** setup.

---

### A. DSN-Based Configuration

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         MS SQL Server
Database Name:      Database that contains the source schemata
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" profiling mode, work tables will be placed in this schema.
Use ODBC:           Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "sqlserver-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         MS SQL Server
Database Name:      Name of the database that contains the source data schemata
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" profiling mode, work tables will be placed in this schema.
Use ODBC:           Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schemata"
```
