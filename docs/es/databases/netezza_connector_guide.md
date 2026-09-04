---
title: Conector Netezza – Integración de Base de Datos | Documentación de digna
description: Configure digna para conectarse a Netezza usando el controlador ODBC NetezzaSQL. Admite autenticación basada en contraseña con configuraciones DSN o sin DSN para una conectividad flexible.
image: /assets/logo_square.png
---


# Source Connector for Netezza

Esta guía describe cómo configurar *digna* para conectarse a Netezza usando el controlador ODBC.

Se hace referencia a la pantalla **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC Driver

El controlador ODBC puede admitir una variedad de opciones de autenticación y conectividad. Esta sección se centra en la autenticación basada en contraseña usando el controlador **NetezzaSQL**.

### 1. Install the ODBC Driver

Instale el controlador **NetezzaSQL** (o similar) siguiendo la guía de instalación oficial del proveedor.

### 2. Configure the ODBC Data Source

Siga estos pasos para configurar una nueva fuente de datos ODBC usando autenticación basada en contraseña:

#### Step 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Dependiendo de su controlador Netezza, los requisitos de instalación y seguridad, puede que también necesite proporcionar datos en las pestañas **Advanced DSN Options**, **SSL DSN Options** o **Driver Options**. Para la configuración más sencilla es suficiente con proporcionar datos en **DSN Options**.

Haga clic en el botón **Test Connection**.

#### Step 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Cuando reciba la pantalla de éxito, ODBC está configurado correctamente.

---

Ahora puede configurar *digna* para usar la conexión ODBC, ya sea con un **DSN (Data Source Name)** o una configuración **DSN-less**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

En la pantalla **"Create a Database Connection"**, proporcione lo siguiente:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

En la pantalla **"Create a Database Connection"**, proporcione lo siguiente:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
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