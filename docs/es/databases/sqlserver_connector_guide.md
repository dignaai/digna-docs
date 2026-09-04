---
title: Conector MS SQL Server – Integración de Base de Datos | Documentación de digna
description: Configure digna para conectarse a Microsoft SQL Server usando el controlador Python pymssql o el controlador ODBC de SQL Server. Admite autenticación basada en contraseña con configuraciones con DSN o sin DSN.
image: /assets/logo_square.png
---


# Conector de origen para MS SQL Server

Esta guía describe cómo configurar *digna* para conectarse a SQL Server usando ya sea el conector nativo de Python o el controlador ODBC.

Hace referencia a la pantalla **"Crear una conexión de base de datos"**.

![Crear una conexión de base de datos](images/data_source_config_input_mask.png)

---

## Controlador nativo de Python

**Librería:** `pymssql`  
**Autenticación compatible:** Solo autenticación basada en contraseña

> Para otros métodos de autenticación, utilice el controlador ODBC.

### Configuración de *digna* (Controlador nativo)

Proporcione la siguiente información en la pantalla **"Crear una conexión de base de datos"**:

```
Technology:      MS SQL Server
Host Address:    Nombre del servidor o dirección IP
Host Port:       Número de puerto, p. ej. 1433
Database Name:   Nombre de la base de datos
Schema Name:     Esquema que contiene los datos de origen
User Name:       Nombre de usuario de la base de datos
User Password:   Contraseña del usuario
Use ODBC:        Disabled (valor por defecto)
```

---

## Controlador ODBC

El controlador ODBC puede admitir una gama más amplia de opciones de autenticación y conectividad. Esta sección se centra en la autenticación basada en contraseña usando el controlador **SQL Server**.

### 1. Instale el controlador ODBC

Instale el controlador **SQL Server** (o uno similar) siguiendo la guía de instalación oficial del proveedor.

### 2. Configure el origen de datos ODBC

Siga estos pasos para configurar un nuevo origen de datos ODBC usando autenticación basada en contraseña:

#### Paso 1
![Paso 1](images/sqlserver/create_odbc_data_source_step1.png)

Haga clic en el botón **Next >**.

#### Paso 2
![Paso 2](images/sqlserver/create_odbc_data_source_step2.png)

Elija el método de autenticación (p. ej. nombre de usuario y contraseña)
y proporcione los datos requeridos.

Haga clic en el botón **Next >**.

#### Paso 3
![Paso 3](images/sqlserver/create_odbc_data_source_step3.png)

Elija las configuraciones compatibles con ANSI y luego haga clic en el botón **Next >**.

#### Paso 4
![Paso 4](images/sqlserver/create_odbc_data_source_step4.png)

Puede dejar las configuraciones por defecto o elegir opciones de registro según sea necesario
y hacer clic en el botón **Finish**. 

#### Paso 5
![Paso 5](images/sqlserver/create_odbc_data_source_step5.png)

Ahora haga clic en el botón **Probar origen de datos**.

#### Paso 6
![Paso 1](images/sqlserver/create_odbc_data_source_step6.png)

Cuando reciba la pantalla de éxito, ODBC está configurado correctamente.

---

Ahora puede configurar *digna* para usar la conexión ODBC, ya sea con un **DSN (Data Source Name)** o una configuración **sin DSN**.

---

### A. Configuración basada en DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      MS SQL Server
Database Name:   Base de datos que contiene el esquema de origen
Schema Name:     Esquema que contiene los datos de origen
Use ODBC:        Enabled
```

#### Propiedades ODBC

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "su usuario de base de datos"
name: "PWD",        value: "su contraseña de base de datos"
name: "DATABASE",   value: "nombre de la base de datos que contiene el esquema de datos de origen"

```

> El `DSN` debe coincidir con el nombre definido en la configuración de su controlador ODBC.

---

### B. Configuración sin DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      MS SQL Server
Database Name:   Esquema que contiene los datos de origen (igual que Schema Name)
Schema Name:     Esquema que contiene los datos de origen
Use ODBC:        Enabled
```

#### Propiedades ODBC

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "su nombre de servidor o dirección IP"
name: "UID",        value: "su usuario de base de datos"
name: "PWD",        value: "su contraseña de base de datos"
name: "DATABASE",   value: "nombre de la base de datos que contiene el esquema de datos de origen"
```