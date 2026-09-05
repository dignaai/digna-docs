# Conector de origen para Snowflake

Esta guía describe cómo configurar *digna* para conectarse a Snowflake usando el conector nativo de Python o el driver ODBC.

Se refiere a la pantalla **"Crear una conexión de base de datos"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Driver nativo de Python

**Librería:** `snowflake-connector-python`  
**Autenticación soportada:** Solo autenticación basada en contraseña

> Para otros métodos de autenticación, por favor use el driver ODBC.

### Configuración de *digna* (Driver nativo)

Proporcione la siguiente información en la pantalla **"Crear una conexión de base de datos"**:

```
Technology:      Snowflake
Host Address:    Nombre de la cuenta de Snowflake
Host Port:       No es necesario
Database Name:   Base de datos que contiene el esquema de origen
Schema Name:     Esquema que contiene los datos de origen
User Name:       Nombre de usuario y warehouse en el formato "user<@>warehouse"
User Password:   Contraseña del usuario
Use ODBC:        Deshabilitado (por defecto)
```

---

## Driver ODBC

El driver ODBC puede soportar una gama más amplia de opciones de autenticación y conectividad. Esta sección se centra en la autenticación basada en contraseña usando el **SnowflakeDSIIDriver**.

### 1. Instalar el driver ODBC

Instale el **SnowflakeDSIIDriver** siguiendo la guía de instalación oficial del proveedor.

### 2. Configurar la fuente de datos ODBC

Siga estos pasos para configurar una nueva fuente de datos ODBC usando autenticación basada en contraseña:

#### Paso 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Notas: 
- Si no proporciona valores para Database, Schema y Warehouse, entonces deberá proporcionarlos como propiedades ODBC durante la configuración de la fuente de datos en *digna*.
- El valor para "Server" consiste en el nombre de su cuenta de Snowflake seguido de ".snowflakecomputing.com"

#### Paso 2 – Probar la conexión

Haga clic en el botón **TEST**. Una conexión exitosa debería verse así:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Ahora puede configurar *digna* para usar la conexión ODBC, ya sea con un **DSN (Data Source Name)** o una configuración **sin DSN**.

---

### A. Configuración basada en DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      Snowflake
Database Name:   Base de datos que contiene el esquema de origen
Schema Name:     Esquema que contiene los datos de origen
Use ODBC:        Habilitado
```

#### Propiedades ODBC

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{su contraseña entre llaves}"

opcionalmente:
name: "Database",       value: "Base de datos que contiene el esquema de origen"
name: "Schema",         value: "Esquema que contiene los datos de origen"
name: "Warehouse",      value: "Warehouse a usar para la ejecución de los SQLs"
```

> El `DSN` debe coincidir con el nombre definido en la configuración de su driver ODBC.

---

### B. Configuración sin DSN

#### Configuración de *digna*

En la pantalla **"Crear una conexión de base de datos"**, proporcione lo siguiente:

```
Technology:      Snowflake
Database Name:   Esquema que contiene los datos de origen (igual que Schema Name)
Schema Name:     Esquema que contiene los datos de origen
Use ODBC:        Habilitado
```

#### Propiedades ODBC

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Base de datos que contiene el esquema de origen"
name: "Schema",     value: "Esquema que contiene los datos de origen"
name: "Warehouse",  value: "Warehouse a usar para la ejecución de los SQLs"
```