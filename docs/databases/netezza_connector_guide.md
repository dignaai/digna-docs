---
title: Netezza Connector – Database Integration | digna Documentation
description: Configure digna to connect to Netezza using the NetezzaSQL ODBC driver. Supports password-based authentication with DSN or DSN-less setups for flexible connectivity.
image: /assets/logo_square.png
---


# Source Connector for Netezza

This guide describes how to configure *digna* to connect to Netezza using the ODBC driver.

It refers to the screen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC Driver

The ODBC driver may support a range of authentication and connectivity options. This section focuses on password-based authentication using the driver **NetezzaSQL**.

### 1. Install the ODBC Driver

Install the driver **NetezzaSQL** (or similar) by following the vendor’s official installation guide.

### 2. Configure the ODBC Data Source

Follow these steps to configure a new ODBC data source using password-based authentication:

#### Step 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Depending on your Netezza driver, setup and security requirements, you may need to also provide data in the tabs **Advanced DSN Options**, **SSL DSN Options** or **Driver Options**. For the simple most setup it is sufficient to provide data in **DSN Options**.

Click the **Test Connection** button.

#### Step 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

When you receive the success screen, ODBC is configured properly.

---

Now you can configure *digna* to use the ODBC connection, either with a **DSN (Data Source Name)** or a **DSN-less** setup.

---

### A. DSN-Based Configuration

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Database Name:      Database that contains the source schemas
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" profiling mode, work tables will be placed in this schema.
Use ODBC:           Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Database Name:      Database that contains the source schemas
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" profiling mode, work tables will be placed in this schema.
Use ODBC:           Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
