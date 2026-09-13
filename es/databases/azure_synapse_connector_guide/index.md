# Conector de origen para Azure Synapse Analytics

Esta guía describe cómo configurar *digna* para conectarse a Azure Synapse Analytics mediante
**ODBC**, usando una cadena de conexión **sin DSN**. Se admiten tanto los grupos SQL serverless
como los dedicados.

La parte de digna de la configuración es la misma para todas las tecnologías: dónde se crean las
conexiones, cómo se cifran los valores de las propiedades, cómo se prueba una conexión y qué
significan los modos de perfilado. Se describe en
[Descripción general de las conexiones de base de datos](overview.md). Esta página cubre lo
específico de Azure Synapse.

!!! note "Tecnología"

    Synapse habla el dialecto de SQL Server, así que la conexión se crea con **Technology:
    SQL Server**. Para un servidor local, véase [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. Instalar el controlador ODBC {: #1-install-the-odbc-driver }

Instale **ODBC Driver 18 for SQL Server** en la máquina que ejecuta el backend de *digna*,
siguiendo [la guía de instalación de Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
y consulte el nombre exacto del controlador registrado en su host como se describe en
[Instalar el controlador ODBC en el host de digna](overview.md#install-the-driver).

---

## 2. Propiedades ODBC {: #2-odbc-properties }

!!! important "Un ejemplo, no una especificación"

    El conjunto siguiente es una combinación que se sabe que funciona. Las propiedades
    pertenecen al controlador ODBC de Microsoft, por lo que sus nombres, valores predeterminados
    y valores aceptados difieren entre versiones del controlador y plataformas, y lo que exige
    el área de trabajo depende de cómo esté configurada: tipo de grupo, método de autenticación,
    firewall. Tómelo como punto de partida y consulte la documentación de la versión del
    controlador que haya instalado.

Añada las siguientes propiedades en la pantalla **Add DB Connection**:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Debe coincidir con el nombre del controlador registrado en el host de *digna* |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Nombre del área de trabajo más el sufijo del punto de conexión; véase más abajo |
| `DATABASE` | `dignadata` | Base de datos que contiene los esquemas de origen. Es la única base que esta conexión puede perfilar |
| `UID` | `sqladminuser` | Inicio de sesión SQL |
| `PWD` | `<password>` | Marque **Encrypted** |

La cadena de conexión resultante tiene este aspecto:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### El valor de `SERVER`

Tome el nombre del área de trabajo de Synapse y añádale el sufijo del punto de conexión:

| Grupo | `SERVER` |
|---|---|
| **Grupo SQL serverless** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Grupo SQL dedicado** | `<workspace>.sql.azuresynapse.net` |

!!! warning "La parte `-ondemand` se pasa por alto con facilidad"

    Sin ella, el nombre se resuelve al punto de conexión dedicado, y la conexión falla o alcanza
    en silencio un grupo distinto del previsto. Ambos puntos de conexión se muestran en la
    página de información general del área de trabajo en el portal de Azure.

### Firewall

El firewall del área de trabajo de Synapse debe permitir la dirección saliente del host de
*digna*. Añádala en **Networking** dentro del área de trabajo antes de probar la conexión: una
dirección bloqueada se manifiesta como un tiempo de espera agotado y no como un error de
autenticación.

### Autenticación con Microsoft Entra ID

En lugar de un inicio de sesión SQL, el controlador puede autenticarse contra Entra ID.
Sustituya `UID`/`PWD` por el método de autenticación que espera su área de trabajo, por ejemplo:

| Clave | Valor de ejemplo | Notas |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` toma entonces el id. de aplicación (cliente) y `PWD` el secreto de cliente |
| `Authentication` | `ActiveDirectoryMSI` | Identidad administrada del host de *digna*, sin credenciales |

---

## 3. Configuración de *digna* {: #3-digna-configuration }

En la pantalla **Add DB Connection**, indique lo siguiente:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Notas sobre Azure Synapse {: #4-notes-on-azure-synapse }

- **Los grupos serverless solo admiten el perfilado *Standard*.** Un grupo SQL serverless no
  puede crear tablas en una base de datos, así que no pueden ejecutarse ni el perfilado
  *Permanent* ni el *Session*. *Standard* calcula las métricas directamente sobre el origen, que
  además es la opción más económica, ya que serverless se factura por datos procesados.
- **Una conexión ve una base de datos.** *digna* ofrece los esquemas de la base nombrada en
  `DATABASE`, porque Synapse, como SQL Server, solo informa de la base actual como catálogo.
- **El cifrado está activado de forma predeterminada** en Driver 18 y los puntos de conexión de
  Synapse presentan certificados públicos válidos, así que no hace falta ninguna propiedad
  `Encrypt` ni `TrustServerCertificate`.
- **Un punto de conexión serverless puede reanudarse desde la inactividad** en la primera
  conexión. Si la prueba de conexión agota el tiempo de espera en un grupo que lleva un rato sin
  usarse, vuelva a intentarlo.

---

## 5. Verificar el controlador (opcional) {: #5-verifying-the-driver-optional }

Configurar un origen de datos ODBC no es necesario para una conexión sin DSN, pero el asistente
propio del controlador es una forma cómoda de confirmar que el controlador funciona y que el
área de trabajo acepta sus credenciales antes de introducirlas en *digna*.

#### Paso 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Rellene el campo «Server».
Use el nombre del área de trabajo de Synapse y amplíelo con «.sql.azuresynapse.net».  
**Atención**: si quiere conectarse mediante un grupo SQL serverless, asegúrese de incluir
«-ondemand» como se muestra en la captura de pantalla anterior.

Haga clic en el botón **Next >**.

#### Paso 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Elija el método de autenticación (p. ej. nombre de usuario y contraseña)
e indique los datos necesarios.

Haga clic en el botón **Next >**.

#### Paso 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Elija los ajustes conformes a ANSI y haga clic en el botón **Next >**.

#### Paso 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Puede dejar los ajustes predeterminados o elegir opciones según sus necesidades
y hacer clic en el botón **Finish**.

#### Paso 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Haga clic ahora en el botón **Test datasource**.

#### Paso 6
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

Una pantalla de éxito confirma que el controlador, el punto de conexión y las credenciales
funcionan. Los valores que ha introducido son exactamente los que toman las propiedades de la
[sección 2](#2-odbc-properties).