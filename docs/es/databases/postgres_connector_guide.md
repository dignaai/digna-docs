---
title: Conector PostgreSQL – Integración de base de datos | Documentación de digna
description: Configure digna para conectarse a PostgreSQL usando el driver Python psycopg o el driver ODBC de PostgreSQL. Soporta autenticación basada en contraseña con configuraciones con DSN o sin DSN.
image: /assets/logo_square.png
---


# Conector de origen para PostgreSQL

Esta guía describe cómo configurar *digna* para conectarse a Postgres usando el conector nativo de Python o el driver ODBC.

Se refiere a la pantalla **"Crear una conexión de base de datos"**.

![Crear una conexión de base de datos](images/data_source_config_input_mask.png)

---

## Driver nativo de Python

**Library:** `psycopg`  
**Autenticación soportada:** Solo autenticación basada en contraseña

> ⚠️ Para otros métodos de autenticación, use el driver ODBC.

### Configuración de *digna* (Driver nativo)

Proporcione la siguiente información en la pantalla **"Crear una conexión de base de datos"**:

```
Technology:      Postgres
Host Address:    Nombre del servidor o dirección IP
Host Port:       Número de puerto, p. ej. 5432
Database Name:   Nombre de la base de datos
Schema Name:     Esquema que contiene los datos de origen
User Name:       Nombre de usuario de la base de datos
User Password:   Contraseña del usuario
Use ODBC:        Deshabilitado (por defecto)
```

---

## Driver ODBC

El driver ODBC puede soportar una gama más amplia de opciones de autenticación y conectividad. Esta sección se centra en la autenticación basada en contraseña usando el driver **PostgreSQL Unicode(x64)**.

### 1. Instale el driver ODBC

Instale **PostgreSQL Unicode(x64)** (o similar) siguiendo la guía de instalación oficial del proveedor.

### 2. Configure el origen de datos ODBC

Siga estos pasos para configurar un nuevo origen de datos ODBC usando autenticación basada en contraseña:

#### Paso 1
![Paso 1](images/postgres/create_odbc_data_source_step1.png)

Nota: Si la configuración de su base de datos requiere elegir un "SSLMode" específico, asegúrese de usarlo también al definir una configuración sin DSN.

#### Paso 2 – Pruebe la conexión

Haga clic en el botón **Test Connection**.

![Paso 2](images/postgres/create_odbc_data_source_step2.png)

---

Ahora puede configurar *digna* para usar la conexión ODBC, ya sea con un **DSN (Data Source Name)** o una configuración **sin DSN**.

---

### A. Configuración basada en DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      PostgreSQL
Database Name:   Base de datos que contiene el esquema de origen
Schema Name:     Esquema que contiene los datos de origen
Use ODBC:        Habilitado
```

#### Propiedades ODBC

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 El `DSN` debe coincidir con el nombre definido en la configuración de su driver ODBC.

---

### B. Configuración sin DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      PostgreSQL
Database Name:   Esquema que contiene los datos de origen (igual que Schema Name)
Schema Name:     Esquema que contiene los datos de origen
Use ODBC:        Habilitado
```

#### Propiedades ODBC

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "nombre del servidor o dirección IP"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres u otro nombre de tu base de datos"
name: "UID",        value: "tu usuario de postgres'
name: "PWD",        value: "tu contraseña de postgres"
name: "SSLMode",    value: "require"
```