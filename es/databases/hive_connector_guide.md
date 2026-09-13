# Conector de origen para Hive

Esta guía describe cómo configurar *digna* para conectarse a Apache Hive mediante **ODBC**,
usando una cadena de conexión **sin DSN**.

La parte de digna de la configuración es la misma para todas las tecnologías: dónde se crean las
conexiones, cómo se cifran los valores de las propiedades, cómo se prueba una conexión y qué
significan los modos de perfilado. Se describe en
[Descripción general de las conexiones de base de datos](overview.md). Esta página cubre lo
específico de Hive.

---

## 1. Instalar el controlador ODBC {: #1-install-the-odbc-driver }

Instale el **Cloudera ODBC Driver for Apache Hive** en la máquina que ejecuta el backend de
*digna*, siguiendo la guía de instalación oficial del proveedor.

Consulte el nombre exacto del controlador registrado en su host como se describe en
[Instalar el controlador ODBC en el host de digna](overview.md#install-the-driver).

---

## 2. Propiedades ODBC {: #2-odbc-properties }

!!! important "Un ejemplo, no una especificación"

    El conjunto siguiente es una combinación que se sabe que funciona. Las propiedades
    pertenecen al controlador de Cloudera para Hive, por lo que sus nombres, valores
    predeterminados y valores aceptados difieren entre versiones del controlador y plataformas,
    y lo que acepta HiveServer2 depende por completo de cómo esté protegido el clúster:
    mecanismo de autenticación, modo de transporte, TLS, pasarela. Tómelo como punto de partida
    y consulte la documentación de la versión del controlador que haya instalado.

Añada las siguientes propiedades en la pantalla **Add DB Connection**:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Debe coincidir con el nombre del controlador registrado en el host de *digna* |
| `HOST` | `hive.example.com` | Nombre de host o dirección IP de HiveServer2 |
| `PORT` | `10000` | Puerto de HiveServer2; `10001` para transporte HTTP |

La cadena de conexión resultante tiene este aspecto:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Autenticación

Un HiveServer2 sin protección acepta las tres propiedades anteriores tal cual. Cuando la
autenticación está activada, añada:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `AuthMech` | `3` | `0` sin autenticación, `2` solo nombre de usuario, `3` nombre de usuario y contraseña, `1` Kerberos |
| `UID` | `digna_source_user` | Necesario para `AuthMech` `2` y `3` |
| `PWD` | `<password>` | Necesario para `AuthMech` `3`. Marque **Encrypted** |

Para Kerberos (`AuthMech=1`), el host de *digna* necesita además un tíquet o keytab válido, más
las propiedades `KrbHostFQDN`, `KrbServiceName` y `KrbRealm` que documenta el controlador.

### Transporte y TLS

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `ThriftTransport` | `2` | `0` binario (el predeterminado, puerto 10000), `1` SASL, `2` HTTP (puerto 10001, y lo que espera una pasarela Knox) |
| `HTTPPath` | `cliservice` | Con `ThriftTransport=2` |
| `SSL` | `1` | Cuando HiveServer2 está protegido con TLS |
| `Schema` | `dignadata` | Base de datos de Hive en la que se inicia la sesión. Opcional: *digna* cualifica sus consultas |

---

## 3. Configuración de *digna* {: #3-digna-configuration }

En la pantalla **Add DB Connection**, indique lo siguiente:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Notas sobre Hive {: #4-notes-on-hive }

- **Los catálogos vienen del controlador.** Hive no tiene catálogo propio, así que *digna* toma
  lo que informa el controlador —normalmente una única entrada llamada `HIVE`— y lista las bases
  de Hive como esquemas por debajo.
- **Work Schema es una base de datos de Hive.** Para el perfilado *Permanent*, el usuario
  necesita el derecho de crear y eliminar tablas en ella, y la ubicación de almacenamiento
  subyacente debe permitir escritura.
- **Modos de perfilado.** *Permanent* crea las tablas de trabajo en **Work Schema**. *Session*
  usa `CREATE TEMPORARY TABLE`, lo que requiere un HiveServer2 que admita tablas temporales, y
  no toca **Work Schema**. *Standard* solo necesita acceso de lectura, y es el modo que hay que
  elegir en un clúster donde *digna* no tiene ningún acceso de escritura.
- **El perfilado es un conjunto de consultas, no un recorrido completo.** Cada estadística la
  calcula HiveServer2, así que la cola a la que envía el usuario de *digna* debe tener capacidad
  suficiente para la ventana de inspección.

---

## 5. Verificar el controlador (opcional) {: #5-verifying-the-driver-optional }

Configurar un origen de datos ODBC no es necesario para una conexión sin DSN, pero el diálogo
propio del controlador es una forma cómoda de confirmar que el controlador, el modo de
transporte y sus credenciales funcionan antes de introducirlos en *digna*.

#### Paso 1
![Step 1](images/hive/create_odbc_data_source_step1.png)

Los campos **Host**, **Port**, **Database**, **Mechanism** y **Thrift Transport** se
corresponden aquí con las propiedades `HOST`, `PORT`, `Schema`, `AuthMech` y `ThriftTransport`
de la [sección 2](#2-odbc-properties).

#### Paso 2 – Probar la conexión

Indique la contraseña y haga clic en el botón **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Tras una prueba correcta, haga clic en el botón **OK**.