---
title: Conector Snowflake – Integración de bases de datos | digna Documentación
description: Configure digna para conectarse a Snowflake mediante ODBC con una cadena de conexión sin DSN. Cubre el controlador ODBC de Snowflake, los tokens de acceso programático, la selección de almacén y rol y los ajustes de conexión del lado de digna.
image: /assets/logo_square.png
---


# Conector de origen para Snowflake

Esta guía describe cómo configurar *digna* para conectarse a Snowflake mediante **ODBC**, usando
una cadena de conexión **sin DSN**.

La parte de digna de la configuración es la misma para todas las tecnologías: dónde se crean las
conexiones, cómo se cifran los valores de las propiedades, cómo se prueba una conexión y qué
significan los modos de perfilado. Se describe en
[Descripción general de las conexiones de base de datos](overview.md). Esta página cubre lo
específico de Snowflake.

---

## 1. Instalar el controlador ODBC {: #1-install-the-odbc-driver }

Instale el **Snowflake ODBC Driver** en la máquina que ejecuta el backend de *digna*, siguiendo
[la guía de instalación de Snowflake](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

El controlador se registra como **SnowflakeDSIIDriver**. Consulte el nombre exacto registrado en
su host como se describe en
[Instalar el controlador ODBC en el host de digna](overview.md#install-the-driver).

---

## 2. Propiedades ODBC {: #2-odbc-properties }

A Snowflake se llega con un **token de acceso programático (PAT)**: la vía de autenticación
frente a la que se verifica *digna*, y la que exige Snowflake en las cuentas donde el inicio de
sesión solo con contraseña está bloqueado.

!!! important "Un ejemplo, no una especificación"

    El conjunto siguiente es una combinación que se sabe que funciona. Las propiedades
    pertenecen al controlador ODBC de Snowflake, por lo que sus nombres, valores predeterminados
    y valores aceptados difieren entre versiones del controlador y plataformas, y qué opciones
    de autenticación permite su cuenta lo decide la política de seguridad de esa cuenta. Tómelo
    como punto de partida y consulte la documentación de la versión del controlador que haya
    instalado.

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Debe coincidir con el nombre del controlador registrado en el host de *digna* |
| `Server` | `<account>.snowflakecomputing.com` | Identificador de cuenta más el sufijo, p. ej. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Usuario de Snowflake al que pertenece el token |
| `Database` | `TEST` | Base de datos que contiene los esquemas de origen. Es la única base que esta conexión puede perfilar |
| `Schema` | `PUBLIC` | Esquema predeterminado de la sesión |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Selecciona la autenticación por token |
| `token` | `<programmatic access token>` | Marque **Encrypted** |

La cadena de conexión resultante tiene este aspecto:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Almacén y rol

Las consultas necesitan un almacén. Si el usuario de *digna* tiene un almacén predeterminado y
un rol predeterminado, la sesión los toma y no hay que configurar nada. En caso contrario,
añada:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Almacén que ejecuta las consultas de perfilado |
| `Role` | `DIGNA_READER` | Rol cuyos permisos usa la sesión |

!!! tip "Dé a digna su propio almacén"

    Un almacén independiente, pequeño y con suspensión automática mantiene visible el coste del
    perfilado y evita que *digna* compita con los usuarios interactivos por la capacidad de
    cómputo.

### Autenticación con contraseña

Donde la cuenta todavía lo permita, una contraseña funciona en lugar del token: elimine
`authenticator` y `token` y añada:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `PWD` | `<password>` | Marque **Encrypted** |

---

## 3. Configuración de *digna* {: #3-digna-configuration }

En la pantalla **Add DB Connection**, indique lo siguiente:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Notas sobre Snowflake {: #4-notes-on-snowflake }

- **Los tokens caducan.** Un token de acceso programático se emite con una vigencia, y el
  perfilado se detiene el día en que expira. Anote la fecha de caducidad al crearlo y vuelva a
  introducir el nuevo token en la propiedad `token`: los valores cifrados pueden sustituirse
  pero no leerse.
- **Una conexión ve una base de datos.** *digna* ofrece los esquemas de la base nombrada en
  `Database`, porque Snowflake solo informa de la base actual como catálogo. Las tablas de
  origen de otra base necesitan su propia conexión.
- **Los identificadores están en mayúsculas**, salvo que se hayan creado entrecomillados.
  *digna* usa los nombres tal como los informa Snowflake.
- **Modos de perfilado.** *Permanent* crea las tablas de trabajo en **Work Schema**, por lo que
  el rol necesita `CREATE TABLE` allí. *Session* usa `CREATE TEMPORARY TABLE` y no toca
  **Work Schema**. *Standard* solo necesita acceso de lectura, y ningún permiso de escritura.

---

## 5. Verificar el controlador (opcional) {: #5-verifying-the-driver-optional }

Configurar un origen de datos ODBC no es necesario para una conexión sin DSN, pero el diálogo
propio del controlador es una forma cómoda de confirmar que el controlador, la URL de la cuenta
y sus credenciales funcionan antes de introducirlos en *digna*.

#### Paso 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Notas:

- El valor de **Server** se compone del identificador de su cuenta de Snowflake seguido de
  `.snowflakecomputing.com`.
- **Database**, **Schema** y **Warehouse** introducidos aquí se corresponden con las propiedades
  `Database`, `Schema` y `Warehouse` de la [sección 2](#2-odbc-properties).

#### Paso 2 – Probar la conexión

Haga clic en el botón **TEST**. Una conexión correcta debería verse así:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)
