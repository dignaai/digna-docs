---
title: Conector Teradata – Integración de bases de datos | digna Documentación
description: Configure digna para conectarse a Teradata mediante ODBC con una cadena de conexión sin DSN. Cubre el controlador ODBC de Teradata, la propiedad DBCNAME, los mecanismos de inicio de sesión y los ajustes de conexión del lado de digna.
image: /assets/logo_square.png
---


# Conector de origen para Teradata

Esta guía describe cómo configurar *digna* para conectarse a Teradata mediante **ODBC**, usando
una cadena de conexión **sin DSN**.

La parte de digna de la configuración es la misma para todas las tecnologías: dónde se crean las
conexiones, cómo se cifran los valores de las propiedades, cómo se prueba una conexión y qué
significan los modos de perfilado. Se describe en
[Descripción general de las conexiones de base de datos](overview.md). Esta página cubre lo
específico de Teradata.

---

## 1. Instalar el controlador ODBC {: #1-install-the-odbc-driver }

Instale el **ODBC Driver for Teradata** en la máquina que ejecuta el backend de *digna*,
siguiendo la guía de instalación oficial del proveedor.

El controlador se registra con su versión en el nombre, por ejemplo
**Teradata Database ODBC Driver 20.00**. Consulte el nombre exacto registrado en su host como se
describe en
[Instalar el controlador ODBC en el host de digna](overview.md#install-the-driver).

---

## 2. Propiedades ODBC {: #2-odbc-properties }

!!! important "Un ejemplo, no una especificación"

    El conjunto siguiente es una combinación que se sabe que funciona. Las propiedades
    pertenecen al controlador ODBC de Teradata, por lo que sus nombres, valores predeterminados
    y valores aceptados difieren entre versiones del controlador —la versión forma parte del
    propio nombre del controlador— y entre plataformas. Tómelo como punto de partida y consulte
    la documentación de la versión del controlador que haya instalado.

Añada las siguientes propiedades en la pantalla **Add DB Connection**:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Debe coincidir con el nombre del controlador registrado en el host de *digna* |
| `DBCNAME` | `teradata.example.com` | Nombre del servidor o dirección IP. Nombre que da Teradata a la propiedad de host |
| `UID` | `digna_source_user` | Usuario de la base de datos |
| `PWD` | `<password>` | Marque **Encrypted** |

La cadena de conexión resultante tiene este aspecto:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Propiedades adicionales útiles:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `MechanismName` | `TD2` | Mecanismo de inicio de sesión. `TD2` es el predeterminado de Teradata; use `LDAP` para la autenticación por directorio |
| `DefaultDatabase` | `dad` | Base de datos en la que se inicia la sesión |
| `CharacterSet` | `UTF8` | Defínalo cuando el juego de caracteres predeterminado de la sesión pueda corromper datos no ASCII |

---

## 3. Configuración de *digna* {: #3-digna-configuration }

En la pantalla **Add DB Connection**, indique lo siguiente:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Notas sobre Teradata {: #4-notes-on-teradata }

- **Una base de datos de Teradata es un catálogo, no un esquema.** *digna* lista como catálogos
  las bases que el usuario puede ver (desde `DBC.DatabasesV`), y el nivel de esquema no aplica.
  Al añadir un origen de datos, elija la base como catálogo; el esquema se informa como *no
  aplicable*.
- **Una conexión alcanza todas las bases permitidas**, de modo que una sola conexión puede dar
  servicio a orígenes de varias bases, a diferencia de las tecnologías en las que la conexión
  queda fijada a una única base.
- **Work Schema es una base de datos.** Para el perfilado *Permanent*, indique la base de
  Teradata que contiene las tablas de trabajo y conceda al usuario derechos de `CREATE TABLE`
  más una asignación de espacio `PERM` en ella: una base sin espacio perm no puede alojar una
  tabla.
- **Modos de perfilado.** *Permanent* crea tablas en **Work Schema**. *Session* usa una tabla
  `VOLATILE`, que necesita espacio `SPOOL` pero ningún espacio perm ni derechos en
  **Work Schema**. *Standard* solo necesita acceso de lectura.

---

## 5. Verificar el controlador (opcional) {: #5-verifying-the-driver-optional }

Configurar un origen de datos ODBC no es necesario para una conexión sin DSN, pero el diálogo
propio del controlador es una forma cómoda de confirmar que el controlador y sus credenciales
funcionan antes de introducirlos en *digna*.

#### Paso 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

El campo **Name or IP address** se corresponde aquí con la propiedad `DBCNAME` de la
[sección 2](#2-odbc-properties).

Haga clic en el botón **Test**.

#### Paso 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Indique el nombre de usuario y la contraseña y haga clic en el botón **OK**. Una pantalla de
éxito confirma que el controlador y las credenciales funcionan.
