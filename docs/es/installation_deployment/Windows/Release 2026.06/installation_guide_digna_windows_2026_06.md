---
title: Windows Installation Guide – digna Release 2026.06 | digna Documentation
description: Step-by-step guide to installing digna Release 2026.06 on Windows — system requirements, PostgreSQL setup, web server configuration, backend and dashboard configuration, running digna as a Windows service, and upgrading to a new release.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Windows Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** August 30, 2026


---

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Pre-Installation Setup](#pre-installation-setup)
4. [PostgreSQL Server Setup](#postgresql-server-setup)
5. [Web Server Configuration](#web-server-configuration)
6. [Initial Installation](#initial-installation)
7. [Backend Configuration](#backend-configuration)
8. [Dashboard Configuration](#dashboard-configuration)
9. [Running digna as a Windows Service](#running-digna-as-a-windows-service)
10. [Upgrading to a New Release](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### About digna

digna es una plataforma integral impulsada por IA diseñada para optimizar la gestión de la calidad de datos en varios entornos de datos como warehouses, lakes y lakehouses. Construida para ser altamente escalable y adaptable, digna aborda los desafíos modernos de datos mediante automatización, monitorización en tiempo real y detección de anomalías.

digna consta de dos componentes principales:

- **dignabackend**: El motor principal de la aplicación, responsable de procesar datos y realizar comprobaciones de calidad.
- **dignadashboard**: Una interfaz web alojada en un servidor web, que proporciona una forma amigable de interactuar con la plataforma digna y visualizar métricas de calidad de datos.

### What's New in Release 2026.06

Esta versión incorpora capacidades de observabilidad de datos directamente en tu código, lo que permite a los desarrolladores monitorizar la calidad de los datos en el origen. Consulta las [release notes](http://docs.digna.ai/changelog/Release_202606/) para más detalles.

---

## System Requirements {: #system-requirements }

Antes de comenzar la instalación, asegúrate de que tu sistema cumpla los siguientes requisitos mínimos:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server or Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB available storage |
| **Database** | PostgreSQL Server 12 or higher |
| **Web Server** | IIS, Apache Tomcat, or equivalent |

### Database Installation Options

**If PostgreSQL is already installed:**
Puedes añadir una nueva base de datos para digna a tu servidor PostgreSQL existente.

**If installing PostgreSQL on the same machine as digna:**

> **Recommended Specifications**
>
> - **Memory**: 32 GB RAM (instead of 16 GB)
> - **Disk Space**: 50 GB available storage (instead of 10 GB)
>
> Estas especificaciones superiores acomodan tanto digna como la base de datos PostgreSQL ejecutándose simultáneamente.

---

## Pre-Installation Setup {: #pre-installation-setup }

Antes de instalar digna, asegúrate de que dos requisitos clave estén en su lugar:

1. **PostgreSQL Server** – para almacenar métricas calculadas y datos de rendimiento
2. **Web Server** – para alojar el digna Dashboard

Si estos componentes aún no están configurados, sigue las secciones a continuación para instalarlos y configurarlos.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### If You Already Have PostgreSQL

Si PostgreSQL ya está instalado y en ejecución en tu máquina local o si estás usando un servidor PostgreSQL remoto gestionado, puedes saltar a la [siguiente sección](#web-server-configuration).

### Installing PostgreSQL

Sigue estos pasos para instalar PostgreSQL en Windows:

#### Step 1: Download PostgreSQL

1. Visita la [página de descargas de PostgreSQL](https://www.postgresql.org/download/)
2. Selecciona **Windows**
3. Descarga el instalador más reciente

#### Step 2: Run the Installer

1. Haz doble clic en el archivo del instalador descargado
2. Sigue las indicaciones del asistente de instalación

#### Step 3: Choose Installation Directory

Selecciona el directorio donde se instalará PostgreSQL. La ubicación por defecto suele ser adecuada.

#### Step 4: Select Components

Para una instalación estándar, mantén las opciones de componentes por defecto seleccionadas.

#### Step 5: Set PostgreSQL Superuser Password

Introduce y confirma una contraseña para el superusuario de PostgreSQL (`postgres`). **Guarda esta contraseña de forma segura** — la necesitarás más adelante.

#### Step 6: Configure Port Number

El puerto por defecto de PostgreSQL es `5432`. Puedes usar el valor por defecto o especificar un puerto diferente si es necesario.

> **Tip**
>
> Si el puerto 5432 ya está en uso, elige un puerto alternativo y anótalo para la configuración posterior.

#### Step 7: Choose Locale

Selecciona la localidad para tu base de datos. La configuración por defecto suele ser adecuada para la mayoría de las instalaciones.

#### Step 8: Complete Installation

Haz clic en **Next** en los pasos restantes y luego en **Finish**.

#### Step 9: Verify Installation

Abre el Símbolo del sistema y verifica que PostgreSQL esté instalado:

```bash
psql --version
```

Deberías ver la versión de PostgreSQL si la instalación fue exitosa.

---

## Web Server Configuration {: #web-server-configuration }

digna requiere un servidor web para alojar el dashboard. Elige una de las siguientes opciones:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Solo necesitas instalar y configurar **uno** de estos servidores.

### IIS Setup {: #iis-setup }

#### Overview

Internet Information Services (IIS) es el servidor web de Microsoft para alojar sitios web y aplicaciones web.

#### Enabling IIS

1. **Abre el Panel de Control**
   - Presiona `Win + R`
   - Escribe `control` y presiona Enter

2. **Navega a Windows Features**
   - Haz clic en **Programs**
   - Selecciona **Turn Windows features on or off**

3. **Habilita Internet Information Services**
   - Desplázate hacia abajo y busca **Internet Information Services (IIS)**
   - Marca la casilla para habilitarlo
   - Haz clic en el **+** para expandir y verifica que estos subcomponentes estén seleccionados:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Haz clic en OK** para aplicar los cambios

5. **Verifica la instalación de IIS**
   - Abre tu navegador
   - Navega a `http://localhost`
   - Deberías ver la página de bienvenida de IIS

#### Required: URL Rewrite Module

IIS requiere el componente URL Rewrite. Descárgalo e instálalo desde la [página oficial de Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Required: MIME Type for Markdown Files

Para asegurar que los archivos Markdown (`.md`) se sirvan correctamente desde IIS:

1. Abre **IIS Manager** (presiona `Win + R`, escribe `inetmgr`, presiona Enter)
2. Navega a **Your Site > MIME Types**
3. Haz clic en **Add...**
4. Configura:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

> **Important**
>
> Sin esta configuración, los archivos `.md` podrían no servir correctamente.

---

### Apache Tomcat Setup {: #apache-tomcat-setup }

#### Overview

Apache Tomcat es un contenedor de servlets Java y servidor web de código abierto.

#### Installation

1. **Download Apache Tomcat**
   - Visita [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Descarga la distribución ZIP para Windows

2. **Extract the Archive**
   - Extrae el archivo ZIP a un directorio en tu sistema
   - Ejemplo: `C:\Program Files\Apache Tomcat`

3. **Verify Tomcat is Running**
   - Abre tu navegador
   - Navega a `http://localhost:8080`
   - Deberías ver la página de bienvenida de Apache Tomcat

> **Tip**
>
> Apache Tomcat normalmente se inicia automáticamente después de la instalación. Si no lo hace, navega a la carpeta `bin` y ejecuta `startup.bat`.

---

## Initial Installation {: #initial-installation }

### Step 1: Set Up the digna Repository

El repositorio de digna almacena todas las métricas calculadas por digna. Actúa como la base de datos central para datos analíticos y de rendimiento.

#### Create Repository Schema and User

Abre tu cliente de PostgreSQL (pgAdmin, psql, o similar) y ejecuta los siguientes comandos SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Reemplaza los siguientes marcadores:**

- `<digna_repo_schema>` — El nombre de esquema deseado (p. ej., `dignarepo`)
- `<digna_repo_user>` — El nombre de usuario deseado (p. ej., `digna_user`)
- `<digna_repo_password>` — Una contraseña segura para este usuario

**Ejemplo:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

> **Best Practice**
>
> Usa contraseñas fuertes y complejas para los usuarios de la base de datos. Evita credenciales fácilmente adivinables.

---

### Step 2: Extract the digna Installation Package

1. Localiza el archivo ZIP de instalación de digna proporcionado
2. Extráelo en la ubicación de instalación deseada
3. Después de la extracción, deberías ver los siguientes elementos:
   - `dashboard/` — Interfaz web del dashboard
   - `digna` — Ejecutable principal (backend + CLI combinados)
   - `config.toml` — Archivo de configuración
   - `license.toml` — Archivo de licencia (copia el tuyo aquí)

### Step 3: Install the License File

> **Important**
>
> El archivo de licencia **no** está incluido en el paquete de instalación y se proporcionará por separado por digna.

1. Localiza el archivo `license.toml` proporcionado
2. Cópialo en el directorio raíz de instalación de digna (donde están `config.toml` y el ejecutable `digna`)

**Por qué importa:**
El archivo de licencia contiene la información del cliente, la fecha de expiración de la licencia y la firma digital. **No modifiques este archivo** — cualquier cambio lo invalidará.

**Estructura de directorios después de la configuración:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend Configuration {: #backend-configuration }

### Step 1: Create and Edit the Configuration File

El archivo `config_template.toml` se proporciona en tu directorio de instalación de digna. Solo necesitas renombrarlo a `config.toml`.

**Ubicación:** `digna_installation/config.toml`

Abre `config.toml` en un editor de texto y configura cada sección a continuación.

#### [app] Section

Esta sección configura los ajustes de la aplicación backend de digna:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` or IP address | Hostname or IP where dignabackend is hosted |
| `digna_APP_PORT` | `8082` (default) | Port for REST API endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL | If dashboard is on different server, include its URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Required for CORS with credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Allow all HTTP methods |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Allow all headers |

#### [repo] Section

Esta sección configura la conexión a la base de datos PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` or IP | PostgreSQL server hostname/IP |
| `digna_REPO_PORT` | `5432` (default) | PostgreSQL port |
| `digna_REPO_DB` | `postgres` | Database name |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema created earlier |
| `digna_REPO_USER` | `digna_user` | User created in PostgreSQL setup |
| `digna_REPO_PASSWORD` | Your password | Password set during schema creation |

#### [base] Section

Esta sección contiene ajustes de seguridad y cookies:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_FERNET_KEY` | Encryption key | Used to encrypt tokens and cookies (default provided) |
| `digna_COOKIE_DOMAIN` | `localhost` | Match your frontend domain |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (production) | Use `true` for HTTPS connections |
| `digna_COOKIE_HTTPONLY` | `true` | Always enabled for security |
| `digna_COOKIE_SAME_SITE` | `lax` | Prevents CSRF attacks |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 hours) | Session timeout in seconds |
| `digna_MAX_WORKERS` | Number of CPU cores - 1 | Number of parallel inspection tasks |

#### [logging] Section

Esta sección configura el comportamiento de los logs:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` or `DEBUG` | `INFO` for production, `DEBUG` for troubleshooting |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Number of daily log backups to retain |

---

### Step 3: Initialize the Repository

1. Abre el Símbolo del sistema
2. Navega al directorio de instalación de digna (donde están `config.toml` y el ejecutable `digna`)
3. Ejecuta la prueba de conexión:

```bash
digna repo check
```

Deberías ver una confirmación de que la conexión está establecida (el repositorio en sí aún no se ha inicializado).

### Step 4: Install the Repository Schema

En el mismo directorio, ejecuta:

```bash
digna repo install
```

Este comando instala las tablas y el esquema necesarios en tu base de datos PostgreSQL.

### Step 5: Start the digna Server

En el directorio de instalación de digna, inicia el servidor con:

```bash
digna serve --address <host> --port <port>
```

**Parámetros:**
- `--address` — Hostname/IP del servidor
- `--port` — Puerto del servidor

Deberías ver mensajes de inicio confirmando que el servidor está en ejecución:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Step 6: Create an Admin User

1. Abre una ventana **nueva** del Símbolo del sistema
2. Navega al directorio de instalación de digna
3. Ejecuta el siguiente comando para crear un usuario admin:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Ejemplo:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

Esto crea un usuario con privilegios administrativos completos.

> **Best Practice**
>
> Usa una contraseña fuerte con una mezcla de mayúsculas, minúsculas, números y caracteres especiales.

---

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

El digna dashboard tiene su propio archivo `config.toml` ubicado en el directorio `dashboard/`. Esta configuración ya está proporcionada y no requiere cambios durante la configuración inicial. Solo necesitas modificarla si necesitas personalizar la conexión al backend.

Si necesitas modificar la configuración del dashboard (por ejemplo, para despliegues multi-instancia), consulta la documentación del dashboard.

Elige tu servidor web y sigue los pasos de despliegue correspondientes.

#### Deploying to IIS

1. **Abre IIS Manager**
   - Presiona `Win + R`, escribe `inetmgr`, presiona Enter

2. **Crea un nuevo sitio web**
   - En el panel izquierdo, haz clic derecho en **Sites**
   - Selecciona **Add Website...**

3. **Configura el sitio**
   - **Site Name**: Introduce un nombre (p. ej., "dignaDashboard")
   - **Physical Path**: Haz clic en Browse y selecciona tu carpeta `dashboard`
   - **Binding**: Configura la dirección IP y el puerto (puerto 80 por defecto para HTTP, 443 para HTTPS)

4. **Inicia el sitio**
   - Haz clic en **OK** para crear el sitio
   - Haz clic derecho en el nuevo sitio y selecciona **Start**

5. **Prueba la instalación**
   - Abre tu navegador
   - Navega a `http://localhost` (o la URL que hayas configurado)
   - Deberías ver la página de login del digna dashboard

#### Deploying to Apache Tomcat

1. **Copia el dashboard a Tomcat**
   - Copia la carpeta `dashboard` al directorio `webapps` de Tomcat
   - Renómbrala si es necesario (p. ej., a `digna`)
   - Ejemplo: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verifica el despliegue**
   - Actualiza o recarga la página de administración de Tomcat (http://localhost:8080)
   - Deberías ver "digna" (o el nombre que hayas elegido) listado en las aplicaciones desplegadas

3. **Accede al dashboard**
   - Abre tu navegador
   - Navega a `http://localhost:8080/digna`
   - Deberías ver la página de login del digna dashboard

---

## Running digna as a Windows Service {: #running-digna-as-a-windows-service }

### Why Use a Windows Service?

Ejecutar el backend de digna como servicio de Windows asegura que:
- Se inicie automáticamente cuando el servidor arranque
- Se ejecute en segundo plano sin una ventana del Símbolo del sistema abierta
- Se reinicie automáticamente si se bloquea
- Se pueda gestionar a través de Servicios de Windows

### Service Management Files

Todos los archivos necesarios se encuentran en el directorio de instalación de digna bajo: `bin/`

Los siguientes archivos batch están disponibles:
- `install_service.bat` — Registra digna como un servicio de Windows
- `uninstall_service.bat` — Anula el registro del servicio
- `start_service.bat` — Inicia el servicio registrado
- `stop_service.bat` — Detiene el servicio registrado

> **Administrator Required**
>
> Todos los archivos batch deben ejecutarse con privilegios de Administrador.

### Installing the Service

1. **Abre el Símbolo del sistema como Administrador**
   - Haz clic derecho en Símbolo del sistema
   - Selecciona "Run as Administrator"

2. **Navega a la carpeta bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Ejecuta el script de instalación**
   ```bash
   install_service.bat
   ```

El servidor digna ya está registrado como un servicio de Windows con inicio **automático** habilitado. El servicio no se inicia inmediatamente — consulta la sección siguiente para iniciarlo.

### Starting and Stopping the Service

#### To Start the Service

1. Abre el Símbolo del sistema como Administrador
2. Navega a `digna\bin`
3. Ejecuta:
   ```bash
   start_service.bat
   ```

#### To Stop the Service

1. Abre el Símbolo del sistema como Administrador
2. Navega a `digna\bin`
3. Ejecuta:
   ```bash
   stop_service.bat
   ```

> **Tip**
>
> Siempre detén el servicio antes de actualizar los archivos de la aplicación.

### Moving the Service to a New Directory

Si necesitas mover la instalación de digna:

1. **Desinstala el servicio actual**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Mueve los archivos de la aplicación**
   - Mueve toda la carpeta de instalación de digna a la nueva ubicación

3. **Reinstala el servicio**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Inicia el servicio**
   ```bash
   start_service.bat
   ```

### Uninstalling the Service

1. **Detén el servicio en ejecución**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Desinstala el servicio**
   ```bash
   uninstall_service.bat
   ```

El servidor digna ya no estará registrado como servicio de Windows.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

### Before You Upgrade

**Creating a digna Repository Backup is Mandatory**

Antes de actualizar digna, realiza una copia de seguridad de tu repositorio (PostgreSQL) para protegerte contra la pérdida de datos.
Una copia de seguridad garantiza que puedas recuperar el estado si la actualización encuentra problemas inesperados.

### Upgrade Process

#### Step 1: Stop digna Service

Si digna se ejecuta como servicio de Windows, deténlo primero:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Step 2: Backup Current Backend Installation

En tu directorio de instalación de digna:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Step 3: Extract and Deploy New Version

1. Extrae el nuevo archivo ZIP de instalación de digna
2. Copia el nuevo ejecutable `digna` y la carpeta `dashboard` a tu directorio de instalación


> **Important**
>
> El archivo `config.toml` **nunca** se incluye en el ZIP de instalación. Tu configuración existente permanece segura.

### Step 4: Restore Your Configuration Files

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Step 5: Upgrade the Repository Schema

Navega a tu directorio de instalación de digna y ejecuta:

```bash
digna repo upgrade
```

Esto actualiza el esquema de PostgreSQL a la versión más reciente preservando todos los datos existentes.

### Step 6: Restart Services

Si se ejecuta como servicio de Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Si se ejecuta manualmente, reinicia el servidor:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Si usas IIS o Tomcat, reinicia el servidor web correspondiente.

#### Step 7: Verify the Upgrade

1. Accede al digna dashboard
2. Verifica que la interfaz cargue correctamente
3. Revisa los logs del servidor en busca de errores
