# Conector de origen para Oracle

Esta guía describe cómo configurar *digna* para conectarse a Oracle Database mediante **ODBC**,
usando una cadena de conexión **sin DSN**.

La parte de digna de la configuración es la misma para todas las tecnologías: dónde se crean las
conexiones, cómo se cifran los valores de las propiedades, cómo se prueba una conexión y qué
significan los modos de perfilado. Se describe en
[Descripción general de las conexiones de base de datos](overview.md). Esta página cubre lo
específico de Oracle.

---

## 1. Instalar el controlador ODBC {: #1-install-the-odbc-driver }

El controlador ODBC de Oracle forma parte del **cliente de Oracle** (basta con el paquete «ODBC»
de Instant Client). Instálelo en la máquina que ejecuta el backend de *digna*, siguiendo la guía
de instalación oficial del proveedor.

El controlador se registra como **Oracle in `<OracleHomeName>`**, por ejemplo
`Oracle in OraDB21Home1` o `Oracle in instantclient_21_13`. El nombre del home varía según la
instalación, así que consulte el nombre exacto en su host como se describe en
[Instalar el controlador ODBC en el host de digna](overview.md#install-the-driver).

---

## 2. Propiedades ODBC {: #2-odbc-properties }

!!! important "Un ejemplo, no una especificación"

    El conjunto siguiente es una combinación que se sabe que funciona. Las propiedades
    pertenecen al controlador ODBC de Oracle, por lo que sus nombres, valores predeterminados y
    valores aceptados difieren entre versiones del cliente, y el nombre del controlador en
    particular depende del home de Oracle de su host. Tómelo como punto de partida y consulte la
    documentación de la versión del cliente que haya instalado.

Añada las siguientes propiedades en la pantalla **Add DB Connection**:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Debe coincidir con el nombre del controlador registrado en el host de *digna* |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | La base a la que conectarse; véase más abajo |
| `UID` | `DIGNA_SOURCE_USER` | Usuario de la base de datos |
| `PWD` | `<password>` | Marque **Encrypted** |

La cadena de conexión resultante tiene este aspecto:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### El valor de `DBQ`

`DBQ` admite tres formas. Son equivalentes para *digna*; se diferencian en lo que hay que
configurar en el host de *digna*:

| Forma | Ejemplo | Requiere |
|---|---|---|
| **Descriptor de conexión completo** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Nada: todo está en la propiedad. Recomendado |
| **Alias TNS** | `DIGNA_SOURCE` | El alias debe existir en el `tnsnames.ora` del cliente de Oracle del host de *digna* |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Un cliente de Oracle que admita Easy Connect (12c y posteriores) |

!!! tip "Prefiera el descriptor completo"

    Un alias TNS traslada la mitad de la definición de la conexión a un archivo del host de
    *digna*, donde es fácil olvidarlo cuando se reconstruye el host o se traslada *digna*. El
    descriptor completo mantiene la conexión autocontenida, que es justamente el sentido de una
    instalación sin DSN.

Tenga en cuenta que los paréntesis de un descriptor no causan problemas dentro de una cadena de
conexión, pero si su contraseña contiene `;`, enciérrela entre llaves: `PWD={p@ss;word}`.

---

## 3. Configuración de *digna* {: #3-digna-configuration }

En la pantalla **Add DB Connection**, indique lo siguiente:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Notas sobre Oracle {: #4-notes-on-oracle }

- **Los esquemas son usuarios.** *digna* lista los usuarios de Oracle como esquemas, así que el
  esquema de origen es el propietario de las tablas: `DIGNA_SOURCE_USER` en el ejemplo anterior.
  El usuario de la conexión necesita `SELECT` sobre esas tablas, directamente o mediante un rol.
- **Una conexión ve una base de datos.** El catálogo que ofrece *digna* es la base a la que está
  asociada la conexión, así que `DBQ` decide qué servicio, y por tanto qué base, se perfila.
- **Los identificadores distinguen mayúsculas una vez entrecomillados.** *digna* entrecomilla
  los nombres que lee del diccionario de datos, que es lo que almacena Oracle: mayúsculas para
  los objetos no entrecomillados.
- **Modos de perfilado.** *Permanent* crea las tablas de trabajo en **Work Schema**, por lo que
  el usuario necesita `CREATE TABLE` allí y una cuota en el tablespace. *Session* usa una tabla
  temporal privada (`ORA$PTT_…`, Oracle 18c y posteriores) y no toca **Work Schema**. *Standard*
  solo necesita acceso de lectura.

---

## 5. Verificar el controlador (opcional) {: #5-verifying-the-driver-optional }

Configurar un origen de datos ODBC no es necesario para una conexión sin DSN, pero el diálogo
propio del controlador es una forma cómoda de confirmar que el cliente de Oracle, el nombre del
servicio y sus credenciales funcionan antes de introducirlos en *digna*.

#### Paso 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

El **TNS Service Name** que se ofrece aquí procede del `tnsnames.ora` de su instalación cliente
de Oracle: ahí es donde se define el alias y, con él, el host, el puerto y el nombre del
servicio. En *digna* puede usar el alias como `DBQ`, o bien el descriptor completo.

#### Paso 2 – Probar la conexión

Haga clic en el botón **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Indique la contraseña y haga clic en el botón **OK**.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

Un mensaje de éxito confirma que el controlador y las credenciales funcionan.