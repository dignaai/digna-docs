---
title: Guía de instalación en Windows – digna Release 2026.11 | Documentación de digna
description: Guía paso a paso para instalar digna Release 2026.11 en Windows — requisitos del sistema, configuración de PostgreSQL, configuración del servidor web, configuración del backend y del panel, ejecución de digna como servicio de Windows y actualización desde la Release 2026.06.
keywords: instalación digna windows, guía de despliegue digna, configuración backend digna, instalación dashboard digna, configuración postgresql, servicio Windows digna, guía de actualización digna
image: /assets/logo_square.png
---

# Guía de instalación en Windows para digna Release 2026.11

**Release:** 2026.11

**Última actualización:** 7 de noviembre de 2026


---

## Tabla de contenidos

1. [Introducción](#introduction)
2. [Requisitos del sistema](#system-requirements)
3. [Preparativos previos a la instalación](#pre-installation-setup)
4. [Configuración del servidor PostgreSQL](#postgresql-server-setup)
5. [Configuración del servidor web](#web-server-configuration)
6. [Instalación inicial](#initial-installation)
7. [Configuración del backend](#backend-configuration)
8. [Configuración del panel (dashboard)](#dashboard-configuration)
9. [Ejecutar digna como servicio de Windows](#running-digna-as-a-windows-service)
10. [Actualizar a una nueva versión](#upgrading-to-a-new-release)

---

## Introducción {: #introduction }

### Acerca de digna

digna es una plataforma integral impulsada por IA diseñada para optimizar la gestión de la calidad de los datos en diversos entornos, como data warehouses, data lakes y lakehouses. Diseñada para ser altamente escalable y adaptable, digna aborda los desafíos modernos de datos mediante automatización, monitoreo en tiempo real y detección de anomalías.

digna consta de dos componentes principales:

- **digna**: el núcleo de la aplicación, responsable de procesar los datos y realizar las comprobaciones de calidad. Combina el backend y la interfaz de línea de comandos en un único ejecutable, sustituyendo a los programas separados `dignabackend` y `dignacli` de versiones anteriores.
- **dignadashboard**: Una interfaz web alojada en un servidor web, que ofrece una forma amigable de interactuar con la plataforma digna y visualizar las métricas de calidad de datos.

### Novedades en la Release 2026.11

Esta versión añade digna Data Reconciliation, digna Agentic con el digna MCP Server y el digna Engine, que puede perfilar datos dentro de digna y comprobar la integridad referencial entre distintas tecnologías de bases de datos. Consulta las [notas de la versión](../../../changelog/Release_202611.md) para obtener detalles completos.

Para una instalación, la versión trae un nuevo mecanismo de migración del repositorio, una sección `[duckdb]` opcional en `config.toml` para el digna Engine y un nuevo archivo de licencia. La [sección de actualización](#upgrading-to-a-new-release) trata cada uno de ellos.

### ¿Buscas macOS o Linux?

Esta guía cubre Windows. Para otras plataformas, consulta la [Guía de instalación para macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) o la [Guía de instalación para Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Requisitos del sistema {: #system-requirements }

Antes de comenzar la instalación, asegúrate de que tu sistema cumpla con los siguientes requisitos mínimos:

| Requisito | Especificación |
|---|---|
| **Sistema operativo** | Windows Server o Windows 10/11 |
| **Memoria (instalación mínima)** | 16 GB RAM |
| **Espacio en disco** | 10 GB de almacenamiento disponible |
| **Base de datos** | PostgreSQL Server 12 o superior |
| **Servidor web** | IIS, Apache Tomcat, o equivalente |

!!! info "digna Engine"

    Las conexiones de base de datos que usan el digna Engine como ubicación de perfilado se perfilan en el
    propio host de digna. Prevé memoria y espacio en disco adicionales para ellas; consulta la
    [sección \[duckdb\]](#duckdb-section).

### Opciones de instalación de la base de datos

**Si PostgreSQL ya está instalado:**
Puedes añadir una nueva base de datos para digna en tu servidor PostgreSQL existente.

**Si vas a instalar PostgreSQL en la misma máquina que digna:**

!!! info "Especificaciones recomendadas"

    - **Memoria**: 32 GB RAM (en lugar de 16 GB)
    - **Espacio en disco**: 50 GB de almacenamiento disponible (en lugar de 10 GB)

    Estas especificaciones superiores acomodan tanto digna como la base de datos PostgreSQL ejecutándose simultáneamente.

---

## Preparativos previos a la instalación {: #pre-installation-setup }

Antes de instalar digna, asegúrate de que dos prerrequisitos clave estén en su lugar:

1. **Servidor PostgreSQL** – para almacenar métricas calculadas y datos de rendimiento
2. **Servidor web** – para alojar el digna Dashboard

Si estos componentes aún no están configurados, sigue las secciones siguientes para instalarlos y configurarlos.

---

## Configuración del servidor PostgreSQL {: #postgresql-server-setup }

### Si ya tienes PostgreSQL

Si PostgreSQL ya está instalado y en funcionamiento en tu máquina local o si estás utilizando un servidor PostgreSQL gestionado de forma remota, puedes saltar a la [siguiente sección](#web-server-configuration).

### Instalación de PostgreSQL

Sigue estos pasos para instalar PostgreSQL en Windows:

#### Paso 1: Descargar PostgreSQL

1. Visita la [página de descargas de PostgreSQL](https://www.postgresql.org/download/)
2. Selecciona **Windows**
3. Descarga el instalador más reciente

#### Paso 2: Ejecutar el instalador

1. Haz doble clic en el archivo del instalador descargado
2. Sigue las indicaciones del asistente de instalación

#### Paso 3: Elegir el directorio de instalación

Selecciona el directorio donde se instalará PostgreSQL. La ubicación predeterminada suele ser adecuada.

#### Paso 4: Seleccionar componentes

Para una configuración estándar, mantiene las opciones de componentes predeterminadas seleccionadas.

#### Paso 5: Establecer la contraseña del superusuario de PostgreSQL

Introduce y confirma una contraseña para el superusuario de PostgreSQL (`postgres`). **Guarda esta contraseña de forma segura** — la necesitarás más adelante.

#### Paso 6: Configurar el número de puerto

El puerto predeterminado de PostgreSQL es `5432`. Puedes usar el predeterminado o especificar otro puerto si es necesario.

!!! tip "Consejo"

    Si el puerto 5432 ya está en uso, elige un puerto alternativo y anótalo para la configuración posterior.

#### Paso 7: Elegir la configuración regional (locale)

Selecciona la configuración regional para tu base de datos. La opción predeterminada suele ser adecuada para la mayoría de las instalaciones.

#### Paso 8: Completar la instalación

Haz clic en **Next** en los pasos restantes y luego en **Finish**.

#### Paso 9: Verificar la instalación

Abre el Símbolo del sistema y verifica que PostgreSQL esté instalado:

```bash
psql --version
```

Deberías ver la versión de PostgreSQL si la instalación fue exitosa.

---

## Configuración del servidor web {: #web-server-configuration }

digna requiere un servidor web para alojar el dashboard. Elige una de las siguientes opciones:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Solo necesitas instalar y configurar **uno** de estos servidores.

### Configuración de IIS {: #iis-setup }

#### Descripción general

Internet Information Services (IIS) es el servidor web de Microsoft para alojar sitios web y aplicaciones web.

#### Habilitar IIS

1. **Abrir el Panel de control**
   - Presiona `Win + R`
   - Escribe `control` y presiona Enter

2. **Ir a Funciones de Windows**
   - Haz clic en **Programs**
   - Selecciona **Turn Windows features on or off**

3. **Habilitar Internet Information Services**
   - Desplázate y busca **Internet Information Services (IIS)**
   - Marca la casilla para habilitarlo
   - Haz clic en el **+** para expandir y verifica que estos subcomponentes estén seleccionados:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Haz clic en OK** para aplicar los cambios

5. **Verificar la instalación de IIS**
   - Abre tu navegador
   - Navega a `http://localhost`
   - Deberías ver la página de bienvenida de IIS

#### Requerido: módulo URL Rewrite

IIS requiere el componente URL Rewrite. Descárgalo e instálalo desde la [página oficial de Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Requerido: tipo MIME para archivos Markdown

Para asegurar que los archivos Markdown (`.md`) se sirvan correctamente en IIS:

1. Abre **IIS Manager** (presiona `Win + R`, escribe `inetmgr`, presiona Enter)
2. Navega a **Your Site > MIME Types**
3. Haz clic en **Add...**
4. Configura:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Importante"

    Sin esta configuración, los archivos `.md` podrían no servirse correctamente.

---

### Configuración de Apache Tomcat {: #apache-tomcat-setup }

#### Descripción general

Apache Tomcat es un contenedor de servlets Java y servidor web de código abierto.

#### Instalación

1. **Descargar Apache Tomcat**
   - Visita [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Descarga la distribución ZIP para Windows

2. **Extraer el archivo**
   - Extrae el archivo ZIP en un directorio de tu sistema
   - Ejemplo: `C:\Program Files\Apache Tomcat`

3. **Verificar que Tomcat esté en ejecución**
   - Abre tu navegador
   - Navega a `http://localhost:8080`
   - Deberías ver la página de bienvenida de Apache Tomcat

!!! tip "Consejo"

    Apache Tomcat normalmente se inicia automáticamente después de la instalación. Si no lo hace, navega a la carpeta `bin` y ejecuta `startup.bat`.

---

## Instalación inicial {: #initial-installation }

### Paso 1: Configurar el repositorio de digna

El repositorio de digna almacena todas las métricas calculadas por digna. Actúa como la base de datos central para datos analíticos y de rendimiento.

#### Crear esquema y usuario del repositorio

Abre tu cliente de PostgreSQL (pgAdmin, psql u otro) y ejecuta los siguientes comandos SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Reemplaza los siguientes marcadores:**

- `<digna_repo_schema>` — El nombre de esquema que desees (p. ej., `dignarepo`)
- `<digna_repo_user>` — El nombre de usuario que desees (p. ej., `digna_user`)
- `<digna_repo_password>` — Una contraseña segura para este usuario

**Ejemplo:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Mejor práctica"

    Usa contraseñas fuertes y complejas para los usuarios de la base de datos. Evita credenciales fáciles de adivinar.

---

### Paso 2: Extraer el paquete de instalación de digna

1. Localiza el archivo ZIP de instalación de digna que se te proporcionó
2. Extrae el archivo en la ubicación de instalación deseada
3. Después de extraer, deberías ver los siguientes elementos:
   - `dashboard/` — Interfaz web del panel
   - `digna` — Ejecutable principal (backend + CLI combinados)

!!! info "Los archivos de configuración y de licencia no están en el paquete"

    Ni `config.toml` ni `dashboard/dashboard_config.toml` se incluyen en la instalación: los
    creas tú mismo, en [Configuración del backend](#backend-configuration) y
    [Configuración del panel (dashboard)](#dashboard-configuration). Tampoco se incluye `license.toml`;
    digna lo proporciona por separado, como se describe en el Paso 3.

### Paso 3: Instalar el archivo de licencia

!!! warning "Importante"

    El archivo de licencia **no** está incluido en el paquete de instalación y se entregará por separado por digna.

1. Localiza el archivo `license.toml` que se te proporcionó
2. Cópialo en el directorio raíz de instalación de digna (donde están `config.toml` y el ejecutable `digna`)

**Por qué esto importa:**
El archivo de licencia contiene la información del cliente, la fecha de expiración de la licencia y la firma digital. **No modifiques este archivo** — cualquier cambio lo invalidará.

**Estructura de directorios después de la configuración:**

```
digna_installation/
├── config.toml         (archivo de configuración)
├── license.toml        (TU ARCHIVO DE LICENCIA - cópialo aquí)
├── digna               (ejecutable principal)
└── dashboard/          (interfaz web)
    └── (archivos del dashboard)
```

---

## Configuración del backend {: #backend-configuration }

### Paso 1: Crear y editar el archivo de configuración

Se proporciona el archivo `config_template.toml` en tu directorio de instalación de digna. Solo necesitas renombrarlo a `config.toml`.

**Ubicación:** `digna_installation/config.toml`

Abre `config.toml` en un editor de texto y configura cada sección a continuación.

#### Sección [app]

Esta sección configura el intercambio de recursos entre orígenes (CORS) entre el dashboard y el backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parámetro | Valor | Notas |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URL del dashboard | Las URL desde las que se sirve el dashboard. Las solicitudes del navegador desde cualquier otro origen se rechazan |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Obligatorio, para que el navegador envíe la cookie de sesión con cada solicitud |

!!! info "La sección [app] es opcional"

    A partir de la Release 2026.11, ambas claves, y toda la sección `[app]`, pueden omitirse. Es la
    configuración adecuada cuando un proxy inverso sirve el dashboard y el backend bajo un mismo origen: el
    navegador no realiza entonces solicitudes entre orígenes, y por defecto no se permite ninguna.

#### Sección [repo]

Esta sección configura la conexión a la base de datos PostgreSQL:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| Parámetro | Valor | Notas |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` o IP | Hostname/IP del servidor PostgreSQL |
| `DIGNA_REPO_PORT` | `5432` (predeterminado) | Puerto de PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Nombre de la base de datos |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Esquema creado anteriormente |
| `DIGNA_REPO_USER` | `digna_user` | Usuario creado en la configuración de PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Tu contraseña | Contraseña establecida durante la creación del esquema |
| `DIGNA_REPO_SSLMODE` | `prefer` (por defecto) | Opcional. Modo SSL de PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` o `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (por defecto) | Opcional. Número de conexiones que digna mantiene abiertas con el repositorio |

#### Sección [base]

Esta sección contiene ajustes de seguridad, cookies e inspecciones:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| Parámetro | Valor | Notas |
|---|---|---|
| `DIGNA_FERNET_KEY` | Valor mostrado arriba | Clave del cifrado que usaban las versiones anteriores. Debe estar presente; conserva el valor mostrado |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Host bajo el que se accede al dashboard. `""` no establece ningún dominio, lo que es correcto detrás de un proxy que sirve el dashboard y el backend bajo un mismo origen |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Debe ser `true` siempre que digna se sirva por HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Mantiene la cookie de sesión fuera del alcance de los scripts |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 horas) | Tiempo de expiración de sesión en segundos |
| `DIGNA_MAX_WORKERS` | Número de núcleos de CPU - 1 | Número de inspecciones que pueden ejecutarse al mismo tiempo |
| `DIGNA_FRONTEND_BASEURL` | URL del dashboard | Obligatorio. Se usa para los enlaces de los mensajes de notificación, por lo que debe ser una URL que los destinatarios puedan abrir |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (por defecto) | Opcional. Segundos que puede ejecutarse una única consulta contra una base de datos de origen antes de interrumpirse; `0` desactiva el tiempo de espera |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (por defecto) | Opcional. Segundos de espera para establecer una conexión con una base de datos de origen; `0` espera indefinidamente |

#### Sección [encryption]

Esta sección contiene la clave utilizada para cifrar los valores sensibles almacenados en el repositorio. Es **obligatoria**: `config check` informa de la sección `[encryption]` como FAILED si falta la clave.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parámetro | Valor | Notas |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Clave codificada en Base64 | Cifra los valores sensibles almacenados en el repositorio de digna |

!!! warning "Proteja config.toml"

    Esta clave es un valor fijo, idéntico en todas las instalaciones de digna, y es la que descifra los valores sensibles de su repositorio. Restrinja `config.toml` a la cuenta que ejecuta digna, manténgalo fuera del control de versiones y de las unidades compartidas, y exclúyalo de cualquier copia de seguridad que se guarde con menos seguridad que el propio repositorio.

#### Sección [logging]

Esta sección configura el comportamiento del registro (logging):

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parámetro | Valor | Notas |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` o `DEBUG` | `INFO` para producción, `DEBUG` para depuración. También se aceptan `TRACE`, `WARN` y `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (por defecto) | Opcional. Directorio para los archivos de registro rotativos, relativo al directorio de trabajo |
| `DIGNA_LOGGING_MAX_FILES` | `30` (por defecto) | Opcional. Número de archivos de registro rotados que se conservan |

!!! warning "Conserva el directorio de registros al ejecutar digna como servicio"

    Un servicio de Windows no tiene consola, por lo que los archivos de registro son la única constancia de lo que hace el
    servicio. No establezcas `DIGNA_LOGGING_DIR` en una cadena vacía, ya que eso desactiva los archivos de registro.

#### Sección [duckdb] (opcional) {: #duckdb-section }

Novedad de la Release 2026.11. Esta sección define los recursos del **digna Engine**, que perfila
datos dentro de digna para las conexiones de base de datos cuya ubicación de perfilado es **digna Engine**, y
ejecuta comprobaciones de integridad referencial entre fuentes de datos de distintas conexiones de base de datos. Consulta
[Ubicación de perfilado](../../../platform/profiling/profiling_location.md).

La sección es opcional. Sin ella, se aplican los valores por defecto que se indican a continuación.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parámetro | Valor | Notas |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (por defecto) | Memoria, en MB, que puede usar una ejecución del digna Engine. Puede haber hasta `DIGNA_MAX_WORKERS` ejecuciones activas al mismo tiempo |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Por defecto: el directorio temporal de la cuenta que ejecuta digna (`%TEMP%`) | Directorio para archivos temporales cuando los datos no caben en memoria |

!!! tip "Dimensionar el digna Engine"

    Prevé hasta `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` de memoria en el host de
    digna, además de la que usa el propio digna, y suficiente espacio libre en disco en el directorio
    temporal para alojar la fecha inspeccionada más grande de las fuentes de datos que usan el digna Engine.
    Apunta `DIGNA_DUCKDB_TEMP_DIRECTORY` a un disco con ese espacio, en el que pueda escribir la cuenta que
    ejecuta digna:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Solo necesitas esta sección si al menos una conexión de base de datos usa el digna Engine, o si una
    comprobación de integridad referencial compara fuentes de datos de distintas conexiones.

---

### Paso 2: Validar la configuración

Antes de inicializar el repositorio, compruebe que `config.toml` está completo y bien formado. En su directorio de instalación de digna, ejecute:

```bash
digna config check
```

Cada sección se valida por separado, de modo que un único error no oculta el estado del resto:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Corrija todo lo que se informe como FAILED y vuelva a ejecutar el comando antes de continuar. Un WARNING en **Unknown keys** enumera las claves de `config.toml` que digna no lee; no tienen ningún efecto, así que elimínelas o corrija su ortografía. La lista completa de opciones está en la [referencia de la CLI](../../../cli/Command_Line_Interface_202611.md).

### Paso 3: Inicializar el repositorio

1. Abre el Símbolo del sistema
2. Navega al directorio de instalación de digna (donde están `config.toml` y el ejecutable `digna`)
3. Ejecuta la prueba de conexión:

```bash
digna repo check
```

En un esquema nuevo, el comando se conecta y después informa de que aún no hay ningún repositorio instalado:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

En este punto, ese es el resultado esperado: confirma que digna llega a PostgreSQL y al esquema. En cambio, un error de conexión o de autenticación apunta a la sección `[repo]` o a la configuración de PostgreSQL.

### Paso 4: Instalar el esquema del repositorio

En el mismo directorio, ejecuta:

```bash
digna repo upgrade
```

Este comando instala las tablas necesarias en el esquema del repositorio y termina con:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade instala y actualiza"

    A partir de la Release 2026.11, `repo upgrade` instala un repositorio nuevo y actualiza uno existente.
    `repo install` sigue funcionando como otro nombre del mismo comando.

### Paso 5: Crear un usuario administrador

1. Abre una ventana **nueva** del Símbolo del sistema
2. Navega al directorio de instalación de digna
3. Ejecuta el siguiente comando para crear un usuario administrador:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Ejemplo:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Esto crea un usuario con privilegios administrativos completos.

!!! tip "Mejor práctica"

    Usa una contraseña fuerte con mezcla de mayúsculas, minúsculas, números y caracteres especiales.

---

### Paso 6: Iniciar el servidor digna

En el directorio de instalación de digna, inicia el servidor con:

```bash
digna serve --address <host> --port <port>
```

**Parámetros:**
- `--address` — Nombre de host/IP del servidor (por defecto `127.0.0.1`)
- `--port` — Puerto del servidor (por defecto `8000`)

Cuando el servidor está en marcha, muestra la dirección en la que escucha:

```text
Server running on http://127.0.0.1:8082
```

!!! note "El servidor ocupa el terminal"

    `serve` se ejecuta en primer plano y sigue funcionando hasta que lo detenga con ++ctrl+c++. Déjelo en ejecución mientras termina la configuración; para iniciarlo automáticamente en el arranque, consulte [Ejecutar digna como servicio de Windows](#running-digna-as-a-windows-service).

## Configuración del panel (dashboard) {: #dashboard-configuration }

### Paso 1: Desplegar el dashboard en el servidor web

El dashboard de digna lee su propia configuración de `dashboard/dashboard_config.toml`. Ese archivo no se incluye en la instalación: lo creas en el directorio `dashboard/`, junto a los archivos del dashboard.

Su contenido se describe en [Inicio de sesión único](../../../sso/overview.md), que es también donde se necesita el archivo: contiene las opciones de inicio de sesión que ofrece el dashboard y, para despliegues multi-instancia, la conexión al backend.

Elige tu servidor web y sigue los pasos de despliegue correspondientes.

#### Despliegue en IIS

1. **Abrir IIS Manager**
   - Presiona `Win + R`, escribe `inetmgr`, presiona Enter

2. **Crear un nuevo sitio web**
   - En el panel izquierdo, clic derecho en **Sites**
   - Selecciona **Add Website...**

3. **Configurar el sitio**
   - **Site Name**: Introduce un nombre (p. ej., "dignaDashboard")
   - **Physical Path**: Haz clic en Browse y selecciona tu carpeta `dashboard`
   - **Binding**: Configura la dirección IP y el puerto (puerto 80 para HTTP, 443 para HTTPS por defecto)

4. **Iniciar el sitio**
   - Haz clic en **OK** para crear el sitio
   - Clic derecho en el nuevo sitio y selecciona **Start**

5. **Probar la instalación**
   - Abre tu navegador
   - Navega a `http://localhost` (o a la URL configurada)
   - Deberías ver la página de inicio de sesión del dashboard de digna

#### Despliegue en Apache Tomcat

1. **Copiar el dashboard a Tomcat**
   - Copia la carpeta `dashboard` a tu directorio `webapps` de Tomcat
   - Renómbrala si es necesario (p. ej., a `digna`)
   - Ejemplo: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verificar el despliegue**
   - Actualiza o recarga la página de administración de Tomcat (http://localhost:8080)
   - Deberías ver "digna" (o el nombre elegido) listado en las aplicaciones desplegadas

3. **Acceder al dashboard**
   - Abre tu navegador
   - Navega a `http://localhost:8080/digna`
   - Deberías ver la página de inicio de sesión del dashboard de digna

---

## Ejecutar digna como servicio de Windows {: #running-digna-as-a-windows-service }

### ¿Por qué usar un servicio de Windows?

Ejecutar el backend de digna como servicio de Windows asegura que:
- Se inicie automáticamente al arrancar el servidor
- Se ejecute en segundo plano sin necesidad de una ventana del Símbolo del sistema abierta
- Se reinicie automáticamente si se bloquea
- Se pueda gestionar a través de Servicios de Windows

### Los comandos `windows`

El servicio se gestiona con el propio ejecutable `digna`, mediante los subcomandos
`digna windows`. No hay archivos batch que ejecutar.

| Comando | Finalidad |
|---|---|
| `digna windows install` | Registra digna como servicio de Windows |
| `digna windows start` | Inicia el servicio registrado |
| `digna windows stop` | Detiene el servicio en ejecución |
| `digna windows uninstall` | Anula el registro del servicio |

!!! warning "Se requieren privilegios de Administrador"

    Los cuatro comandos deben ejecutarse desde un Símbolo del sistema abierto como Administrador.

Cada comando acepta `--name` para dirigirse a un servicio registrado con un nombre distinto del predeterminado. La lista
completa de opciones está en la [referencia de la CLI](../../../cli/Command_Line_Interface_202611.md).

### Instalar el servicio

1. **Abrir Símbolo del sistema como Administrador**
   - Clic derecho en Símbolo del sistema
   - Selecciona "Run as Administrator"

2. **Navegar a tu directorio de instalación de digna**
   ```bash
   cd C:\path\to\digna
   ```

3. **Registrar el servicio**
   ```bash
   digna windows install
   ```

!!! important "Indica la dirección y el puerto, salvo que te sirvan los valores predeterminados"

    `install` guarda la dirección y el puerto en el registro del servicio, y el servicio se enlaza
    exactamente a lo que se guardó. Los valores predeterminados son `127.0.0.1` y `8000`, que solo aceptan conexiones
    desde la propia máquina. Un dashboard en otro host no puede alcanzarlos, así que indica la
    dirección en la que debe escuchar el backend:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Estos valores no se leen de `config.toml`. Para cambiarlos más adelante, desinstala el servicio y
    vuelve a instalarlo con los nuevos valores.

El servicio se registra con inicio **automático**, por lo que se iniciará con Windows. No se
inicia inmediatamente — consulta la sección siguiente.

#### Opciones de instalación

| Opción | Valor predeterminado | Finalidad |
|---|---|---|
| `--name` | `digna` | Nombre con el que se registra el servicio |
| `--display-name` | `digna` | Nombre que se muestra en services.msc |
| `--description` | `digna data quality backend` | Descripción que se muestra en services.msc |
| `--address` | `127.0.0.1` | Dirección a la que el servicio enlaza su API |
| `--port` | `8000` | Puerto al que el servicio enlaza su API |
| `--working-dir` | el directorio del ejecutable `digna` | Directorio que contiene `config.toml` y `license.toml`, que el servicio convierte en su directorio de trabajo |
| `--start-type` | `auto` | `auto` se inicia con Windows, `manual` solo se inicia cuando se solicita, `disabled` registra el servicio pero se niega a iniciarlo |
| `--account` | `LocalSystem` | Cuenta con la que se ejecuta, p. ej. `DOMAIN\user` o `.\user` |
| `--password` | | Contraseña de `--account` |

!!! tip "Ejecución con una cuenta de dominio"

    `LocalSystem` no tiene identidad de red, por lo que la autenticación de Windows con SQL Server y cualquier
    acceso a un recurso compartido de red fallarán. Instala con `--account` y `--password` cuando el
    servicio necesite acceder a recursos como un usuario concreto.

### Iniciar y detener el servicio

#### Para iniciar el servicio

```bash
digna windows start
```

#### Para detener el servicio

```bash
digna windows stop
```

!!! tip "Consejo"

    Siempre detén el servicio antes de actualizar los archivos de la aplicación.

### Mover el servicio a un nuevo directorio

Si necesitas reubicar la instalación de digna:

1. **Detener el servicio actual y anular su registro**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Mover los archivos de la aplicación**
   - Mueve toda la carpeta de instalación de digna a la nueva ubicación

3. **Registrar de nuevo el servicio desde la nueva ubicación**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Repite los valores de `--address`, `--port` o `--account` que usaste la primera vez: el registro
   anterior ya no existe.

4. **Iniciar el servicio**
   ```bash
   digna windows start
   ```

### Desinstalar el servicio

1. **Detener el servicio en ejecución**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Anular el registro del servicio**
   ```bash
   digna windows uninstall
   ```

El servidor digna ahora está dado de baja como servicio de Windows.

---

## Actualizar a una nueva versión {: #upgrading-to-a-new-release }

Esta sección actualiza una instalación de la Release 2026.06 a la Release 2026.11.

!!! warning "Actualizar desde una release anterior a 2026.06"

    Realiza primero los pasos de actualización de la Release 2026.06: [Actualizar a una nueva versión](../Release%202026.06/installation_guide_digna_windows_2026_06.md#upgrading-to-a-new-release). Después, continúa con los pasos siguientes.

### Antes de actualizar

**Es obligatorio crear una copia de seguridad del repositorio de digna**

Antes de actualizar digna, realiza una copia de seguridad de tu repositorio (PostgreSQL) para protegerte contra pérdida de datos.
Una copia de seguridad asegura que puedas recuperar si la actualización encuentra problemas inesperados.

**Solicitar el archivo de licencia para la Release 2026.11**

La Release 2026.11 necesita un nuevo `license.toml`. Solicítalo al equipo de digna antes de empezar y
tenlo preparado para el [paso 7](#step-7-replace-the-license-file).

### Proceso de actualización

#### Paso 1: Detener el servicio digna {: #step-1-stop-the-digna-service }

Abre un Símbolo del sistema como administrador y detén el servicio con el ejecutable `digna` de
tu instalación actual:

```bash
cd C:\path\to\digna
digna windows stop
```

El servicio sigue registrado. El nuevo ejecutable ocupa el lugar del anterior en el mismo
directorio, por lo que el registro sigue apuntando al archivo correcto.

Si digna se está ejecutando en primer plano, pulsa ++ctrl+c++ en su ventana del Símbolo del sistema.

#### Paso 2: Respaldar la instalación actual {: #step-2-backup-current-installation }

En tu directorio de instalación de digna, cambia el nombre del ejecutable y de la carpeta del dashboard de tu
instalación actual, para que la nueva versión pueda desplegarse junto a ellos:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Conserva `digna_old.exe` hasta que hayas verificado la actualización, y `dashboard_old` hasta que hayas restaurado
desde ella tus archivos de configuración (consulta el paso 4). Después puedes eliminar ambos.

#### Paso 3: Extraer y desplegar la nueva versión {: #step-3-extract-and-deploy-new-version }

1. Extrae el nuevo archivo ZIP de instalación de digna
2. Copia el nuevo ejecutable `digna` y la carpeta `dashboard` a tu directorio de instalación


!!! warning "Importante"

    Ni `config.toml` ni `dashboard/dashboard_config.toml` se incluyen **nunca** en el
    ZIP de instalación: el equipo de digna no entrega ninguno de los dos archivos. Por tanto, la actualización no
    toca tu configuración existente, y las copias de las carpetas renombradas `*_old` son las
    únicas que tienes.

#### Paso 4: Restaurar tus archivos de configuración {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

La Release 2026.11 no requiere ningún cambio en `config.toml`: un archivo que funciona con la Release 2026.06
sigue funcionando. Hay dos cambios opcionales:

- Añade una [sección `[duckdb]`](#duckdb-section) si las conexiones de base de datos van a usar el digna Engine
  y sus valores por defecto no se ajustan a tu host.
- Omite la sección `[app]` si un proxy inverso sirve el dashboard y el backend bajo un mismo
  origen.

!!! warning "Ajustes que digna no lee"

    Versiones anteriores de esta guía mostraban algunos ajustes que digna no lee. No tienen ningún
    efecto, y `config check` los enumera en **Unknown keys** en el paso 6. Elimínalos o
    corrígelos:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` y
      `digna_LOGGING_BACKUP_COUNT` no existen. Elimínalos.
    - Los nombres de los ajustes distinguen entre mayúsculas y minúsculas. digna lee `DIGNA_REPO_HOST`, no
      `digna_REPO_HOST`. Escribe todos los nombres en mayúsculas, como en [Configuración del backend](#backend-configuration).

!!! warning "Inicio de sesión único: mantén [[oidc_clients]]"

    digna lee los proveedores de inicio de sesión único como una lista de entradas `[[oidc_clients]]`, cada una
    con su propio `DIGNA_OIDC_KEY`. Si cambiaste tus proveedores a secciones `[oidc_clients.<key>]`, como
    mostraba una versión anterior de esta guía, vuelve a cambiarlos. `config check` informa de
    `OIDC config(s)` como FAILED mientras esa forma siga presente:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Repite la entrada para cada proveedor y mantén cada `DIGNA_OIDC_KEY` igual al `key` de
    `dashboard_config.toml`. Solo afecta a las instalaciones que usan inicio de sesión único.

#### Paso 5: Recargar el servidor web {: #step-5-reload-the-web-server }

El dashboard es un conjunto de archivos estáticos, por lo que tu servidor web —y el navegador— pueden seguir
sirviendo la versión anterior. Recarga o reinicia el servidor web que aloje la carpeta `dashboard`
y, a continuación, recarga la página forzando la actualización (++ctrl+f5++).

#### Paso 6: Validar la configuración {: #step-6-validate-the-configuration }

Confirma que `config.toml` está completo antes de tocar el repositorio:

```bash
digna config check
```

Todas las secciones deben informar OK. Corrige todo lo que se informe como FAILED, elimina las claves
enumeradas en **Unknown keys** y vuelve a ejecutar el comando antes de continuar.

#### Paso 7: Sustituir el archivo de licencia {: #step-7-replace-the-license-file }

Un archivo de licencia emitido para una versión anterior no funciona con la Release 2026.11. Copia
el `license.toml` que el equipo de digna te proporcionó para la Release 2026.11 en el directorio de
instalación, sustituyendo el anterior:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "No conserves la licencia anterior"

    Con la licencia anterior, todos los comandos que comprueban la licencia —`serve`, `user`,
    `inspection`, `repo`— fallan, por lo que digna no arranca y el repositorio no se puede
    actualizar. Verifica la nueva licencia antes de continuar:

    ```bash
    digna license check
    ```

#### Paso 8: Actualizar el esquema del repositorio {: #step-8-upgrade-the-repository-schema }

En tu directorio de instalación de digna, ejecuta:

```bash
digna repo upgrade
```

La Release 2026.11 gestiona el esquema del repositorio con migraciones versionadas. La primera actualización
desde una versión anterior lleva el esquema a la última versión del sistema anterior, registra ese estado como
punto de partida y, a continuación, aplica las migraciones de la Release 2026.11. Termina con:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Se conservan todos los datos existentes. Para ver el estado del repositorio en cualquier momento, ejecuta
`digna repo check`: muestra la última migración aplicada y las que estén pendientes.

!!! warning "digna no arranca con un repositorio desactualizado"

    A partir de la Release 2026.11, el servidor se niega a arrancar mientras el repositorio necesite una
    actualización, y lo indica, por ejemplo:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Ejecuta `repo upgrade` antes de iniciar el servidor o el servicio.

#### Paso 9: Reiniciar los servicios {: #step-9-restart-services }

Si digna se ejecuta como servicio de Windows, vuelve a iniciarlo:

```bash
cd C:\path\to\digna
digna windows start
```

Si se ejecuta manualmente, reinicia el servidor:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Si usas IIS o Tomcat, reinicia el servidor web correspondiente.

#### Paso 10: Verificar la actualización {: #step-10-verify-the-upgrade }

1. Confirma la versión del nuevo ejecutable:

    ```bash
    digna version
    ```

    La primera línea debe ser `Release: 2026.11`.

2. Accede al dashboard de digna y verifica que la interfaz carga correctamente.
3. Revisa los archivos del directorio `logs` de la instalación por si hay errores.
4. Prueba tus conexiones de base de datos: consulta
   [Probar una conexión](../../../databases/overview.md#testing-a-connection).

Para empezar con los nuevos módulos, consulta [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Conectar un agente de IA](../../../platform/agentic/connect_ai_agent.md) para el digna MCP Server y
[Ubicación de perfilado](../../../platform/profiling/profiling_location.md) para el digna Engine.
