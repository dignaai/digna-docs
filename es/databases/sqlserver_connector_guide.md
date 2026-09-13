# Conector de origen para MS SQL Server

Esta guía describe cómo configurar *digna* para conectarse a Microsoft SQL Server mediante
**ODBC**, usando una cadena de conexión **sin DSN**.

La parte de digna de la configuración es la misma para todas las tecnologías: dónde se crean las
conexiones, cómo se cifran los valores de las propiedades, cómo se prueba una conexión y qué
significan los modos de perfilado. Se describe en
[Descripción general de las conexiones de base de datos](overview.md). Esta página cubre lo
específico de SQL Server.

!!! note "Azure Synapse Analytics"

    Synapse también se configura como una conexión de SQL Server, con un nombre de host distinto
    y algunas consideraciones adicionales; véase
    [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Instalar el controlador ODBC {: #1-install-the-odbc-driver }

Instale **ODBC Driver 18 for SQL Server** en la máquina que ejecuta el backend de *digna*,
siguiendo [la guía de instalación de Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

El controlador que viene con Windows bajo el nombre simple **SQL Server** también funciona, pero
está ampliamente superado y no admite ni los ajustes TLS modernos ni la autenticación de Azure.
Úselo solo donde no sea posible instalar el controlador actual.

Consulte el nombre exacto del controlador registrado en su host como se describe en
[Instalar el controlador ODBC en el host de digna](overview.md#install-the-driver).

---

## 2. Propiedades ODBC {: #2-odbc-properties }

!!! important "Un ejemplo, no una especificación"

    El conjunto siguiente es una combinación que se sabe que funciona. Las propiedades
    pertenecen al controlador ODBC de Microsoft, por lo que sus nombres, valores predeterminados
    y valores aceptados difieren entre versiones del controlador —Driver 18 cifra de forma
    predeterminada, cosa que Driver 17 no hacía— y entre plataformas. Tómelo como punto de
    partida y consulte la documentación de la versión del controlador que haya instalado.

Añada las siguientes propiedades en la pantalla **Add DB Connection**:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Debe coincidir con el nombre del controlador registrado en el host de *digna* |
| `SERVER` | `sql.example.com` | Nombre del servidor o dirección IP. Instancias con nombre: `host\instance`; puerto no predeterminado: `host,1433` |
| `PORT` | `1433` | Omítalo cuando el puerto ya forme parte de `SERVER` |
| `DATABASE` | `digna_source_db` | Base de datos que contiene los esquemas de origen. Es la única base que esta conexión puede perfilar |
| `UID` | `digna_source_user` | Usuario de la base de datos |
| `PWD` | `<password>` | Marque **Encrypted** |

La cadena de conexión resultante tiene este aspecto:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Cifrado con ODBC Driver 18

Driver 18 cifra las conexiones de forma predeterminada y valida el certificado del servidor.
Frente a un servidor con un certificado en el que su host de *digna* no confía —normalmente un
certificado autofirmado— la conexión falla con un error de cadena de certificados. Añada:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `Encrypt` | `yes` | Predeterminado en Driver 18; póngalo en `no` solo si el servidor no admite TLS |
| `TrustServerCertificate` | `yes` | Omite la validación del certificado. Cómodo en entornos de prueba; en producción es preferible instalar el certificado |

### Autenticación de Windows

Para conectarse con la cuenta que ejecuta el servicio *digna* en lugar de con un inicio de
sesión de SQL, elimine `UID` y `PWD` y añada:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `Trusted_Connection` | `yes` | La cuenta de servicio de *digna* necesita los derechos sobre la base de datos |

---

## 3. Configuración de *digna* {: #3-digna-configuration }

En la pantalla **Add DB Connection**, indique lo siguiente:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Notas sobre MS SQL Server {: #4-notes-on-ms-sql-server }

- **Una conexión ve una base de datos.** *digna* ofrece los esquemas de la base nombrada en
  `DATABASE`, porque SQL Server solo informa de la base actual como catálogo. Las tablas de
  origen de otra base necesitan su propia conexión.
- **Modos de perfilado.** *Permanent* crea las tablas de trabajo en **Work Schema**, por lo que
  el usuario necesita `CREATE TABLE` allí. *Session* usa tablas temporales locales (`#wt_…`) en
  `tempdb` y no toca **Work Schema**. *Standard* solo necesita acceso de lectura.
- **`SERVER` lleva la instancia y el puerto.** Con una instancia con nombre, `host\instance`
  requiere que el servicio SQL Server Browser sea accesible; `host,port` lo evita.

---

## 5. Verificar el controlador (opcional) {: #5-verifying-the-driver-optional }

Configurar un origen de datos ODBC no es necesario para una conexión sin DSN, pero el asistente
propio del controlador es una forma cómoda de confirmar que el controlador funciona y que el
servidor acepta sus credenciales antes de introducirlas en *digna*.

#### Paso 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Haga clic en el botón **Next >**.

#### Paso 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Elija el método de autenticación (p. ej. nombre de usuario y contraseña)
e indique los datos necesarios.

Haga clic en el botón **Next >**.

#### Paso 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Elija los ajustes conformes a ANSI y haga clic en el botón **Next >**.

#### Paso 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Puede dejar los ajustes predeterminados o elegir opciones de registro según sus necesidades
y hacer clic en el botón **Finish**.

#### Paso 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Haga clic ahora en el botón **Test datasource**.

#### Paso 6
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

Una pantalla de éxito confirma que el controlador y las credenciales funcionan. Los valores que
ha introducido son exactamente los que toman las propiedades de la
[sección 2](#2-odbc-properties).