---
title: Conector de Databricks con Unity Catalog – Integración de Base de Datos | digna Documentation
description: Configure digna para conectarse a Databricks con Unity Catalog usando el conector nativo de Python o el controlador ODBC. Soporta autenticación basada en token y conectividad flexible.
image: /assets/logo_square.png
---

# Conector de origen para Databricks - con Unity Catalog

Esta guía describe cómo configurar *digna* para conectarse a Databricks usando el conector nativo de Python o el driver ODBC.

Se refiere a la pantalla **"Create a Database Connection"**.

![Crear una conexión de base de datos](images/data_source_config_input_mask.png)

---

## Driver nativo de Python

**Library:** `databricks-sql-connector`  
**Autenticación compatible:** Token de acceso personal (PAT) únicamente

> ⚠️ Para otros métodos de autenticación, use el driver ODBC.

### Token de acceso personal (PAT)

Para autenticar usando un token de acceso personal, consulte la documentación oficial de Databricks:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### Configuración de *digna* (Driver nativo)

Proporcione la siguiente información en la pantalla **"Create a Database Connection"**:

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

## Driver ODBC

El driver ODBC soporta una gama más amplia de opciones de autenticación y conectividad. Esta sección se centra en la autenticación basada en token usando el **Simba Spark ODBC Driver**.

### 1. Instale el driver ODBC

Instale el **Simba Spark ODBC Driver** siguiendo la guía de instalación oficial del proveedor.

### 2. Configure el origen de datos ODBC

Siga estos pasos para configurar un nuevo origen de datos ODBC usando un Token de Acceso Personal:

#### Paso 1
![Paso 1](images/databricks/create_odbc_data_source_step1.png)

#### Paso 2
![Paso 2](images/databricks/create_odbc_data_source_step2.png)

#### Paso 3
![Paso 3](images/databricks/create_odbc_data_source_step3.png)

#### Paso 4
![Paso 4](images/databricks/create_odbc_data_source_step4.png)

#### Paso 5 – Pruebe la conexión

Haga clic en el botón **TEST**. Una conexión exitosa debería verse así:

![Paso 5](images/databricks/create_odbc_data_source_step5.png)

---

Ahora puede configurar *digna* para usar la conexión ODBC, ya sea con un **DSN (Data Source Name)** o una configuración **sin DSN**.

---

### A. Configuración basada en DSN

#### Configuración de *digna*

En la pantalla **"Create a Database Connection"**, proporcione lo siguiente:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propiedades ODBC

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 El `DSN` debe coincidir con el nombre definido en la configuración de su driver ODBC.

---

### B. Configuración sin DSN

#### Configuración de *digna*

En la pantalla **"Create a Database Connection"**, proporcione lo siguiente:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propiedades ODBC

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