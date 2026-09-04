---
title: Conector de Azure Synapse – Integración de Base de Datos | documentación de digna
description: Configure digna para conectarse a Azure Synapse Analytics usando el conector nativo de Python o el controlador ODBC. Soporta pools SQL serverless y dedicados.
image: /assets/logo_square.png
canonical_url: https://docs.digna.ai/databases/azure_synapse_connector_guide/
---


# Conector de origen para Azure Synapse Analytics

Esta guía describe cómo configurar *digna* para conectarse a Azure Synapse Analytics usando el conector nativo de Python o el controlador ODBC.
Soporta tanto pools SQL serverless como dedicados.

Se refiere a la pantalla **"Crear una conexión de base de datos"**.

![Crear una conexión de base de datos](images/data_source_config_input_mask.png)

---

## Controlador nativo de Python

**Library:** `pymssql`  
**Autenticación compatible:** Solo autenticación basada en contraseña

> Para otros métodos de autenticación, utilice el controlador ODBC.

### Configuración de *digna* (Controlador nativo)

Proporcione la siguiente información en la pantalla **"Crear una conexión de base de datos"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## Controlador ODBC

El controlador ODBC puede soportar una gama más amplia de opciones de autenticación y conectividad. Esta sección se centra en la autenticación basada en contraseña usando el controlador **ODBC Driver 18 for SQL Server**.

### 1. Instale el controlador ODBC

Instale el controlador **ODBC Driver 18 for SQL Server** (u otro similar) siguiendo la guía de instalación oficial del proveedor.

### 2. Configure la fuente de datos ODBC

Siga estos pasos para configurar una nueva fuente de datos ODBC usando autenticación basada en contraseña:

#### Paso 1
![Paso 1](images/azure_synapse/create_odbc_data_source_step1.png)

Rellene el campo "Server".
Use el nombre del workspace de Synapse y añádale ".sql.azuresynapse.net".  
**Atención**, si desea conectarse usando un pool SQL serverless, asegúrese de incluir "-ondemand" tal como se muestra en la captura de pantalla a continuación.

Haga clic en el botón **Next >**.

#### Paso 2
![Paso 2](images/azure_synapse/create_odbc_data_source_step2.png)

Elija el método de autenticación (p. ej. nombre de usuario y contraseña)
y proporcione los datos requeridos.

Haga clic en el botón **Next >**.

#### Paso 3
![Paso 3](images/azure_synapse/create_odbc_data_source_step3.png)

Elija la configuración compatible con ANSI y luego haga clic en el botón **Next >**.

#### Paso 4
![Paso 4](images/azure_synapse/create_odbc_data_source_step4.png)

Puede dejar la configuración por defecto o elegir las opciones que necesite 
y haga clic en el botón **Finish**. 

#### Paso 5
![Paso 5](images/azure_synapse/create_odbc_data_source_step5.png)

Ahora haga clic en el botón **Test datasource**.

#### Paso 6
![Paso 6](images/azure_synapse/create_odbc_data_source_step6.png)

Cuando reciba la pantalla de éxito, ODBC está configurado correctamente.

---

Ahora puede configurar *digna* para usar la conexión ODBC, ya sea con un **DSN (Data Source Name)** o con una configuración **sin DSN**.

---

### A. Configuración basada en DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propiedades ODBC

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> El `DSN` debe coincidir con el nombre definido en la configuración de su controlador ODBC.

---

### B. Configuración sin DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propiedades ODBC

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Nota** respecto a la propiedad SERVER:  
Use el nombre del workspace de Synapse y añádale ".sql.azuresynapse.net". Si desea conectarse usando un pool SQL serverless, asegúrese de incluir "-ondemand" tal como se muestra en la captura de pantalla a continuación.