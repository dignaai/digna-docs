---
title: Conector de Apache Hive – Integración de Base de Datos | Documentación de digna
description: Configure digna para conectarse a Apache Hive usando el driver nativo PyHive o el driver ODBC de Cloudera. Soporta autenticación basada en contraseña y configuraciones con DSN o sin DSN.
image: /assets/logo_square.png
---


# Conector de origen para Hive

Esta guía describe cómo configurar *digna* para conectarse a Hive usando el conector nativo de Python o el driver ODBC.

Hace referencia a la pantalla **"Crear una conexión de base de datos"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Driver Python nativo

**Library:** `PyHive`  
**Autenticación compatible:** Sólo autenticación basada en contraseña

> Para otros métodos de autenticación, utilice el driver ODBC.

### Configuración de *digna* (Driver nativo)

Proporcione la siguiente información en la pantalla **"Crear una conexión de base de datos"**:

```
Technology:      Apache Hive
Host Address:    Nombre del servidor o dirección IP
Host Port:       Número de puerto, p. ej. 10000
Database Name:   Esquema que contiene los datos fuente
Schema Name:     Esquema que contiene los datos fuente
User Name:       Nombre de usuario de la base de datos
User Password:   Contraseña del usuario
Use ODBC:        Deshabilitado (por defecto)
```

---

## Driver ODBC

El driver ODBC puede admitir una gama más amplia de opciones de autenticación y conectividad. Esta sección se centra en la autenticación basada en contraseña usando el driver **Cloudera ODBC Driver for Apache Hive**.

### 1. Instale el driver ODBC

Instale el **Cloudera ODBC Driver for Apache Hive** (o similar) siguiendo la guía de instalación oficial del proveedor.

### 2. Configure la fuente de datos ODBC

Siga estos pasos para configurar una nueva fuente de datos ODBC usando autenticación basada en contraseña:

#### Paso 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Paso 2 – Probar la conexión

Introduzca la contraseña y haga clic en el botón **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Después de una prueba exitosa, haga clic en el botón **OK**.

---

Ahora puede configurar *digna* para usar la conexión ODBC, ya sea con un **DSN (Data Source Name)** o una configuración **sin DSN**.

---

### A. Configuración basada en DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      Apache Hive
Database Name:   Esquema que contiene los datos fuente (igual que Schema Name)
Schema Name:     Esquema que contiene los datos fuente
Use ODBC:        Habilitado
```

#### Propiedades ODBC

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> El `DSN` debe coincidir con el nombre definido en la configuración de su driver ODBC.

---

### B. Configuración sin DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      Apache Hive
Database Name:   Esquema que contiene los datos fuente (igual que Schema Name)
Schema Name:     Esquema que contiene los datos fuente
Use ODBC:        Habilitado
```

#### Propiedades ODBC

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "nombre de su servidor o dirección IP"
name: "PORT",       value: "Número de puerto, p. ej. 10000"
name: "Schema",     value: "Esquema que contiene los datos fuente"
name: "UID",        value: "tu usuario de hive'
name: "PWD",        value: "tu contraseña de hive"
name: "AuthMech",   value: "3"
```