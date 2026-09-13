# Descripción general de las conexiones de base de datos

---

## Índice

1. [Cómo funcionan las conexiones](#how-connections-work)
2. [Guías por tecnología](#technology-guides)
3. [Requisito previo: instalar el controlador ODBC en el host de digna](#install-the-driver)
4. [Crear una conexión de base de datos](#create-a-database-connection)
5. [Propiedades ODBC](#odbc-properties)
6. [Cifrar los valores de las propiedades](#encrypting-property-values)
7. [Probar una conexión](#testing-a-connection)
8. [Qué base de datos ve la conexión](#which-database-the-connection-sees)
9. [Modo de perfilado y Work Schema](#profiling-mode-and-work-schema)
10. [Usar un DSN en su lugar](#using-a-dsn-instead)
11. [Resolución de problemas](#troubleshooting)

---

## Cómo funcionan las conexiones {: #how-connections-work }

*digna* llega a cada tecnología de origen mediante **ODBC**. Una conexión es una lista de
propiedades ODBC que usted introduce como pares clave/valor. Cuando *digna* abre la conexión,
une esos pares en una cadena de conexión —`Key=Value`, separados por `;`, en el orden en que los
haya listado— y se la entrega al administrador de controladores ODBC del host de *digna*.

Introducir usted mismo las propiedades es lo que hace que la configuración sea **sin DSN**: la
conexión lleva todo lo que el controlador necesita, de modo que no hay que registrar ningún
origen de datos ODBC (DSN) en el host. Es la forma recomendada de configurar *digna*, porque la
definición de la conexión reside por completo en *digna* y se traslada con él.

### Por qué ODBC {: #why-odbc }

Las versiones anteriores ofrecían la opción entre un controlador por tecnología y ODBC,
seleccionada con un conmutador **Use ODBC**. A partir de la versión 2026.06, *digna* se apoya
únicamente en ODBC. Una interfaz única y estándar aporta más que un conjunto de controladores a
medida:

- **Autenticación**: la autenticación forma parte de ODBC, así que una conexión puede usar todo
  lo que admita su controlador: contraseñas, tokens y PAT, Kerberos y Active Directory, MFA e
  inicio de sesión único desde el navegador, identidades en la nube, certificados de cliente y
  TLS. Los métodos nuevos llegan con una actualización del controlador, en lugar de esperar a
  una versión de *digna*.
- **Controladores mantenidos por los fabricantes de bases de datos**: el controlador del propio
  fabricante sigue las nuevas versiones del servidor y las correcciones de seguridad, y puede
  actualizarlo según su propio calendario, con independencia de *digna*.
- **Una única forma de configurarlo todo**: cada tecnología es una lista de propiedades
  clave/valor, con la misma interfaz, el mismo cifrado de valores sensibles y la misma
  resolución de problemas, en lugar de un conjunto de campos distinto por origen.
- **Ajuste y alcance**: las opciones del controlador, como tiempos de espera, configuración TLS,
  proxies y tamaños de lectura, están disponibles para todos los orígenes, y puede conectarse
  cualquier tecnología con un controlador ODBC conforme, incluidas aquellas para las que *digna*
  no publica una guía específica.

!!! note "Qué ha cambiado en la interfaz"

    El conmutador **Use ODBC** y los campos separados de host, puerto, base de datos, usuario y
    contraseña ya no existen. Una conexión que no use ya ODBC necesita que se introduzcan sus
    propiedades ODBC antes de volver a funcionar; véase
    [Crear una conexión de base de datos](#create-a-database-connection).

---

## Guías por tecnología {: #technology-guides }

Los nombres de las propiedades difieren según el controlador, y cada tecnología tiene uno o dos
detalles que las demás no tienen. Las guías siguientes cubren esa parte; esta página cubre el
lado de *digna*, que es el mismo para todas.

!!! important "Los conjuntos de propiedades de las guías son ejemplos"

    Cada guía muestra una combinación que se sabe que funciona: aquella frente a la que se
    prueba *digna*. Es un punto de partida, no una especificación: las propiedades pertenecen al
    controlador ODBC, y cuáles existen, cómo se llaman y qué valores aceptan difiere entre
    versiones y fabricantes de controladores, entre Windows, Linux y macOS, y según cómo esté
    configurado el servidor de origen: método de autenticación, TLS, pasarela, puerto. Cuente
    con ajustar algún valor, y considere autoritativa la documentación de la versión del
    controlador que haya instalado.

| Tecnología | Guía | Conviene saber |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Los grupos serverless necesitan `-ondemand` en el nombre de host y solo admiten el perfilado *Standard* |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Autenticación por token: `UID=token`, PAT en `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Los catálogos vienen del controlador, no de una consulta |
| **Netezza** | [Netezza](netezza_connector_guide.md) | El nombre del controlador va entre llaves: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` admite un descriptor de conexión completo o un alias de `tnsnames.ora` |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` debe coincidir con lo que exige el servidor |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` decide qué esquemas puede ver *digna* |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | El token de acceso programático es la vía de autenticación probada |
| **Teradata** | [Teradata](teradata_connector_guide.md) | El host va en `DBCNAME`; las bases actúan como esquemas |

---

## Requisito previo: instalar el controlador ODBC en el host de digna {: #install-the-driver }

*digna* abre las conexiones de origen desde el **servidor que ejecuta el backend de digna**, no
desde el navegador. El controlador ODBC debe estar instalado, por tanto, en esa máquina, y su
nombre registrado en el administrador de controladores local.

=== "Windows"

    Instale el controlador de 64 bits del proveedor, abra después el **Administrador de orígenes
    de datos ODBC (64 bits)** y vaya a la pestaña **Drivers**. Los nombres que aparecen ahí son
    exactamente los valores que puede usar para la propiedad `Driver`.

=== "Linux"

    Instale **unixODBC** y el controlador del proveedor, y liste después los nombres de
    controlador registrados:

    ```bash
    odbcinst -q -d
    ```

    Los nombres impresos entre corchetes son los valores que puede usar para la propiedad
    `Driver`. Proceden de `/etc/odbcinst.ini` (o del archivo que indique `odbcinst -j`).

=== "macOS"

    Instale **unixODBC** (por ejemplo con `brew install unixodbc`) y el controlador del
    proveedor, y liste después los nombres de controlador registrados:

    ```bash
    odbcinst -q -d
    ```

!!! warning "El nombre del controlador debe coincidir carácter por carácter"

    `Driver` se pasa sin modificar al administrador de controladores. `Simba Spark ODBC Driver` y
    `Simba Spark ODBC Driver 64` son controladores distintos para el administrador, y un nombre
    no registrado produce un error *data source name not found* aunque no intervenga ningún DSN.

En lugar de un nombre registrado, todos los administradores de controladores habituales aceptan
también la ruta completa a la biblioteca del controlador, por ejemplo
`Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Resulta útil cuando el controlador está
instalado pero no registrado.

---

## Crear una conexión de base de datos {: #create-a-database-connection }

Abra el **Admin Panel**, vaya a la pestaña **Database Connections** y haga clic en
**Add DB Connection**. La pantalla pide cinco cosas:

| Campo | Descripción |
|---|---|
| **Name** | Nombre de la conexión. Se usa para referenciar la conexión en otras pantallas. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake o Hive. Selecciona el dialecto SQL que genera *digna*, así que debe coincidir con el origen, no con el controlador. Azure Synapse Analytics es una conexión de **SQL Server**. |
| **ODBC Properties** | Los pares clave/valor descritos en [Propiedades ODBC](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* o *Session*; véase [Modo de perfilado y Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Esquema que contiene las tablas de trabajo del perfilado *Permanent*. |

Una conexión se administra de forma centralizada y luego se asigna a uno o varios proyectos, de
modo que la misma conexión puede dar servicio a varios proyectos.

---

## Propiedades ODBC {: #odbc-properties }

Haga clic en **Add Property** para cada propiedad y rellene **Key**, **Value** y, en el caso de
los secretos, la casilla **Encrypted**. Cada guía de tecnología lista un conjunto de ejemplo
para esa tecnología, que usted adapta a su versión de controlador y a su servidor; véase
[la nota anterior](#technology-guides).

Sea cual sea el controlador, un conjunto de propiedades cubre las mismas cuatro cosas:

- **`Driver`**: el nombre del controlador registrado, como se describe
  [más arriba](#install-the-driver).
- **La dirección del servidor**: la clave difiere según el controlador: `SERVER`, `HOST`,
  `DBCNAME`, `Server` o, en el caso de Oracle, el descriptor de conexión `DBQ`.
- **Las credenciales**: normalmente `UID` y `PWD`; Snowflake usa `UID` más un `token`, y
  Databricks el usuario literal `token` más el token de acceso personal en `PWD`.
- **La base de datos o el catálogo en el que trabajar**, cuando la tecnología lo tiene; véase
  [Qué base de datos ve la conexión](#which-database-the-connection-sees).

Cualquier otra cosa que documente el controlador puede añadirse de la misma manera: agrupación
de conexiones, tiempos de espera de socket, ajustes de Kerberos, ajustes de proxy. *digna* no
interpreta las propiedades; solo las transmite.

!!! warning "Los valores no se escapan: encierre entre llaves todo lo que lleve punto y coma"

    Como las propiedades se unen con `;`, un valor que contenga a su vez `;` dividiría la cadena
    de conexión en el lugar equivocado. Encierre esos valores entre llaves: `PWD={p@ss;word}`.
    Lo mismo vale para valores con `=` o con espacios iniciales. Por eso, además, algunos
    controladores se escriben por convención entre llaves, como `{NetezzaSQL}` o
    `{SnowflakeDSIIDriver}`.

---

## Cifrar los valores de las propiedades {: #encrypting-property-values }

Marque **Encrypted** en cada propiedad que contenga un secreto: `PWD`, `token`, un secreto de
cliente. El valor se cifra entonces antes de almacenarse en el repositorio de *digna*, se
enmascara en la pantalla y solo se descifra al ensamblar la cadena de conexión.

!!! tip "Consejo"

    Un valor cifrado no puede leerse de vuelta, ni en la interfaz ni a través de la API: solo
    puede sustituirse. Guarde también los secretos en su propio gestor de contraseñas.

Las propiedades que no son secretas —nombre del controlador, host, puerto, base de datos— es
mejor dejarlas sin cifrar, para que sigan siendo legibles para quien mantenga la conexión más
adelante.

---

## Probar una conexión {: #testing-a-connection }

Haga clic en **Test** en el diálogo *Add DB Connection* **antes** de guardar. La prueba usa los
valores que hay en ese momento en el formulario y realiza una conexión real, así que informa
exactamente de lo que encontraría una inspección: un nombre de controlador erróneo, una
contraseña rechazada, un host inaccesible. No se almacena nada: la conexión de prueba se revierte
tanto si tiene éxito como si falla.

Para una conexión que ya existe, sitúe el cursor sobre su fila en la pestaña
**Database Connections** y haga clic en el icono del **enchufe** para volver a probarla. Es la
forma más rápida de comprobar si un origen es accesible tras una rotación de contraseña o un
cambio en el firewall.

---

## Qué base de datos ve la conexión {: #which-database-the-connection-sees }

Cuando añade un origen de datos, *digna* ofrece los catálogos, esquemas y tablas que la conexión
puede alcanzar. Hasta dónde llega depende de la tecnología:

| Tecnología | Catálogos ofrecidos |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Solo la base **actual** de la conexión |
| **Teradata**, **Netezza**, **Databricks** | Todas las bases o catálogos que el usuario tiene permitido ver |
| **Hive**, **Impala** | Los que informa el controlador |

!!! important "Una conexión, una base de datos"

    Para PostgreSQL, SQL Server, Oracle y Snowflake, las propiedades deben apuntar a la base que
    contiene los esquemas de origen: `DATABASE=…`, `Database=…`, o el nombre del servicio dentro
    del `DBQ` de Oracle. Las tablas de otra base no son accesibles a través de esa conexión;
    añada una segunda conexión para ello.

---

## Modo de perfilado y Work Schema {: #profiling-mode-and-work-schema }

El modo de perfilado determina cómo procesa *digna* los datos y calcula las métricas:

- **Standard:** las métricas se calculan directamente sobre las tablas de origen, sin copiar los
  datos.
- **Permanent:** los datos del día inspeccionado se copian en una tabla permanente y las
  métricas se calculan sobre los datos copiados.
- **Session:** los datos se copian en una tabla de sesión o temporal y las métricas se calculan
  sobre esos datos temporales.

El modo decide qué debe estar permitido al usuario de la conexión:

| Modo | Escribe | Derechos que necesita el usuario de la conexión |
|---|---|---|
| **Standard** | nada | Lectura sobre las tablas de origen |
| **Permanent** | una tabla por origen de datos en **Work Schema** | Crear y eliminar tablas en **Work Schema** |
| **Session** | una tabla temporal que la base elimina con la sesión | Crear tablas temporales; **Work Schema** no se usa |

*Standard* solo lee, lo que lo convierte en el modo que hay que elegir cuando *digna* dispone de
acceso de solo lectura. **Work Schema** solo se lee para *Permanent*, pero conviene rellenarlo
de todos modos para que la conexión siga funcionando si el modo se cambia más adelante.

---

## Usar un DSN en su lugar {: #using-a-dsn-instead }

Un DSN sigue funcionando: `DSN` no es más que otra propiedad:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

El DSN debe estar registrado en el host de *digna*, para la misma cuenta de usuario que ejecuta
el backend de *digna*, y como **System DSN** cuando *digna* se ejecuta como servicio. Todo lo
que esté configurado en el DSN puede anularse añadiéndolo también como propiedad.

El modo sin DSN es el valor predeterminado documentado porque evita ese estado en el host: la
conexión queda descrita por completo en *digna*, y un host de *digna* nuevo necesita el
controlador instalado, pero nada configurado.

---

## Resolución de problemas {: #troubleshooting }

### No se encuentra el nombre del origen de datos / no se especificó un controlador predeterminado

**Síntomas:**
- El botón **Test** informa de un error que menciona *data source name not found*, aunque la
  configuración sea sin DSN

**Causas y soluciones:**
1. El valor de `Driver` no coincide con ningún nombre de controlador registrado: compárelo con
   la pestaña **Drivers** del *Administrador de orígenes de datos ODBC (64 bits)*, o con
   `odbcinst -q -d`
2. El controlador está instalado en su estación de trabajo pero no en el host de *digna*
3. El controlador es de 32 bits mientras que *digna* es de 64 bits: instale el controlador de
   64 bits
4. La propiedad `Driver` falta por completo, y tampoco se indicó ningún `DSN`
5. En Linux y macOS, el controlador está instalado pero no registrado: indique en su lugar la
   ruta completa a la biblioteca del controlador, o regístrelo en `odbcinst.ini`

---

### La prueba de conexión agota el tiempo de espera

**Síntomas:**
- **Test** se queda bloqueado y falla al cabo de aproximadamente medio minuto

**Causas y soluciones:**
1. El host o el puerto son inaccesibles desde el host de *digna*: revise el firewall y, en el
   caso de orígenes en la nube, la lista de direcciones IP permitidas
2. El nombre de host es correcto, pero el puerto pertenece a otro servicio
3. El origen necesita más de los 30 segundos predeterminados para aceptar una conexión: suba
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` en la sección `[base]` de `config.toml` (`0` espera
   indefinidamente) y reinicie el backend
4. Un punto de conexión serverless se está reanudando desde la inactividad: reinténtelo y, si
   ocurre de forma habitual, suba el tiempo de espera de inicio de sesión como se indica arriba

---

### La autenticación falla aunque las credenciales son correctas

**Síntomas:**
- El controlador informa de credenciales no válidas, pero el mismo usuario funciona en otro
  cliente SQL

**Causas y soluciones:**
1. La contraseña contiene `;`: encierre el valor entre llaves: `{p@ss;word}`
2. Se copió un espacio final dentro del valor
3. El controlador espera un mecanismo de autenticación concreto, por ejemplo `AuthMech` en los
   controladores de Hive y Databricks, o `authenticator` en Snowflake
4. El valor se almacenó cifrado y luego se editó: los valores cifrados no pueden leerse de
   vuelta, así que vuelva a introducir el secreto completo
5. Un token ha caducado: los tokens de acceso personal y los de acceso programático se emiten
   con fecha de caducidad

---

### La pantalla de origen de datos no ofrece la base o el esquema esperados

**Síntomas:**
- Faltan catálogos, esquemas o tablas al añadir un origen de datos

**Causas y soluciones:**
1. La conexión apunta a otra base: véase
   [Qué base de datos ve la conexión](#which-database-the-connection-sees)
2. El usuario de la conexión carece de derechos de lectura sobre el esquema o sobre el
   diccionario de datos
3. **Technology** no coincide con el origen, así que *digna* consulta el diccionario de datos
   equivocado
4. En Snowflake, no hay ningún almacén predeterminado asignado al usuario y no se indicó ninguna
   propiedad `Warehouse`, de modo que las consultas de metadatos no pueden ejecutarse

---

### El perfilado falla aunque la prueba de conexión tiene éxito

**Síntomas:**
- **Test** pasa, pero una inspección falla al crear las tablas de trabajo

**Causas y soluciones:**
1. Está seleccionado el perfilado *Permanent* y el usuario de la conexión no puede crear tablas
   en **Work Schema**: conceda los derechos o cambie a *Session* o *Standard*
2. **Work Schema** está vacío o nombra un esquema que no existe, mientras está seleccionado el
   perfilado *Permanent*
3. Está seleccionado el perfilado *Session* y el usuario de la conexión no puede crear tablas
   temporales
4. Una consulta de perfilado de larga duración alcanza el tiempo de espera de consulta: suba
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` en la sección `[base]` de `config.toml` (3600 segundos por
   defecto, `0` desactiva el tiempo de espera)

---

## Buenas prácticas

**HAGA:**

- Instalar y registrar el controlador en el host de *digna* antes de configurar la conexión
- Marcar **Encrypted** en cada contraseña y cada token
- Hacer clic en **Test** antes de guardar, y volver a probar tras una rotación de contraseña
- Nombrar las conexiones según el origen y el entorno, por ejemplo `sales_dwh_prod`
- Dar a *digna* un usuario de base de datos dedicado, de solo lectura cuando baste el perfilado
  *Standard*
- Mantener una conexión por base de datos de origen, y añadir una segunda en lugar de cambiar la
  primera

**NO HAGA:**

- Almacenar secretos sin cifrar, ni compartir un usuario de base de datos entre *digna* y otras
  herramientas
- Usar un controlador de 32 bits con una instalación de *digna* de 64 bits
- Confiar en un DSN de usuario cuando *digna* se ejecuta como servicio: no será visible
- Poner un valor que contenga `;` en una propiedad sin llaves
- Apuntar **Work Schema** a un esquema que contenga datos de origen

---

## Soporte

¿Necesita ayuda con una conexión de base de datos?

- **Correo electrónico:** support@digna.ai
- **Documentación:** https://docs.digna.ai
- **Sitio web:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**