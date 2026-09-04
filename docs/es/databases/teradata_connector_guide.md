---
title: Conector Teradata – Integración de Base de Datos | Documentación de digna
description: Configure digna para conectarse a Teradata usando el driver Python teradatasql o el driver ODBC de Teradata. Soporta autenticación basada en contraseña con configuraciones DSN o sin DSN.
image: /assets/logo_square.png
---


# Source Connector for Teradata

Esta guía describe cómo configurar *digna* para conectarse a Teradata usando el conector nativo de Python o el driver ODBC.

Hace referencia a la pantalla **"Create a Database Connection"**.

![Crear una conexión de base de datos](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `teradatasql`  
**Supported Authentication:** Password-based authentication only

> Para otros métodos de autenticación, utilice el driver ODBC.

### *digna* Configuration (Native Driver)

Proporcione la siguiente información en la pantalla **"Create a Database Connection"**:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

El driver ODBC puede admitir una gama más amplia de opciones de autenticación y conectividad. Esta sección se centra en la autenticación basada en contraseña usando el driver **Teradata Database ODBC Driver 20.00**.

### 1. Install the ODBC Driver

Instale el driver **Teradata Database ODBC Driver 20.00** (o similar) siguiendo la guía oficial de instalación del proveedor.

### 2. Configure the ODBC Data Source

Siga estos pasos para configurar una nueva fuente de datos ODBC usando autenticación basada en contraseña:

#### Paso 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Haga clic en el botón **Test**.

#### Paso 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Proporcione nombre de usuario y contraseña.

Haga clic en el botón **OK**.  
Cuando reciba la pantalla de éxito, ODBC está configurado correctamente.

---

Ahora puede configurar *digna* para usar la conexión ODBC, ya sea con un **DSN (Data Source Name)** o una configuración **sin DSN**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

En la pantalla **"Create a Database Connection"**, proporcione lo siguiente:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> El `DSN` debe coincidir con el nombre definido en la configuración de su driver ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

En la pantalla **"Create a Database Connection"**, proporcione lo siguiente:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```