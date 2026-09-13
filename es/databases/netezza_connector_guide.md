# Conector de origen para Netezza

Esta guía describe cómo configurar *digna* para conectarse a Netezza mediante **ODBC**, usando
una cadena de conexión **sin DSN**.

La parte de digna de la configuración es la misma para todas las tecnologías: dónde se crean las
conexiones, cómo se cifran los valores de las propiedades, cómo se prueba una conexión y qué
significan los modos de perfilado. Se describe en
[Descripción general de las conexiones de base de datos](overview.md). Esta página cubre lo
específico de Netezza.

---

## 1. Instalar el controlador ODBC {: #1-install-the-odbc-driver }

Instale el controlador ODBC **NetezzaSQL** (parte de las herramientas cliente de IBM Netezza) en
la máquina que ejecuta el backend de *digna*, siguiendo la guía de instalación oficial del
proveedor.

Consulte el nombre exacto del controlador registrado en su host como se describe en
[Instalar el controlador ODBC en el host de digna](overview.md#install-the-driver).

---

## 2. Propiedades ODBC {: #2-odbc-properties }

!!! important "Un ejemplo, no una especificación"

    El conjunto siguiente es una combinación que se sabe que funciona. Las propiedades
    pertenecen al controlador NetezzaSQL, por lo que sus nombres, valores predeterminados y
    valores aceptados difieren entre versiones del cliente y plataformas, y un appliance
    protegido con TLS necesita más que las propiedades mostradas aquí. Tómelo como punto de
    partida y consulte la documentación de la versión del cliente que haya instalado.

Añada las siguientes propiedades en la pantalla **Add DB Connection**:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Debe coincidir con el nombre del controlador registrado en el host de *digna*. Las llaves son la forma habitual de escribir este nombre |
| `SERVER` | `netezza.example.com` | Nombre del servidor o dirección IP |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Base de datos en la que se inicia la sesión |
| `UID` | `ADMIN` | Usuario de la base de datos |
| `PWD` | `<password>` | Marque **Encrypted** |

La cadena de conexión resultante tiene este aspecto:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Según su versión de controlador, su instalación y sus requisitos de seguridad, pueden ser
necesarias más propiedades, por ejemplo `SecurityLevel` y `CaCertFile` para un appliance
protegido con TLS. Cualquier opción que ofrezcan los diálogos *Advanced*, *SSL* y *Driver* del
controlador puede añadirse como propiedad.

---

## 3. Configuración de *digna* {: #3-digna-configuration }

En la pantalla **Add DB Connection**, indique lo siguiente:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Notas sobre Netezza {: #4-notes-on-netezza }

- **Se aplican tanto catálogos como esquemas.** *digna* lista como catálogos las bases de datos
  que el usuario puede ver (desde `_V_DATABASE`) y debajo sus esquemas (desde `_V_SCHEMA`), de
  modo que una conexión puede dar servicio a orígenes de más de una base. `DATABASE` solo decide
  dónde se inicia la sesión.
- **Los identificadores están en mayúsculas**, salvo que se hayan creado entrecomillados, que es
  la razón por la que los ejemplos anteriores usan `TEST` y `ADMIN`.
- **Modos de perfilado.** *Permanent* crea las tablas de trabajo en **Work Schema**, por lo que
  el usuario necesita `CREATE TABLE` allí. *Session* usa `CREATE TEMPORARY TABLE` y no toca
  **Work Schema**. *Standard* solo necesita acceso de lectura.

---

## 5. Verificar el controlador (opcional) {: #5-verifying-the-driver-optional }

Configurar un origen de datos ODBC no es necesario para una conexión sin DSN, pero el diálogo
propio del controlador es una forma cómoda de confirmar que el controlador y sus credenciales
funcionan antes de introducirlos en *digna*.

#### Paso 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Los campos de **DSN Options** se corresponden uno a uno con las propiedades de la
[sección 2](#2-odbc-properties). Según su controlador de Netezza, su instalación y sus
requisitos de seguridad, es posible que también necesite datos en las pestañas
**Advanced DSN Options**, **SSL DSN Options** o **Driver Options**; para la instalación más
sencilla, **DSN Options** es suficiente.

Haga clic en el botón **Test Connection**.

#### Paso 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Cuando aparezca la pantalla de éxito, el controlador funciona y los valores son correctos.