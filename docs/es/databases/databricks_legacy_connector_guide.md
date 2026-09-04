---
title: Conector de Databricks (Legacy, without Unity Catalog) | digna Documentation
description: Configure digna para conectarse a Databricks sin Unity Catalog usando el conector nativo de Python o el controlador Simba Spark ODBC. Admite autenticación basada en tokens y conectividad flexible.
image: /assets/logo_square.png
---

# Source Connector for Databricks - without Unity Catalog

Esta guía describe cómo configurar *digna* para conectarse a Databricks usando el conector nativo de Python o el controlador ODBC.

Hace referencia a la pantalla **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> Para otros métodos de autenticación, usa el controlador ODBC.

### Personal Access Token (PAT)

Para autenticarse usando un token de acceso personal, consulta la documentación oficial de Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Provide the following information in the **"Create a Database Connection"** screen:

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

El controlador ODBC admite una gama más amplia de opciones de autenticación y conectividad. Esta sección se centra en la autenticación basada en tokens usando el **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Instala el **Simba Spark ODBC Driver** siguiendo la guía de instalación oficial del proveedor.

### 2. Configure the ODBC Data Source

Sigue estos pasos para configurar una nueva fuente de datos ODBC usando un Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Haz clic en el botón **TEST**. Una conexión exitosa debería verse así:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Ahora puedes configurar *digna* para usar la conexión ODBC, ya sea con un **DSN (Data Source Name)** o una configuración **sin DSN**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

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

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

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