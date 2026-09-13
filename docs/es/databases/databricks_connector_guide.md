---
title: Conector Databricks – Integración de bases de datos | digna Documentación
description: Configure digna para conectarse a Databricks con Unity Catalog mediante ODBC y una cadena de conexión sin DSN. Cubre el controlador ODBC de Databricks, los tokens de acceso personal, la ruta HTTP y los ajustes de conexión del lado de digna.
image: /assets/logo_square.png
---

# Conector de origen para Databricks

Esta guía describe cómo configurar *digna* para conectarse a Databricks mediante **ODBC**,
usando una cadena de conexión **sin DSN**.

La parte de digna de la configuración es la misma para todas las tecnologías: dónde se crean las
conexiones, cómo se cifran los valores de las propiedades, cómo se prueba una conexión y qué
significan los modos de perfilado. Se describe en
[Descripción general de las conexiones de base de datos](overview.md). Esta página cubre lo
específico de Databricks.

!!! note "Se requiere Unity Catalog"

    *digna* lee los catálogos disponibles desde `system.information_schema.catalogs`, así que el
    área de trabajo debe tener Unity Catalog habilitado. Versiones anteriores de *digna* ofrecían
    una tecnología independiente «Databricks Legacy» para áreas de trabajo sin Unity Catalog; ya
    no está disponible.

---

## 1. Instalar el controlador ODBC {: #1-install-the-odbc-driver }

Instale el **Databricks ODBC Driver** en la máquina que ejecuta el backend de *digna*, siguiendo
[la guía de instalación de Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

Según la versión, el controlador se registra como **Simba Spark ODBC Driver** o como
**Databricks ODBC Driver**. Consulte el nombre exacto registrado en su host como se describe en
[Instalar el controlador ODBC en el host de digna](overview.md#install-the-driver).

---

## 2. Reunir los datos de conexión {: #2-gather-the-connection-details }

Todos los valores proceden del almacén SQL (o clúster) que quiere que use *digna*. Ábralo en el
área de trabajo de Databricks y vaya a **Connection details**:

| Campo de Databricks | Se usa como |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, normalmente `443` |
| **HTTP path** | `HTTPPath` |

Para la autenticación, cree un **token de acceso personal**; véase
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Los tokens pertenecen a un usuario o entidad de servicio, y esa entidad necesita `USE CATALOG`,
`USE SCHEMA` y `SELECT` sobre los datos de origen.

---

## 3. Propiedades ODBC {: #3-odbc-properties }

!!! important "Un ejemplo, no una especificación"

    El conjunto siguiente es una combinación que se sabe que funciona. Las propiedades
    pertenecen al controlador de Databricks/Simba, por lo que sus nombres, valores
    predeterminados y valores aceptados difieren entre versiones del controlador —el controlador
    se ha renombrado y ha ampliado sus opciones de autenticación más de una vez— y entre
    plataformas. Tómelo como punto de partida y consulte la documentación de la versión del
    controlador que haya instalado.

Añada las siguientes propiedades en la pantalla **Add DB Connection**:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Debe coincidir con el nombre del controlador registrado en el host de *digna* |
| `Host` | `<workspace>.cloud.databricks.com` | Nombre de host del servidor del almacén, p. ej. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | Ruta HTTP del almacén o clúster |
| `SSL` | `1` | Los puntos de conexión de Databricks son solo TLS |
| `ThriftTransport` | `2` | Transporte HTTP, que es el que hablan los puntos de conexión SQL |
| `AuthMech` | `3` | Autenticación por token |
| `UID` | `token` | La palabra literal `token`, no un nombre de usuario |
| `PWD` | `dapi…` | El token de acceso personal. Marque **Encrypted** |
| `UseNativeQuery` | `1` | Pasa el SQL de *digna* sin modificar; véase más abajo |

La cadena de conexión resultante tiene este aspecto:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Mantenga `UseNativeQuery=1`"

    Con `UseNativeQuery=0` —el valor predeterminado del controlador— el controlador reescribe el
    SQL entrante en lo que considera sintaxis ODBC portable. *digna* ya genera SQL de
    Databricks, así que la reescritura puede alterar el uso de comillas invertidas y los
    literales de fecha, y el perfilado falla entonces en sentencias que son válidas tal como
    están escritas.

### OAuth en lugar de un token

Para una entidad de servicio con autenticación OAuth de máquina a máquina, sustituya
`AuthMech`, `UID` y `PWD` por:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Credenciales de cliente |
| `Auth_Client_ID` | `<application id>` | Entidad de servicio |
| `Auth_Client_Secret` | `<client secret>` | Marque **Encrypted** |

---

## 4. Configuración de *digna* {: #4-digna-configuration }

En la pantalla **Add DB Connection**, indique lo siguiente:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Notas sobre Databricks {: #5-notes-on-databricks }

- **El almacén debe estar en ejecución**, o poder arrancar, cuando *digna* se conecte. Un
  almacén que se reanuda desde un estado detenido puede tardar más que el tiempo de espera de la
  conexión: si la prueba falla en el primer intento tras un periodo de inactividad, vuelva a
  intentarlo.
- **Los catálogos vienen del área de trabajo.** A diferencia de la mayoría de las tecnologías,
  una conexión de Databricks alcanza todos los catálogos que la entidad tiene permitido ver, de
  modo que una sola conexión puede dar servicio a orígenes de varios catálogos.
- **Modos de perfilado.** *Permanent* crea las tablas de trabajo en **Work Schema** dentro del
  catálogo del origen, por lo que la entidad necesita `CREATE TABLE` allí. *Session* usa
  `CREATE TEMPORARY TABLE` y no toca **Work Schema**. *Standard* solo necesita acceso de
  lectura.
- **Los almacenes serverless funcionan** igual; solo cambia `HTTPPath`.

---

## 6. Verificar el controlador (opcional) {: #6-verifying-the-driver-optional }

Configurar un origen de datos ODBC no es necesario para una conexión sin DSN, pero el diálogo
propio del controlador es una forma cómoda de confirmar que el controlador, el almacén y el
token funcionan antes de introducirlos en *digna*.

#### Paso 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Paso 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Paso 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Paso 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Paso 5 – Probar la conexión

Haga clic en el botón **TEST**. Una conexión correcta debería verse así:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

El host, la ruta HTTP y el token introducidos aquí son exactamente los valores que toman las
propiedades de la [sección 3](#3-odbc-properties).
