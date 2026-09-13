---
title: Conector PostgreSQL – Integración de bases de datos | digna Documentación
description: Configure digna para conectarse a PostgreSQL mediante ODBC con una cadena de conexión sin DSN. Cubre el controlador psqlODBC, las propiedades ODBC necesarias, los modos SSL y los ajustes de conexión del lado de digna.
image: /assets/logo_square.png
---


# Conector de origen para PostgreSQL

Esta guía describe cómo configurar *digna* para conectarse a PostgreSQL mediante **ODBC**,
usando una cadena de conexión **sin DSN**.

La parte de digna de la configuración es la misma para todas las tecnologías: dónde se crean las
conexiones, cómo se cifran los valores de las propiedades, cómo se prueba una conexión y qué
significan los modos de perfilado. Se describe en
[Descripción general de las conexiones de base de datos](overview.md). Esta página cubre lo
específico de PostgreSQL.

---

## 1. Instalar el controlador ODBC {: #1-install-the-odbc-driver }

Instale el controlador ODBC de PostgreSQL (**psqlODBC**) en la máquina que ejecuta el backend de
*digna*, siguiendo la guía de instalación oficial del proveedor.

El controlador se registra con un nombre que varía según la plataforma y el paquete: normalmente
**PostgreSQL Unicode(x64)** en Windows y **PostgreSQL ODBC Driver(UNICODE)** en Linux. Consulte
el nombre exacto en su host como se describe en
[Instalar el controlador ODBC en el host de digna](overview.md#install-the-driver), y use ese
nombre para la propiedad `DRIVER` que aparece más abajo.

---

## 2. Propiedades ODBC {: #2-odbc-properties }

!!! important "Un ejemplo, no una especificación"

    El conjunto siguiente es una combinación que se sabe que funciona. Las propiedades
    pertenecen al controlador psqlODBC, por lo que sus nombres, valores predeterminados y
    valores aceptados difieren entre versiones del controlador y plataformas, y lo que exige su
    servidor —SSL en particular— también puede diferir. Tómelo como punto de partida y consulte
    la documentación de la versión del controlador que haya instalado.

Añada las siguientes propiedades en la pantalla **Add DB Connection**:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Debe coincidir con el nombre del controlador registrado en el host de *digna* |
| `SERVER` | `db.example.com` | Nombre del servidor o dirección IP |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Base de datos que contiene los esquemas de origen. Es la única base que esta conexión puede perfilar |
| `UID` | `digna_source_user` | Usuario de la base de datos |
| `PWD` | `<password>` | Marque **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` o `verify-full`: el servidor debe aceptarlo |

La cadena de conexión resultante tiene este aspecto:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Cualquier otra opción de psqlODBC puede añadirse como propiedad adicional, por ejemplo
`ReadOnly=1` para una sesión de solo lectura, o `ConnSettings` para ejecutar sentencias `SET` al
conectar.

---

## 3. Configuración de *digna* {: #3-digna-configuration }

En la pantalla **Add DB Connection**, indique lo siguiente:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Notas sobre PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` debe coincidir con el servidor.** Un servidor configurado con `hostssl` rechaza
  `SSLMode=disable`, y `verify-ca` o `verify-full` necesitan además que el certificado raíz esté
  disponible para el controlador en el host de *digna*. Si tuvo que elegir un modo concreto al
  probar el controlador, use el mismo aquí.
- **Una conexión ve una base de datos.** *digna* ofrece los esquemas de la base nombrada en
  `DATABASE`, porque PostgreSQL solo informa de la base actual como catálogo. Las tablas de
  origen de otra base necesitan su propia conexión.
- **Modos de perfilado.** *Permanent* crea las tablas de trabajo en **Work Schema**, por lo que
  el usuario necesita `CREATE` sobre ese esquema. *Session* usa `CREATE TEMPORARY TABLE` y no
  toca **Work Schema**. *Standard* solo necesita acceso de lectura.

---

## 5. Verificar el controlador (opcional) {: #5-verifying-the-driver-optional }

Configurar un origen de datos ODBC no es necesario para una conexión sin DSN, pero el diálogo
propio del controlador es una forma cómoda de confirmar que el controlador funciona y que el
servidor acepta sus credenciales y su modo SSL antes de introducirlos en *digna*.

#### Paso 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### Paso 2 – Probar la conexión

Haga clic en el botón **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

Los valores que ha introducido aquí son exactamente los que toman las propiedades de la
[sección 2](#2-odbc-properties).
