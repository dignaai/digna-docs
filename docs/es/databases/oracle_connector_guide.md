---
title: Conector de Oracle – Integración de bases de datos | Documentación de digna
description: Configure digna para conectarse a Oracle usando el controlador python-oracledb o el controlador ODBC de Oracle. Admite autenticación basada en contraseña con configuraciones DSN o sin DSN.
image: /assets/logo_square.png
---


# Conector de origen para Oracle

Esta guía describe cómo configurar *digna* para conectarse a Oracle DB usando el conector nativo de Python o el controlador ODBC.

Se refiere a la pantalla **"Crear una conexión de base de datos"**.

![Crear una conexión de base de datos](images/data_source_config_input_mask.png)

---

## Controlador nativo de Python

**Library:** `python-oracledb`  
**Supported Authentication:** Solo autenticación basada en contraseña

> ⚠️ Para otros métodos de autenticación, utilice el controlador ODBC.

### Configuración de *digna* (Controlador nativo)

Proporcione la siguiente información en la pantalla **"Crear una conexión de base de datos"**:

```
Technology:      Oracle
Host Address:    Nombre del servidor o dirección IP
Host Port:       Número de puerto, p. ej. 1521
Database Name:   Nombre de la instancia, nombre del servicio
Schema Name:     Esquema que contiene los datos fuente
User Name:       Nombre de usuario de la base de datos
User Password:   Contraseña del usuario
Use ODBC:        Disabled (default)
```

---

## Controlador ODBC

El controlador ODBC puede admitir una gama más amplia de opciones de autenticación y conectividad. Esta sección se centra en la autenticación basada en contraseña usando el controlador **Oracle in OraDB21Home1**.

### 1. Instale el controlador ODBC

Instale **Oracle in OraDB21Home1** (o similar) siguiendo la guía de instalación oficial del proveedor.

### 2. Configure la fuente de datos ODBC

Siga estos pasos para configurar una nueva fuente de datos ODBC usando autenticación basada en contraseña:

#### Paso 1
![Paso 1](images/oracle/create_odbc_data_source_step1.png)

Nota:
El TNS Service Name debe configurarse en el archivo tnsnames.ora de la instalación de su cliente Oracle. Ahí debe proporcionar el descriptor de conexión (host, puerto, nombre del servicio).

#### Paso 2 – Probar la conexión

Haga clic en el botón **Test Connection**.

![Paso 2](images/oracle/create_odbc_data_source_step2.png)

Introduzca la contraseña y haga clic en el botón **OK**.

![Paso 2](images/oracle/create_odbc_data_source_step3.png)

---

Ahora puede configurar *digna* para usar la conexión ODBC, ya sea con un **DSN (Data Source Name)** o una configuración **DSN-less**.

---

### A. Configuración basada en DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      Oracle
Database Name:   Base de datos que contiene el esquema fuente
Schema Name:     Esquema que contiene los datos fuente
Use ODBC:        Enabled
```

#### Propiedades ODBC

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "tu usuario de Oracle"
name: "PWD",            value: "{tu contraseña entre llaves}"
```

> 🔹 El `DSN` debe coincidir con el nombre definido en la configuración de su controlador ODBC.

---

### B. Configuración sin DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      Oracle
Database Name:   Esquema que contiene los datos fuente (igual que Schema Name)
Schema Name:     Esquema que contiene los datos fuente
Use ODBC:        Enabled
```

#### Propiedades ODBC

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "tu usuario oracle'"
name: "PWD",        value: "tu contraseña de Oracle"
```