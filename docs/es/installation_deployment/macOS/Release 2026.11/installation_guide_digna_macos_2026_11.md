---
title: Guía de instalación en macOS – digna Release 2026.11 | Documentación de digna
description: Guía paso a paso para instalar digna Release 2026.11 en macOS — requisitos del sistema, configuración de Homebrew y PostgreSQL, configuración de nginx o Apache, configuración del backend y del dashboard, ejecución de digna como servicio en segundo plano y actualización desde la Release 2026.06.
keywords: digna instalación macos, guía de despliegue digna mac, configuración backend digna, instalación dashboard digna, postgresql homebrew, nginx macos, servicio launchd digna, guía de actualización digna
image: /assets/logo_square.png
---

# Guía de instalación en macOS para digna Release 2026.11

**Release:** 2026.11

**Última actualización:** 7 de noviembre de 2026


---

## Tabla de contenidos

1. [Introducción](#introduction)
2. [Requisitos del sistema](#system-requirements)
3. [Preparación previa a la instalación](#pre-installation-setup)
4. [Configuración del servidor PostgreSQL](#postgresql-server-setup)
5. [Configuración del servidor web](#web-server-configuration)
6. [Instalación inicial](#initial-installation)
7. [Configuración del backend](#backend-configuration)
8. [Configuración del dashboard](#dashboard-configuration)
9. [Ejecutar digna como servicio en segundo plano](#running-digna-as-a-background-service)
10. [Actualizar a una nueva versión](#upgrading-to-a-new-release)

---

## Introducción {: #introduction }

### Acerca de digna

digna es una plataforma completa impulsada por IA diseñada para optimizar la gestión de la calidad de los datos en diversos entornos de datos, como warehouses, lakes y lakehouses. Diseñada para ser altamente escalable y adaptable, digna aborda los desafíos modernos de datos mediante automatización, monitorización en tiempo real y detección de anomalías.

digna consta de dos componentes principales:

- **digna**: el núcleo de la aplicación, responsable de procesar los datos y realizar las comprobaciones de calidad. Combina el backend y la interfaz de línea de comandos en un único ejecutable, sustituyendo a los programas separados `dignabackend` y `dignacli` de versiones anteriores.
- **dignadashboard**: Una interfaz web alojada en un servidor web, que proporciona una forma amigable de interactuar con la plataforma digna y visualizar métricas de calidad de datos.

### Novedades en la Release 2026.11

Esta versión añade digna Data Reconciliation, digna Agentic con el digna MCP Server y el digna Engine, que puede perfilar datos dentro de digna y comprobar la integridad referencial entre distintas tecnologías de bases de datos. Consulta las [notas de la versión](../../../changelog/Release_202611.md) para obtener detalles completos.

Para una instalación, la versión trae un nuevo mecanismo de migración del repositorio, una sección `[duckdb]` opcional en `config.toml` para el digna Engine y un nuevo archivo de licencia. La [sección de actualización](#upgrading-to-a-new-release) trata cada uno de ellos.

### ¿Buscas Windows o Linux?

Esta guía cubre macOS. Para otras plataformas, consulta la [Guía de instalación para Windows](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) o la [Guía de instalación para Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Requisitos del sistema {: #system-requirements }

Antes de comenzar la instalación, asegúrate de que tu sistema cumple los siguientes requisitos mínimos:

| Requisito | Especificación |
|---|---|
| **Sistema operativo** | macOS 13 (Ventura) o posterior |
| **Arquitectura** | Apple Silicon (arm64) o Intel (x86_64) |
| **Memoria (Configuración mínima)** | 16 GB RAM |
| **Espacio en disco** | 10 GB de almacenamiento disponible |
| **Base de datos** | PostgreSQL Server 12 o superior |
| **Servidor web** | nginx, Apache httpd u equivalente |
| **Herramientas de línea de comandos** | Xcode Command Line Tools (requerido por Homebrew) |

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

    Estas especificaciones más altas acomodan tanto digna como la base de datos PostgreSQL ejecutándose simultáneamente.

### Verificar tu arquitectura

Varios caminos en esta guía difieren entre Macs con Apple Silicon e Intel. Para comprobar cuál tienes, abre **Terminal** y ejecuta:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew se instala en `/opt/homebrew`.
- `x86_64` — Intel. Homebrew se instala en `/usr/local`.

!!! tip "Consejo"

    En lugar de codificar una u otra ruta, esta guía usa `$(brew --prefix)`, que se expande a la ubicación correcta en ambas arquitecturas. Puedes copiar los comandos tal cual.

---

## Preparación previa a la instalación {: #pre-installation-setup }

Antes de instalar digna, asegúrate de que tres prerrequisitos clave estén presentes:

1. **Homebrew** – el gestor de paquetes usado para instalar los componentes que siguen
2. **PostgreSQL Server** – para almacenar métricas calculadas y datos de rendimiento
3. **Servidor web** – para alojar el Dashboard de digna

Si estos componentes aún no están configurados, sigue las secciones a continuación para instalarlos y configurarlos.

### Instalación de Homebrew

Homebrew es el gestor de paquetes estándar para macOS y se usa en toda esta guía para instalar PostgreSQL y nginx.

#### Paso 1: Comprobar si Homebrew ya está instalado

Abre **Terminal** (pulsa `Cmd + Space`, escribe `Terminal`, pulsa Enter) y ejecuta:

```bash
brew --version
```

Si se devuelve un número de versión, continúa con la sección de [Configuración del servidor PostgreSQL](#postgresql-server-setup).

#### Paso 2: Instalar Homebrew

Si el comando no se encontró, instala Homebrew siguiendo las instrucciones en el [sitio oficial de Homebrew](https://brew.sh). El instalador también instala las Xcode Command Line Tools si no están ya presentes.

#### Paso 3: Añadir Homebrew a tu PATH

En Apple Silicon, el instalador muestra dos comandos para añadir Homebrew a tu entorno de shell. Ejecútalos según se indique y luego confirma:

```bash
brew --prefix
```

Esto debería imprimir `/opt/homebrew` en Apple Silicon o `/usr/local` en Intel.

---

## Configuración del servidor PostgreSQL {: #postgresql-server-setup }

### Si ya tienes PostgreSQL

Si PostgreSQL ya está instalado y en ejecución en tu máquina local o si estás usando un servidor PostgreSQL remoto gestionado, puedes saltar a la [siguiente sección](#web-server-configuration).

### Opciones de instalación

macOS ofrece dos maneras sencillas de instalar PostgreSQL. Elige **una**:

- [Homebrew](#postgresql-homebrew) — instalación desde la línea de comandos, recomendada para despliegues de servidor
- [Postgres.app](#postgresql-app) — instalación gráfica, conveniente para evaluación local

### Instalar PostgreSQL con Homebrew {: #postgresql-homebrew }

#### Paso 1: Instalar la fórmula de PostgreSQL

```bash
brew install postgresql@16
```

#### Paso 2: Añadir PostgreSQL a tu PATH

Las fórmulas versionadas de PostgreSQL son *keg-only*, lo que significa que Homebrew no enlaza sus comandos en tu PATH automáticamente. Añádelos tú mismo:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Nota"

    Esto asume el shell `zsh` por defecto que usa macOS. Si usas `bash`, añade la misma línea a `~/.bash_profile` en su lugar.

#### Paso 3: Iniciar el servicio PostgreSQL

```bash
brew services start postgresql@16
```

Esto inicia PostgreSQL inmediatamente y lo configura para que se inicie automáticamente cuando inicies sesión.

#### Paso 4: Verificar la instalación

```bash
psql --version
```

Deberías ver la versión de PostgreSQL si la instalación fue exitosa.

#### Paso 5: Conectarse al servidor

```bash
psql postgres
```

!!! warning "Importante — macOS difiere de Windows aquí"

    El instalador de Windows te pide crear un superusuario `postgres` y una contraseña. Homebrew no lo hace. En su lugar, crea un superusuario con el mismo nombre que tu **cuenta de macOS**, sin contraseña, accesible solo desde la máquina local.

    Esto significa que no existe el rol `postgres` en una instalación nueva con Homebrew. Usa tu propio nombre de cuenta cuando necesites un superusuario, y crea un usuario explícito para digna como se describe en [Instalación inicial](#initial-installation).

#### Paso 6: Confirmar el puerto

El puerto por defecto de PostgreSQL es `5432`. Para confirmar el puerto en el que escucha tu servidor:

```bash
psql postgres -c "SHOW port;"
```

Anota el valor — lo necesitarás cuando configures el backend de digna.

### Instalar PostgreSQL con Postgres.app {: #postgresql-app }

Si prefieres una instalación gráfica:

1. Descarga [Postgres.app](https://postgresapp.com) y arrástralo a tu carpeta **Applications**
2. Abre la app y haz clic en **Initialize** para crear un nuevo servidor
3. Sigue las instrucciones de la app para añadir sus herramientas de línea de comandos a tu PATH
4. Verifica la instalación:

```bash
psql --version
```

Postgres.app también crea un superusuario con el mismo nombre que tu cuenta de macOS.

---

## Configuración del servidor web {: #web-server-configuration }

digna requiere un servidor web para alojar el dashboard. Elige una de las siguientes opciones:

- [nginx](#nginx-setup) — instalado vía Homebrew, recomendado
- [Apache httpd](#apache-setup) — incluido con macOS

Solo necesitas instalar y configurar **uno** de estos servidores.

Ambas secciones configuran dos cosas de las que depende el dashboard:

- **Un fallback para aplicaciones de una sola página**, de modo que al actualizar una URL del dashboard no devuelva 404
- **Un tipo MIME para `.md`**, para que los archivos Markdown se sirvan correctamente

### Configuración de nginx {: #nginx-setup }

#### Resumen

nginx es un servidor web ligero y de alto rendimiento, bien adaptado para servir el dashboard estático de digna.

#### Instalación

```bash
brew install nginx
```

#### Iniciar nginx

```bash
brew services start nginx
```

#### Verificar la instalación

1. Abre tu navegador
2. Navega a `http://localhost:8080`
3. Deberías ver la página de bienvenida de nginx

!!! note "Nota — el puerto por defecto es 8080, no 80"

    Homebrew configura nginx para escuchar en el puerto `8080` para que pueda ejecutarse sin privilegios de administrador. En macOS, enlazar al puerto `80` o a cualquier puerto por debajo de 1024 requiere root.

    Para servir el dashboard en el puerto 80, cambia `listen 8080;` por `listen 80;` en la configuración que sigue y arranca nginx con `sudo brew services start nginx` en su lugar.

#### Configurar un sitio para el dashboard

La configuración de nginx de Homebrew incluye todos los archivos en su directorio `servers`. Crea un archivo de configuración dedicado para digna ahí:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Pega lo siguiente, reemplazando `/path/to/digna/dashboard` por la ruta real a tu carpeta `dashboard` extraída:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Servir archivos Markdown con el tipo MIME correcto.
    types {
        text/markdown  md;
    }

    # Fallback para aplicación de una sola página: las rutas desconocidas devuelven index.html
    # en lugar de un 404, de modo que las rutas del dashboard sobrevivan a una actualización del navegador.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Importante"

    Sin la directiva `try_files`, recargar cualquier página del dashboard que no sea la URL raíz devuelve un 404. Esto es el equivalente en nginx del módulo URL Rewrite requerido por IIS en Windows.

#### Aplicar la configuración

Prueba la sintaxis de la configuración y luego recarga nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Configuración de Apache httpd {: #apache-setup }

#### Resumen

macOS incluye Apache httpd, por lo que no es necesario instalarlo. Está deshabilitado por defecto.

#### Iniciar Apache

```bash
sudo apachectl start
```

#### Verificar la instalación

1. Abre tu navegador
2. Navega a `http://localhost`
3. Deberías ver el mensaje "It works!"

#### Obligatorio: habilitar mod_rewrite

El dashboard requiere reescritura de URL. Abre la configuración de Apache:

```bash
sudo nano /etc/apache2/httpd.conf
```

Encuentra la siguiente línea y elimina el `#` inicial para descomentarlo:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Obligatorio: permitir overrides con .htaccess

En el mismo archivo, localiza el bloque `<Directory "/Library/WebServer/Documents">` y cambia:

```apache
AllowOverride None
```

por:

```apache
AllowOverride All
```

#### Obligatorio: tipo MIME para archivos Markdown

Aún en `httpd.conf`, añade la siguiente línea para que los archivos Markdown se sirvan correctamente:

```apache
AddType text/markdown .md
```

!!! warning "Importante"

    Sin esta configuración, los archivos `.md` podrían no servirse correctamente.

#### Aplicar la configuración

Comprueba la sintaxis de la configuración y luego reinicia Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Instalación inicial {: #initial-installation }

### Paso 1: Configurar el repositorio de digna

El repositorio de digna almacena todas las métricas calculadas por digna. Actúa como la base de datos central para datos analíticos y de rendimiento.

#### Crear esquema y usuario del repositorio

Abre tu cliente PostgreSQL (psql, pgAdmin u otro) y ejecuta las siguientes sentencias SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Reemplaza los siguientes marcadores:**

- `<digna_repo_schema>` — El nombre de esquema que desees (por ejemplo, `dignarepo`)
- `<digna_repo_user>` — El nombre de usuario que desees (por ejemplo, `digna_user`)
- `<digna_repo_password>` — Una contraseña segura para este usuario

**Ejemplo:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Para ejecutar esto desde Terminal en un solo paso:

```bash
psql postgres
```

Luego pega las sentencias en el prompt `postgres=#` y escribe `\q` para salir.

!!! tip "Buena práctica"

    Usa contraseñas fuertes y complejas para los usuarios de la base de datos. Evita credenciales fácilmente adivinables.

---

### Paso 2: Extraer el paquete de instalación de digna

1. Localiza el archivo ZIP de instalación de digna proporcionado
2. Extráelo en la ubicación de instalación deseada — por ejemplo `/opt/digna` o `~/digna`
3. Tras la extracción, deberías ver los siguientes elementos:
   - `dashboard/` — Interfaz web del dashboard
   - `digna` — Ejecutable principal (backend + CLI combinados)

!!! info "Los archivos de configuración y de licencia no están en el paquete"

    Ni `config.toml` ni `dashboard/dashboard_config.toml` se incluyen en la instalación: los
    creas tú mismo, en [Configuración del backend](#backend-configuration) y
    [Configuración del dashboard](#dashboard-configuration). Tampoco se incluye `license.toml`;
    digna lo proporciona por separado, como se describe en el Paso 3.

Para extraer desde Terminal:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Hacer el ejecutable ejecutable

Dependiendo de cómo se transfirió el archivo, el bit de ejecutable puede no conservarse tras la extracción. Establécelo explícitamente:

```bash
cd /opt/digna
chmod +x digna
```

#### Si macOS bloquea la aplicación

Los archivos descargados mediante un navegador o cliente de correo se marcan con un atributo de cuarentena. Si macOS informa que la app *"cannot be opened because the developer cannot be verified"*, quita el atributo de cuarentena del directorio de instalación:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternativamente, abre **System Settings → Privacy & Security**, encuentra el elemento bloqueado cerca del final de la página y haz clic en **Open Anyway**.

!!! note "Nota"

    Este paso solo es necesario si macOS realmente bloquea el ejecutable. Los paquetes transferidos por SSH o desde recursos compartidos internos no suelen estar en cuarentena.

### Paso 3: Instalar el archivo de licencia

!!! warning "Importante"

    El archivo de licencia **no** está incluido en el paquete de instalación y te será proporcionado por digna por separado.

1. Localiza el archivo `license.toml` que se te proporcionó
2. Copia este archivo al directorio raíz de instalación de digna (donde están `config.toml` y el ejecutable `digna`)

**Por qué importa:**
El archivo de licencia contiene la información de cliente, la fecha de expiración de la licencia y la firma digital. **No modifiques este archivo** — cualquier cambio lo invalidará.

**Estructura de directorios después de la configuración:**

```
/opt/digna/
├── config.toml         (archivo de configuración)
├── license.toml        (TU ARCHIVO DE LICENCIA - cópialo aquí)
├── digna               (ejecutable principal)
├── bin/                (scripts para gestión del servicio)
└── dashboard/          (interfaz web)
    └── (archivos del dashboard)
```

---

## Configuración del backend {: #backend-configuration }

### Paso 1: Crear y editar el archivo de configuración

El archivo `config_template.toml` se proporciona en el directorio de instalación de digna. Solo necesitas renombrarlo a `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Ubicación:** `/opt/digna/config.toml`

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

!!! note "Nota"

    Si sirves el dashboard desde nginx de Homebrew en su puerto por defecto, el origin a permitir es `http://localhost:8080`.

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
| `DIGNA_REPO_PORT` | `5432` (por defecto) | Puerto de PostgreSQL |
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
| `DIGNA_MAX_WORKERS` | Número de núcleos CPU - 1 | Número de inspecciones que pueden ejecutarse al mismo tiempo |
| `DIGNA_FRONTEND_BASEURL` | URL del dashboard | Obligatorio. Se usa para los enlaces de los mensajes de notificación, por lo que debe ser una URL que los destinatarios puedan abrir |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (por defecto) | Opcional. Segundos que puede ejecutarse una única consulta contra una base de datos de origen antes de interrumpirse; `0` desactiva el tiempo de espera |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (por defecto) | Opcional. Segundos de espera para establecer una conexión con una base de datos de origen; `0` espera indefinidamente |

!!! tip "Consejo"

    Para encontrar el número de núcleos CPU disponibles en tu Mac, ejecuta `sysctl -n hw.ncpu`.

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
| `DIGNA_LOGGING_MODE` | `INFO` o `DEBUG` | `INFO` para producción, `DEBUG` para solución de problemas. También se aceptan `TRACE`, `WARN` y `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (por defecto) | Opcional. Directorio para los archivos de registro rotativos, relativo al directorio de trabajo |
| `DIGNA_LOGGING_MAX_FILES` | `30` (por defecto) | Opcional. Número de archivos de registro rotados que se conservan |

#### Sección [duckdb] (opcional) {: #duckdb-section }

Novedad de la Release 2026.11. Esta sección define los recursos del **digna Engine**, que perfila
datos dentro de digna para las conexiones de base de datos cuya ubicación de perfilado es **digna Engine**, y
ejecuta comprobaciones de integridad referencial entre fuentes de datos de distintas conexiones de base de datos. Consulta
[Ubicación de perfilado](../../../platform/profiling/profiling_location.md).

La sección es opcional. Sin ella, se aplican los valores por defecto que se indican a continuación.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parámetro | Valor | Notas |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (por defecto) | Memoria, en MB, que puede usar una ejecución del digna Engine. Puede haber hasta `DIGNA_MAX_WORKERS` ejecuciones activas al mismo tiempo |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Por defecto: el directorio temporal del sistema (`$TMPDIR` de la cuenta que ejecuta digna) | Directorio para archivos temporales cuando los datos no caben en memoria |

!!! tip "Dimensionar el digna Engine"

    Prevé hasta `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` de memoria en el host de
    digna, además de la que usa el propio digna, y suficiente espacio libre en disco en el directorio
    temporal para alojar la fecha inspeccionada más grande de las fuentes de datos que usan el digna Engine.
    Apunta `DIGNA_DUCKDB_TEMP_DIRECTORY` a un disco con ese espacio, en el que pueda escribir la cuenta que
    ejecuta digna:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Solo necesitas esta sección si al menos una conexión de base de datos usa el digna Engine, o si una
    comprobación de integridad referencial compara fuentes de datos de distintas conexiones.

---

### Paso 2: Validar la configuración

Antes de inicializar el repositorio, compruebe que `config.toml` está completo y bien formado. En su directorio de instalación de digna, ejecute:

```bash
./digna config check
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

1. Abre **Terminal**
2. Navega al directorio de instalación de digna (donde están `config.toml` y el ejecutable `digna`)
3. Ejecuta la prueba de conexión:

```bash
cd /opt/digna
./digna repo check
```

En un esquema nuevo, el comando se conecta y después informa de que aún no hay ningún repositorio instalado:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

En este punto, ese es el resultado esperado: confirma que digna llega a PostgreSQL y al esquema. En cambio, un error de conexión o de autenticación apunta a la sección `[repo]` o a la configuración de PostgreSQL.

!!! note "Nota"

    En macOS, los comandos en el directorio actual no están en tu PATH, así que el ejecutable se invoca como `./digna` en lugar de `digna`. Para usar la forma corta en todo momento, añade el directorio de instalación a tu PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Paso 4: Instalar el esquema del repositorio

En el mismo directorio, ejecuta:

```bash
./digna repo upgrade
```

Este comando instala las tablas necesarias en el esquema del repositorio y termina con:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade instala y actualiza"

    A partir de la Release 2026.11, `repo upgrade` instala un repositorio nuevo y actualiza uno existente.
    `repo install` sigue funcionando como otro nombre del mismo comando.

### Paso 5: Crear un usuario administrador

1. Abre una ventana de Terminal **nueva**
2. Navega al directorio de instalación de digna
3. Ejecuta el siguiente comando para crear un usuario administrador:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Ejemplo:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Esto crea un usuario con el correo electrónico `admin@example.com` y privilegios administrativos completos.

!!! tip "Consejo"

    Envuelve la contraseña entre comillas simples. `zsh` trata caracteres como `!`, `$` y `*` de forma especial, y una contraseña sin comillas que los contenga no se pasará tal como se escribió.

!!! tip "Buena práctica"

    Usa una contraseña fuerte con una mezcla de mayúsculas, minúsculas, números y caracteres especiales.

---

### Paso 6: Iniciar el servidor digna

En el directorio de instalación de digna, inicia el servidor con:

```bash
./digna serve --address <host> --port <port>
```

**Parámetros:**
- `--address` — Nombre de host/IP del servidor (por defecto `127.0.0.1`)
- `--port` — Puerto del servidor (por defecto `8000`)

Cuando el servidor está en marcha, muestra la dirección en la que escucha:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Consejo"

    La primera vez que inicies el servidor, macOS puede preguntar si deseas que la aplicación acepte conexiones de red entrantes. Haz clic en **Allow**, de lo contrario el dashboard no podrá comunicarse con el backend.

!!! note "El servidor ocupa el terminal"

    `serve` se ejecuta en primer plano y sigue funcionando hasta que lo detenga con ++ctrl+c++. Déjelo en ejecución mientras termina la configuración; para iniciarlo automáticamente en el arranque, consulte [Ejecutar digna como servicio en segundo plano](#running-digna-as-a-background-service).

## Configuración del dashboard {: #dashboard-configuration }

### Paso 1: Desplegar el dashboard en el servidor web

El dashboard de digna lee su propia configuración de `dashboard/dashboard_config.toml`. Ese archivo no se incluye en la instalación: lo creas en el directorio `dashboard/`, junto a los archivos del dashboard.

Su contenido se describe en [Inicio de sesión único](../../../sso/overview.md), que es también donde se necesita el archivo: contiene las opciones de inicio de sesión que ofrece el dashboard y, para despliegues multi-instancia, la conexión al backend.

Elige tu servidor web y sigue los pasos de despliegue correspondientes.

#### Desplegar en nginx

Si seguiste la sección de [Configuración de nginx](#nginx-setup), el bloque del servidor ya apunta a tu carpeta `dashboard` y no es necesario copiar nada.

1. **Confirmar la ruta**
   - Abre `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Verifica que `root` apunte a tu carpeta `dashboard` extraída

2. **Asegurarse de que la carpeta sea legible**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Recargar nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Probar la instalación**
   - Abre tu navegador
   - Navega a `http://localhost:8080` (o a la URL configurada)
   - Deberías ver la página de inicio de sesión del dashboard de digna

#### Desplegar en Apache httpd

1. **Copiar el dashboard al Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Añadir las reglas de reescritura**

   Crea un archivo `.htaccess` dentro de la carpeta desplegada para que las rutas del dashboard sobrevivan a una actualización del navegador:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Pega lo siguiente:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Servir archivos y directorios existentes tal cual.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Todo lo demás vuelve al punto de entrada de la aplicación de una sola página.
   RewriteRule ^ index.html [L]
   ```

3. **Reiniciar Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Acceder al dashboard**
   - Abre tu navegador
   - Navega a `http://localhost/digna`
   - Deberías ver la página de inicio de sesión del dashboard de digna

---

## Ejecutar digna como servicio en segundo plano {: #running-digna-as-a-background-service }

### ¿Por qué ejecutar digna como servicio?

Ejecutar el backend de digna como un servicio en segundo plano garantiza que:

- Se inicie automáticamente cuando la máquina arranque
- Se ejecute en segundo plano sin una ventana de Terminal abierta
- Se reinicie automáticamente si falla
- Puede gestionarse mediante `launchctl`, el gestor de servicios de macOS

### Archivos de gestión del servicio

Todos los archivos necesarios se encuentran en el directorio de instalación de digna bajo: `bin/`

Los siguientes scripts shell están disponibles:

- `install_service.sh` — Registra digna con launchd
- `uninstall_service.sh` — Desregistra el servicio
- `start_service.sh` — Inicia el servicio registrado
- `stop_service.sh` — Detiene el servicio en ejecución

!!! warning "Se requiere administrador"

    Todos los scripts deben ejecutarse con `sudo`, porque registrar un servicio que se inicia en el arranque escribe en `/Library/LaunchDaemons`.

### Hacer los scripts ejecutables

La extracción puede no preservar el bit ejecutable. Antes del primer uso:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Instalar el servicio

1. **Abrir Terminal**

2. **Navegar a la carpeta bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Ejecutar el script de instalación**
   ```bash
   sudo ./install_service.sh
   ```

El servidor digna ahora está registrado en launchd con el inicio automático habilitado. El servicio no se inicia inmediatamente — consulta la sección siguiente para iniciarlo.

### Iniciar y detener el servicio

#### Para iniciar el servicio

1. Abre Terminal
2. Navega a `/opt/digna/bin`
3. Ejecuta:
   ```bash
   sudo ./start_service.sh
   ```

#### Para detener el servicio

1. Abre Terminal
2. Navega a `/opt/digna/bin`
3. Ejecuta:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Consejo"

    Siempre detén el servicio antes de actualizar archivos de la aplicación.

### Verificar el servicio

Para confirmar que el servicio está registrado y en ejecución:

```bash
sudo launchctl list | grep digna
```

Una línea que comience con un ID de proceso indica que el servicio está en ejecución. Un `-` en la primera columna significa que está registrado pero detenido.

### Mover el servicio a un nuevo directorio

launchd almacena la ruta absoluta al ejecutable, por lo que mover la instalación requiere volver a registrar el servicio:

1. **Desinstalar el servicio actual**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Mover los archivos de la aplicación**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Reinstalar el servicio**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Iniciar el servicio**
   ```bash
   sudo ./start_service.sh
   ```

### Desinstalar el servicio

1. **Detener el servicio en ejecución**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Desinstalar el servicio**
   ```bash
   sudo ./uninstall_service.sh
   ```

El servidor digna ya no estará registrado en launchd.

---

## Actualizar a una nueva versión {: #upgrading-to-a-new-release }

Esta sección actualiza una instalación de la Release 2026.06 a la Release 2026.11. Si tu
instalación es más antigua, lee primero [Actualizar desde una versión anterior a la 2026.06](#upgrading-from-a-release-before-2026-06).

### Antes de actualizar

**Es obligatorio crear una copia de seguridad del repositorio de digna**

Antes de actualizar digna, realiza una copia de seguridad de tu repositorio (PostgreSQL) para protegerte contra pérdida de datos.
Una copia de seguridad asegura que puedas recuperar los datos si la actualización encuentra problemas inesperados.

Para crear una copia de seguridad desde Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Solicitar el archivo de licencia para la Release 2026.11**

La Release 2026.11 necesita un nuevo `license.toml`. Solicítalo al equipo de digna antes de empezar y
tenlo preparado para el [paso 7](#step-7-replace-the-license-file).

### Actualizar desde una versión anterior a la 2026.06 {: #upgrading-from-a-release-before-2026-06 }

La Release 2026.06 introdujo tres cambios que siguen aplicándose cuando actualizas una instalación más
antigua directamente a la 2026.11:

- **Solo ODBC.** digna accede a cada tecnología de origen mediante ODBC. Toda conexión de base de datos que
  aún no use ODBC debe cambiarse a ODBC después de la actualización; no hay conversión
  automática. Instala de antemano los controladores ODBC en el host de digna (consulta
  [Instalar el controlador ODBC en el host de digna](../../../databases/overview.md#install-the-driver))
  y ten preparadas las propiedades de cada conexión a partir de las
  [guías por tecnología](../../../databases/overview.md#technology-guides). El conector Databricks Legacy
  ya no existe; traslada esas conexiones al conector
  [Databricks](../../../databases/databricks_connector_guide.md).
- **Un único ejecutable.** `dignabackend` y `dignacli` se sustituyen por el ejecutable único `digna`,
  que combina el backend y la CLI.
- **config.toml.** La sección `[encryption]` es obligatoria, y `DIGNA_APP_HOST` y
  `DIGNA_APP_PORT` ya no se leen: el servidor toma su dirección y su puerto de `digna serve`.
  Compara tu archivo con [Configuración del backend](#backend-configuration).

Los pasos siguientes indican dónde una instalación más antigua necesita algo distinto. La actualización
del repositorio del paso 8 lleva un repositorio de cualquier versión anterior directamente a la 2026.11.

### Proceso de actualización

#### Paso 1: Detener el servicio digna {: #step-1-stop-the-digna-service }

Si digna se está ejecutando como servicio en segundo plano, deténlo primero:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Si digna se ejecuta en primer plano, presiona ++ctrl+c++ en la ventana de Terminal donde se esté ejecutando.

#### Paso 2: Respaldar la instalación actual {: #step-2-backup-current-installation }

En tu directorio de instalación de digna, cambia el nombre del ejecutable y de la carpeta del dashboard de tu
instalación actual, para que la nueva versión pueda desplegarse junto a ellos:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Conserva `digna_old` hasta que hayas verificado la actualización, y `dashboard_old` hasta que hayas restaurado
desde ella tus archivos de configuración (consulta el paso 4). Después puedes eliminar ambos.

!!! info "Actualizar desde una versión anterior a la 2026.06"

    Cambia el nombre de las carpetas `dignabackend` y `dignacli` en lugar del ejecutable:
    `mv dignabackend dignabackend_old` y `mv dignacli dignacli_old`. La Release 2026.11 no usa ninguna de las dos.

#### Paso 3: Extraer y desplegar la nueva versión {: #step-3-extract-and-deploy-new-version }

1. Extrae el nuevo archivo ZIP de instalación de digna
2. Copia el nuevo ejecutable `digna` y la carpeta `dashboard` a tu directorio de instalación
3. Restaura el bit de ejecutable y, si es necesario, quita el atributo de cuarentena:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Importante"

    Ni `config.toml` ni `dashboard/dashboard_config.toml` se incluyen **nunca** en el
    ZIP de instalación: el equipo de digna no entrega ninguno de los dos archivos. Por tanto, la actualización no
    toca tu configuración existente, y las copias de las carpetas renombradas `*_old` son las
    únicas que tienes.

#### Paso 4: Restaurar tus archivos de configuración {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
y, a continuación, recarga la página forzando la actualización (++cmd+shift+r++).

#### Paso 6: Validar la configuración {: #step-6-validate-the-configuration }

Confirma que `config.toml` está completo antes de tocar el repositorio:

```bash
./digna config check
```

Todas las secciones deben informar OK. Corrige todo lo que se informe como FAILED, elimina las claves
enumeradas en **Unknown keys** y vuelve a ejecutar el comando antes de continuar.

#### Paso 7: Sustituir el archivo de licencia {: #step-7-replace-the-license-file }

Normalmente, un archivo de licencia sigue sirviendo de una versión a la siguiente. La Release 2026.11 es una
excepción: añade dos módulos con licencia, digna Data Reconciliation y digna Agentic, y una licencia
emitida antes de la 2026.11 no los contiene. Copia el `license.toml` que el equipo de digna te
proporcionó para la Release 2026.11 en el directorio de instalación, sustituyendo el anterior:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "No conserves la licencia anterior"

    Con la licencia anterior, digna sigue arrancando, pero digna Data Reconciliation y el digna
    MCP Server permanecen desactivados. Todos los comandos que comprueban la licencia —`user`,
    `inspection`, `repo`— se interrumpen antes de tocar el repositorio si la comprobación falla.
    Verifica la nueva licencia antes de continuar:

    ```bash
    ./digna license check
    ```

#### Paso 8: Actualizar el esquema del repositorio {: #step-8-upgrade-the-repository-schema }

En tu directorio de instalación de digna, ejecuta:

```bash
./digna repo upgrade
```

La Release 2026.11 gestiona el esquema del repositorio con migraciones versionadas. La primera actualización
desde una versión anterior lleva el esquema a la última versión del sistema anterior, registra ese estado como
punto de partida y, a continuación, aplica las migraciones de la Release 2026.11. Termina con:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Se conservan todos los datos existentes. Para ver el estado del repositorio en cualquier momento, ejecuta
`./digna repo check`: muestra la última migración aplicada y las que estén pendientes.

!!! warning "digna no arranca con un repositorio desactualizado"

    A partir de la Release 2026.11, el servidor se niega a arrancar mientras el repositorio necesite una
    actualización, y lo indica, por ejemplo:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Ejecuta `repo upgrade` antes de iniciar el servidor o el servicio.

#### Paso 9: Reiniciar servicios {: #step-9-restart-services }

Si se ejecuta como servicio en segundo plano:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Si se ejecuta manualmente, reinicia el servidor:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Si usas nginx o Apache, reinicia el servidor web correspondiente:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Paso 10: Verificar la actualización {: #step-10-verify-the-upgrade }

1. Confirma la versión del nuevo ejecutable:

    ```bash
    ./digna version
    ```

    La primera línea debe ser `Release: 2026.11`.

2. Accede al dashboard de digna y verifica que la interfaz carga correctamente.
3. Revisa la salida del servidor y los archivos del directorio `logs` por si hay errores.
4. Prueba tus conexiones de base de datos: consulta
   [Probar una conexión](../../../databases/overview.md#testing-a-connection). Tras una actualización
   desde una versión anterior a la 2026.06, convierte primero a ODBC todas las conexiones que aún no lo
   usaran.

Para empezar con los nuevos módulos, consulta [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Conectar un agente de IA](../../../platform/agentic/connect_ai_agent.md) para el digna MCP Server y
[Ubicación de perfilado](../../../platform/profiling/profiling_location.md) para el digna Engine.
